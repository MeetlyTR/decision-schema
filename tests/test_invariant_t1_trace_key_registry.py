# Decision Ecosystem — decision-schema
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INVARIANT T1: Trace external key registry and format validation."""

from __future__ import annotations

from decision_schema.trace_registry import (
    TRACE_KEY_RE,
    CONTEXT_KEY_RE,
    RESERVED_NAMESPACES,
    EXTERNAL_KEY_REGISTRY,
    validate_external_dict,
    is_valid_external_key,
    is_valid_context_key,
    is_valid_trace_key,
    registry_keys,
)


def test_inv_t1_trace_key_regex_accepts_valid_examples() -> None:
    """TRACE_KEY_RE accepts valid namespaced keys."""
    assert TRACE_KEY_RE.match("harness.fail_closed")
    assert TRACE_KEY_RE.match("ops.deny_actions")
    assert TRACE_KEY_RE.match("eval.report_ready")
    assert TRACE_KEY_RE.match("mdm.confidence_score")


def test_inv_t1_trace_key_regex_rejects_invalid_examples() -> None:
    """TRACE_KEY_RE rejects invalid formats."""
    assert not TRACE_KEY_RE.match("FailClosed")
    assert not TRACE_KEY_RE.match("harness_fail_closed")
    assert not TRACE_KEY_RE.match("harness.fail-closed")
    assert not TRACE_KEY_RE.match("harness.")  # trailing dot
    assert not TRACE_KEY_RE.match("harness")  # no dot
    assert not TRACE_KEY_RE.match("")  # empty


def test_inv_t1_context_key_regex_accepts_valid_examples() -> None:
    """CONTEXT_KEY_RE accepts plain keys (PARAMETER_INDEX)."""
    assert CONTEXT_KEY_RE.match("now_ms")
    assert CONTEXT_KEY_RE.match("run_id")
    assert CONTEXT_KEY_RE.match("ops_deny_actions")
    assert CONTEXT_KEY_RE.match("error_timestamps")


def test_inv_t1_context_key_regex_rejects_invalid_examples() -> None:
    """CONTEXT_KEY_RE rejects dot-separated keys."""
    assert not CONTEXT_KEY_RE.match("harness.fail_closed")
    assert not CONTEXT_KEY_RE.match("FailClosed")
    assert not CONTEXT_KEY_RE.match("now-ms")  # dash
    assert not CONTEXT_KEY_RE.match("")  # empty


def test_inv_t1_is_valid_external_key() -> None:
    """is_valid_external_key helper supports both modes."""
    assert is_valid_external_key("harness.fail_closed", mode="trace")
    assert is_valid_external_key("now_ms", mode="context")
    assert is_valid_external_key("harness.fail_closed", mode="both")
    assert is_valid_external_key("now_ms", mode="both")
    assert not is_valid_external_key("FailClosed", mode="both")


def test_inv_t1_registry_is_well_formed_and_namespaced() -> None:
    """Registry keys match format and use reserved namespaces."""
    assert "harness.fail_closed" in EXTERNAL_KEY_REGISTRY
    # Execution-orchestration-core trace keys should also be registered.
    assert "exec.total_latency_ms" in EXTERNAL_KEY_REGISTRY
    assert "exec.success_count" in EXTERNAL_KEY_REGISTRY
    assert "exec.failed_count" in EXTERNAL_KEY_REGISTRY
    assert "exec.skipped_count" in EXTERNAL_KEY_REGISTRY
    assert "exec.denied_count" in EXTERNAL_KEY_REGISTRY
    assert "exec.fail_closed" in EXTERNAL_KEY_REGISTRY
    assert "exec.attempt_count" in EXTERNAL_KEY_REGISTRY

    for k, meta in EXTERNAL_KEY_REGISTRY.items():
        assert TRACE_KEY_RE.match(k), f"registry key must match TRACE_KEY_RE: {k}"
        prefix = k.split(".", 1)[0]
        assert prefix in RESERVED_NAMESPACES, f"registry key must use reserved namespace: {k}"

        # minimal metadata contract
        assert "owner" in meta and meta["owner"]
        assert "introduced_in" in meta and meta["introduced_in"]
        assert "description" in meta and meta["description"]


def test_inv_t1_validate_context_mode_accepts_plain_keys() -> None:
    """Context mode accepts PARAMETER_INDEX keys (now_ms, run_id, etc.)."""
    errors = validate_external_dict(
        {"now_ms": 1000, "run_id": "test", "ops_deny_actions": False},
        mode="context",
    )
    assert errors == []


def test_inv_t1_validate_trace_mode_accepts_dot_separated_keys() -> None:
    """Trace mode accepts dot-separated keys."""
    errors = validate_external_dict(
        {"harness.fail_closed": True},
        mode="trace",
    )
    assert errors == []


def test_inv_t1_validate_both_mode_accepts_either_format() -> None:
    """Both mode accepts context keys and trace keys."""
    errors = validate_external_dict(
        {"now_ms": 1000, "harness.fail_closed": True},
        mode="both",
    )
    assert errors == []


def test_inv_t1_validate_format_only_allows_unregistered_keys() -> None:
    """Format-only validation should not force registration by default."""
    errors = validate_external_dict({"harness.some_future_key": True}, mode="trace")
    assert errors == []


def test_inv_t1_validate_strict_requires_registry_for_selected_prefixes() -> None:
    """Strict mode requires registry membership for selected namespaces."""
    errors = validate_external_dict(
        {"harness.some_future_key": True},
        require_registry_for_prefixes={"harness"},
        mode="trace",
    )
    assert any(e.startswith("INV-T1:unregistered_key:") for e in errors)

    errors_ok = validate_external_dict(
        {"harness.fail_closed": True},
        require_registry_for_prefixes={"harness"},
        mode="trace",
    )
    assert errors_ok == []


def test_inv_t1_validate_rejects_invalid_format() -> None:
    """Validation rejects invalid key formats."""
    errors = validate_external_dict({"InvalidKey": True}, mode="both")
    assert any(e.startswith("INV-T1:invalid_key_format:") for e in errors)


def test_inv_t1_validate_handles_none() -> None:
    """Validation handles None external dict."""
    errors = validate_external_dict(None)
    assert errors == []


def test_inv_t1_registry_keys() -> None:
    """registry_keys() returns set of registered keys."""
    keys = registry_keys()
    assert isinstance(keys, set)
    assert "harness.fail_closed" in keys
