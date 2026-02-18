<!--
Decision Ecosystem — decision-schema
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Trace External Key Registry (SSOT)

This document defines the naming and registration rules for `PacketV2.external` keys.

## Scope

- `PacketV2.external` is a **trace extension** surface owned by the integration layer.
- Keys must be **domain-agnostic**, stable, and conflict-free.
- The SSOT registry is implemented in `decision_schema/trace_registry.py`.

## Key format (INV-T1.1)

All keys must match:

`^[a-z0-9_]+(\.[a-z0-9_]+)+$`

Examples:
- ✅ `harness.fail_closed`
- ✅ `ops.deny_actions`
- ❌ `FailClosed`
- ❌ `harness_fail_closed`
- ❌ `harness.fail-closed`

## Reserved namespaces

The following namespaces are reserved by the ecosystem:

- `harness`, `integration`, `ops`, `dmc`, `mdm`, `eval`, `adapter`, `exec`

Using a reserved namespace implies the key should be **registered** (INV-T1.2 in strict mode).

## Registry table (SSOT)

Registered keys (source of truth: `decision_schema/trace_registry.py`):

| Key | Owner | Introduced | Description |
|-----|-------|------------|-------------|
| `harness.fail_closed` | integration-harness | 0.2.0 | Harness-level fail-closed marker when an exception is caught. |
| `exec.total_latency_ms` | execution-orchestration-core | 0.2.2 | Total execution latency in milliseconds for the decision execution pipeline. |
| `exec.success_count` | execution-orchestration-core | 0.2.2 | Number of successful execution attempts. |
| `exec.failed_count` | execution-orchestration-core | 0.2.2 | Number of failed execution attempts. |
| `exec.skipped_count` | execution-orchestration-core | 0.2.2 | Number of skipped actions (not executed). |
| `exec.denied_count` | execution-orchestration-core | 0.2.2 | Number of denied actions due to policies or kill-switch. |
| `exec.fail_closed` | execution-orchestration-core | 0.2.2 | Fail-closed marker for execution orchestrator when an exception path is taken. |
| `exec.attempt_count` | execution-orchestration-core | 0.2.2 | Total number of execution attempts across all actions. |

## How to add a new key

1) Add the key entry to `decision_schema/trace_registry.py` (`EXTERNAL_KEY_REGISTRY`)  
2) Ensure the key matches the format and uses an appropriate namespace  
3) Add/extend a unit test in `tests/test_invariant_t1_trace_key_registry.py`  
4) If an integration layer emits the key, add a harness test asserting it is registered

## Validation API

Use:

- `decision_schema.trace_registry.validate_external_dict(external, require_registry_for_prefixes={...})`

Non-strict mode (default) checks **format only**. Strict mode additionally requires registry membership for selected namespaces.
