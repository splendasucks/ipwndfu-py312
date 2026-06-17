# Tracks — ipwndfu-py312

## Handoff (maintainer)

| Item | Value |
|------|-------|
| Hardware | iPhone 16 Pro — Port DFU only (no A5–A11) |
| Verified (post-pivot) | `devices`, `identify`, `devices --json` — pytest 48 tests |
| Resume copy | Diagnostics toolkit — **not** "working checkm8 port" |
| Branch | `fix/port-dfu-detection-issue-1` → merge then `feat/scope-pivot-v1` or direct to `main` |

## Active

_None — pivot v1 complete._

## Completed

| Track | Notes |
|-------|-------|
| scope-pivot-v1 | Chip DB, `identify`, JSON CLI, docs split, context rewrite |
| ci-github-actions | `.github/workflows/ci.yml` + README badge |
| phase-1-usb-foundation | `75a8913` |
| phase-2-exploit-routing | Stubs — `54ca56b` |
| port-dfu-pwn-routing | `24e33bf` — absorbed into diagnostics |
| clearer-unsupported-cpid | Merged into chip DB + `identify` |

## Cancelled (maintainer)

| Track | Notes |
|-------|-------|
| phase-2.1-usb-payloads | Community-only; needs A5–A11 HIL |
| phase-3-shell | — |

## Backlog (community)

| Track | Notes |
|-------|-------|
| checkm8-usb-primitives | See `docs/CHECKM8.md` |
| bdid-disambiguation | Shared CPIDs |
| hardware-validation-template | GitHub issue template |

## Links

- [DIAGNOSTICS.md](../docs/DIAGNOSTICS.md)
- [CHECKM8.md](../docs/CHECKM8.md)
- [CHIPDB.md](../docs/CHIPDB.md)
