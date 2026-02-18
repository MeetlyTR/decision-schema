"""INVARIANT T1: Trace external key registry and format validation."""

from __future__ import annotations

from decision_schema.trace_registry import (
    KEY_RE,
    RESERVED_NAMESPACES,
    EXTERNAL_KEY_REGISTRY,
    validate_external_dict,
    is_valid_external_key,
    registry_keys,
)


def test_inv_t1_key_regex_accepts_valid_examples() -> None:
    """KEY_RE accepts valid namespaced keys."""
    assert KEY_RE.match("harness.fail_closed")
    assert KEY_RE.match("ops.deny_actions")
    assert KEY_RE.match("eval.report_ready")
    assert KEY_RE.match("mdm.confidence_score")


def test_inv_t1_key_regex_rejects_invalid_examples() -> None:
    """KEY_RE rejects invalid formats."""
    assert not KEY_RE.match("FailClosed")
    assert not KEY_RE.match("harness_fail_closed")
    assert not KEY_RE.match("harness.fail-closed")
    assert not KEY_RE.match("harness.")  # trailing dot
    assert not KEY_RE.match("harness")  # no dot
    assert not KEY_RE.match("")  # empty


def test_inv_t1_is_valid_external_key() -> None:
    """is_valid_external_key helper matches KEY_RE."""
    assert is_valid_external_key("harness.fail_closed")
    assert not is_valid_external_key("FailClosed")


def test_inv_t1_registry_is_well_formed_and_namespaced() -> None:
    """Registry keys match format and use reserved namespaces."""
    assert "harness.fail_closed" in EXTERNAL_KEY_REGISTRY

    for k, meta in EXTERNAL_KEY_REGISTRY.items():
        assert KEY_RE.match(k), f"registry key must match KEY_RE: {k}"
        prefix = k.split(".", 1)[0]
        assert prefix in RESERVED_NAMESPACES, f"registry key must use reserved namespace: {k}"

        # minimal metadata contract
        assert "owner" in meta and meta["owner"]
        assert "introduced_in" in meta and meta["introduced_in"]
        assert "description" in meta and meta["description"]


def test_inv_t1_validate_format_only_allows_unregistered_keys() -> None:
    """Format-only validation should not force registration by default."""
    errors = validate_external_dict({"harness.some_future_key": True})
    assert errors == []


def test_inv_t1_validate_strict_requires_registry_for_selected_prefixes() -> None:
    """Strict mode requires registry membership for selected namespaces."""
    errors = validate_external_dict(
        {"harness.some_future_key": True},
        require_registry_for_prefixes={"harness"},
    )
    assert any(e.startswith("INV-T1:unregistered_key:") for e in errors)

    errors_ok = validate_external_dict(
        {"harness.fail_closed": True},
        require_registry_for_prefixes={"harness"},
    )
    assert errors_ok == []


def test_inv_t1_validate_rejects_invalid_format() -> None:
    """Validation rejects invalid key formats."""
    errors = validate_external_dict({"InvalidKey": True})
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
