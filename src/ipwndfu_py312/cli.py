"""CLI entry point for ipwndfu-py312."""

from __future__ import annotations

import argparse
import sys

from ipwndfu_py312.exploits.runner import run_checkm8
from ipwndfu_py312.usb.device import (
    AppleDfuMode,
    apple_dfu_mode,
    find_dfu_devices,
    find_port_dfu_devices,
    list_usb_devices,
)


def _cmd_devices() -> int:
    dfu = find_dfu_devices()
    port_dfu = find_port_dfu_devices()
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

    if dfu:
        print(f"\nDFU targets (checkm8): {len(dfu)}")
    elif port_dfu:
        print(f"\nPort DFU devices: {len(port_dfu)} (not classic DFU 05ac:1227)")
        print("Re-enter DFU on the device to reach checkm8-ready mode.")
    else:
        print("\nNo Apple DFU devices (05ac:1227). Put device in DFU mode and retry.")
    return 0


def _cmd_pwn() -> int:
    print(
        "WARNING: checkm8 is for authorized security research only. Only exploit devices you own.",
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
        description="checkm8 / DFU research CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("devices", help="List USB devices visible to libusb")
    sub.add_parser("pwn", help="Run checkm8 exploit on connected DFU device")
    sub.add_parser("shell", help="Interactive post-exploit shell")

    args = parser.parse_args(argv)

    if args.command == "devices":
        return _cmd_devices()

    if args.command == "pwn":
        return _cmd_pwn()

    print(f"ipwndfu-py312: command '{args.command}' not yet implemented.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
