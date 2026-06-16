"""Tests for exploit result types."""

from __future__ import annotations

import pytest

from ipwndfu_py312.exploits.base import ExploitResult, ExploitStatus


class TestExploitResult:
    @pytest.mark.unit
    def test_payload_pending_result_carries_soc_and_cpid(self):
        result = ExploitResult(
            status=ExploitStatus.PAYLOAD_PENDING,
            soc="a11",
            message="payload port pending",
            cpid=0x8015,
        )
        assert result.status is ExploitStatus.PAYLOAD_PENDING
        assert result.soc == "a11"
        assert result.cpid == 0x8015
