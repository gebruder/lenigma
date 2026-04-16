#!/usr/bin/env python3
"""
Round-trip test: encode a known code+timestamp+serial using the protocol
spec, render it as a PCM tone sequence, pipe through lenigma.py, and
check that it recovers the original values.
"""

import math
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lenigma import decode_pcm, SAMPLE_RATE, _BANDS

# center frequency per symbol, from band midpoints
_CENTER = {label: (lo + hi) / 2 for lo, hi, label in _BANDS}


def byte_to_nibbles(b: int) -> tuple[int, int]:
    """Low-then-high, matching the protocol's byte assembly."""
    return (b & 0x0F, (b >> 4) & 0x0F)


def checksum(nibbles: list[int]) -> tuple[int, int]:
    """Return the two checksum nibbles (low, high) for the given data nibbles."""
    total = 0
    for i in range(0, len(nibbles), 2):
        total += (nibbles[i + 1] << 4) | nibbles[i]
    return (total & 0x0F, (total >> 4) & 0x0F)


def build_serial_message(serial: str) -> list[str]:
    assert len(serial) == 8, "serial must be 8 ASCII chars"
    data: list[int] = []
    for ch in serial:
        lo, hi = byte_to_nibbles(ord(ch))
        data += [lo, hi]
    ck_lo, ck_hi = checksum(data)
    data += [ck_lo, ck_hi]
    return ["START"] + ["0123456789ABCDEF"[n] for n in data] + ["STOP"]


def build_code_message(code: str, y: int, m: int, d: int, H: int, M: int, S: int) -> list[str]:
    assert len(code) == 4, "code must be 4 ASCII chars"
    data: list[int] = []
    for b in (y - 2000, m, d, H, M, S):
        lo, hi = byte_to_nibbles(b)
        data += [lo, hi]
    for ch in code:
        lo, hi = byte_to_nibbles(ord(ch))
        data += [lo, hi]
    ck_lo, ck_hi = checksum(data)
    data += [ck_lo, ck_hi]
    return ["START"] + ["0123456789ABCDEF"[n] for n in data] + ["STOP"]


def synthesize(labels: list[str], tone_ms: float = 120.0, gap_ms: float = 20.0,
               amplitude: float = 0.4) -> list[int]:
    """Render a symbol stream to 16-bit PCM samples at 16 kHz."""
    tone_samples = int(SAMPLE_RATE * tone_ms / 1000.0)
    gap_samples = int(SAMPLE_RATE * gap_ms / 1000.0)
    out: list[int] = [0] * int(SAMPLE_RATE * 0.05)
    for label in labels:
        f = _CENTER[label]
        for n in range(tone_samples):
            v = amplitude * math.sin(2 * math.pi * f * n / SAMPLE_RATE)
            out.append(int(v * 32767))
        out += [0] * gap_samples
    out += [0] * int(SAMPLE_RATE * 0.05)
    return out


def run_case(name: str, labels: list[str], expect: dict) -> bool:
    pcm = synthesize(labels)
    result = decode_pcm(pcm)
    ok = True
    for k, want in expect.items():
        got = result.get(k)
        if got != want:
            print(f"  FAIL {name}: {k} = {got!r}, expected {want!r}")
            ok = False
    if ok:
        extra = ""
        if result.get("serial"):
            extra += f" serial={result['serial']}"
        if result.get("codes"):
            extra += f" codes={result['codes']}"
        print(f"  PASS {name}:{extra}")
    return ok


def add_noise(pcm: list[int], snr_db: float, seed: int = 1) -> list[int]:
    import random
    rng = random.Random(seed)
    sq = sum(v * v for v in pcm) / max(1, len(pcm))
    sig_rms = math.sqrt(sq) or 1.0
    noise_rms = sig_rms / (10 ** (snr_db / 20.0))
    out = []
    for v in pcm:
        n = rng.gauss(0, noise_rms)
        s = max(-32768, min(32767, int(v + n)))
        out.append(s)
    return out


def main() -> int:
    cases = [
        ("serial 'AB123456'",
         build_serial_message("AB123456"),
         {"serial": "AB123456", "codes": []}),
        ("serial 'ZZ999999'",
         build_serial_message("ZZ999999"),
         {"serial": "ZZ999999", "codes": []}),
        ("code 'S001' @ 2026-04-16 10:30:00",
         build_code_message("S001", 2026, 4, 16, 10, 30, 0),
         {"codes": ["S001"]}),
        ("code 'T110' @ 2026-12-31 23:59:59",
         build_code_message("T110", 2026, 12, 31, 23, 59, 59),
         {"codes": ["T110"]}),
        ("code '0188' @ 2026-04-16 10:30:00",
         build_code_message("0188", 2026, 4, 16, 10, 30, 0),
         {"codes": ["0188"]}),
        ("code 'FFFF' @ 2026-01-01 00:00:00",
         build_code_message("FFFF", 2026, 1, 1, 0, 0, 0),
         {"codes": ["FFFF"]}),
        ("code 'O?_o' (hex-coverage)",
         build_code_message("O?_o", 2026, 1, 1, 0, 0, 0),
         {"codes": ["O?_o"]}),
    ]

    all_ok = True
    for name, labels, expect in cases:
        if not run_case(name, labels, expect):
            all_ok = False

    print("\nNoise robustness (code 'S001'):")
    labels = build_code_message("S001", 2026, 4, 16, 10, 30, 0)
    for snr in (40, 30, 20, 15, 10):
        pcm = synthesize(labels)
        pcm = add_noise(pcm, snr_db=snr)
        result = decode_pcm(pcm)
        ok = result["codes"] == ["S001"]
        print(f"  SNR={snr:2d}dB  {'PASS' if ok else 'FAIL'}  codes={result['codes']}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
