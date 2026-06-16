"""Tests for USB device enumeration (unit path for TDD hook)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from ipwndfu_py312.usb.device import UsbDeviceInfo, find_dfu_devices, list_usb_devices


class TestUsbEnumeration:
    """Feature: Researcher can list USB devices relevant to DFU workflow."""

    @pytest.mark.unit
    def test_usb_device_info_str_includes_vid_pid(self):
        info = UsbDeviceInfo(vendor_id=0x05AC, product_id=0x1227, manufacturer="Apple Inc.", product="DFU Mode")
        text = str(info)
        assert "05ac" in text.lower()
        assert "1227" in text

    @pytest.mark.unit
    def test_find_dfu_devices_filters_apple_dfu_pid(self):
        dfu = UsbDeviceInfo(0x05AC, 0x1227, "Apple Inc.", "DFU Mode")
        other = UsbDeviceInfo(0x046D, 0xC52B, "Logitech", "USB Receiver")
        with patch("ipwndfu_py312.usb.device.list_usb_devices", return_value=[dfu, other]):
            result = find_dfu_devices()
        assert result == [dfu]

    @pytest.mark.unit
    def test_list_usb_devices_returns_empty_when_no_backend(self):
        with patch("ipwndfu_py312.usb.device._iter_usb_devices", side_effect=RuntimeError("no backend")):
            assert list_usb_devices() == []
