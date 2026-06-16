# Tech stack — ipwndfu-py312

## Platform

| Item | Choice |
|------|--------|
| OS (primary) | macOS Sequoia, arm64 |
| Python | `>=3.12` (developed/tested on 3.14 in venv) |
| USB backend | Homebrew `libusb` at `/opt/homebrew/lib` |
| Hardware | Physical Apple device in DFU for HIL; mocks in CI |

## Languages & frameworks

- **Python 3.12+** — stdlib `argparse` CLI (no Click yet)
- **pyusb** — USB enumeration and string descriptors
- **libusb1** — libusb bindings / backend for pyusb

## Dependencies (`pyproject.toml`)

| Package | Constraint | Role |
|---------|------------|------|
| `pyusb` | `>=1.2.1` | USB device access |
| `libusb1` | `>=3.1.0` | libusb backend |
| `pytest` | `>=8.0` (dev) | Tests |
| `ruff` | `>=0.8` (dev) | Lint + import sort |

**Policy:** Add deps only via `pyproject.toml`; use `uv sync`, not bare `pip install`.

## Build & packaging

- **Build backend:** Hatchling
- **Layout:** `src/ipwndfu_py312/` (src layout)
- **CLI entry:** `ipwndfu = ipwndfu_py312.cli:main`

## Tooling

```bash
uv sync              # install deps
uv sync --dev        # include pytest, ruff
uv run pytest        # tests (pythonpath=src)
uv run ruff check .  # lint (line-length 100, py312)
```

## USB identifiers

| PID | Mode | Notes |
|-----|------|-------|
| `0x1227` | Classic DFU | Bootrom checkm8 target |
| `0xf014` | Port DFU | AP CPID encoded in packed `BDID:` (libirecovery layout) |

## External references

- Upstream: [axi0mX/ipwndfu](https://github.com/axi0mX/ipwndfu)
- Port DFU parsing: libirecovery `irecv_devices_get_device_by_client`
- Docs in repo: `docs/PORTING.md`, `STRUCTURE.md`, `payloads/README.md`

## Infrastructure

- **Git remote:** `github.com/splendasucks/ipwndfu-py312`
- **CI:** Not yet configured; local pytest + ruff are the gate
- **License:** GPL-3.0-or-later

## Environment variables

| Variable | When |
|----------|------|
| `DYLD_LIBRARY_PATH=/opt/homebrew/lib:...` | If pyusb cannot load libusb |
| `sudo` | Sometimes required for raw USB on macOS |

Verify libusb: `scripts/check_libusb.sh`
