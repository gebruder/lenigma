# Lenovo ThinkStation Smart-Beep Protocol Specification

Binary FSK (frequency-shift keying). Each symbol is one tone at one of
18 narrow-band frequencies. Duration and inter-tone gap are not used to
discriminate symbols — only center frequency matters.

---

## 1. Audio capture parameters

| Parameter | Value |
|---|---|
| Sample rate | **16 000 Hz** |
| Channels | **1 (mono)** |
| Bit depth | **16-bit signed little-endian PCM** |
| Audio source preset | `VOICE_RECOGNITION` (Android preset 2) preferred; falls back to `VOICE_COMMUNICATION` (preset 1) if background noise exceeds **51 dB** |
| Capture chunk | 3200 samples per chunk (200 ms) |
| Ring-buffer capacity | 96 000 samples (6 s) |

## 2. Tone detection

The decoder uses a **1024-point complex FFT** with a precomputed window
(the specific window shape is not material — any symmetric window with
comparable side-lobe suppression, e.g. Hann, gives equivalent results).

| Parameter | Value |
|---|---|
| FFT size (N) | **1024 samples** (64 ms) |
| Bin resolution | **15.625 Hz / bin** (= 16 000 / 1024) |
| Frequency search band | **690 – 2125 Hz** |
| Search bin range | bins 44 – 136 |
| Peak magnitude → dB | `dB = 10·log10(sqrt(re²+im²)) − 30` (non-standard ×10 multiplier, not ×20) |
| Detection condition | `(peak_dB − mean_dB_in_band) > 12 dB`; else "no tone" |
| Peak refinement | After finding peakBin, search neighbours in `[max(minBin, peakBin-5) .. peakBin+6]`; pick the bin where `dB + 5.0` first exceeds the provisional peak dB |
| Returned frequency | `int(bestBin · 16 000 / 1024)` |

## 3. Symbol alphabet — FSK bands

Every symbol is one continuous tone in exactly one of these 18 bands:

| Symbol | Nibble value | Band (Hz) |
|---|---|---|
| **START** | (marker) | 1975 – 2125 |
| **STOP**  | (marker) | 690 – 771 |
| `0` | 0  | 774 – 826  |
| `1` | 1  | 825 – 876  |
| `2` | 2  | 875 – 926  |
| `3` | 3  | 934 – 986  |
| `4` | 4  | 984 – 1036 |
| `5` | 5  | 1044 – 1096 |
| `6` | 6  | 1114 – 1166 |
| `7` | 7  | 1169 – 1231 |
| `8` | 8  | 1234 – 1306 |
| `9` | 9  | 1314 – 1386 |
| `A` | 10 | 1389 – 1476 |
| `B` | 11 | 1479 – 1556 |
| `C` | 12 | 1555 – 1651 |
| `D` | 13 | 1650 – 1746 |
| `E` | 14 | 1745 – 1860 |
| `F` | 15 | 1859 – 1975 |

Bands are non-overlapping except for 1-Hz seams at adjacent boundaries;
a frequency outside every band is treated as a missing / corrupted
nibble (flagged as a segment error, which will cause the per-message
checksum to fail).

## 4. Timing

**There are no long/short tone distinctions.** Durations are used only
for scheduling, not decoding. One `onFrequency(hz, tailDurationMs)`
callback fires per detected tone edge, regardless of tone length.

| Phase | Duration |
|---|---|
| Initial record window | 5.0 s |
| Serial-retrieval record window | 3.5 s |
| Code-retrieval record window | 3.5 s (4.5 s on retry) |
| Message-to-message period | **2250 ms** from the first tone of the previous message |
| Retry delay after bad-serial checksum | 50 ms |
| Retry delay after bad-code checksum | `750 − tailDurationMs` |

`decodeFor(seconds)` allocates `sample_rate × seconds × 2` bytes,
records that many samples, then scans the buffer and fires one or more
`onFrequency` callbacks in a batch.

## 5. Message framing

Two message types, both delimited by START / STOP tones.

### Serial-number message

```
START  n0 n1 n2 n3 n4 n5 n6 n7 n8 n9 nA nB nC nD nE nF  cksumLo cksumHi  STOP
         \----------- 16 data nibbles (8 ASCII bytes) --------/
```

- 16 data nibbles = 8 bytes = 8-character ASCII serial number.
- 2 checksum nibbles.
- Total: **18 nibbles** between START and STOP.

### Error-code message

```
START  yy mm dd HH MM SS  c0 c1 c2 c3  cksumLo cksumHi  STOP
         \--- 12 nibbles ---/ \-- 8 --/
         date-time (BCD)     code (4 ASCII chars)
```

- 12 date-time nibbles = 6 bytes: `year - 2000`, month (1-based on the
  wire), day, hour, minute, second. Each byte is assembled as
  `(nibble[odd] << 4) | nibble[even]`, i.e. nibble pairs are
  transmitted **low-nibble first**.
- 8 code nibbles = 4 bytes = 4-character ASCII error code
  (e.g. `"0188"`, `"S001"`, `"T110"`).
- 2 checksum nibbles.
- Total: **22 nibbles** between START and STOP.

### Session ending

An error-code message consisting of just `START … STOP` with zero data
nibbles signals "no more codes" and advances the session state to
"done".

## 6. Byte / nibble ordering

Bytes are assembled as:

```
byte[i/2] = (nibbles[i+1] << 4) | nibbles[i]
```

Within each two-nibble byte, the **low nibble is transmitted first** and
the **high nibble second**. Example: the ASCII byte `'S'` (0x53) is
transmitted as `nibble=3`, then `nibble=5`.

## 7. Checksum

```
sum = 0
for i = 0, 2, 4, ..., length - 4:             # stop two nibbles short
    if nibbles[i]   not in 0..15: return false
    if nibbles[i+1] not in 0..15: return false
    sum += (nibbles[i+1] << 4) + nibbles[i]   # byte, low-first
return (sum mod 256) == (nibbles[length-1] << 4) + nibbles[length-2]
```

The last two nibbles are the checksum byte (again low-nibble first),
equal to the sum of all preceding bytes mod 256. Called with
`length = 18` for serial messages and `length = 22` for code messages.

## 8. Noise handling and retries

- Before a decode pass, the capture buffer's peak amplitude is
  measured: `dB = 20·log10(max_abs / 32767) + 84`. If this exceeds
  51 dB while in `VOICE_RECOGNITION` mode, the session restarts in
  `VOICE_COMMUNICATION` mode (latched — only one switch happens).
- The per-FFT detection threshold is **12 dB** (peak-minus-mean across
  the 690-2125 Hz search band). Frames that fail this are silently
  dropped (no `onFrequency` fires for that window).
- Retries on failed checksum: up to **2 retries**, after which the
  session is abandoned with an error.
- An out-of-band frequency in a message flags `segmentError`; the
  message is still counted, but a mismatched checksum forces a retry.

## 9. What is *not* specified by this protocol

- **Minimum tone duration.** The edge detector accepts a run of only
  three consecutive samples with amplitude change > threshold (well
  under 1 ms at 16 kHz). The effective minimum is therefore set by the
  FFT window (64 ms) plus the 12 dB-over-mean detection threshold.
- **Inter-tone gap.** Not tracked. Two consecutive tones in different
  bands are two symbols; two consecutive tones in the same band appear
  to register as one symbol (there is no repeated-symbol mechanism,
  which matches the observed data — no code or timestamp ever needs
  two identical nibbles adjacent within one transmitted byte's nibble
  pair, and identical adjacent bytes appear to be separated by a brief
  gap by the transmitter).
- **Parity on individual symbols.** None. Integrity is provided by the
  per-message checksum and the segment-error flag only.

## 10. Error-code database

- Local dataset: `codes.json` — 204 codes (10 ThinkPad + 194
  ThinkStation), across categories System Voltages & Power, BIOS,
  Thermal, Fans, Power Supply, Storage, USB, System, ThinkPad.
- Schema per entry: `{id, sev, sevDescription, cat, catDescription,
  description, srcs[], reps[]}`.
- Remote update endpoint:
  `https://www.thinkworkstationsoftware.com/apps/MessageAPI/api/query?locale=%s`
  — GET, returns the same schema as a JSON array.
- Version probe:
  `https://www.thinkworkstationsoftware.com/apps/MessageAPI/api/version`.
- Separate product-info lookup (for serial-number expansion, not error
  codes):
  `https://supportapi.lenovo.com/v2.5/Product/<serial>` with the HTTP
  header `clientID: 5LN+Uw2dMZrSwEGnWEk9qQ==`.
