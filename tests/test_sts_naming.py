"""Shared naming and address regressions, with no application dependencies."""

import pytest

from sts_utils.sts_naming import (
    NAMING_VERSION,
    build_module_name_prefix,
    convert_to_cbm_sts_address,
    decode_sts_address,
    make_sts_address,
    patch_ladder_name,
)
from sts_utils.units import CM, MM


@pytest.mark.parametrize(
    "unit,face,renumbered",
    [
        (0, "D", 0),
        (2, "U", 2),
        (3, "U", 3),
        (3, "D", 4),
        (4, "U", 5),
        (4, "D", 5),
        (8, "U", 9),
    ],
)
@pytest.mark.parametrize("version", NAMING_VERSION)
def test_naming_schemes(unit, face, renumbered, version):
    expected_unit = unit if version == "STS8" else renumbered
    assert build_module_name_prefix(unit, face, "R", 12, "T", 0, version) == (
        f"M{expected_unit}{face}R12T0"
    )
    assert patch_ladder_name(f"L{unit}{face}R000001", version) == (
        f"L{expected_unit}{face}R000001"
    )


def test_default_naming_scheme():
    assert build_module_name_prefix(3, "D", "L", 1, "B", 2) == "M4DL1B2"


@pytest.mark.parametrize("version", [None, "", "latest", "STS9"])
def test_unknown_naming_scheme_is_rejected(version):
    with pytest.raises(ValueError, match="Unknown naming version"):
        build_module_name_prefix(3, "D", "R", 1, "T", 0, version)


def test_known_address_and_round_trip():
    address = convert_to_cbm_sts_address("M5DL1B2001162B2", version=1)
    assert address == 0x12028452
    fields = decode_sts_address(address)
    assert fields.pop("system") == 2
    assert make_sts_address(**fields) == address


def test_legacy_address_encoding():
    assert make_sts_address(5, 1, 1, 2, version=0, side=1) == (
        2 | (5 << 4) | (1 << 8) | (1 << 12) | (2 << 13) | (1 << 18)
    )


def test_unit_constants_are_preserved():
    assert MM == 1
    assert CM == 0.1
