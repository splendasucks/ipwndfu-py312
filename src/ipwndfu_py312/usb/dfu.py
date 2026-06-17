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


def extract_ap_identifiers_from_port_dfu(packed_bdid: int) -> DfuIdentifiers:
    """Map Port DFU packed BDID to AP CPID/BDID (libirecovery device lookup)."""
    ap_cpid = (packed_bdid >> 8) & 0xFFFF
    ap_bdid = (packed_bdid >> 24) & 0xFF
    return DfuIdentifiers(cpid=ap_cpid, bdid=ap_bdid)


def parse_dfu_serial(serial: str, *, port_dfu: bool = False) -> DfuIdentifiers:
    """Parse CPID/BDID from Apple DFU USB serial string."""
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

    if port_dfu:
        if bdid is None:
            return DfuIdentifiers(cpid=None, bdid=None)
        return extract_ap_identifiers_from_port_dfu(bdid)

    return DfuIdentifiers(cpid=cpid, bdid=bdid)


def session_from_device(device: UsbDeviceInfo) -> DfuSession:
    from ipwndfu_py312.usb.device import AppleDfuMode, apple_dfu_mode

    port_dfu = apple_dfu_mode(device) is AppleDfuMode.PORT
    return DfuSession(
        device=device,
        identifiers=parse_dfu_serial(device.serial, port_dfu=port_dfu),
    )
