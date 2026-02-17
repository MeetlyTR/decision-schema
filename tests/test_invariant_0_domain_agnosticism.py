"""Test INVARIANT 0: Domain-agnosticism in public surface.

This test ensures that public documentation and schema sources do not contain
domain-specific terminology (trading, market, order, bid, ask, exchange, etc.).
"""

import re
from pathlib import Path

# Domain-specific terms that must not appear in public surface
FORBIDDEN_TERMS = {
    "trade",
    "trading",
    "trader",
    "market",
    "marketplace",
    "order",
    "bid",
    "ask",
    "exchange",
    "orderbook",
    "order-book",
    "quote",
    "fill",
    "execution",
    "position",
    "portfolio",
}

# Files/directories to check
PUBLIC_SURFACE_PATHS = [
    "README.md",
    "docs/",
    "decision_schema/",
]

# Files/directories to exclude (examples, tests with domain-specific content)
EXCLUDE_PATTERNS = [
    r"docs/examples/",
    r"tests/.*example.*",
    r".*_example\.py",
    r".*test.*domain.*",
]


def find_files_to_check(repo_root: Path) -> list[Path]:
    """Find all files in public surface that should be checked."""
    files_to_check = []
    
    for path_pattern in PUBLIC_SURFACE_PATHS:
        path = repo_root / path_pattern
        if not path.exists():
            continue
            
        if path.is_file():
            files_to_check.append(path)
        elif path.is_dir():
            for file_path in path.rglob("*"):
                if file_path.is_file() and file_path.suffix in (".md", ".py", ".rst", ".txt"):
                    # Check if file should be excluded
                    rel_path = file_path.relative_to(repo_root)
                    should_exclude = any(
                        re.search(pattern, str(rel_path), re.IGNORECASE)
                        for pattern in EXCLUDE_PATTERNS
                    )
                    if not should_exclude:
                        files_to_check.append(file_path)
    
    return files_to_check


def check_file_for_domain_terms(file_path: Path) -> list[tuple[int, str, str]]:
    """Check a file for forbidden domain-specific terms.
    
    Returns:
        List of (line_number, term, line_content) tuples for violations.
    """
    violations = []
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Skip binary files
        return violations
    
    lines = content.split("\n")
    
    for line_num, line in enumerate(lines, start=1):
        line_lower = line.lower()
        for term in FORBIDDEN_TERMS:
            # Use word boundaries to avoid false positives
            pattern = r"\b" + re.escape(term) + r"\b"
            if re.search(pattern, line_lower):
                violations.append((line_num, term, line.strip()))
    
    return violations


def test_invariant_0_domain_agnosticism():
    """Test that public surface does not contain domain-specific terms."""
    repo_root = Path(__file__).parent.parent
    
    files_to_check = find_files_to_check(repo_root)
    
    all_violations = []
    
    for file_path in files_to_check:
        violations = check_file_for_domain_terms(file_path)
        if violations:
            rel_path = file_path.relative_to(repo_root)
            for line_num, term, line_content in violations:
                all_violations.append((str(rel_path), line_num, term, line_content))
    
    if all_violations:
        error_msg = "\nDomain-specific terms found in public surface (INVARIANT 0 violation):\n\n"
        for rel_path, line_num, term, line_content in all_violations:
            error_msg += f"  {rel_path}:{line_num}: Found '{term}' in:\n"
            error_msg += f"    {line_content}\n\n"
        error_msg += "\nThese terms violate domain-agnosticism. Move domain-specific content to docs/examples/ or use generic terminology.\n"
        raise AssertionError(error_msg)
    
    # Test passes if no violations found
    assert True, "INVARIANT 0: Domain-agnosticism check passed"


if __name__ == "__main__":
    test_invariant_0_domain_agnosticism()
    print("✅ INVARIANT 0 test passed: No domain-specific terms found in public surface")
