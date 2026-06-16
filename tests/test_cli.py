"""Tests for ipwndfu-py312 CLI (scaffold)."""

from __future__ import annotations

import pytest

from ipwndfu_py312 import __version__
from ipwndfu_py312.cli import main


class TestCliEntry:
    """Feature: CLI exposes subcommands for DFU research workflow."""

    @pytest.mark.unit
    def test_version_is_semver_string(self):
        """Scenario: Package exposes a version string for tooling."""
        assert isinstance(__version__, str)
        assert len(__version__.split(".")) >= 2

    @pytest.mark.unit
    def test_devices_command_not_yet_implemented(self):
        """Scenario: devices subcommand exists but returns non-zero until ported."""
        assert main(["devices"]) == 2

    @pytest.mark.unit
    def test_missing_command_exits_nonzero(self):
        """Scenario: Invoking CLI without subcommand fails."""
        with pytest.raises(SystemExit) as exc:
            main([])
        assert exc.value.code != 0
