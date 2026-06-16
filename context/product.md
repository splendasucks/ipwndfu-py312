# Product — ipwndfu-py312

## One-liner

Python 3.12+ port of axi0mX/ipwndfu for checkm8 / DFU security research on Apple Silicon Macs.

## Problem

Upstream ipwndfu targets legacy Python and is painful to run on macOS Sequoia arm64. Researchers need a typed, testable fork with modern tooling (`uv`, pytest, ruff) while preserving GPL licensing and axi0mX attribution.

## Solution

Incremental port: USB discovery → DFU session parsing → per-SoC checkm8 routing → (future) USB exploit primitives and payloads → (future) post-exploit shell.

## Users

| Persona | Need |
|---------|------|
| Security researcher | Reproduce checkm8 on owned A5–A11 hardware |
| DFU / recovery hobbyist | Understand device mode and SoC from USB serial |
| Maintainer (splendasucks) | Extend port without re-reading upstream each session |

## Core capabilities (by phase)

| Phase | Status | Delivers |
|-------|--------|----------|
| 1 — USB foundation | Done | `devices` CLI, classic DFU detection (`05ac:1227`) |
| 2 — Exploit routing | Done (stubs) | CPID registry, `pwn` CLI, A5–A11 modules return `PAYLOAD_PENDING` |
| 2.1 — USB + payloads | Planned | Port upstream DFU transfers; binary payloads under `payloads/` |
| 3 — Shell & recovery | Planned | Post-exploit shell, NOR/NAND helpers (subset) |

## Device scope (checkm8)

**In scope:** Apple SoCs A5 through A11 (iPhone 4s era through iPhone X / 8).

**Out of scope:** A12 and newer (e.g. A18 / iPhone 16 family, CPID `0x8140`). Port DFU (`05ac:f014`) may appear on modern devices; CLI accepts it for discovery and routing, but checkm8 does not apply.

## Success metrics

- `uv run pytest` and `uv run ruff check .` pass on every change
- `uv run ipwndfu devices` / `pwn` give actionable messages without hardware surprises
- Hardware matrix documented in `docs/PORTING.md` before claiming exploit support

## Legal / ethics

Authorized research and owned devices only. Disclaimer shown on `pwn`. No silent exploitation of non-DFU devices.

## Roadmap (high level)

1. Land Port DFU routing (accept `f014`, decode AP CPID from packed `BDID`)
2. Phase 2.1: USB control transfers + one SoC end-to-end on hardware
3. Expand SoC coverage and payload provenance
4. Phase 3 shell (deferred)

## Related repos (splendasucks workspace)

Sibling repos under `quick-wins/`: `macos-devtools`, `dotfiles-m1`, `splendasucks-profile`. This product doc applies only to **ipwndfu-py312**.
