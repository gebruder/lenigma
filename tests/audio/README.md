# Audio samples

Recordings of actual machines emitting smart-beep codes, for regression
testing of the decoder against real-world audio.

## Required format

16 kHz · mono · 16-bit signed PCM · WAV.

Anything else will be rejected by `decode_wav()`. Convert with:

```sh
ffmpeg -i input.m4a -ar 16000 -ac 1 -sample_fmt s16 output.wav
```

## File naming

Use the expected code and a short descriptor separated by dashes, e.g.:

```
0188-thinkpad-t480-coldboot.wav
S001-thinkstation-p520-bench.wav
```

If a single recording contains multiple codes, use the first code for
the filename and note the rest in a sibling `.txt` with the same base
name:

```
S001-thinkstation-p520-bench.wav
S001-thinkstation-p520-bench.txt     # expected: S001, T110 at 2026-04-16 10:30
```

## What to verify before committing

```sh
python3 lenigma.py wav tests/audio/<yourfile>.wav -v
```

Confirm:
1. The expected serial (if any) decodes.
2. The expected code(s) appear with plausible timestamps.
3. `-v` shows START and STOP tones bracketing each message.

If decoding fails, commit the file anyway and open an issue describing
the environment (room, mic, distance to chassis) — that's precisely the
real-world data the decoder needs to harden against.
