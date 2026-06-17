"""Tests for DFU device identification API."""

from __future__ import annotations

import pytest

from ipwndfu_py312.identify import identify_device, parse_ecid
from ipwndfu_py312.usb.device import UsbDeviceInfo

CLASSIC_A11 = UsbDeviceInfo(
    vendor_id=0x05AC,
    product_id=0x1227,
    manufacturer="Apple Inc.",
    product="DFU Mode",
    serial="SDOM:01 CPID:8015 CPRV:11 BDID:04 ECID:000123",
)

PORT_DFU_A18 = UsbDeviceInfo(
    vendor_id=0x05AC,
    product_id=0xF014,
    manufacturer="Apple Inc.",
    product="Apple Device (Port DFU Mode)",
    serial=(
        "SDOM:01 CPID:0022 BDID:000000000C814000 ECID:747D1772145A9529 "
        "CPFM:03 SCEP:00 CPRV:1A3 PREV:2F"
    ),
)


class TestParseEcid:
    @pytest.mark.unit
    def test_extracts_ecid_token(self):
        assert parse_ecid(PORT_DFU_A18.serial) == "747D1772145A9529"


class TestIdentifyDevice:
    @pytest.mark.unit
    def test_classic_dfu_a11(self):
        identity = identify_device(CLASSIC_A11)
        assert identity.ap_cpid == 0x8015
        assert identity.ap_bdid == 0x04
        assert identity.chip_name == "Apple A11 (T8015)"
        assert identity.checkm8_eligible is True
        assert identity.mode is not None
        assert identity.mode.value == "checkm8"

    @pytest.mark.unit
    def test_port_dfu_a18(self):
        identity = identify_device(PORT_DFU_A18)
        assert identity.ap_cpid == 0x8140
        assert identity.ap_bdid == 0x0C
        assert identity.chip_name == "Apple A18 (T8140)"
        assert identity.checkm8_eligible is False
        assert identity.mode is not None
        assert identity.mode.value == "port"

    @pytest.mark.unit
    def test_to_dict_json_schema(self):
        identity = identify_device(PORT_DFU_A18)
        data = identity.to_dict()
        assert data["ap_cpid"] == "0x8140"
        assert data["checkm8_eligible"] is False
        assert data["chip_name"] == "Apple A18 (T8140)"
        assert data["ecid"] == "747D1772145A9529"
