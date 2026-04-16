# lenigma

Decode Lenovo ThinkStation / ThinkPad smart-beep error codes on Linux.

A Lenovo workstation that can't boot plays its error code as a sequence
of narrow-band tones (FSK, not Morse-style beep counts). `lenigma`
decodes these from any Linux machine with a microphone, a WAV file,
or raw PCM bytes.

## Install

Single file, standard library only for the core decoder. Live mic capture
needs two extras:

```sh
git clone https://github.com/gebruder/lenigma
cd lenigma
pip install sounddevice numpy    # only for the `listen` subcommand
```

## Usage

```sh
# Look up a known code
lenigma lookup 0281
lenigma lookup S001
lenigma lookup B8FF       # wildcards resolve: matches the B8xx template

# List every known code
lenigma list

# Capture from the default mic for N seconds, decode
python3 lenigma.py listen --seconds 15
python3 lenigma.py listen --seconds 30 -v   # -v prints every detected tone

# Decode a saved recording (must be 16 kHz mono 16-bit PCM WAV)
python3 lenigma.py wav recording.wav
```

Output looks like:

```
serial: AB123456
code:   S001   at 2026-04-16 10:30:00   — 3.3 V standby rail is above tolerance
```

## Extending the code database

`codes.json` ships with 204 codes covering BIOS, thermal, power, fans,
storage, USB, and ThinkPad POST. Drop a `codes.json` next to
`lenigma.py`, or at `~/.config/lenigma/codes.json`, to override or
extend. Both schemas are accepted:

```json
{ "0281": "Your own description" }
```

```json
{ "0281": { "description": "...", "category": "...", "repairs": [...] } }
```

Keys may use lowercase `x` as a hex wildcard (e.g. `B4x0` matches
`B400`, `B410`, ..., `B4F0`), following the same convention used by
Lenovo's own tables.

## Protocol

Full spec: [`protocol.md`](./protocol.md).

Briefly: 16 kHz mono 16-bit PCM, 18-band FSK. `START` = 1975-2125 Hz,
`STOP` = 690-771 Hz, hex `0`-`F` fill 774-1975 Hz. Every symbol is one
tone; duration and inter-tone gap are not used to discriminate symbols.
Each message is `START + N data nibbles + 2-nibble mod-256 checksum +
STOP`, with nibble pairs assembled low-nibble first.

## Status

- **Correctness**: the FSK bands, checksum, byte assembly, and message
  framing are faithful to the on-device implementation. Round-trip
  tests synthesise every hex symbol and several real error codes; all
  pass.
- **Noise robustness**: clean down to about 20 dB SNR in synthetic
  tests. Real room acoustics / fan noise / mic placement are untested
  and are the biggest known risk.
- **Real-audio validation**: **pending**. Contributions of WAV
  recordings from actual ThinkStations are welcome — see
  [Contributing](#contributing).

## Contributing

The most useful contribution right now is audio. If you have a
ThinkStation or ThinkPad that emits smart-beep codes, please:

1. Record the full sequence with a phone or laptop mic.
2. Convert to 16 kHz mono 16-bit PCM WAV (`ffmpeg -i in.m4a -ar 16000
   -ac 1 -sample_fmt s16 out.wav`).
3. Open a PR adding the file under `tests/audio/` with a short
   description of the machine and the codes you expected.

For code changes, `python3 tests/test_roundtrip.py` should pass before
and after.

## Security

See [`SECURITY.md`](./SECURITY.md). Vulnerability reports go to the
private advisory endpoint listed there, not public issues.

## License

MIT — see [`LICENSE`](./LICENSE).
