# Annotated project structure

Target layout for the Python 3.12 port. Files marked `(scaffold)` exist in this repo; others are planned for the full port.

```
ipwndfu-py312/
├── README.md                 # Install, compatibility, disclaimers
├── STRUCTURE.md              # This file — annotated tree
├── pyproject.toml            # PEP 518 project metadata (hatchling + uv)
├── .gitignore                # Python, macOS, Xcode, firmware dumps
├── LICENSE                   # GPL-3.0-or-later (to add)
│
├── src/
│   └── ipwndfu_py312/        # Main package (scaffold)
│       ├── __init__.py       # Version string, package docstring
│       ├── cli.py            # Click/argparse entry: devices, pwn, shell
│       ├── usb/              # USB transport layer
│       │   ├── __init__.py
│       │   ├── device.py     # pyusb + libusb1 device discovery
│       │   └── dfu.py        # DFU mode detection and transfers
│       ├── exploits/         # Per-SoC checkm8 payloads
│       │   ├── __init__.py
│       │   ├── a5.py         # A5 exploit chain
│       │   ├── a6.py
│       │   ├── a7.py
│       │   ├── a8.py
│       │   ├── a9.py
│       │   ├── a10.py
│       │   └── a11.py        # A11 requires no-SEP boot path
│       ├── payloads/         # Binary blobs (git-lfs or submodule)
│       │   └── README.md     # Provenance for each payload
│       └── util/
│           ├── __init__.py
│           ├── hex.py        # Hex dump helpers
│           └── logger.py     # Structured logging for USB traces
│
├── tests/
│   ├── __init__.py
│   ├── test_usb_mock.py      # Mock USB fixtures (no hardware)
│   └── conftest.py           # pytest fixtures
│
├── scripts/
│   └── check_libusb.sh       # Verify Homebrew libusb on arm64
│
└── docs/
    ├── DFU.md                # Entering DFU per device family
    └── PORTING.md            # Notes from original ipwndfu
```

## Module map (original → fork)

| Original (ipwndfu) | Planned location        |
|--------------------|-------------------------|
| `usb`              | `src/ipwndfu_py312/usb/` |
| `checkm8`          | `src/ipwndfu_py312/exploits/` |
| `dfuexec`          | `src/ipwndfu_py312/usb/dfu.py` |
| `ipwndfu.py`       | `src/ipwndfu_py312/cli.py` |
