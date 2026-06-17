"""Tests for ipwndfu-py312 CLI."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from ipwndfu_py312 import __version__
from ipwndfu_py312.cli import main
from ipwndfu_py312.usb.device import UsbDeviceInfo

CLASSIC_DFU = UsbDeviceInfo(0x05AC, 0x1227, "Apple Inc.", "DFU Mode", serial="CPID:8015 BDID:04")
PORT_DFU = UsbDeviceInfo(
    0x05AC,
    0xF014,
    "Apple Inc.",
    "Apple Device (Port DFU Mode)",
    serial="BDID:000000000C814000 ECID:747D1772145A9529",
)


class TestCliEntry:
    """Feature: CLI exposes diagnostics-first subcommands."""

    @pytest.mark.unit
    def test_version_is_semver_string(self):
        assert isinstance(__version__, str)
        assert len(__version__.split(".")) >= 2

    @pytest.mark.unit
    def test_devices_command_lists_usb(self):
        with patch("ipwndfu_py312.cli.list_usb_devices", return_value=[CLASSIC_DFU]):
            with patch("ipwndfu_py312.cli.find_all_dfu_devices", return_value=[CLASSIC_DFU]):
                assert main(["devices"]) == 0

    @pytest.mark.unit
    def test_devices_command_marks_port_dfu(self, capsys):
        with patch("ipwndfu_py312.cli.list_usb_devices", return_value=[PORT_DFU]):
            with patch("ipwndfu_py312.cli.find_all_dfu_devices", return_value=[PORT_DFU]):
                assert main(["devices"]) == 0
        out = capsys.readouterr().out
        assert "[Port DFU]" in out
        assert "identify" in out

    @pytest.mark.unit
    def test_devices_json_emits_identity(self, capsys):
        with patch("ipwndfu_py312.cli.find_all_dfu_devices", return_value=[PORT_DFU]):
            assert main(["devices", "--json"]) == 0
        out = capsys.readouterr().out
        assert '"ap_cpid": "0x8140"' in out
        assert '"chip_name": "Apple A18 (T8140)"' in out

    @pytest.mark.unit
    def test_identify_command_success(self, capsys):
        with patch("ipwndfu_py312.cli.identify_connected") as mock_identify:
            from ipwndfu_py312.identify import identify_device

            mock_identify.return_value = [identify_device(PORT_DFU)]
            assert main(["identify"]) == 0
        out = capsys.readouterr().out
        assert "Apple A18" in out

    @pytest.mark.unit
    def test_identify_without_device_exits_one(self):
        with patch("ipwndfu_py312.cli.identify_connected", return_value=[]):
            assert main(["identify"]) == 1

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
