# Decision Schema

**Decision Schema** is the Single Source of Truth (SSOT) for contracts in the multi-core decision ecosystem. It provides shared types and contracts that all decision cores depend on.

## Purpose

This package defines:
- **Shared types**: `Action`, `Proposal`, `FinalDecision`, `MismatchInfo`
- **Tracing contract**: `PacketV2` for end-to-end decision tracing
- **Version compatibility**: SemVer-based compatibility checks

## Installation

```bash
pip install decision-schema
```

Or from source:
```bash
pip install -e .
```

## Quick Start

### Importing Types

```python
from decision_schema.types import Proposal, FinalDecision, Action
from decision_schema.packet_v2 import PacketV2
from decision_schema.compat import is_compatible
```

### Creating a Proposal

```python
from decision_schema.types import Proposal, Action

proposal = Proposal(
    action=Action.ACT,
    confidence=0.8,
    reasons=["signal", "imbalance"],
    params={"value": 100},
)
```

### Checking Compatibility

```python
from decision_schema.compat import is_compatible, get_current_version

version = get_current_version()
if is_compatible(version, expected_major=0, min_minor=1, max_minor=1):
    print("Schema version is compatible")
```

## Version Pinning

Pin schema version in your `pyproject.toml`:

```toml
dependencies = ["decision-schema>=0.1,<0.2"]
```

This ensures compatibility with `0.1.x` versions but prevents upgrades to `0.2.0+` (which may include deprecations).

## Ecosystem

Decision Schema is used by:
- **mdm-engine**: Produces `Proposal`
- **decision-modulation-core**: Consumes `Proposal`, produces `FinalDecision`
- **evaluation-calibration-core**: Reads `PacketV2` traces
- **ops-health-core**: Integrates with `PacketV2` for operational signals

See `ECOSYSTEM_CONTRACT_MATRIX.md` for version compatibility details.

## Documentation

- `docs/ARCHITECTURE.md`: System architecture
- `docs/FORMULAS.md`: Version compatibility formulas
- `docs/INTEGRATION_GUIDE.md`: Integration examples
- `docs/DEPRECATION_PLAN.md`: Deprecation timeline
- `docs/RELEASE_PLAN.md`: Release process

## Versioning

Decision Schema follows Semantic Versioning (SemVer):
- **0.x versions**: Minor increments may include deprecations
- **1.x+ versions**: Minor/patch increments are backward compatible

See `docs/RELEASE_PLAN.md` for details.

## Migration

If migrating from deprecated aliases or legacy fields, see `docs/DEPRECATION_PLAN.md` and `docs/INTEGRATION_GUIDE.md`.
