"""Tests for CPID → exploit module routing."""

from __future__ import annotations

import pytest

from ipwndfu_py312.exploits.registry import resolve_exploit, supported_cpids


class TestExploitRegistry:
    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("cpid", "expected_soc"),
        [
            (0x8950, "a5"),
            (0x8960, "a6"),
            (0x8965, "a7"),
            (0x7001, "a8"),
            (0x8003, "a9"),
            (0x8010, "a10"),
            (0x8015, "a11"),
        ],
    )
    def test_resolve_exploit_maps_cpid_to_soc_module(self, cpid: int, expected_soc: str):
        exploit = resolve_exploit(cpid)
        assert exploit.soc == expected_soc

    @pytest.mark.unit
    def test_unknown_cpid_raises(self):
        with pytest.raises(LookupError, match="0x9999"):
            resolve_exploit(0x9999)

    @pytest.mark.unit
    def test_supported_cpids_is_nonempty_and_unique(self):
        cpids = supported_cpids()
        assert len(cpids) >= 7
        assert len(cpids) == len(set(cpids))
