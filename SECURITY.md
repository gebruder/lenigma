# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | Yes       |
| < 0.1   | No        |

## Reporting a Vulnerability

Report security vulnerabilities via GitHub's private vulnerability reporting at [github.com/gebruder/lenigma/security/advisories](https://github.com/gebruder/lenigma/security/advisories).

Do not open a public issue for security vulnerabilities.

You should receive an initial response within 72 hours. If the vulnerability is accepted, a fix will be released as a patch version (e.g., 0.1.1) and the advisory will be published after the fix is available.

## Scope

The following are in scope for security reports:

- WAV / PCM parser memory safety (malformed input crashing or misbehaving the decoder)
- FFT or envelope arithmetic overflow / underflow on adversarial audio
- `codes.json` parsing (injection through crafted keys or values, path traversal via config paths)
- `load_extra_codes()` path resolution (symlink attacks, unintended file reads)
- CLI argument handling (shell-expansion or quoting issues in `listen` / `wav` / `lookup`)
- Any behaviour that lets a supplied audio file or config file execute code

The following are out of scope:

- Incorrect decoding of low-quality recordings (this is a quality-of-result issue, not a security issue — open a normal issue with a sample WAV)
- Denial of service via extremely long input files (CPU cost is proportional to input size by design)
- Vulnerabilities in third-party dependencies `sounddevice` or `numpy` (report upstream, but let us know)
- Copyright questions about the bundled `codes.json` descriptions (open a normal issue or PR)
