# Workflow — ipwndfu-py312

## Methodology

**Incremental port with TDD for routing logic.** USB exploit bytes are ported in focused slices (phase 2.1+). Mock USB in unit tests; hardware validation documented, not CI-gated.

## Git workflow

| Item | Convention |
|------|------------|
| Default branch | `main` |
| Feature branches | `fix/…`, `feat/…` (e.g. `fix/port-dfu-detection-issue-1`) |
| Commits | Conventional: `feat:`, `fix:`, `docs:`, `test:` |
| GitHub | Issues referenced in commits/PRs (`#1`) |
| Author | `splendasucks` / `68843866+splendasucks@users.noreply.github.com` via `-c` flags |

Commit only when the user asks. Push/PR via `gh` when requested.

## Quality gates (before PR)

```bash
cd ipwndfu-py312
uv run pytest --quiet
uv run ruff check src tests
uv run ipwndfu devices   # optional smoke (needs libusb)
```

## Code conventions

- **Imports:** Top of file only (no inline imports except documented circular-deps)
- **Types:** `dataclass(frozen=True, slots=True)` for value objects; `Protocol` for exploit interface
- **Switch:** Exhaustive `match` on enums with `never` in default where applicable
- **Line length:** 100 (ruff)
- **Scope:** Minimal diffs; match existing module layout under `src/ipwndfu_py312/`

## Testing strategy

| Layer | Location | Notes |
|-------|----------|-------|
| Unit | `tests/unit/` | Mock `find_*_devices`, serial parsing, registry |
| CLI | `tests/test_cli.py` | Patch runner/USB helpers |
| Hardware | Manual | Document in `docs/PORTING.md`; exit code 3 = payload pending |

Marker: `@pytest.mark.unit` for fast tests.

## CLI exit codes (`pwn`)

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | No DFU device |
| 2 | Unsupported CPID / failed |
| 3 | Routed correctly; payload/USB exploit not ported yet |

## AI / session workflow

1. Read `context/` artifacts (this folder) before implementation
2. Check `context/tracks.md` for active work
3. Read `docs/PORTING.md` for USB/SoC constraints
4. Update `tracks.md` when status changes
5. Update `tech-stack.md` if dependencies change
6. Update `product.md` if scope or device support changes

## Plans (workspace)

Long-form plans also live at `quick-wins/docs/plans/` (parent workspace). Prefer `context/tracks.md` for status; link to plan files for detail.

## Security

- Never commit secrets, firmware dumps, or user ECIDs
- `.gitignore` excludes firmware dumps and local artifacts
- Research disclaimer on `pwn` is mandatory
