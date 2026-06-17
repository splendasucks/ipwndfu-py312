# ipwndfu-py312

[![CI](https://github.com/splendasucks/ipwndfu-py312/actions/workflows/ci.yml/badge.svg)](https://github.com/splendasucks/ipwndfu-py312/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20Sequoia%20%7C%20Apple%20Silicon-lightgrey.svg)](https://developer.apple.com/macos/)

Python 3.12 toolkit for **Apple DFU USB diagnostics** on macOS Apple Silicon. Enumerates classic and Port DFU interfaces, decodes libirecovery-compatible AP processor IDs from USB serial strings, and exposes a typed CLI with JSON output.

Includes a modular **checkm8 routing scaffold** (A5–A11) for community continuation — payloads are not ported; use `identify` on modern hardware.

> **Disclaimer:** For authorized security research, education, and device recovery only. Exploiting devices you do not own or lack permission to test may violate law.

## Quick start: identify your device

Put the device in **DFU mode**, then:

```bash
git clone https://github.com/splendasucks/ipwndfu-py312.git
cd ipwndfu-py312
uv sync
uv run ipwndfu identify
```

Example output (Port DFU, A18-class hardware):

```
Mode:     port
Chip:     Apple A18 (T8140)
AP CPID:  0x8140
AP BDID:  0x0c
ECID:     747D1772145A9529
checkm8:  no
USB:      Apple Inc. Apple Device (Port DFU Mode) (vid=0x05ac pid=0xf014)
```

Machine-readable export:

```bash
uv run ipwndfu devices --json
uv run ipwndfu identify --json
```

See [docs/DIAGNOSTICS.md](docs/DIAGNOSTICS.md) for the full command reference and JSON schema.

## Prerequisites (macOS Sequoia, arm64)

1. [Homebrew](https://brew.sh) (`/opt/homebrew`)
2. libusb:

```bash
brew install libusb
```

3. [uv](https://docs.astral.sh/uv/):

```bash
brew install uv
```

If `pyusb` cannot open devices, ensure the arm64 library path is visible:

```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_LIBRARY_PATH:-}"
```

Run `scripts/check_libusb.sh` to verify the install.

## Commands

| Command | Purpose |
|---------|---------|
| `devices` | List USB devices; mark Apple DFU interfaces |
| `devices --json` | JSON identity records for DFU devices |
| **`identify`** | Chip name, CPID/BDID/ECID, checkm8 eligibility (**primary**) |
| `pwn` | Experimental checkm8 route (A5–A11 only; payloads not ported) |
| `shell` | Post-exploit shell (not implemented) |

### checkm8 (historical / contributors)

| SoC | checkm8 | Notes |
|-----|---------|-------|
| A5–A11 | Yes (bootrom) | Routed in `exploits/`; USB payloads pending |
| A12+ | No | Use `identify` — `pwn` reports unsupported with chip name |

Contributor guide: [docs/CHECKM8.md](docs/CHECKM8.md)

## Development

```bash
uv sync --dev
uv run pytest
uv run ruff check .
```

Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)

## Project structure

```
ipwndfu-py312/
├── src/ipwndfu_py312/
│   ├── identify.py          # Public diagnostics API
│   ├── data/apple_chips.py  # CPID database
│   ├── usb/                 # Enumeration + serial parse
│   └── exploits/            # checkm8 scaffold (A5–A11)
├── docs/
│   ├── DIAGNOSTICS.md
│   ├── CHECKM8.md
│   └── CHIPDB.md
└── tests/
```

See [STRUCTURE.md](STRUCTURE.md) for the annotated tree.

## License

GPL-3.0-or-later — see [LICENSE](LICENSE). Forked from axi0mX/ipwndfu.

## Acknowledgments

- [axi0mX](https://github.com/axi0mX) — original ipwndfu and checkm8
- [libirecovery](https://github.com/libimobiledevice/libirecovery) — CPID/device tables
