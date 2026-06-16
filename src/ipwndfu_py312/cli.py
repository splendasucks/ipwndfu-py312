"""CLI entry point for ipwndfu-py312."""

from __future__ import annotations

import argparse
import sys

from ipwndfu_py312.usb.device import find_dfu_devices, list_usb_devices


def _cmd_devices() -> int:
    dfu = find_dfu_devices()
    all_devices = list_usb_devices()

    if not all_devices:
        print("No USB devices found (is libusb installed? run scripts/check_libusb.sh)", file=sys.stderr)
        return 1

    print(f"USB devices ({len(all_devices)}):")
    for dev in all_devices:
        marker = " [DFU]" if dev in dfu else ""
        print(f"  - {dev}{marker}")

    if dfu:
        print(f"\nDFU targets: {len(dfu)}")
    else:
        print("\nNo Apple DFU devices (05ac:1227). Put device in DFU mode and retry.")
    return 0


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

    print(f"ipwndfu-py312: command '{args.command}' not yet implemented.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
