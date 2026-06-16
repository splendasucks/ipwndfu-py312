# Python styleguide — ipwndfu-py312

Project-specific conventions beyond ruff defaults.

## Layout

- Package root: `src/ipwndfu_py312/`
- USB layer: `usb/` — no exploit logic
- Exploits: `exploits/` — per-SoC modules + `registry.py`, `runner.py`
- Tests mirror domains: `tests/unit/test_*.py`, `tests/test_cli.py`

## Naming

- Modules: `a5.py` … `a11.py` match SoC generation, not marketing names
- Functions: `find_*_devices`, `parse_dfu_serial`, `run_checkm8`
- Constants: `APPLE_VID`, `CHECKM8_DFU_PID`, `PORT_DFU_PID`

## Types

- Use `int | None` for optional parsed fields
- `ExploitResult` / `ExploitStatus` for all `pwn` outcomes
- Avoid `Any` unless interfacing with pyusb opaque handles

## USB / DFU

- Never hardcode only `0x1227`; use `find_exploit_dfu_devices()` for `pwn`
- Port DFU: pass `port_dfu=True` to serial parser (or use `session_from_device`)
- Document USB mode assumptions in `docs/PORTING.md` when changing transfer code

## Tests

- Patch at use site: `ipwndfu_py312.exploits.runner.find_exploit_dfu_devices`
- Use realistic Apple serial strings in fixtures (classic and Port DFU)
- No network or hardware in unit tests

## Dependencies

- Document new packages in `context/tech-stack.md` before adding to `pyproject.toml`
