# Apple DFU diagnostics

User-facing guide for identifying Apple devices in DFU mode with **ipwndfu-py312** on macOS Apple Silicon.

## Quick start

1. Install [Homebrew libusb](https://formulae.brew.sh/formula/libusb) and [uv](https://docs.astral.sh/uv/).
2. Put the device in **DFU mode** (classic `05ac:1227` or Port DFU `05ac:f014`).
3. Run:

```bash
uv sync
uv run ipwndfu identify
```

Exit code **0** means the device was identified (including A12+ chips that are not checkm8-eligible).

## Commands

| Command | Purpose |
|---------|---------|
| `ipwndfu devices` | List all USB devices; marks Apple DFU interfaces |
| `ipwndfu devices --json` | JSON array of `DeviceIdentity` for DFU devices only |
| `ipwndfu identify` | Human-readable chip, CPID, BDID, ECID, checkm8 eligibility |
| `ipwndfu identify --json` | Same fields as JSON |

### Example (Port DFU, iPhone 16 Pro class hardware)

```
Mode:     port
Chip:     Apple A18 (T8140)
AP CPID:  0x8140
AP BDID:  0x0c
ECID:     747D1772145A9529
checkm8:  no
USB:      Apple Inc. Apple Device (Port DFU Mode) (vid=0x05ac pid=0xf014)
```

### JSON schema (`devices --json` / `identify --json`)

Each record includes:

- `mode` — `"checkm8"` or `"port"`
- `ap_cpid` — hex string, e.g. `"0x8140"`
- `ap_bdid` — hex string
- `chip_name` — marketing name from chip database
- `checkm8_eligible` — boolean (A5–A11 only)
- `ecid` — from USB serial when present
- `raw_serial` — full DFU serial string
- `usb` — `vendor_id`, `product_id`, `product`

## Classic vs Port DFU

| USB PID | Mode | Serial layout |
|---------|------|----------------|
| `05ac:1227` | Classic DFU | `CPID:` and `BDID:` name the application processor directly |
| `05ac:f014` | Port DFU | AP CPID/BDID are packed in the `BDID:` field (libirecovery-compatible) |

See `src/ipwndfu_py312/usb/dfu.py` for parsing details.

## Library API

```python
from ipwndfu_py312.identify import identify_connected, identify_device
from ipwndfu_py312.usb.device import find_port_dfu_devices

for dev in find_port_dfu_devices():
    identity = identify_device(dev)
    print(identity.chip_name, identity.ap_cpid)
```

## Troubleshooting

- **No USB devices** — run `scripts/check_libusb.sh`; set `DYLD_LIBRARY_PATH=/opt/homebrew/lib` if needed.
- **Device not in DFU** — recovery or normal mode will not show `05ac:1227` / `05ac:f014`.
- **Unknown CPID** — chip may be newer than the bundled database; open an issue with `identify --json` output.

## checkm8

The `pwn` command is an **experimental contributor scaffold** for A5–A11 only. Modern devices should use `identify`. See [CHECKM8.md](CHECKM8.md).
