"""Tests for ipwndfu-py312 CLI."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from ipwndfu_py312 import __version__
from ipwndfu_py312.cli import main
from ipwndfu_py312.usb.device import UsbDeviceInfo


class TestCliEntry:
    """Feature: CLI exposes subcommands for DFU research workflow."""

    @pytest.mark.unit
    def test_version_is_semver_string(self):
        assert isinstance(__version__, str)
        assert len(__version__.split(".")) >= 2

    @pytest.mark.unit
    def test_devices_command_lists_usb(self):
        sample = UsbDeviceInfo(0x05AC, 0x1227, "Apple Inc.", "DFU Mode")
        with patch("ipwndfu_py312.cli.list_usb_devices", return_value=[sample]):
            with patch("ipwndfu_py312.cli.find_dfu_devices", return_value=[sample]):
                with patch("ipwndfu_py312.cli.find_port_dfu_devices", return_value=[]):
                    assert main(["devices"]) == 0

    @pytest.mark.unit
    def test_devices_command_marks_port_dfu(self, capsys):
        port = UsbDeviceInfo(0x05AC, 0xF014, "Apple Inc.", "Apple Device (Port DFU Mode)")
        with patch("ipwndfu_py312.cli.list_usb_devices", return_value=[port]):
            with patch("ipwndfu_py312.cli.find_dfu_devices", return_value=[]):
                with patch("ipwndfu_py312.cli.find_port_dfu_devices", return_value=[port]):
                    assert main(["devices"]) == 0
        assert "[Port DFU]" in capsys.readouterr().out

    @pytest.mark.unit
    def test_pwn_without_device_exits_one(self):
        with patch("ipwndfu_py312.cli.run_checkm8") as mock_pwn:
            from ipwndfu_py312.exploits.base import ExploitResult, ExploitStatus

            mock_pwn.return_value = ExploitResult(
                status=ExploitStatus.NO_DEVICE,
                soc="",
                message="No Apple DFU device",
            )
            assert main(["pwn"]) == 1

    @pytest.mark.unit
    def test_missing_command_exits_nonzero(self):
        with pytest.raises(SystemExit) as exc:
            main([])
        assert exc.value.code != 0
