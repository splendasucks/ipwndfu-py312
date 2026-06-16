# Tracks — ipwndfu-py312

Registry of work units. Update status when starting, blocking, or finishing work.

## Active

### port-dfu-pwn-routing

| Field | Value |
|-------|-------|
| Type | fix / feat |
| Branch | `fix/port-dfu-detection-issue-1` |
| Issue | [#1](https://github.com/splendasucks/ipwndfu-py312/issues/1) |
| PR | [#2](https://github.com/splendasucks/ipwndfu-py312/pull/2) (base); follow-up commit pending |
| Status | **in progress** (uncommitted local changes) |

**Goal:** Accept Port DFU (`05ac:f014`) for `pwn` when classic DFU (`05ac:1227`) is absent. Decode AP CPID from packed `BDID:` per libirecovery.

**Done locally:**
- `find_exploit_dfu_devices()` — classic preferred, Port DFU fallback
- `parse_dfu_serial(..., port_dfu=True)` + `extract_ap_identifiers_from_port_dfu()`
- Runner + CLI messaging updated
- 38 tests passing; ruff clean

**Remaining:**
- [ ] Commit and push to PR branch
- [ ] Phase 2.1: Port DFU USB packet size / `IRECV_SEND_OPT_DFU_SMALL_PKT` when sending payloads

**Hardware note:** User device decodes to CPID `0x8140` (A18 / iPhone 16 Pro) — correctly reports `unsupported CPID`, not “no device”.

---

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
