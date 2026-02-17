"""Compat gate: current schema is 0.2.x; is_compatible(min_minor=2, max_minor=2) passes."""

from decision_schema.compat import get_current_version, is_compatible, parse_version


def test_current_version_minor_is_2() -> None:
    """Current schema version must be 0.2.x (SSOT)."""
    version = get_current_version()
    major, minor, _ = parse_version(version)
    assert major == 0
    assert minor == 2


def test_is_compatible_minor_2_range() -> None:
    """is_compatible(..., min_minor=2, max_minor=2) must be True for current version."""
    version = get_current_version()
    assert is_compatible(version, expected_major=0, min_minor=2, max_minor=2) is True
