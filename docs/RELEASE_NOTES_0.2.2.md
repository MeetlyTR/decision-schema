<!--
Decision Ecosystem — decision-schema
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Release Notes — decision-schema 0.2.2

**Release Date:** 2026-02-18  
**Type:** Patch Release (backward-compatible)

---

## Summary

This patch release registers the `exec.*` execution trace keys in the SSOT trace registry, formally connecting `execution-orchestration-core`'s `PacketV2.external` keys to the ecosystem-wide TRACE KEY REGISTRY (INV-T1).

---

## Changes

### ✅ INV-T1 — Execution Trace Keys Registration (exec.* namespace)

**Problem:** `execution-orchestration-core` emits `exec.*` trace keys into `PacketV2.external`, but these keys were not yet registered in the SSOT registry, leaving a small gap in external key hygiene and collision prevention.

**Solution:** Extend the trace key registry to include the `exec.*` namespace and execution trace keys:

- Added `exec` to `RESERVED_NAMESPACES`
- Registered the following trace keys in `EXTERNAL_KEY_REGISTRY`:
  - `exec.total_latency_ms`
  - `exec.success_count`
  - `exec.failed_count`
  - `exec.skipped_count`
  - `exec.denied_count`
  - `exec.fail_closed`
  - `exec.attempt_count`

**Files Changed:**
- `decision_schema/trace_registry.py`: Added `exec` namespace and execution trace key entries
- `docs/TRACE_KEY_REGISTRY.md`: Updated reserved namespaces and registry table
- `tests/test_invariant_t1_trace_key_registry.py`: Extended registry invariant tests

**Invariant:** INV-T1.1 (format) and INV-T1.2 (registry) now cover `exec.*` keys used by `execution-orchestration-core`.

---

## Backward Compatibility

✅ **Fully backward-compatible:**
- No breaking changes to public APIs
- Existing `harness.*` and context keys continue to work unchanged
- `exec.*` keys become formally registered, improving hygiene without changing behavior

---

## Migration Guide

**No migration needed.** Existing code continues to work.

**Optional (strict mode):**

If you want to enforce registry membership for the `exec` namespace:

```python
from decision_schema.trace_registry import validate_external_dict

errors = validate_external_dict(
    external,
    require_registry_for_prefixes={"exec"},
    mode="trace",
)
```

---

## Testing

- ✅ All existing tests pass
- ✅ Registry invariants extended to cover `exec.*` keys

---

## References

- **Invariant:** INV-T1 (Trace Key Registry)
- **Related:** `docs/TRACE_KEY_REGISTRY.md`, `execution-orchestration-core/docs/PARAMETER_INDEX_EXECUTION.md`

---

**Upgrade Path:** `pip install "decision-schema>=0.2.2,<0.3"`

