# PARAMETER_INDEX (SSOT)

This document is the **Single Source of Truth** for structured keys used across the decision ecosystem.
Cores MUST NOT introduce undocumented keys in public integrations.

## Proposal.params

| Key | Type | Meaning | Stability |
|---|---:|---|---|
| value | number | Example numeric parameter (domain-agnostic placeholder) | example-only |

**Note**: Domain-specific parameters should be documented in domain adapters, not in core contract.

## Integration context dictionary (context key registry)

Cores pass a context dict (e.g. to `modulate(proposal, policy, context)`). PacketV2 does not have a `context` field; it has `input`, `external`, `mdm`, `final_action`. The following **generic** keys are the SSOT registry for integration:

| Key | Type | Meaning | Producer | Consumer |
|---|---:|---|---|---|
| now_ms | int | Current timestamp (ms) | caller | DMC, guards |
| last_event_ts_ms | int | Last event timestamp (ms); staleness checks | caller | DMC |
| run_id | string | Correlates packets across components | any core | evaluation |
| fail_closed | bool | Indicates fail-closed path was taken | any core | ops/eval |
| ops_deny_actions | bool | Ops-health: deny all actions | ops-health | DMC |
| ops_state | string | Ops-health state (GREEN/YELLOW/RED) | ops-health | DMC |
| ops_cooldown_until_ms | int \| None | Ops-health cooldown end (ms) | ops-health | DMC |
| errors_in_window | int | Error count in window | caller | DMC |
| steps_in_window | int | Step count in window | caller | DMC |
| rate_limit_events | int | Rate-limit event count | caller | DMC |
| recent_failures | int | Recent failure count (circuit breaker) | caller | DMC |
| cooldown_until_ms | int \| None | Generic cooldown end (ms) | caller | DMC |

## PacketV2 fields

| Field | Type | Meaning | Required |
|---|---:|---|---|
| run_id | string | Unique run identifier | yes |
| step | int | Step number within run | yes |
| input | dict | Input state snapshot (redacted) | yes |
| external | dict | External context (redacted) | yes |
| mdm | dict | Proposal snapshot | yes |
| final_action | dict | Final decision snapshot | yes |

### PacketV2.external (context snapshot + trace extension)

`PacketV2.external` contains two types of keys:

1. **Context keys** (PARAMETER_INDEX): Plain format `^[a-z0-9_]+$` (e.g., `now_ms`, `run_id`, `ops_deny_actions`)
   - These are integration context keys documented in PARAMETER_INDEX above
   - Used by cores for decision-making (DMC, guards, etc.)

2. **Trace-extension keys** (INV-T1): Dot-separated format `^[a-z0-9_]+(\.[a-z0-9_]+)+$` (e.g., `harness.fail_closed`)
   - Reserved namespaces (e.g., `harness`, `ops`, `dmc`, `mdm`, `eval`, `integration`, `adapter`) SHOULD be registered in the SSOT registry:
     - `decision_schema/trace_registry.py` (`EXTERNAL_KEY_REGISTRY`)
     - See: `docs/TRACE_KEY_REGISTRY.md`
   - Used for trace-level metadata and debugging markers

Validation: Use `decision_schema.trace_registry.validate_external_dict(external, mode="both")` to validate both types.
| latency_ms | int | Total latency in milliseconds | yes |
| mismatch | dict\|None | Mismatch info if guards triggered | no |
| schema_version | string | Schema version for compatibility | yes |

## Reserved namespaces

- `x_*`: experimental (must be removed or promoted before stable release)
- `example_*`: example-domain only (must not be required by cores)
- `_private_*`: private/internal use only (must not be in public API)

## Context dictionary conventions

### Standard keys (optional but recommended)
- `state`: Current system state
- `signals`: Current signals/observations
- `history`: Historical data (compressed)
- `metadata`: Domain-specific metadata

### Domain-specific keys
- Use namespaced keys: `domain:key` (e.g., `robotics:state`)
- Document in domain adapter
- Keep core logic domain-agnostic
