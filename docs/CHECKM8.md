# checkm8 contributor guide

**checkm8 is not the primary product of this repository.** The maintained happy path is [DFU diagnostics](DIAGNOSTICS.md) (`identify`, `devices --json`). This document is for contributors porting exploit USB primitives from [axi0mX/ipwndfu](https://github.com/axi0mX/ipwndfu).

## Scope

| SoC generation | checkm8 | Status in this fork |
|----------------|---------|---------------------|
| A5–A11 | Vulnerable | Routed modules in `exploits/a5.py` … `a11.py`; **payloads not ported** (`PAYLOAD_PENDING`) |
| A12+ | Not vulnerable | Use `identify` — `pwn` exits unsupported with chip name |

## Maintainer policy

- **No maintainer HIL validation** without loaner A5–A11 hardware.
- PRs that change exploit USB transfers must include a **hardware validation report** (device model, iOS/bridgeOS build, exit codes, logs).
- Port DFU (`05ac:f014`) uses a different USB packet layout than classic DFU (`05ac:1227`); see `usb/device.py`.

## Upstream module map

| Module | Upstream focus | CPIDs (hex) |
|--------|----------------|-------------|
| `a5` | S5L8940X, S5L8950X | 8950, 8955 |
| `a6` | S5L8960X | 8960 |
| `a7` | S5L8965X, T7002 | 8965, 7002 |
| `a8` | T7000, T7001 | 7000, 7001 |
| `a9` | S8000, S8001, S8003 | 8000, 8001, 8003, 8012 |
| `a10` | T8010, T8011 | 8010, 8011 |
| `a11` | T8015 | 8015 |

CPID is parsed from the Apple DFU USB serial string. Port DFU packs AP identifiers in `BDID:` — see `usb/dfu.py`.

## Contributor checklist

```bash
uv run ipwndfu devices          # DFU visible
uv run ipwndfu identify         # correct CPID / chip name
uv run ipwndfu pwn              # expect exit 3 (payload pending) on supported SoC
uv run pytest --quiet
uv run ruff check .
```

## A11 note

iPhone 8 / X require DFU entry **without** Secure Enclave bootrom patch — use the documented button sequence before `pwn`.

## Phase 2.1 (community)

1. Port USB control transfers from upstream `dfu.py` into this package's USB layer
2. Port per-SoC logic from upstream `checkm8.py` into `exploits/a*.py`
3. Vendor payloads under `payloads/` with attribution
4. Hardware matrix: one validated device per SoC generation
