# Workflow — ipwndfu-py312

## Methodology

**Diagnostics-first.** README happy path must pass on maintainer hardware (A18 Port DFU). checkm8 work is community-contribution unless HIL evidence is provided.

## Git workflow

| Item | Convention |
|------|------------|
| Default branch | `main` |
| Feature branches | `feat/…`, `fix/…` |
| Commits | Conventional (`feat:`, `fix:`, `docs:`) |
| Author email | `68843866+splendasucks@users.noreply.github.com` via `-c` when committing |

Commit/push only when user requests or plan execution requires it.

## Quality gates

```bash
cd ipwndfu-py312
uv run pytest --quiet
uv run ruff check src tests
```

## CLI exit codes

### `identify`

| Code | Meaning |
|------|---------|
| 0 | Device identified (including non-checkm8 chips) |
| 1 | No DFU device |

### `pwn` (experimental)

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | No DFU device |
| 2 | Unsupported CPID / failed (includes A12+) |
| 3 | Routed; payload port pending |

## checkm8 contribution policy

- PRs touching `exploits/` USB bytes require hardware validation notes
- Maintainer will not merge "should work" exploit claims without HIL evidence
- See `docs/CHECKM8.md` and `CONTRIBUTING.md`

## AI / session workflow

1. Read `context/product.md` and `context/tracks.md`
2. Primary command to verify: `uv run ipwndfu identify`
3. Update `tracks.md` when work completes
4. Do not promise `pwn` success in profile/resume copy

## Code conventions

See `context/styleguides/python.md`. Public API in `identify.py`; `exploits/` is experimental.
