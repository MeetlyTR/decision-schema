<!--
Decision Ecosystem — decision-schema
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Release Notes — decision-schema 0.2.1

**Release Date:** 2026-02-17  
**Type:** Patch Release (backward-compatible)

---

## Summary

This patch release fixes INV-T1 external key validation to support both context keys (PARAMETER_INDEX) and trace-extension keys (INV-T1), resolving validation conflicts with harness context keys.

---

## Changes

### ✅ F1 — INV-T1 Two-Mode Validation

**Problem:** `validate_external_dict()` only accepted dot-separated keys (`harness.fail_closed`), but harness places plain context keys (`now_ms`, `run_id`, `ops_deny_actions`) into `external_snapshot`, causing validation failures.

**Solution:** Added two-mode validation:
- **Context keys:** Plain format `^[a-z0-9_]+$` (PARAMETER_INDEX keys)
- **Trace-extension keys:** Dot-separated format `^[a-z0-9_]+(\.[a-z0-9_]+)+$` (INV-T1 keys)
- **Both mode:** Accepts either format (default)

**Files Changed:**
- `decision_schema/trace_registry.py`: Added `CONTEXT_KEY_RE`, `TRACE_KEY_RE`, `mode` parameter
- `docs/PARAMETER_INDEX.md`: Documented context vs trace-extension keys
- `tests/test_invariant_t1_trace_key_registry.py`: Updated tests (14/14 passed)

**Invariant:** INV-T1.1 (format) and INV-T1.2 (registry) now correctly handle both key types.

---

## Backward Compatibility

✅ **Fully backward-compatible:**
- Default `mode="both"` accepts existing usage patterns
- No API changes (only new optional parameter)
- Existing code continues to work without modification

---

## Migration Guide

**No migration needed.** Existing code continues to work.

**Optional:** If you want to validate only context or trace keys:
```python
from decision_schema.trace_registry import validate_external_dict

# Validate as context dict (PARAMETER_INDEX keys)
errors = validate_external_dict(external, mode="context")

# Validate as trace-extension dict (INV-T1 keys)
errors = validate_external_dict(external, mode="trace")

# Default: accepts both (backward-compatible)
errors = validate_external_dict(external, mode="both")
```

---

## Testing

- ✅ All existing tests pass (42/42)
- ✅ New tests added for two-mode validation (14 tests)
- ✅ Harness integration verified: `validate_external_dict(packet.external, mode="both")` passes

---

## References

- **Invariant:** INV-T1 (Trace Key Registry)
- **Related:** `docs/TRACE_KEY_REGISTRY.md`, `docs/PARAMETER_INDEX.md`
- **Issue:** F1 from static analysis report

---

**Upgrade Path:** `pip install "decision-schema>=0.2.1,<0.3"`
