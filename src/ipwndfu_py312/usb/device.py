"""USB device discovery for DFU research."""

from __future__ import annotations

from dataclasses import dataclass

APPLE_VID = 0x05AC
DFU_PID = 0x1227


@dataclass(frozen=True, slots=True)
class UsbDeviceInfo:
    vendor_id: int
    product_id: int
    manufacturer: str
    product: str

    def __str__(self) -> str:
        return (
            f"{self.manufacturer} {self.product} "
            f"(vid=0x{self.vendor_id:04x} pid=0x{self.product_id:04x})"
        )


def _iter_usb_devices():
    import usb.core
    import usb.util

    for dev in usb.core.find(find_all=True):
        try:
            manufacturer = usb.util.get_string(dev, dev.iManufacturer) or ""
            product = usb.util.get_string(dev, dev.iProduct) or ""
        except (usb.core.USBError, ValueError, IndexError):
            manufacturer = ""
            product = ""
        yield UsbDeviceInfo(
            vendor_id=int(dev.idVendor),
            product_id=int(dev.idProduct),
            manufacturer=manufacturer,
            product=product,
        )


def list_usb_devices() -> list[UsbDeviceInfo]:
    try:
        return list(_iter_usb_devices())
    except (ImportError, RuntimeError, OSError):
        return []


def find_dfu_devices() -> list[UsbDeviceInfo]:
    return [
        d
        for d in list_usb_devices()
        if d.vendor_id == APPLE_VID and d.product_id == DFU_PID
    ]
