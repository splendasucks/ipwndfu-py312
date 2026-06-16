"""DFU session helpers — parse Apple DFU USB serial strings."""

from __future__ import annotations

from dataclasses import dataclass

from ipwndfu_py312.usb.device import UsbDeviceInfo


@dataclass(frozen=True, slots=True)
class DfuIdentifiers:
    cpid: int | None
    bdid: int | None


@dataclass(frozen=True, slots=True)
class DfuSession:
    device: UsbDeviceInfo
    identifiers: DfuIdentifiers

    @property
    def cpid(self) -> int | None:
        return self.identifiers.cpid

    @property
    def bdid(self) -> int | None:
        return self.identifiers.bdid


def parse_dfu_serial(serial: str) -> DfuIdentifiers:
    """Parse CPID/BDID from Apple DFU mode USB serial string."""
    cpid: int | None = None
    bdid: int | None = None

    for token in serial.split():
        if ":" not in token:
            continue
        key, _, value = token.partition(":")
        if key == "CPID":
            try:
                cpid = int(value, 16)
            except ValueError as exc:
                raise ValueError(f"invalid CPID in serial: {value!r}") from exc
        elif key == "BDID":
            try:
                bdid = int(value, 16)
            except ValueError as exc:
                raise ValueError(f"invalid BDID in serial: {value!r}") from exc

    return DfuIdentifiers(cpid=cpid, bdid=bdid)


def session_from_device(device: UsbDeviceInfo) -> DfuSession:
    return DfuSession(device=device, identifiers=parse_dfu_serial(device.serial))
