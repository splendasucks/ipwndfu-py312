# Chip database provenance

The CPID → chip name mapping lives in `src/ipwndfu_py312/data/apple_chips.py`.

## Source

Entries are derived from the **libirecovery** `irecv_devices` table (application-processor CPID, internal codename, and generation labels). When adding CPIDs:

1. Cross-check [libimobiledevice/libirecovery](https://github.com/libimobiledevice/libirecovery) `irecv_devices.c`
2. Add a unit test in `tests/unit/test_apple_chips.py`
3. Add an identification fixture in `tests/unit/test_identify.py` if serial parsing is non-obvious

## Fields

| Field | Meaning |
|-------|---------|
| `generation` | Marketing SoC (e.g. `A18`) |
| `codename` | Internal name (e.g. `T8140`) |
| `chip_name` | Display string (`Apple A18 (T8140)`) |
| `checkm8_eligible` | `True` only for CPIDs in `exploits.registry.supported_cpids()` (A5–A11) |

## Port DFU example

Serial fragment `BDID:000000000C814000` decodes to AP CPID `0x8140`, BDID `0x0C` — validated on maintainer iPhone 16 Pro Port DFU hardware.
