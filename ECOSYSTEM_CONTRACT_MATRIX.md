# Ecosystem Contract Matrix

This document tracks contract version compatibility across all cores in the decision ecosystem.

## Core Compatibility Table

| Core | Dependency Range | expected_major | min_minor | max_minor | CI/Test Location |
|------|------------------|----------------|-----------|-----------|------------------|
| **decision-schema** | N/A | 0 | 2 | 2 | `tests/test_semver_compat.py` |
| **mdm-engine** | `>=0.2,<0.3` | 0 | 2 | 2 | `tests/test_schema_dependency.py` |
| **decision-modulation-core** | `>=0.2,<0.3` | 0 | 2 | 2 | `tests/test_schema_dependency.py` |
| **evaluation-calibration-core** | `>=0.2,<0.3` | 0 | 2 | 2 | `tests/test_contract_compat.py` |
| **ops-health-core** | `>=0.2,<0.3` | 0 | 2 | 2 | `tests/test_contract_compat.py` |

## How to Update This Matrix

When `decision-schema` minor version increments (e.g., `0.1.0` → `0.2.0`):

1. **Update decision-schema version**: Bump `decision_schema/version.py` to `0.2.0`
2. **Update this matrix**: Change `max_minor` from `1` to `2` for all cores
3. **Update core dependencies**: Each core updates `pyproject.toml` to `>=0.2,<0.3`
4. **Update compatibility checks**: Each core updates `check_schema_compatibility(expected_minor=2)`
5. **Run tests**: Verify all compatibility tests pass

**Breaking changes** (major version bump `0.x.0` → `1.0.0`):
- All cores must update dependency range to `>=1.0,<2.0`
- Update `expected_major` to `1` in compatibility checks
- Review deprecation plan (aliases/legacy fields removed)

## CI Expectation

Each core **must fail fast** if schema version is incompatible:

- Compatibility check runs on import/startup (via `check_schema_compatibility()`)
- Tests verify compatibility (see test locations in table above)
- CI pipelines should treat compatibility failures as errors

**Example failure**:
```
RuntimeError: decision-schema version 0.2.0 is incompatible. Expected 0.1.x
```

## Released Versions

| Version   | Status   | Notes |
|-----------|----------|--------|
| `0.1.x`   | EOL      | Pre-contract; not supported. |
| `0.2.0`   | Current  | Domain-agnostic contract; PacketV2; Action, Proposal, FinalDecision, MismatchInfo. |

Cores must pin `>=0.2,<0.3` and use min_minor=2, max_minor=2 for 0.2.x.

## Deprecation Timeline

- **0.1.x**: No longer supported. Cores using 0.1.x should upgrade to 0.2.x.
- **0.2.x:** Supported. Patch releases (0.2.1, 0.2.2, …) must remain backward-compatible. Any minor bump (0.3.0) requires explicit matrix + pins + expected_minor update.
- **Major 1.0**: When released, 0.x will enter deprecation window (e.g. 6 months) before EOL; migration guide will be published.

## Current Status

- **Schema Version**: `0.2.0`
- **Contract**: Domain-agnostic (legacy aliases/fields removed)
- **All Cores**: Should pin `>=0.2,<0.3` and use min_minor=2, max_minor=2

## Verification

Run compatibility tests in each core:

```bash
# decision-schema
cd decision-schema && pytest tests/test_semver_compat.py

# mdm-engine
cd mdm-engine && pytest tests/test_schema_dependency.py

# decision-modulation-core
cd decision-modulation-core && pytest tests/test_schema_dependency.py

# evaluation-calibration-core
cd evaluation-calibration-core && pytest tests/test_contract_compat.py

# ops-health-core
cd ops-health-core && pytest tests/test_contract_compat.py
```

All tests should pass when schema version is within expected range.
