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
                assert main(["devices"]) == 0

    @pytest.mark.unit
    def test_pwn_not_yet_implemented(self):
        assert main(["pwn"]) == 2

    @pytest.mark.unit
    def test_missing_command_exits_nonzero(self):
        with pytest.raises(SystemExit) as exc:
            main([])
        assert exc.value.code != 0
