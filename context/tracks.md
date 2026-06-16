# Tracks — ipwndfu-py312

Registry of work units. Update status when starting, blocking, or finishing work.

## Active

### phase-2.1-usb-payloads

| Field | Value |
|-------|-------|
| Type | feat |
| Status | **planned** |
| Plan | `../../docs/plans/2026-06-15-feat-ipwndfu-checkm8-phase2-plan.md` (phase 2.1 section) |

**Goal:** Port upstream DFU USB primitives; replace `PAYLOAD_PENDING` with real exploit attempt on at least one SoC (HIL).

**Blocked by:** Payload binaries + USB transfer layer design (`docs/PORTING.md`).

## Completed

### phase-1-usb-foundation

| Field | Value |
|-------|-------|
| Status | **done** |
| Commit | `75a8913` — device enumeration, `devices` CLI |

### phase-2-exploit-routing

| Field | Value |
|-------|-------|
| Status | **done** (stubs) |
| Commit | `54ca56b` — registry, runner, A5–A11 modules, `pwn` CLI |

### port-dfu-pwn-routing

| Field | Value |
|-------|-------|
| Status | **done** |
| Commit | `24e33bf` on `fix/port-dfu-detection-issue-1` |
| Issue | [#1](https://github.com/splendasucks/ipwndfu-py312/issues/1) |
| PR | [#2](https://github.com/splendasucks/ipwndfu-py312/pull/2) |

## Backlog

| Track | Priority | Notes |
|-------|----------|-------|
| phase-3-shell | low | Post-exploit shell; after 2.1 |
| ci-github-actions | medium | pytest + ruff on push |
| clearer-unsupported-cpid | low | Map known CPIDs (e.g. `0x8140` → A18) in error message |
| bdid-disambiguation | medium | Shared CPIDs need BDID routing |

## Links

- [Phase 1 plan](../../docs/plans/2026-06-15-feat-ipwndfu-py312-port-phase1-plan.md) (workspace)
- [Phase 2 plan](../../docs/plans/2026-06-15-feat-ipwndfu-checkm8-phase2-plan.md) (workspace)
- [PORTING.md](../docs/PORTING.md)
