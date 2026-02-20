# Decision Ecosystem — decision-schema
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
INV-PARAM-INDEX-1: Ensure PARAMETER_INDEX.md exists and is in sync with trace registry.

Run from decision-schema repo root. Exit 0 if pass; non-zero if drift or missing doc.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PARAM_INDEX = REPO_ROOT / "docs" / "PARAMETER_INDEX.md"
TRACE_REGISTRY_DOC = REPO_ROOT / "docs" / "TRACE_KEY_REGISTRY.md"


def main() -> int:
    if not PARAM_INDEX.exists():
        print("INV-PARAM-INDEX-1: docs/PARAMETER_INDEX.md missing", file=sys.stderr)
        return 1

    text = PARAM_INDEX.read_text(encoding="utf-8")
    required = ["PacketV2", "external"]
    for phrase in required:
        if phrase not in text:
            print(f"INV-PARAM-INDEX-1: PARAMETER_INDEX.md must mention '{phrase}'", file=sys.stderr)
            return 1

    # Trace registry must be referenced (SSOT link)
    if "trace_registry" not in text and "EXTERNAL_KEY_REGISTRY" not in text and "TRACE_KEY_REGISTRY" not in text:
        print(
            "INV-PARAM-INDEX-1: PARAMETER_INDEX.md should reference trace_registry or TRACE_KEY_REGISTRY",
            file=sys.stderr,
        )
        return 1

    # Optional: every key in EXTERNAL_KEY_REGISTRY should be documented in PARAMETER_INDEX or TRACE_KEY_REGISTRY
    try:
        from decision_schema.trace_registry import EXTERNAL_KEY_REGISTRY
    except ImportError:
        return 0

    doc_text = text
    if TRACE_REGISTRY_DOC.exists():
        doc_text += "\n" + TRACE_REGISTRY_DOC.read_text(encoding="utf-8")
    missing: list[str] = []
    for key in EXTERNAL_KEY_REGISTRY:
        if key not in doc_text:
            missing.append(key)
    if missing:
        print(
            "INV-PARAM-INDEX-1: Registered keys not documented in PARAMETER_INDEX or TRACE_KEY_REGISTRY:",
            missing,
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
