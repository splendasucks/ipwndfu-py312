"""Apple DFU device identification — public API."""

from __future__ import annotations

from dataclasses import dataclass

from ipwndfu_py312.data.apple_chips import lookup_chip
from ipwndfu_py312.usb.device import (
    AppleDfuMode,
    UsbDeviceInfo,
    apple_dfu_mode,
    find_dfu_devices,
    find_port_dfu_devices,
)
from ipwndfu_py312.usb.dfu import session_from_device


def parse_ecid(serial: str) -> str | None:
    for token in serial.split():
        if ":" not in token:
            continue
        key, _, value = token.partition(":")
        if key == "ECID" and value:
            return value.upper()
    return None


@dataclass(frozen=True, slots=True)
class DeviceIdentity:
    device: UsbDeviceInfo
    mode: AppleDfuMode | None
    ap_cpid: int | None
    ap_bdid: int | None
    chip_name: str | None
    checkm8_eligible: bool
    ecid: str | None
    raw_serial: str

    def to_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode.value if self.mode is not None else None,
            "ap_cpid": f"0x{self.ap_cpid:04x}" if self.ap_cpid is not None else None,
            "ap_bdid": f"0x{self.ap_bdid:02x}" if self.ap_bdid is not None else None,
            "chip_name": self.chip_name,
            "checkm8_eligible": self.checkm8_eligible,
            "ecid": self.ecid,
            "raw_serial": self.raw_serial,
            "usb": {
                "vendor_id": f"0x{self.device.vendor_id:04x}",
                "product_id": f"0x{self.device.product_id:04x}",
                "product": self.device.product,
            },
        }


def identify_device(device: UsbDeviceInfo) -> DeviceIdentity:
    mode = apple_dfu_mode(device)
    session = session_from_device(device) if mode is not None else None
    ap_cpid = session.cpid if session else None
    ap_bdid = session.bdid if session else None
    chip = lookup_chip(ap_cpid) if ap_cpid is not None else None
    chip_name = chip.chip_name if chip else None
    eligible = chip.checkm8_eligible if chip else False
    if ap_cpid is not None and chip is None:
        chip_name = f"Unknown (CPID 0x{ap_cpid:04x})"

    return DeviceIdentity(
        device=device,
        mode=mode,
        ap_cpid=ap_cpid,
        ap_bdid=ap_bdid,
        chip_name=chip_name,
        checkm8_eligible=eligible,
        ecid=parse_ecid(device.serial),
        raw_serial=device.serial,
    )


def find_all_dfu_devices() -> list[UsbDeviceInfo]:
    return find_dfu_devices() + find_port_dfu_devices()


def identify_connected() -> list[DeviceIdentity]:
    return [identify_device(dev) for dev in find_all_dfu_devices()]
