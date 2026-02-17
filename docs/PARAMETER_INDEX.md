# PARAMETER_INDEX (SSOT)

This document is the **Single Source of Truth** for structured keys used across the decision ecosystem.
Cores MUST NOT introduce undocumented keys in public integrations.

## Proposal.params

| Key | Type | Meaning | Stability |
|---|---:|---|---|
| value | number | Example numeric parameter (domain-agnostic placeholder) | example-only |

**Note**: Domain-specific parameters should be documented in domain adapters, not in core contract.

## PacketV2.context

| Key | Type | Meaning | Producer | Consumer |
|---|---:|---|---|---|
| run_id | string | Correlates packets across components | any core | evaluation |
| fail_closed | bool | Indicates fail-closed path was taken | any core | ops/eval |

## PacketV2 fields

| Field | Type | Meaning | Required |
|---|---:|---|---|
| run_id | string | Unique run identifier | yes |
| step | int | Step number within run | yes |
| input | dict | Input state snapshot (redacted) | yes |
| external | dict | External context (redacted) | yes |
| mdm | dict | Proposal snapshot | yes |
| final_action | dict | Final decision snapshot | yes |
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
- Use namespaced keys: `domain:key` (e.g., `robotics:position`)
- Document in domain adapter
- Keep core logic domain-agnostic
