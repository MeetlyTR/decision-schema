"""Trace external key registry and validation (INV-T1).

SSOT for PacketV2.external key naming and registration rules.
"""

from __future__ import annotations

import re
from typing import Any, Mapping, Iterable

# Trace-extension keys MUST be namespaced, lowercase, dot-separated.
# Example: "harness.fail_closed"
TRACE_KEY_RE = re.compile(r"^[a-z0-9_]+(\.[a-z0-9_]+)+$")

# Context keys (PARAMETER_INDEX): plain lowercase alphanumeric + underscore (no dot required).
# Example: "now_ms", "run_id", "ops_deny_actions"
CONTEXT_KEY_RE = re.compile(r"^[a-z0-9_]+$")

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
        "exec",
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
    # Execution-orchestration-core trace keys (exec.* namespace)
    "exec.total_latency_ms": {
        "owner": "execution-orchestration-core",
        "introduced_in": "0.2.2",
        "description": "Total execution latency in milliseconds for the decision execution pipeline.",
    },
    "exec.success_count": {
        "owner": "execution-orchestration-core",
        "introduced_in": "0.2.2",
        "description": "Number of successful execution attempts.",
    },
    "exec.failed_count": {
        "owner": "execution-orchestration-core",
        "introduced_in": "0.2.2",
        "description": "Number of failed execution attempts.",
    },
    "exec.skipped_count": {
        "owner": "execution-orchestration-core",
        "introduced_in": "0.2.2",
        "description": "Number of skipped actions (not executed).",
    },
    "exec.denied_count": {
        "owner": "execution-orchestration-core",
        "introduced_in": "0.2.2",
        "description": "Number of denied actions due to policies or kill-switch.",
    },
    "exec.fail_closed": {
        "owner": "execution-orchestration-core",
        "introduced_in": "0.2.2",
        "description": "Fail-closed marker for execution orchestrator when an exception path is taken.",
    },
    "exec.attempt_count": {
        "owner": "execution-orchestration-core",
        "introduced_in": "0.2.2",
        "description": "Total number of execution attempts across all actions.",
    },
}


def is_valid_trace_key(key: str) -> bool:
    """True if key matches trace-extension format (dot-separated, INV-T1.1)."""
    return bool(TRACE_KEY_RE.match(key))


def is_valid_context_key(key: str) -> bool:
    """True if key matches context format (plain, PARAMETER_INDEX)."""
    return bool(CONTEXT_KEY_RE.match(key))


def is_valid_external_key(key: str, mode: str = "both") -> bool:
    """
    True if key matches required format.
    
    Args:
        key: Key to validate
        mode: "context" (PARAMETER_INDEX keys), "trace" (trace-extension keys), "both" (either)
    """
    if mode == "context":
        return is_valid_context_key(key)
    elif mode == "trace":
        return is_valid_trace_key(key)
    else:  # both
        return is_valid_context_key(key) or is_valid_trace_key(key)


def validate_external_dict(
    external: Mapping[str, Any] | None,
    *,
    require_registry_for_prefixes: Iterable[str] | None = None,
    mode: str = "both",
) -> list[str]:
    """
    Validate PacketV2.external key hygiene.

    PacketV2.external contains two types of keys:
    - Context keys (PARAMETER_INDEX): plain format (now_ms, run_id, ops_*)
    - Trace-extension keys (INV-T1): dot-separated (harness.fail_closed)

    Args:
        external: Dictionary to validate
        require_registry_for_prefixes: If set, trace keys under these prefixes must be registered
        mode: "context" (validate as context dict), "trace" (validate as trace-extension),
              "both" (accept either format, default)

    Returns:
        List of error codes (empty list means PASS).

    - Always enforces key format (context or trace depending on mode).
    - Optionally enforces INV-T1.2: trace keys under selected namespaces must be registered.
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

        # Format validation based on mode
        if mode == "context":
            if not is_valid_context_key(k):
                errors.append(f"INV-T1:invalid_context_key_format:{k}")
                continue
        elif mode == "trace":
            if not is_valid_trace_key(k):
                errors.append(f"INV-T1:invalid_trace_key_format:{k}")
                continue
            # Registry check only for trace keys
            prefix = k.split(".", 1)[0]
            if prefix in strict_prefixes and k not in EXTERNAL_KEY_REGISTRY:
                errors.append(f"INV-T1:unregistered_key:{k}")
        else:  # both
            if not is_valid_external_key(k, mode="both"):
                errors.append(f"INV-T1:invalid_key_format:{k}")
                continue
            # Registry check only for trace keys (dot-separated)
            if "." in k:
                prefix = k.split(".", 1)[0]
                if prefix in strict_prefixes and k not in EXTERNAL_KEY_REGISTRY:
                    errors.append(f"INV-T1:unregistered_key:{k}")

    return errors


def registry_keys() -> set[str]:
    """Return set of all registered external keys."""
    return set(EXTERNAL_KEY_REGISTRY.keys())
