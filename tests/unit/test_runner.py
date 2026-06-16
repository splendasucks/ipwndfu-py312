"""Tests for checkm8 runner orchestration."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from ipwndfu_py312.exploits.base import ExploitStatus
from ipwndfu_py312.exploits.runner import run_checkm8
from ipwndfu_py312.usb.device import PORT_DFU_PID, UsbDeviceInfo

DFU = UsbDeviceInfo(
    vendor_id=0x05AC,
    product_id=0x1227,
    manufacturer="Apple Inc.",
    product="DFU Mode",
    serial="SDOM:01 CPID:8015 CPRV:11 BDID:04 ECID:001",
)


class TestRunCheckm8:
    @pytest.mark.unit
    def test_returns_error_when_no_dfu_device(self):
        with (
            patch("ipwndfu_py312.exploits.runner.find_dfu_devices", return_value=[]),
            patch("ipwndfu_py312.exploits.runner.find_port_dfu_devices", return_value=[]),
        ):
            result = run_checkm8()
        assert result.status == ExploitStatus.NO_DEVICE

    @pytest.mark.unit
    def test_port_dfu_only_returns_actionable_message(self):
        port_dfu = UsbDeviceInfo(
            0x05AC,
            PORT_DFU_PID,
            "Apple Inc.",
            "Apple Device (Port DFU Mode)",
        )
        with (
            patch("ipwndfu_py312.exploits.runner.find_dfu_devices", return_value=[]),
            patch("ipwndfu_py312.exploits.runner.find_port_dfu_devices", return_value=[port_dfu]),
        ):
            result = run_checkm8()
        assert result.status == ExploitStatus.NO_DEVICE
        assert "f014" in result.message.lower()
        assert "1227" in result.message

    @pytest.mark.unit
    def test_routes_a11_cpid_to_a11_module(self):
        with patch("ipwndfu_py312.exploits.runner.find_dfu_devices", return_value=[DFU]):
            result = run_checkm8()
        assert result.soc == "a11"
        assert result.status == ExploitStatus.PAYLOAD_PENDING

    @pytest.mark.unit
    def test_returns_error_when_serial_missing_cpid(self):
        no_cpid = UsbDeviceInfo(0x05AC, 0x1227, "Apple", "DFU", serial="ECID:001")
        with patch("ipwndfu_py312.exploits.runner.find_dfu_devices", return_value=[no_cpid]):
            result = run_checkm8()
        assert result.status == ExploitStatus.UNSUPPORTED
