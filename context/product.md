# Product — ipwndfu-py312

## One-liner

Python 3.12+ Apple DFU USB diagnostics library and CLI for macOS Apple Silicon.

## Problem

Upstream ipwndfu targets legacy Python and is painful on macOS Sequoia arm64. Modern iPhones often expose **Port DFU** (`05ac:f014`) rather than classic DFU (`05ac:1227`), and owners need a typed way to read SoC identity from USB serial strings without running closed tools. A checkm8-only narrative fails for maintainers without A5–A11 hardware.

## Solution

Ship a **diagnostics-first** toolkit:

1. libusb USB enumeration (classic + Port DFU)
2. libirecovery-compatible AP CPID/BDID extraction from serial strings
3. Chip identification database (CPID → human-readable name, checkm8 eligibility)
4. CLI: `devices`, `identify`, JSON export
5. Optional **checkm8 scaffold** (`exploits/`) for community contributors with legacy hardware

## Users

| Persona | Need |
|---------|------|
| **Device owner (modern iPhone)** | Know chip, mode, and recovery state from DFU USB |
| DFU / recovery hobbyist | Understand Port DFU vs classic DFU |
| Security researcher | Foundation for authorized research; checkm8 path if A5–A11 available |
| Maintainer (splendasucks) | Extend without re-reading upstream; validate on own hardware |

## Core capabilities (by phase)

| Phase | Status | Delivers |
|-------|--------|----------|
| 1 — USB foundation | Done | `devices`, classic/Port DFU detection |
| 2 — Session parsing | Done | CPID/BDID parse, Port DFU packed BDID decode |
| **v1 — Identify** | **Active** | Chip DB, `identify` CLI, `devices --json` |
| checkm8 scaffold | Done (stubs) | `pwn` routes A5–A11; payloads not ported |
| checkm8 port | Community | Requires contributor hardware + HIL validation |

## Device scope

**Diagnostics:** Any Apple DFU-capable device (classic `1227` or Port `f014`), including A12+ (e.g. A18 / CPID `0x8140`).

**checkm8:** A5–A11 only. Not a v1 success metric for the maintainer.

## Success metrics

- `uv run pytest` and `uv run ruff check .` pass on every change
- `uv run ipwndfu identify` exits **0** on maintainer hardware (iPhone 16 Pro, Port DFU, CPID `0x8140`)
- `devices --json` emits stable schema
- CI green on push
- README happy path does not require checkm8 hardware

## Non-goals (maintainer)

- Shipping working checkm8 exploit without hardware-in-the-loop validation
- Phase 3 post-exploit shell as primary roadmap
- Repo rename (keep `ipwndfu-py312` for GPL lineage)

## Legal / ethics

Authorized research and owned devices only. `pwn` shows research disclaimer. No silent exploitation of non-DFU devices.

## Portfolio framing

> Modern Python 3.12 toolkit for Apple DFU USB analysis on macOS Apple Silicon: libusb enumeration, Port DFU decode, libirecovery-compatible AP identification, typed CLI with JSON output. Modular checkm8 scaffold (A5–A11) for community continuation; validated on current-generation hardware.

## Related repos

Sibling repos under `quick-wins/`: `macos-devtools`, `dotfiles-m1`, `splendasucks-profile`.
