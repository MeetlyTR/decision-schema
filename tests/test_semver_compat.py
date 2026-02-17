"""SemVer compatibility tests."""

import pytest

from decision_schema.compat import is_compatible, get_current_version, parse_version


def test_is_compatible_same_major() -> None:
    """Verify same major version is compatible."""
    assert is_compatible("0.1.0", 0) is True
    assert is_compatible("0.2.0", 0) is True
    assert is_compatible("0.9.9", 0) is True


def test_is_compatible_different_major() -> None:
    """Verify different major version is incompatible."""
    assert is_compatible("1.0.0", 0) is False
    assert is_compatible("2.0.0", 0) is False


def test_is_compatible_minor_range() -> None:
    """Verify minor version range checking for 0.x versions."""
    # Within range
    assert is_compatible("0.1.0", 0, min_minor=1, max_minor=2) is True
    assert is_compatible("0.2.0", 0, min_minor=1, max_minor=2) is True
    
    # Below range
    assert is_compatible("0.0.9", 0, min_minor=1, max_minor=2) is False
    
    # Above range
    assert is_compatible("0.3.0", 0, min_minor=1, max_minor=2) is False


def test_is_compatible_min_minor_only() -> None:
    """Verify min_minor without max_minor."""
    assert is_compatible("0.2.0", 0, min_minor=1) is True
    assert is_compatible("0.0.9", 0, min_minor=1) is False


def test_is_compatible_max_minor_only() -> None:
    """Verify max_minor without min_minor."""
    assert is_compatible("0.1.0", 0, max_minor=2) is True
    assert is_compatible("0.3.0", 0, max_minor=2) is False


def test_is_compatible_invalid_format() -> None:
    """Verify invalid version format is incompatible."""
    assert is_compatible("invalid", 0) is False
    assert is_compatible("", 0) is False
    assert is_compatible("1", 0) is False


def test_get_current_version() -> None:
    """Verify get_current_version returns string."""
    version = get_current_version()
    assert isinstance(version, str)
    assert version.count(".") == 2  # SemVer format: X.Y.Z


def test_parse_version() -> None:
    """Verify parse_version parses SemVer correctly."""
    assert parse_version("0.1.0") == (0, 1, 0)
    assert parse_version("1.2.3") == (1, 2, 3)
    assert parse_version("0.10.5") == (0, 10, 5)
    
    # Missing patch defaults to 0
    assert parse_version("0.1") == (0, 1, 0)
    
    # Invalid format raises ValueError
    with pytest.raises(ValueError):
        parse_version("invalid")
