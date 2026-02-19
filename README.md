<!--
Decision Ecosystem — decision-schema
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Decision Schema

Decision Schema is the **Single Source of Truth (SSOT)** contract for a **domain-agnostic, multi-core decision ecosystem**. It defines the shared language used by independent decision cores: *proposal generation*, *decision modulation/guards*, *ops safety*, and *evaluation/calibration*.

## What this is (domain-agnostic)

This contract is intentionally free of domain vocabulary. It is suitable for any autonomous or AI-assisted decision system, e.g.:
- **Robotics and safety controllers**: Navigation, manipulation, and safety decisions
- **Healthcare triage and escalation workflows**: Patient prioritization and care decisions
- **Content moderation and human-in-the-loop review**: Content flagging and review decisions
- **Autonomous ops automation**: Incident response, remediation, and infrastructure decisions
- **Scheduling/education policy engines**: Resource allocation and policy decisions

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
    reasons=["anomaly_signal", "constraint_violation"],
    params={"value": 100},
)
```

### Checking Compatibility

```python
from decision_schema.compat import is_compatible, get_current_version

version = get_current_version()
if is_compatible(version, expected_major=0, min_minor=2, max_minor=2):
    print("Schema version is compatible (0.2.x)")
```

## Version Pinning

Pin schema version in your `pyproject.toml`:

```toml
dependencies = ["decision-schema>=0.2,<0.3"]
```

This ensures compatibility with `0.2.x` (current minor). Next minor (0.3.x) may introduce deprecations; see `docs/DEPRECATION_PLAN.md`.

## Ecosystem integration

Decision Schema is used by:

- **mdm-engine**: produces `Proposal`
- **decision-modulation-core**: consumes `Proposal`, produces `FinalDecision`
- **evaluation-calibration-core**: reads `PacketV2` traces
- **ops-health-core**: produces operational safety signals, integrates via `PacketV2`

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

## License

MIT License. See [LICENSE](LICENSE).
