# Porting checkm8 from ipwndfu

Phase 2 implements **CPID detection**, **per-SoC modules** (`exploits/a5.py` … `a11.py`), and CLI routing. USB DFU transfers and shellcode execution are **not yet ported**.

## Upstream mapping

| Module | Upstream focus | CPIDs (hex) |
|--------|----------------|-------------|
| `a5` | S5L8940X, S5L8950X | 8950, 8955 |
| `a6` | S5L8960X | 8960 |
| `a7` | S5L8965X, T7002 | 8965, 7002 |
| `a8` | T7000, T7001 | 7000, 7001 |
| `a9` | S8000, S8001, S8003 | 8000, 8001, 8003, 8012 |
| `a10` | T8010, T8011 | 8010, 8011 |
| `a11` | T8015 | 8015 |

CPID is parsed from the Apple DFU USB serial string (`CPID:8015 …`). See `usb/dfu.py`.

### DFU USB modes

| PID | Mode | checkm8 |
|-----|------|---------|
| `05ac:1227` | Classic DFU | Yes (direct bootrom USB) |
| `05ac:f014` | Port DFU | Yes for routing — AP CPID is packed in the `BDID:` field (see `usb/dfu.py`) |

Classic DFU exposes `CPID:` for the application processor. Port DFU exposes `CPID:0022` for the USB port controller; libirecovery derives AP `CPID`/`BDID` from the packed `BDID:` value. Phase 2.1 must use the correct USB packet size for the active PID.

## Phase 2.1 work

1. Port `dfu.py` USB control transfers from upstream into `usb/dfu_session.py` (or extend `usb/dfu.py`)
2. Port per-SoC logic from `checkm8.py` / device-specific paths into each `exploits/a*.py`
3. Vendor payloads under `payloads/` with attribution
4. BDID-based disambiguation where CPID alone is insufficient
5. Hardware validation matrix (one device per SoC generation)

## Hardware test checklist

```bash
uv run ipwndfu devices    # DFU device visible, serial contains CPID
uv run ipwndfu pwn        # routes to correct SoC module (exit 3 = payload pending)
```

On macOS Sequoia / Apple Silicon, ensure Homebrew `libusb` is linked (`scripts/check_libusb.sh`).

## A11 note

iPhone 8 / X require DFU entry **without** Secure Enclave bootrom patch — hold buttons per README before running `pwn`.
