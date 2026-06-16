# ipwndfu-py312

[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20Sequoia%20%7C%20Apple%20Silicon-lightgrey.svg)](https://developer.apple.com/macos/)

Python 3.12-compatible fork of [ipwndfu](https://github.com/axi0mX/ipwndfu) for iOS device exploitation research on Apple Silicon Macs. Supports checkm8-based DFU mode operations for security research and device recovery.

> **Disclaimer:** This software is for authorized security research, education, and device recovery only. Exploiting devices you do not own or lack permission to test may violate law. The authors accept no liability for misuse.

## Device compatibility

| SoC   | Devices (examples)              | iOS / bridgeOS range   | checkm8 |
|-------|---------------------------------|------------------------|---------|
| A5    | iPhone 4s, iPad 2, iPod touch 4 | iOS 4–9                | Yes     |
| A6    | iPhone 5, iPad 4                | iOS 6–10               | Yes     |
| A7    | iPhone 5s, iPad Air             | iOS 7–12               | Yes     |
| A8    | iPhone 6, iPad mini 4           | iOS 8–12               | Yes     |
| A9    | iPhone 6s, iPhone SE (1st)      | iOS 9–15               | Yes     |
| A10   | iPhone 7, iPad (6th gen)        | iOS 10–16              | Yes     |
| A11   | iPhone 8/X, iPhone SE (2nd)*    | iOS 11–17              | Yes     |

\* A11 devices require booting with a specific key combination so the Secure Enclave does not patch the bootrom exploit window.

Devices with A12 and newer SoCs are **not** vulnerable to checkm8.

## Prerequisites (macOS Sequoia, arm64)

1. [Homebrew](https://brew.sh) (`/opt/homebrew`)
2. libusb (required for USB access to DFU devices):

```bash
brew install libusb
```

3. [uv](https://docs.astral.sh/uv/) package manager:

```bash
brew install uv
```

### libusb on macOS Sequoia

Apple Silicon Macs use the arm64 Homebrew prefix. After installing libusb, ensure the dynamic library is visible:

```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_LIBRARY_PATH:-}"
```

If `pyusb` cannot find the device, run with elevated privileges only when necessary (`sudo` may be required for raw USB on some macOS versions). Prefer a single Terminal session with libusb installed via Homebrew rather than mixing Intel and arm64 Python builds.

## Install

Clone and sync dependencies with uv (never use bare `pip install`):

```bash
git clone https://github.com/splendasucks/ipwndfu-py312.git
cd ipwndfu-py312
uv sync
```

## Usage

Put a compatible device into **DFU mode**, then:

```bash
# List USB devices / sanity check
uv run python -m ipwndfu_py312.cli devices

# Run checkm8 exploit (research use only)
uv run python -m ipwndfu_py312.cli pwn

# Interactive shell after successful pwn
uv run python -m ipwndfu_py312.cli shell
```

Legacy entry point (when port is complete):

```bash
uv run ipwndfu
```

## Project structure

```
ipwndfu-py312/
├── README.md              # Install, compatibility, disclaimers
├── LICENSE                # GPL-3.0-or-later (+ axi0mX attribution)
├── pyproject.toml         # Hatchling build, uv deps (pyusb, libusb1)
├── .gitignore             # Python, macOS, Xcode, firmware dumps
├── STRUCTURE.md           # Full annotated tree (modules & port map)
├── scripts/
│   └── check_libusb.sh    # Verify Homebrew libusb on arm64
├── src/ipwndfu_py312/     # Package (cli scaffold + future exploits)
└── tests/                 # pytest (TDD for CLI)
```

See [STRUCTURE.md](STRUCTURE.md) for the complete annotated file tree and module port map.

## Development

```bash
uv sync --dev
uv run pytest
uv run ruff check .
```

## License

GPL-3.0-or-later — see [LICENSE](LICENSE). Forked from axi0mX/ipwndfu; respect original licensing and device laws in your jurisdiction.

## Acknowledgments

- [axi0mX](https://github.com/axi0mX) — original ipwndfu and checkm8
- [checkm8](https://github.com/axi0mX/ipwndfu) community
