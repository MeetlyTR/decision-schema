"""CI-0: Workflow file hygiene — LF-only, no control/embedding Unicode, multi-line YAML."""
import re
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parent.parent / ".github" / "workflows"

FORBIDDEN_UNICODE_CODEPOINT_RANGES = [
    ("\u202A", "\u202E"),
    ("\u2066", "\u2069"),
    ("\u2028", "\u2029"),
]
FORBIDDEN_UNICODE_CHARS = [
    "\ufeff", "\u200b", "\u200c", "\u200d", "\u2060",
]
MIN_EXPECTED_NEWLINES = 10


def _contains_forbidden_unicode(text: str) -> list[str]:
    hits: list[str] = []
    for ch in FORBIDDEN_UNICODE_CHARS:
        if ch in text:
            hits.append(f"U+{ord(ch):04X}")
    for start, end in FORBIDDEN_UNICODE_CODEPOINT_RANGES:
        s, e = ord(start), ord(end)
        for cp in range(s, e + 1):
            if chr(cp) in text:
                hits.append(f"U+{cp:04X}")
    return sorted(set(hits))


def test_invariant_ci_0_workflow_hygiene():
    assert WORKFLOW_DIR.exists(), f"{WORKFLOW_DIR} does not exist"
    workflow_files = sorted(
        [p for p in WORKFLOW_DIR.rglob("*") if p.is_file() and p.suffix in {".yml", ".yaml"}]
    )
    assert workflow_files, "No workflow YAML files found under .github/workflows"
    failures: list[str] = []
    for path in workflow_files:
        b = path.read_bytes()
        if b"\r" in b:
            failures.append(f"{path}: contains CR bytes (count={b.count(b'\r')})")
        lf_count = b.count(b"\n")
        if lf_count < MIN_EXPECTED_NEWLINES:
            failures.append(f"{path}: too few LF newlines (count={lf_count})")
        try:
            text = b.decode("utf-8")
        except UnicodeDecodeError as e:
            failures.append(f"{path}: not valid UTF-8 ({e})")
            continue
        hits = _contains_forbidden_unicode(text)
        if hits:
            failures.append(f"{path}: forbidden Unicode present: {', '.join(hits)}")
        if not re.search(r"(?m)^\s*on:\s*$", text) and "on:" not in text:
            failures.append(f"{path}: missing 'on:' key")
        if not re.search(r"(?m)^\s*jobs:\s*$", text) and "jobs:" not in text:
            failures.append(f"{path}: missing 'jobs:' key")
    assert not failures, "CI-0 workflow hygiene violations:\n- " + "\n- ".join(failures)
