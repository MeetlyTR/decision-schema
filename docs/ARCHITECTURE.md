<!--
Decision Ecosystem — decision-schema
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Decision Schema Architecture

## Purpose

**Decision Schema** is the Single Source of Truth (SSOT) for contracts in the multi-core decision ecosystem. It provides shared types and contracts that all decision cores depend on.

## Core Components

### Types (`decision_schema/types.py`)

- **`Action`**: Generic action enum (HOLD, ACT, EXIT, CANCEL, STOP)
- **`Proposal`**: MDM output (action, confidence, reasons, params dict)
- **`FinalDecision`**: Post-modulation action (action, allowed, reasons, mismatch)
- **`MismatchInfo`**: Guard failure flags and reason codes

### Packet (`decision_schema/packet_v2.py`)

- **`PacketV2`**: End-to-end tracing packet
  - `packet_version`: Packet format version (currently "2")
  - `schema_version`: Schema contract version (e.g., "0.1.0")
  - Fields: `run_id`, `step`, `input`, `external`, `mdm`, `final_action`, `latency_ms`, `mismatch`

### Compatibility (`decision_schema/compat.py`)

- **`is_compatible()`**: Check schema version compatibility (supports minor version ranges for 0.x)
- **`parse_version()`**: Parse SemVer string to (major, minor, patch) tuple
- **`get_current_version()`**: Get current schema version

### Version (`decision_schema/version.py`)

- **`__version__`**: Current schema version (SemVer format)

## Inputs/Outputs

**Inputs**: None (foundation package)

**Outputs**: Type definitions and contracts used by all cores:
- `Proposal` → consumed by DMC
- `FinalDecision` → consumed by executor or downstream systems
- `PacketV2` → consumed by evaluation-core
- `Action` enum → used by all cores

## Non-Goals

- **Domain-specific logic**: Schema is domain-agnostic (no domain vocabulary in types)
- **Runtime behavior**: Schema does not execute decisions
- **Policy enforcement**: Schema does not enforce risk policies
- **Metrics computation**: Schema does not compute metrics

## Design Principles

1. **SSOT**: Single source of truth for all contracts
2. **SemVer**: Semantic versioning with compatibility guarantees
3. **Domain-agnostic**: Generic types work across domains
4. **Backward compatibility**: Deprecation plan ensures smooth transitions
5. **Fail-closed**: Invalid versions raise errors (no silent failures)

## Versioning Policy

- **0.x versions**: Minor increments may include deprecations
- **1.x+ versions**: Minor/patch increments are backward compatible
- **Compatibility**: Cores pin major version (e.g., `>=0.1,<0.2`)

See `docs/DEPRECATION_PLAN.md` and `docs/RELEASE_PLAN.md` for details.
