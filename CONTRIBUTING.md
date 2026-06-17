# Contributing

Thanks for helping improve **ipwndfu-py312**.

## Primary focus

We prioritize **DFU diagnostics** (`identify`, chip database, JSON export, tests, docs). Changes should keep the README happy path working on modern Port DFU hardware without requiring checkm8-capable devices.

## Development setup

```bash
uv sync --dev
uv run pytest
uv run ruff check .
```

## checkm8 / exploit work

checkm8 support is a **community extension**. The maintainer does not ship working exploit payloads without hardware-in-the-loop validation on loaner A5–A11 devices.

If you submit exploit or USB payload changes:

1. Read [docs/CHECKM8.md](docs/CHECKM8.md)
2. Include a hardware validation report in the PR (device, CPID, mode, commands run, exit codes)
3. Add or extend unit tests for any serial parsing or routing logic

## Pull requests

- Use conventional commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`)
- Keep GPL-3.0 licensing and axi0mX attribution intact
- Do not commit firmware dumps or private device identifiers without redaction
