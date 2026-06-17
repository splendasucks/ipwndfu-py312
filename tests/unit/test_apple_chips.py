"""Tests for Apple CPID chip database."""

from __future__ import annotations

import pytest

from ipwndfu_py312.data.apple_chips import lookup_chip


class TestLookupChip:
    @pytest.mark.unit
    def test_a11_is_checkm8_eligible(self):
        chip = lookup_chip(0x8015)
        assert chip is not None
        assert chip.generation == "A11"
        assert chip.checkm8_eligible is True

    @pytest.mark.unit
    def test_a18_is_not_checkm8_eligible(self):
        chip = lookup_chip(0x8140)
        assert chip is not None
        assert chip.generation == "A18"
        assert chip.codename == "T8140"
        assert chip.checkm8_eligible is False

    @pytest.mark.unit
    def test_unknown_cpid_returns_none(self):
        assert lookup_chip(0xFFFF) is None
