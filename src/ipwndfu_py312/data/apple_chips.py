"""Apple application-processor CPID lookup (libirecovery-derived)."""

from __future__ import annotations

from dataclasses import dataclass

from ipwndfu_py312.exploits.registry import supported_cpids

# CPID hex -> (marketing generation, internal codename). checkm8_eligible from registry.
_CHIPS: dict[int, tuple[str, str]] = {
    0x8950: ("A5", "S5L8940X"),
    0x8955: ("A5", "S5L8955X"),
    0x8960: ("A6", "S5L8960X"),
    0x8965: ("A7", "S5L8965X"),
    0x7002: ("A7", "T7002"),
    0x7000: ("A8", "T7000"),
    0x7001: ("A8", "T7001"),
    0x8000: ("A9", "S8000"),
    0x8001: ("A9", "S8001"),
    0x8003: ("A9", "S8003"),
    0x8012: ("A9", "S8003"),
    0x8010: ("A10", "T8010"),
    0x8011: ("A10", "T8011"),
    0x8015: ("A11", "T8015"),
    0x8020: ("A12", "T8020"),
    0x8027: ("A12", "T8027"),
    0x8030: ("A13", "T8030"),
    0x8101: ("A14", "T8101"),
    0x8103: ("A14", "T8103"),
    0x8110: ("A15", "T8110"),
    0x8112: ("A15", "T8112"),
    0x8120: ("A16", "T8120"),
    0x8122: ("A16", "T8122"),
    0x8130: ("A17", "T8130"),
    0x8132: ("A17", "T8132"),
    0x8140: ("A18", "T8140"),
    0x8142: ("A18", "T8142"),
}


@dataclass(frozen=True, slots=True)
class ChipInfo:
    cpid: int
    generation: str
    codename: str
    chip_name: str
    checkm8_eligible: bool

    @property
    def display_name(self) -> str:
        return self.chip_name


def lookup_chip(cpid: int) -> ChipInfo | None:
    entry = _CHIPS.get(cpid)
    if entry is None:
        return None
    generation, codename = entry
    eligible = cpid in supported_cpids()
    chip_name = f"Apple {generation} ({codename})"
    return ChipInfo(
        cpid=cpid,
        generation=generation,
        codename=codename,
        chip_name=chip_name,
        checkm8_eligible=eligible,
    )
