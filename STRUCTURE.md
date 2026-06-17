# Annotated project structure

Diagnostics-first layout for the Python 3.12 Apple DFU toolkit. checkm8 exploit modules are contributor scaffolding.

```
ipwndfu-py312/
├── README.md                 # Quick start (identify), install, disclaimers
├── STRUCTURE.md              # This file
├── CONTRIBUTING.md           # Contributor policy (HIL for checkm8)
├── pyproject.toml            # Hatchling + uv (pyusb, libusb1)
├── LICENSE                   # GPL-3.0-or-later
│
├── context/                  # Product/tech/workflow artifacts for AI handoff
│   ├── product.md
│   ├── tech-stack.md
│   ├── workflow.md
│   ├── tracks.md
│   └── styleguides/python.md
│
├── src/ipwndfu_py312/
│   ├── __init__.py           # Version
│   ├── cli.py                # devices, identify, pwn, shell
│   ├── identify.py           # DeviceIdentity, identify_device(), identify_connected()
│   ├── data/
│   │   └── apple_chips.py    # CPID → chip name, checkm8_eligible
│   ├── usb/
│   │   ├── device.py         # libusb enumeration, DFU mode detection
│   │   └── dfu.py            # Serial parse, Port DFU AP ID extraction
│   ├── exploits/             # Per-SoC checkm8 routes (stubs / contrib)
│   │   ├── registry.py
│   │   ├── runner.py
│   │   └── a5.py … a11.py
│   └── util/                 # hex, logger helpers
│
├── tests/
│   ├── test_cli.py
│   └── unit/                 # dfu, identify, apple_chips, runner, …
│
├── scripts/
│   └── check_libusb.sh
│
└── docs/
    ├── DIAGNOSTICS.md        # User-facing identify workflow
    ├── CHECKM8.md            # Contributor exploit porting
    ├── CHIPDB.md             # CPID database provenance
    └── PORTING.md            # Redirect to CHECKM8.md (legacy link)
```

## Module map (original ipwndfu → fork)

| Original | Fork location | Role |
|----------|---------------|------|
| USB discovery | `usb/device.py` | Enumeration |
| DFU serial | `usb/dfu.py` | CPID/BDID parse |
| — | `identify.py` + `data/apple_chips.py` | **Primary public API** |
| `checkm8` | `exploits/` | Contributor scaffold |
| `ipwndfu.py` | `cli.py` | CLI entry |
