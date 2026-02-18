"""Trace external key registry and validation (INV-T1).

SSOT for PacketV2.external key naming and registration rules.
"""

from __future__ import annotations

import re
from typing import Any, Mapping, Iterable

# External keys MUST be namespaced, lowercase, dot-separated.
# Example: "harness.fail_closed"
KEY_RE = re.compile(r"^[a-z0-9_]+(\.[a-z0-9_]+)+$")

# Prefixes reserved by the ecosystem. These are *namespaces*, not domains.
RESERVED_NAMESPACES = frozenset(
    {
        "harness",
        "integration",
        "ops",
        "dmc",
        "mdm",
        "eval",
        "adapter",
    }
)

# SSOT registry for external trace keys.
# Only keys here are considered "registered". Use strict validation to enforce registration.
EXTERNAL_KEY_REGISTRY: dict[str, dict[str, str]] = {
    "harness.fail_closed": {
        "owner": "integration-harness",
        "introduced_in": "0.2.0",
        "description": "Harness-level fail-closed marker set when run_one_step catches an exception.",
    },
}


def is_valid_external_key(key: str) -> bool:
    """True if key matches the required format (INV-T1.1)."""
    return bool(KEY_RE.match(key))


def validate_external_dict(
    external: Mapping[str, Any] | None,
    *,
    require_registry_for_prefixes: Iterable[str] | None = None,
) -> list[str]:
    """
    Validate PacketV2.external key hygiene.

    Returns a list of error codes (empty list means PASS).

    - Always enforces INV-T1.1: key format.
    - Optionally enforces INV-T1.2: keys under selected namespaces must be registered.
      (Default is non-strict to avoid breaking integrators.)
    """
    if external is None:
        return []

    if not isinstance(external, Mapping):
        return ["INV-T1:external_not_mapping"]

    strict_prefixes = set(require_registry_for_prefixes or [])

    errors: list[str] = []
    for k in external.keys():
        if not isinstance(k, str):
            errors.append("INV-T1:key_not_str")
            continue

        if not is_valid_external_key(k):
            errors.append(f"INV-T1:invalid_key_format:{k}")
            continue

        prefix = k.split(".", 1)[0]
        if prefix in strict_prefixes and k not in EXTERNAL_KEY_REGISTRY:
            errors.append(f"INV-T1:unregistered_key:{k}")

    return errors


def registry_keys() -> set[str]:
    """Return set of all registered external keys."""
    return set(EXTERNAL_KEY_REGISTRY.keys())
