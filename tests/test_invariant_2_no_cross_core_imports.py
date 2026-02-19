# Decision Ecosystem — decision-schema
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
# INV2: This package must not import other ecosystem cores (schema is SSOT).
import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_NAMES = ["decision_schema"]
FORBIDDEN_IMPORTS = {
    "mdm_engine",
    "decision_modulation_core",
    "ops_health",
    "eval_calibration_core",
}


def _collect_imports(path: Path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return []
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.append(node.module.split(".")[0])
    return names


def test_invariant_2_no_cross_core_imports():
    violations = []
    for pkg in PACKAGE_NAMES:
        src_dir = REPO_ROOT / pkg.replace(".", "/")
        if not src_dir.exists():
            continue
        for py in src_dir.rglob("*.py"):
            for imp in _collect_imports(py):
                if imp in FORBIDDEN_IMPORTS:
                    violations.append(f"{py.relative_to(REPO_ROOT)}: imports '{imp}'")
    assert not violations, "INV2 cross-core import violations:\n- " + "\n- ".join(violations)
