"""Tests for A6 (S5L8960X) checkm8 exploit stub."""

from __future__ import annotations

import pytest

from ipwndfu_py312.exploits.a6 import EXPLOIT
from ipwndfu_py312.exploits.base import ExploitStatus
from ipwndfu_py312.usb.device import UsbDeviceInfo
from ipwndfu_py312.usb.dfu import session_from_device


class TestA6Exploit:
    @pytest.mark.unit
    def test_run_returns_payload_pending(self):
        device = UsbDeviceInfo(0x05AC, 0x1227, "Apple", "DFU", serial="CPID:8960")
        result = EXPLOIT.run(session_from_device(device))
        assert result.soc == "a6"
        assert result.status is ExploitStatus.PAYLOAD_PENDING
