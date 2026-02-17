"""Schema compatibility utilities."""

from decision_schema.version import __version__


def is_compatible(
    schema_version: str,
    expected_major: int,
    min_minor: int | None = None,
    max_minor: int | None = None,
) -> bool:
    """
    Check if schema version is compatible with expected version range.
    
    SemVer compatibility rules:
    - For 0.x versions: compatible if major matches AND minor is within range (if specified)
    - For 1.x+ versions: compatible if major matches (minor/patch changes are backward compatible)
    
    Args:
        schema_version: Schema version string (e.g., "0.1.0")
        expected_major: Expected major version number (e.g., 0)
        min_minor: Minimum minor version (inclusive). If None, no lower bound.
        max_minor: Maximum minor version (inclusive). If None, no upper bound.
    
    Returns:
        True if compatible, False otherwise.
    
    Example:
        >>> is_compatible("0.1.0", 0)
        True
        >>> is_compatible("0.1.0", 0, min_minor=1, max_minor=2)
        True
        >>> is_compatible("0.3.0", 0, min_minor=1, max_minor=2)
        False
        >>> is_compatible("1.0.0", 0)
        False
    """
    try:
        parts = schema_version.split(".")
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        
        if major != expected_major:
            return False
        
        # For 0.x versions, check minor version range
        if major == 0:
            if min_minor is not None and minor < min_minor:
                return False
            if max_minor is not None and minor > max_minor:
                return False
        
        # For 1.x+ versions, minor/patch changes are backward compatible
        return True
    except (ValueError, IndexError):
        # Invalid version format - assume incompatible
        return False


def get_current_version() -> str:
    """Get current schema version."""
    return __version__


def parse_version(version: str) -> tuple[int, int, int]:
    """
    Parse SemVer string into (major, minor, patch) tuple.
    
    Args:
        version: Version string (e.g., "0.1.0")
    
    Returns:
        Tuple of (major, minor, patch)
    
    Raises:
        ValueError: If version format is invalid
    """
    parts = version.split(".")
    if len(parts) < 2:
        raise ValueError(f"Invalid version format: {version}")
    major = int(parts[0])
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    return (major, minor, patch)
