"""USB device discovery for DFU research."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

APPLE_VID = 0x05AC
CHECKM8_DFU_PID = 0x1227
PORT_DFU_PID = 0xF014

# Back-compat alias used across the codebase and docs.
DFU_PID = CHECKM8_DFU_PID

PORT_DFU_HINT = (
    "Found Apple Port DFU (05ac:f014) but checkm8 requires classic DFU (05ac:1227). "
    "Re-enter DFU on the device (screen stays black, iTunes/Finder does not show a "
    "restore prompt). Unplug hubs/adapters if both normal and Port DFU interfaces appear."
)


class AppleDfuMode(Enum):
    CHECKM8 = "checkm8"
    PORT = "port"


@dataclass(frozen=True, slots=True)
class UsbDeviceInfo:
    vendor_id: int
    product_id: int
    manufacturer: str
    product: str
    serial: str = ""

    def __str__(self) -> str:
        return (
            f"{self.manufacturer} {self.product} "
            f"(vid=0x{self.vendor_id:04x} pid=0x{self.product_id:04x})"
        )


def apple_dfu_mode(device: UsbDeviceInfo) -> AppleDfuMode | None:
    if device.vendor_id != APPLE_VID:
        return None
    if device.product_id == CHECKM8_DFU_PID:
        return AppleDfuMode.CHECKM8
    if device.product_id == PORT_DFU_PID:
        return AppleDfuMode.PORT
    return None


def _iter_usb_devices():
    import usb.core
    import usb.util

    for dev in usb.core.find(find_all=True):
        try:
            manufacturer = usb.util.get_string(dev, dev.iManufacturer) or ""
            product = usb.util.get_string(dev, dev.iProduct) or ""
            serial = usb.util.get_string(dev, dev.iSerialNumber) or ""
        except (usb.core.USBError, ValueError, IndexError):
            manufacturer = ""
            product = ""
            serial = ""
        yield UsbDeviceInfo(
            vendor_id=int(dev.idVendor),
            product_id=int(dev.idProduct),
            manufacturer=manufacturer,
            product=product,
            serial=serial,
        )


def list_usb_devices() -> list[UsbDeviceInfo]:
    try:
        return list(_iter_usb_devices())
    except (ImportError, RuntimeError, OSError):
        return []


def find_dfu_devices() -> list[UsbDeviceInfo]:
    """Devices in classic checkm8 DFU mode (05ac:1227)."""
    return [d for d in list_usb_devices() if apple_dfu_mode(d) is AppleDfuMode.CHECKM8]


def find_port_dfu_devices() -> list[UsbDeviceInfo]:
    """Devices exposing Apple's Port DFU interface (05ac:f014)."""
    return [d for d in list_usb_devices() if apple_dfu_mode(d) is AppleDfuMode.PORT]
