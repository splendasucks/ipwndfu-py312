# Tech stack — ipwndfu-py312

## Platform

| Item | Choice |
|------|--------|
| OS (primary) | macOS Sequoia, arm64 |
| Python | `>=3.12` |
| USB backend | Homebrew `libusb` at `/opt/homebrew/lib` |
| Maintainer hardware | iPhone 16 Pro, Port DFU (`05ac:f014`, AP CPID `0x8140`) |

## Languages & frameworks

- **Python 3.12+** — stdlib `argparse`, `json`, `dataclasses`
- **pyusb** — USB enumeration
- **libusb1** — libusb backend

## Dependencies (`pyproject.toml`)

| Package | Role |
|---------|------|
| `pyusb` | USB device access |
| `libusb1` | libusb backend |
| `pytest`, `ruff` | dev only |

Policy: `uv sync` only; document new deps in this file.

## Public API surface

| Module | Role |
|--------|------|
| `identify.py` | `DeviceIdentity`, `identify_device()`, `identify_connected()` |
| `data/apple_chips.py` | CPID → chip name, `checkm8_eligible` |
| `usb/device.py` | Enumeration, DFU mode detection |
| `usb/dfu.py` | Serial parsing, Port DFU AP ID extraction |
| `exploits/*` | **Experimental** — checkm8 routing scaffold |

## JSON schema (`devices --json` / `identify --json`)

Array of objects:

```json
{
  "mode": "port",
  "ap_cpid": "0x8140",
  "ap_bdid": "0x0c",
  "chip_name": "Apple A18 (T8140)",
  "checkm8_eligible": false,
  "ecid": "747D1772145A9529",
  "raw_serial": "..."
}
```

`mode`: `checkm8` | `port` | `unknown`. Hex fields as `0x` prefixed strings.

## Chip database

- Location: `src/ipwndfu_py312/data/apple_chips.py`
- Provenance: libirecovery `irecv_devices` CPID table (see `docs/CHIPDB.md`)
- `checkm8_eligible`: true for A5–A11 CPIDs in registry only

## CLI commands (v1)

| Command | Primary? |
|---------|----------|
| `identify` | Yes |
| `devices` / `devices --json` | Yes |
| `pwn` | Experimental (A5–A11, payloads not ported) |
| `shell` | Not implemented |

## USB identifiers

| PID | Mode |
|-----|------|
| `0x1227` | Classic DFU |
| `0xf014` | Port DFU |

## Infrastructure

- **Remote:** `github.com/splendasucks/ipwndfu-py312`
- **CI:** GitHub Actions — pytest + ruff
- **License:** GPL-3.0-or-later
