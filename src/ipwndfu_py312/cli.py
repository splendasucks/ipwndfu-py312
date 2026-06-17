"""CLI entry point for ipwndfu-py312."""

from __future__ import annotations

import argparse
import json
import sys

from ipwndfu_py312.exploits.runner import run_checkm8
from ipwndfu_py312.identify import (
    DeviceIdentity,
    find_all_dfu_devices,
    identify_connected,
    identify_device,
)
from ipwndfu_py312.usb.device import (
    AppleDfuMode,
    apple_dfu_mode,
    list_usb_devices,
)


def _print_identity_table(identities: list[DeviceIdentity]) -> None:
    for identity in identities:
        mode = identity.mode.value if identity.mode is not None else "unknown"
        cpid = f"0x{identity.ap_cpid:04x}" if identity.ap_cpid is not None else "—"
        bdid = f"0x{identity.ap_bdid:02x}" if identity.ap_bdid is not None else "—"
        chip = identity.chip_name or "—"
        checkm8 = "yes" if identity.checkm8_eligible else "no"
        ecid = identity.ecid or "—"
        print(f"Mode:     {mode}")
        print(f"Chip:     {chip}")
        print(f"AP CPID:  {cpid}")
        print(f"AP BDID:  {bdid}")
        print(f"ECID:     {ecid}")
        print(f"checkm8:  {checkm8}")
        print(f"USB:      {identity.device}")
        if len(identities) > 1:
            print()


def _cmd_devices(*, as_json: bool) -> int:
    if as_json:
        identities = [identify_device(dev) for dev in find_all_dfu_devices()]
        print(json.dumps([item.to_dict() for item in identities], indent=2))
        return 0

    all_devices = list_usb_devices()
    if not all_devices:
        print(
            "No USB devices found (is libusb installed? run scripts/check_libusb.sh)",
            file=sys.stderr,
        )
        return 1

    print(f"USB devices ({len(all_devices)}):")
    for dev in all_devices:
        mode = apple_dfu_mode(dev)
        if mode is AppleDfuMode.CHECKM8:
            marker = " [DFU]"
        elif mode is AppleDfuMode.PORT:
            marker = " [Port DFU]"
        else:
            marker = ""
        print(f"  - {dev}{marker}")

    dfu_devices = find_all_dfu_devices()
    if dfu_devices:
        print(f"\nApple DFU interfaces: {len(dfu_devices)}")
        print("Run `ipwndfu identify` for chip name, CPID, and JSON export (`devices --json`).")
    else:
        print("\nNo Apple DFU devices (05ac:1227 or 05ac:f014). Put device in DFU mode and retry.")
    return 0


def _cmd_identify(*, as_json: bool) -> int:
    identities = identify_connected()
    if not identities:
        print(
            "No Apple DFU devices (05ac:1227 or 05ac:f014). Put device in DFU mode and retry.",
            file=sys.stderr,
        )
        return 1

    if as_json:
        print(json.dumps([item.to_dict() for item in identities], indent=2))
        return 0

    _print_identity_table(identities)
    return 0


def _cmd_pwn() -> int:
    print(
        "WARNING: checkm8 is experimental (A5–A11 only; payloads not fully ported). "
        "Authorized research on devices you own only.",
        file=sys.stderr,
    )
    result = run_checkm8()
    print(result.message)
    if result.soc:
        cpid = f"0x{result.cpid:04x}" if result.cpid is not None else "unknown"
        print(f"SoC module: {result.soc} (CPID {cpid})")

    from ipwndfu_py312.exploits.base import ExploitStatus

    match result.status:
        case ExploitStatus.SUCCESS:
            return 0
        case ExploitStatus.PAYLOAD_PENDING:
            return 3
        case ExploitStatus.NO_DEVICE:
            return 1
        case ExploitStatus.UNSUPPORTED | ExploitStatus.FAILED:
            return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ipwndfu",
        description="Apple DFU USB diagnostics (checkm8 scaffold for A5–A11 contributors)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    devices_parser = sub.add_parser("devices", help="List USB devices visible to libusb")
    devices_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit Apple DFU device identity records as JSON",
    )

    identify_parser = sub.add_parser(
        "identify",
        help="Identify connected Apple DFU devices (chip, mode, CPID/BDID/ECID)",
    )
    identify_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit identity records as JSON",
    )

    sub.add_parser(
        "pwn",
        help="Experimental checkm8 route (A5–A11 only; payloads not fully ported)",
    )
    sub.add_parser("shell", help="Interactive post-exploit shell (not implemented)")

    args = parser.parse_args(argv)

    if args.command == "devices":
        return _cmd_devices(as_json=args.json)

    if args.command == "identify":
        return _cmd_identify(as_json=args.json)

    if args.command == "pwn":
        return _cmd_pwn()

    print(f"ipwndfu-py312: command '{args.command}' not yet implemented.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
