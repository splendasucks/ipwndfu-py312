"""Tests for A10 (T8010 / T8011) checkm8 exploit stub."""

from __future__ import annotations

import pytest

from ipwndfu_py312.exploits.a10 import EXPLOIT
from ipwndfu_py312.exploits.base import ExploitStatus
from ipwndfu_py312.usb.device import UsbDeviceInfo
from ipwndfu_py312.usb.dfu import session_from_device


class TestA10Exploit:
    @pytest.mark.unit
    def test_run_returns_payload_pending(self):
        device = UsbDeviceInfo(0x05AC, 0x1227, "Apple", "DFU", serial="CPID:8010")
        result = EXPLOIT.run(session_from_device(device))
        assert result.soc == "a10"
        assert result.status is ExploitStatus.PAYLOAD_PENDING
