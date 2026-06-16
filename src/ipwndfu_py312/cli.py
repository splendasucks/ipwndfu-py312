"""CLI entry point for ipwndfu-py312 (scaffold)."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ipwndfu",
        description="checkm8 / DFU research CLI (scaffold — full port in progress)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("devices", help="List USB devices visible to libusb")
    sub.add_parser("pwn", help="Run checkm8 exploit on connected DFU device")
    sub.add_parser("shell", help="Interactive post-exploit shell")

    args = parser.parse_args(argv)
    print(f"ipwndfu-py312: command '{args.command}' not yet implemented.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
