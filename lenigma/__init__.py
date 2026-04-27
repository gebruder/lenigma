#!/usr/bin/env python3
"""
lenigma — decode Lenovo ThinkStation/ThinkPad smart beep error codes.

A Lenovo workstation that can't boot plays a 4-character error code as a
sequence of narrow-band tones. Lenovo's mobile app listens with the mic
and decodes. This does the same on Linux without the Play Store gating.

    lenigma lookup 0281       # look up a known code
    lenigma list              # list all known codes
    lenigma listen            # capture mic, decode, report
    lenigma listen --seconds 30
    lenigma wav message.wav   # decode a saved 16 kHz mono WAV

See protocol.md for the full encoding spec (16 kHz FSK, 18 bands,
START/STOP framing, mod-256 checksum).

listen mode needs: pip install sounddevice numpy
"""

from __future__ import annotations

import argparse
import json
import math
import struct
import sys
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence


# ---------------------------------------------------------------------------
# Codes — starter set shipped inline; extend by putting codes.json next to
# this file (or under ~/.config/lenigma/). Two JSON shapes are accepted:
#   1. flat:   {"0281": "Generic embedded controller error"}
#   2. rich:   {"0281": {"description": "...", "category": "...", ...}}
# ---------------------------------------------------------------------------
CODES: dict[str, str] = {
    "0164": "MEBx password retry count exceeded",
    "0167": "No microcode update found for processor",
    "0175": "Bad CRC1 — stop POST task",
    "0176": "System security — chassis tampered with",
    "0177": "Bad SVP data — stop POST task",
    "0182": "Bad CRC of security settings in EEPROM",
    "0187": "EAIA data access error",
    "0188": "Invalid RFID Serialization or Configuration information area",
    "0189": "Invalid RFID configuration information area",
    "0190": "Critical low battery error",
    "0191": "System security — invalid remote change requested",
    "0192": "Embedded security hardware tamper detected",
    "0199": "Security password retry count exceeded",
    "0251": "System CMOS checksum bad — replace CMOS battery or reset defaults",
    "0253": "EFI variable block data destroyed",
    "0270": "Real-time clock error",
    "0271": "Check date and time settings",
    "0280": "Previous boot incomplete — default configuration used",
    "0281": "Generic embedded controller error",
    "0282": "Illegal memory configuration — reseat DIMMs",
    "02B2": "Incorrect drive A type",
    "02D0": "System cache error",
    "02F0": "CPU ID failing",
    "02F4": "EISA CMOS not writable",
    "02F5": "DMA test failed",
    "02F6": "Software NMI failed",
    "02F7": "Fail-safe timer NMI failed",
    "1802": "Unauthorized network card — power off and remove",
    "1820": "More than one external fingerprint reader attached",
    "2100": "Initialization error on HDD0 (main)",
    "2102": "Initialization error on HDD1",
    "2110": "Read error on HDD0 (main)",
    "2112": "Read error on HDD1",
}


def _safe_str(s: str) -> str:
    """
    Strip ASCII control characters (except tab) so attacker-supplied
    strings from audio or codes.json cannot manipulate the terminal
    with ANSI escapes, cursor moves, window-title sequences, etc.
    Printable ASCII and ordinary non-control Unicode pass through.
    """
    return "".join(
        c for c in s
        if c == "\t" or 0x20 <= ord(c) < 0x7F or ord(c) >= 0xA0
    )


# Rich records (severity, category, repairs[], sources[]) for codes that
# came from a JSON entry rather than the inline starter dict. Populated
# alongside `CODES` by `load_extra_codes`. `cmd_lookup --long` reaches
# in here to print the repair steps.
_FULL: dict[str, dict] = {}


def _normalise_extras(data: dict) -> tuple[dict[str, str], dict[str, dict]]:
    """Return (descriptions, full_records). Both are sanitised."""
    descriptions: dict[str, str] = {}
    full: dict[str, dict] = {}
    for code, val in data.items():
        if not isinstance(code, str) or code != _safe_str(code):
            continue
        if isinstance(val, str):
            descriptions[code] = _safe_str(val)
        elif isinstance(val, dict):
            desc = val.get("description") or val.get("desc") or ""
            if not desc:
                continue
            descriptions[code] = _safe_str(desc)
            record: dict = {"description": _safe_str(desc)}
            for field_name in ("severity", "category", "origin"):
                v = val.get(field_name)
                if isinstance(v, str):
                    record[field_name] = _safe_str(v)
            for list_name in ("repairs", "sources"):
                items = val.get(list_name)
                if isinstance(items, list):
                    record[list_name] = [
                        _safe_str(s) for s in items if isinstance(s, str)
                    ]
            full[code] = record
    return descriptions, full


def load_extra_codes() -> None:
    """Merge optional codes.json from the script directory or ~/.config/lenigma."""
    for path in (
        Path(__file__).parent / "codes.json",
        Path.home() / ".config" / "lenigma" / "codes.json",
    ):
        if path.is_file():
            try:
                descs, full = _normalise_extras(json.loads(path.read_text()))
                CODES.update(descs)
                _FULL.update(full)
            except (json.JSONDecodeError, OSError) as e:
                print(f"warning: skipped {path}: {e}", file=sys.stderr)


# ===========================================================================
# Smart-beep decoder (FSK, 16 kHz mono 16-bit PCM).
# ===========================================================================
SAMPLE_RATE = 16_000
FFT_SIZE = 1024
MIN_HZ = 690
MAX_HZ = 2125
PEAK_MARGIN_DB = 12.0   # peak-minus-mean in the search band

# FSK bands: (min_hz_inclusive, max_hz_inclusive, label)
_BANDS: list[tuple[int, int, str]] = [
    (774, 826, "0"),
    (825, 876, "1"),
    (875, 926, "2"),
    (934, 986, "3"),
    (984, 1036, "4"),
    (1044, 1096, "5"),
    (1114, 1166, "6"),
    (1169, 1231, "7"),
    (1234, 1306, "8"),
    (1314, 1386, "9"),
    (1389, 1476, "A"),
    (1479, 1556, "B"),
    (1555, 1651, "C"),
    (1650, 1746, "D"),
    (1745, 1860, "E"),
    (1859, 1975, "F"),
    (1975, 2125, "START"),
    (690, 771, "STOP"),
]
_CENTERS: list[tuple[float, str]] = sorted(((lo + hi) / 2, label) for lo, hi, label in _BANDS)


def classify(hz: float) -> str | None:
    """
    Map a frequency (Hz) to a protocol symbol via nearest-center matching.
    Returns None if hz is outside the search band or more than ~80 Hz
    from any centre.
    """
    if hz <= 0:
        return None
    best_label: str | None = None
    best_dist = float("inf")
    for center, label in _CENTERS:
        d = abs(hz - center)
        if d < best_dist:
            best_dist = d
            best_label = label
    if best_dist > 80.0:
        return None
    return best_label


# --- FFT (pure stdlib, radix-2 iterative, windowed) -----------------------
def _hann(n: int) -> list[float]:
    return [0.5 - 0.5 * math.cos(2 * math.pi * i / (n - 1)) for i in range(n)]


_WINDOW = _hann(FFT_SIZE)
_BIN_HZ = SAMPLE_RATE / FFT_SIZE   # 15.625
_MIN_BIN = int(MIN_HZ / _BIN_HZ)   # 44
_MAX_BIN = math.ceil(MAX_HZ / _BIN_HZ)  # 136


def _fft(re: list[float], im: list[float]) -> None:
    """In-place radix-2 FFT. len(re) must be a power of two."""
    n = len(re)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            re[i], re[j] = re[j], re[i]
            im[i], im[j] = im[j], im[i]
    size = 2
    while size <= n:
        half = size >> 1
        theta = -2 * math.pi / size
        wr_step = math.cos(theta)
        wi_step = math.sin(theta)
        for start in range(0, n, size):
            wr, wi = 1.0, 0.0
            for k in range(half):
                a = start + k
                b = a + half
                tr = wr * re[b] - wi * im[b]
                ti = wr * im[b] + wi * re[b]
                re[b] = re[a] - tr
                im[b] = im[a] - ti
                re[a] = re[a] + tr
                im[a] = im[a] + ti
                wr, wi = wr * wr_step - wi * wi_step, wr * wi_step + wi * wr_step
        size <<= 1


def dominant_hz(samples: Sequence[int], offset: int) -> float:
    """
    One windowed FFT at `offset`; returns the peak frequency in the
    search band, or 0.0 if peak-minus-mean is below PEAK_MARGIN_DB.
    """
    if offset + FFT_SIZE > len(samples):
        return 0.0
    re = [samples[offset + i] * _WINDOW[i] for i in range(FFT_SIZE)]
    im = [0.0] * FFT_SIZE
    _fft(re, im)

    NEG_INF = -1e9
    peak_bin = -1
    peak_db = NEG_INF
    db_sum = 0.0
    count = 0
    db = [0.0] * (_MAX_BIN - _MIN_BIN)
    for b in range(_MIN_BIN, _MAX_BIN):
        mag = math.sqrt(re[b] * re[b] + im[b] * im[b])
        # 10*log10 (not 20) — matches the upstream implementation; the
        # 12 dB margin below is calibrated against this scale.
        d = 10.0 * math.log10(mag) - 30.0 if mag > 0 else NEG_INF
        db[b - _MIN_BIN] = d
        db_sum += d
        count += 1
        if d > peak_db:
            peak_db = d
            peak_bin = b
    if count == 0 or peak_bin < 0:
        return 0.0
    mean_db = db_sum / count
    if (peak_db - mean_db) < PEAK_MARGIN_DB:
        return 0.0

    lo = max(_MIN_BIN, peak_bin - 5)
    hi = min(_MAX_BIN, peak_bin + 6)
    best_bin = peak_bin
    best_val = peak_db
    for b in range(lo, hi):
        if db[b - _MIN_BIN] + 5.0 > best_val:
            best_val = db[b - _MIN_BIN]
            best_bin = b
    return best_bin * _BIN_HZ


# --- tone regions & symbol stream ----------------------------------------
@dataclass
class Symbol:
    label: str           # "0".."F" / "START" / "STOP"
    start_sample: int
    end_sample: int
    freq_hz: float

    @property
    def duration_ms(self) -> float:
        return (self.end_sample - self.start_sample) * 1000.0 / SAMPLE_RATE


# Sliding-FFT step in samples. 20 ms at 16 kHz = 320 samples. Short
# enough to localise tone onsets within real recordings (where beeps
# have soft attack envelopes), long enough to keep the per-decode cost
# bounded.
HOP = 320

# Drop any symbol shorter than this after merging same-label hops.
# Real smart-beep tones are ~100 ms; classification flicker at tone
# boundaries lasts ~20-40 ms (one or two hops while the FFT window
# straddles a silence gap between adjacent tones). 60 ms is the sweet
# spot: filters out the flicker without eating into real tones.
MIN_SYMBOL_MS = 60.0


def symbols(samples: Sequence[int]) -> list[Symbol]:
    """
    Slide a 1024-sample FFT across `samples` at HOP spacing, classify
    each window's dominant frequency into a protocol symbol (or None
    if the FFT's peak-minus-mean margin is below threshold), then merge
    consecutive windows with the same label into one Symbol. Ultra-short
    runs (below MIN_SYMBOL_MS) are discarded as classification flicker
    at tone boundaries.
    """
    n = len(samples)
    if n < FFT_SIZE:
        return []

    # Pass 1: per-hop classification.
    positions: list[int] = []
    freqs: list[float] = []
    labels: list[str] = []
    i = 0
    while i + FFT_SIZE <= n:
        hz = dominant_hz(samples, i)
        label = classify(hz) if hz > 0 else None
        positions.append(i)
        freqs.append(hz)
        labels.append(label or "")
        i += HOP

    # Pass 2: compress into (label, start_hop, end_hop) runs.
    runs: list[tuple[str, int, int]] = []
    j = 0
    while j < len(labels):
        k = j
        while k < len(labels) and labels[k] == labels[j]:
            k += 1
        runs.append((labels[j], j, k))
        j = k

    # Pass 3: collapse a short run sandwiched between two longer same-
    # label runs into a silence break. This is the classic FFT-band-
    # crossing transient when two same-band tones abut across a short
    # gap — the FFT window spans the boundary and the peak briefly
    # drifts into an adjacent band. Treating it as a break (rather
    # than merging) preserves the two-symbol count.
    min_len_hops = max(1, int(SAMPLE_RATE * MIN_SYMBOL_MS / 1000.0) // HOP)
    smoothed: list[tuple[str, int, int]] = []
    r = 0
    while r < len(runs):
        lbl, a, b = runs[r]
        length = b - a
        if (lbl and length < min_len_hops
                and 0 < r < len(runs) - 1
                and runs[r - 1][0] == runs[r + 1][0]
                and runs[r - 1][0]  # both neighbours are real tones
                and (runs[r - 1][2] - runs[r - 1][1]) >= min_len_hops
                and (runs[r + 1][2] - runs[r + 1][1]) >= min_len_hops):
            # Replace with a silence run; leave the two neighbours as
            # separate same-label runs so they emit two symbols.
            smoothed.append(("", a, b))
        else:
            smoothed.append((lbl, a, b))
        r += 1

    # Pass 4: emit Symbols for each run that is both labelled and long
    # enough to not be classification flicker.
    out: list[Symbol] = []
    for lbl, a, b in smoothed:
        if not lbl or (b - a) < min_len_hops:
            continue
        start_sample = positions[a]
        end_sample = positions[b] if b < len(positions) else positions[-1] + FFT_SIZE
        hs = [freqs[k] for k in range(a, b) if freqs[k] > 0]
        mean_hz = sum(hs) / len(hs) if hs else 0.0
        out.append(Symbol(lbl, start_sample, end_sample, mean_hz))
    return out


# --- message framing & checksum ------------------------------------------
@dataclass
class Message:
    kind: str                   # "serial" or "code"
    nibbles: list[int] = field(default_factory=list)
    checksum_ok: bool = False
    serial: str | None = None
    code: str | None = None
    year: int | None = None
    month: int | None = None
    day: int | None = None
    hour: int | None = None
    minute: int | None = None
    second: int | None = None


def _checksum_ok(nibbles: list[int], length: int) -> bool:
    if length < 2 or length % 2 != 0 or len(nibbles) < length:
        return False
    total = 0
    for i in range(0, length - 2, 2):
        a, b = nibbles[i], nibbles[i + 1]
        if a < 0 or b < 0 or a > 15 or b > 15:
            return False
        total += (b << 4) | a
    expected = (nibbles[length - 1] << 4) | nibbles[length - 2]
    return (total & 0xFF) == expected


def _bytes_from_nibbles(nibbles: list[int], offset: int, count: int) -> bytes:
    out = bytearray()
    for i in range(offset, offset + count, 2):
        out.append(((nibbles[i + 1] & 0xF) << 4) | (nibbles[i] & 0xF))
    return bytes(out)


def _printable_ascii(b: bytes) -> str | None:
    """
    Decode `b` as ASCII only if every byte is a printable character
    (0x20-0x7E). Returns None otherwise. Guards against an attacker
    planting ANSI escapes or control characters in the code/serial
    strings via a crafted audio message that passes the checksum.
    """
    try:
        s = b.decode("ascii")
    except UnicodeDecodeError:
        return None
    if all(0x20 <= ord(c) < 0x7F for c in s):
        return s
    return None


def _decode_message(raw: list[int]) -> Message | None:
    if len(raw) == 18 and _checksum_ok(raw, 18):
        m = Message("serial", nibbles=raw, checksum_ok=True)
        m.serial = _printable_ascii(_bytes_from_nibbles(raw, 0, 16))
        return m
    if len(raw) == 22 and _checksum_ok(raw, 22):
        m = Message("code", nibbles=raw, checksum_ok=True)
        ts = _bytes_from_nibbles(raw, 0, 12)
        m.year = 2000 + ts[0]
        m.month = ts[1]
        m.day = ts[2]
        m.hour = ts[3]
        m.minute = ts[4]
        m.second = ts[5]
        m.code = _printable_ascii(_bytes_from_nibbles(raw, 12, 8))
        return m
    return None


def frame(syms: Iterable[Symbol]) -> list[Message]:
    """Walk a symbol stream, collecting nibbles between each START and STOP."""
    messages: list[Message] = []
    buffer: list[int] | None = None
    hex_to_val = {h: i for i, h in enumerate("0123456789ABCDEF")}
    for s in syms:
        if s.label == "START":
            buffer = []
            continue
        if s.label == "STOP":
            if buffer is None:
                continue
            msg = _decode_message(buffer)
            if msg is not None:
                messages.append(msg)
            buffer = None
            continue
        if buffer is None:
            continue
        v = hex_to_val.get(s.label)
        buffer.append(v if v is not None else -1)
    return messages


# --- top-level entry points ----------------------------------------------
def decode_pcm(samples: Sequence[int], sample_rate: int = SAMPLE_RATE) -> dict:
    """
    Decode a buffer of 16-bit signed PCM samples at 16 kHz. Returns:
        {"symbols": [Symbol, ...], "messages": [Message, ...],
         "codes": ["0281", ...], "serial": "<serial>"|None}
    """
    if sample_rate != SAMPLE_RATE:
        raise ValueError(f"decoder requires {SAMPLE_RATE} Hz input, got {sample_rate}")
    syms = symbols(samples)
    msgs = frame(syms)
    codes = [m.code for m in msgs if m.kind == "code" and m.code]
    serial = next((m.serial for m in msgs if m.kind == "serial" and m.serial), None)
    return {"symbols": syms, "messages": msgs, "codes": codes, "serial": serial}


# Max WAV size the decoder will accept, in samples (at 16 kHz). A full
# smart-beep transmission is well under a minute; 5 minutes is a generous
# ceiling that still prevents a crafted WAV from OOMing the process.
MAX_WAV_SAMPLES = SAMPLE_RATE * 300


def _downsample_int(samples: list[int], factor: int) -> list[int]:
    """
    Box-filter then decimate by an integer factor. The box-filter
    average attenuates frequencies near the destination Nyquist enough
    to keep aliasing out of the 690-2125 Hz protocol band, which is
    well below SAMPLE_RATE / 2. Pure-stdlib; quality is fine for
    integer ratios like 48 kHz -> 16 kHz (factor 3).
    """
    if factor <= 1:
        return list(samples)
    out: list[int] = []
    n = len(samples)
    i = 0
    while i + factor <= n:
        out.append(sum(samples[i:i + factor]) // factor)
        i += factor
    return out


def decode_wav(path: str) -> dict:
    with wave.open(path, "rb") as w:
        rate = w.getframerate()
        channels = w.getnchannels()
        if w.getsampwidth() != 2:
            raise ValueError(f"{path}: expected 16-bit, got {w.getsampwidth()*8}")
        if channels < 1 or channels > 8:
            raise ValueError(f"{path}: unexpected channel count {channels}")
        if rate != SAMPLE_RATE and (rate <= 0 or rate % SAMPLE_RATE != 0):
            raise ValueError(
                f"{path}: sample rate {rate} Hz isn't an integer multiple of "
                f"{SAMPLE_RATE} Hz. Convert with:\n"
                f"  ffmpeg -i {path} -ar 16000 -ac 1 -sample_fmt s16 out.wav"
            )
        nframes = w.getnframes()
        # Cap source-rate samples so the post-downmix/decimate buffer
        # is always under MAX_WAV_SAMPLES.
        max_src = MAX_WAV_SAMPLES * (rate // SAMPLE_RATE if rate >= SAMPLE_RATE else 1)
        if nframes > max_src:
            raise ValueError(
                f"{path}: {nframes/rate:.0f}s is longer than the "
                f"{MAX_WAV_SAMPLES/SAMPLE_RATE:.0f}s maximum"
            )
        raw = w.readframes(nframes)
    interleaved = list(struct.unpack("<%dh" % (len(raw) // 2), raw))
    if channels > 1:
        # Downmix by averaging across channels per frame.
        samples = [
            sum(interleaved[i:i + channels]) // channels
            for i in range(0, len(interleaved), channels)
        ]
    else:
        samples = interleaved
    if rate != SAMPLE_RATE:
        samples = _downsample_int(samples, rate // SAMPLE_RATE)
    return decode_pcm(samples)


# ===========================================================================
# CLI
# ===========================================================================
def _describe_partial(symbols_list: list) -> str | None:
    """
    If the symbol stream starts with START but never reaches STOP with
    a valid-length payload, return a short diagnostic line describing
    what was captured. Helps users of truncated recordings (e.g. help
    videos that cut off mid-transmission) understand why no code was
    decoded. Returns None if there's no partial-message pattern.
    """
    labels = [s.label for s in symbols_list]
    if "START" not in labels:
        return None
    i = labels.index("START")
    nibbles_after_start = [l for l in labels[i + 1:] if l != "START" and l != "STOP"]
    has_stop = "STOP" in labels[i + 1:]
    n = len(nibbles_after_start)
    if has_stop and n in (18, 22):
        return None  # Full message — already surfaced via result.messages.
    if n == 0:
        return "START detected but no data nibbles followed"
    nib_str = "".join(nibbles_after_start[:24])
    if has_stop:
        return (f"partial message: START + {n} nibble{'s' if n != 1 else ''} "
                f"({nib_str}) + STOP — {n} isn't a valid message length "
                f"(18 for serial, 22 for code)")
    return (f"partial message: START + {n} nibble{'s' if n != 1 else ''} "
            f"({nib_str}), no STOP — recording may be truncated before the "
            f"transmission completed")


def _print_result(result: dict, verbose: bool = False) -> bool:
    """Pretty-print decoded result; returns True if anything decoded."""
    if verbose:
        for s in result["symbols"]:
            print(f"  {s.start_sample/SAMPLE_RATE:7.3f}s  "
                  f"{s.duration_ms:6.0f} ms  {s.freq_hz:7.1f} Hz  {s.label}")
    anything = False
    if result["serial"]:
        print(f"serial: {_safe_str(result['serial'])}")
        anything = True
    for m in result["messages"]:
        if m.kind == "code" and m.code:
            ts = (f"{m.year:04d}-{m.month:02d}-{m.day:02d} "
                  f"{m.hour:02d}:{m.minute:02d}:{m.second:02d}")
            desc = CODES.get(m.code.upper())
            line = f"code:   {_safe_str(m.code)}   at {ts}"
            if desc:
                line += f"   — {_safe_str(desc)}"
            print(line)
            anything = True
    if not anything:
        partial = _describe_partial(result.get("symbols", []))
        if partial:
            print(_safe_str(partial))
    return anything


def _match_code(query: str) -> tuple[str, str] | None:
    """
    Resolve a code query against CODES, honouring lowercase-'x' wildcards
    in the keys (e.g. "B8xx" matches "B8FF", "B8FF" matches "B8xx",
    "T711" matches "T7x1").
    """
    # Exact (case-insensitive) match first.
    q_up = query.upper()
    for code in CODES:
        if code.upper() == q_up:
            return code, CODES[code]
    # Template match: lowercase 'x' in the stored key is a wildcard hex digit.
    for code in CODES:
        if "x" not in code:
            continue
        if len(code) != len(query):
            continue
        if all(kc == "x" or kc.upper() == qc for kc, qc in zip(code, q_up)):
            return code, CODES[code]
    # Reverse template: if the query itself has 'x' wildcards and a stored
    # key is a concrete match, surface the stored key.
    if "x" in query.lower():
        for code in CODES:
            if len(code) != len(query):
                continue
            if all(qc.lower() == "x" or kc.upper() == qc.upper()
                   for kc, qc in zip(code, query)):
                return code, CODES[code]
    return None


def cmd_lookup(args):
    code = args.code.removeprefix("0x").removeprefix("0X")
    # Zero-pad short all-hex inputs (e.g. "281" -> "0281") so the common
    # case of typing the code without leading zeros still resolves.
    if len(code) < 4 and code and all(c in "0123456789ABCDEFabcdef" for c in code):
        code = code.zfill(4)
    hit = _match_code(code)
    if hit:
        key, desc = hit
        print(f"{_safe_str(key)}  {_safe_str(desc)}")
        if args.long:
            full = _FULL.get(key)
            if full:
                cat = full.get("category")
                sev = full.get("severity")
                meta_bits = [b for b in (sev, cat) if b]
                if meta_bits:
                    print(f"  [{' · '.join(_safe_str(b) for b in meta_bits)}]")
                for r in full.get("repairs", []):
                    print(f"  · {_safe_str(r)}")
                for s in full.get("sources", []):
                    print(f"  source: {_safe_str(s)}")
        return 0
    print(f"{_safe_str(code)}  unknown code", file=sys.stderr)
    return 1


def cmd_list(_args):
    for code in sorted(CODES):
        print(f"{_safe_str(code)}  {_safe_str(CODES[code])}")
    return 0


def _save_wav(path: str, pcm: list[int]) -> None:
    """Write 16 kHz mono 16-bit PCM to `path`."""
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in pcm))


def cmd_listen(args):
    if args.seconds <= 0:
        print(f"--seconds must be positive, got {args.seconds}", file=sys.stderr)
        return 2
    try:
        import numpy as np
        import sounddevice as sd
    except ImportError:
        print("listen mode needs: pip install sounddevice numpy", file=sys.stderr)
        return 2

    total = int(args.seconds * SAMPLE_RATE)
    print(f"recording {args.seconds:.0f}s at {SAMPLE_RATE} Hz "
          f"(Ctrl-C to stop early) — hold the mic near the machine...")
    buf = sd.rec(total, samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    interrupted = False
    try:
        sd.wait()
    except KeyboardInterrupt:
        interrupted = True
        sd.stop()
        print("\nstopped early, decoding what was captured...")

    # On interrupt, trim to the portion actually filled so we don't feed
    # the decoder a buffer of trailing zeros.
    if interrupted:
        nz = np.flatnonzero(buf.flatten())
        end = int(nz[-1]) + 1 if nz.size else 0
        pcm = buf.flatten()[:end].tolist()
    else:
        pcm = buf.flatten().tolist()

    if not pcm:
        print("no audio captured", file=sys.stderr)
        return 1

    # Save the raw capture *before* decoding so even a decoder crash
    # leaves a WAV on disk that the user can share for diagnosis.
    if args.save:
        try:
            _save_wav(args.save, pcm)
            print(f"saved capture: {args.save}")
        except OSError as e:
            print(f"warning: could not save {args.save}: {e}", file=sys.stderr)

    result = decode_pcm(pcm)
    if not _print_result(result, verbose=args.verbose):
        print("no valid messages decoded — try again, closer to the speaker")
        if not args.verbose:
            print("(re-run with --verbose to see every detected tone)")
        if not args.save:
            print("(re-run with --save out.wav to keep the recording for sharing)")
        return 1
    return 0


def cmd_wav(args):
    result = decode_wav(args.path)
    if not _print_result(result, verbose=args.verbose):
        print("no valid messages decoded")
        return 1
    return 0


def main():
    load_extra_codes()
    p = argparse.ArgumentParser(
        prog="lenigma",
        description=__doc__.split("\n\n")[0] if __doc__ else None,
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("lookup", help="look up a known error code")
    pl.add_argument("code", help="error code, e.g. 0281 or S001")
    pl.add_argument("-l", "--long", action="store_true",
                    help="also print severity, category, and repair steps")
    pl.set_defaults(func=cmd_lookup)

    sub.add_parser("list", help="list known codes").set_defaults(func=cmd_list)

    ln = sub.add_parser("listen", help="capture from mic and decode")
    ln.add_argument("--seconds", type=float, default=15.0)
    ln.add_argument("--save", metavar="FILE",
                    help="write the captured audio to FILE (16 kHz mono WAV) "
                         "for later analysis or sharing in a bug report")
    ln.add_argument("-v", "--verbose", action="store_true",
                    help="print every detected tone")
    ln.set_defaults(func=cmd_listen)

    pw = sub.add_parser("wav", help="decode a saved 16 kHz mono WAV")
    pw.add_argument("path")
    pw.add_argument("-v", "--verbose", action="store_true")
    pw.set_defaults(func=cmd_wav)

    args = p.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
