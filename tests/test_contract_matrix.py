# Decision Ecosystem — decision-schema
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Test that ECOSYSTEM_CONTRACT_MATRIX.md exists and contains all cores."""

from pathlib import Path


def test_contract_matrix_exists() -> None:
    """Verify ECOSYSTEM_CONTRACT_MATRIX.md exists."""
    repo_root = Path(__file__).resolve().parents[1]
    matrix_file = repo_root / "ECOSYSTEM_CONTRACT_MATRIX.md"
    assert matrix_file.exists(), "ECOSYSTEM_CONTRACT_MATRIX.md must exist"


def test_contract_matrix_contains_all_cores() -> None:
    """Verify ECOSYSTEM_CONTRACT_MATRIX.md contains all 5 cores."""
    repo_root = Path(__file__).resolve().parents[1]
    matrix_file = repo_root / "ECOSYSTEM_CONTRACT_MATRIX.md"
    content = matrix_file.read_text(encoding="utf-8")

    # Check for all core names
    cores = [
        "decision-schema",
        "mdm-engine",
        "decision-modulation-core",
        "evaluation-calibration-core",
        "ops-health-core",
    ]

    for core in cores:
        assert core in content, f"ECOSYSTEM_CONTRACT_MATRIX.md must mention {core}"


def test_release_plan_exists() -> None:
    """Verify RELEASE_PLAN.md exists."""
    repo_root = Path(__file__).resolve().parents[1]
    release_plan = repo_root / "docs" / "RELEASE_PLAN.md"
    assert release_plan.exists(), "docs/RELEASE_PLAN.md must exist"
