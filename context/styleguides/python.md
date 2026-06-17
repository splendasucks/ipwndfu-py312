# Python styleguide — ipwndfu-py312

## Layout

- Package root: `src/ipwndfu_py312/`
- **Public API:** `identify.py`, `usb/` — stable for library consumers
- **Experimental:** `exploits/` — checkm8 scaffold; not v1 promise
- **Data:** `data/apple_chips.py` — CPID lookup table
- Tests: `tests/unit/`, `tests/test_cli.py`

## JSON output

- Use `DeviceIdentity.to_dict()` + stdlib `json.dumps`
- No new JSON dependency
- Hex integers as `0x` prefixed strings in JSON for stability

## identify module

- `identify_device(UsbDeviceInfo)` — pure, testable
- `identify_connected()` — calls `find_exploit_dfu_devices()` or all DFU modes as appropriate
- ECID parsed from `ECID:` token in serial when present

## USB / DFU

- Port DFU: use `session_from_device` / `parse_dfu_serial(..., port_dfu=True)`
- Chip lookup: `lookup_chip(ap_cpid)` from `data.apple_chips`

## Tests

- Include Port DFU A18 fixture: `BDID:000000000C814000` → CPID `0x8140`
- Patch USB at CLI boundary; unit-test `identify.py` directly

## Dependencies

- Document in `context/tech-stack.md` before adding to `pyproject.toml`
