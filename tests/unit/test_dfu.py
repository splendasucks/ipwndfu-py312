"""Tests for DFU serial parsing and session helpers."""

from __future__ import annotations

import pytest

from ipwndfu_py312.usb.dfu import (
    DfuIdentifiers,
    extract_ap_identifiers_from_port_dfu,
    parse_dfu_serial,
)


class TestParseDfuSerial:
    @pytest.mark.unit
    def test_parses_cpid_and_bdid_from_apple_serial(self):
        serial = "SDOM:01 CPID:8015 CPRV:11 CPFM:03 SCEP:01 BDID:04 IBFL:3C ECID:000123"
        ids = parse_dfu_serial(serial)
        assert ids == DfuIdentifiers(cpid=0x8015, bdid=0x04)

    @pytest.mark.unit
    def test_parses_cpid_without_bdid(self):
        ids = parse_dfu_serial("CPID:8960 CPRV:00")
        assert ids.cpid == 0x8960
        assert ids.bdid is None

    @pytest.mark.unit
    def test_empty_serial_returns_none_fields(self):
        ids = parse_dfu_serial("")
        assert ids.cpid is None
        assert ids.bdid is None

    @pytest.mark.unit
    def test_malformed_cpid_raises(self):
        with pytest.raises(ValueError, match="CPID"):
            parse_dfu_serial("CPID:ZZZZ")

    @pytest.mark.unit
    def test_port_dfu_derives_ap_cpid_from_packed_bdid(self):
        serial = "SDOM:01 CPID:0022 BDID:000000000C801500 ECID:001 CPFM:03 SCEP:00 CPRV:1A3"
        ids = parse_dfu_serial(serial, port_dfu=True)
        assert ids == DfuIdentifiers(cpid=0x8015, bdid=0x0C)


class TestExtractApIdentifiersFromPortDfu:
    @pytest.mark.unit
    def test_matches_libirecovery_bit_layout(self):
        packed = int("000000000C801500", 16)
        assert extract_ap_identifiers_from_port_dfu(packed) == DfuIdentifiers(
            cpid=0x8015,
            bdid=0x0C,
        )
