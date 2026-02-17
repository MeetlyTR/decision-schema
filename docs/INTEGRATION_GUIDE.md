# Decision Schema Integration Guide

## Installation

```bash
pip install decision-schema
```

Or from source:
```bash
pip install -e .
```

## Basic Usage

### Importing Types

```python
from decision_schema.types import Proposal, FinalDecision, Action, MismatchInfo
from decision_schema.packet_v2 import PacketV2
from decision_schema.version import __version__
```

### Creating a Proposal

```python
from decision_schema.types import Proposal, Action

proposal = Proposal(
    action=Action.ACT,
    confidence=0.8,
    reasons=["signal", "imbalance"],
    params={
        "value": 100,
        "threshold": 0.5,
    },
)
```

### Creating a FinalDecision

```python
from decision_schema.types import FinalDecision, Action, MismatchInfo

decision = FinalDecision(
    action=Action.ACT,
    allowed=True,
    reasons=["approved"],
    mismatch=None,
)
```

### Checking Compatibility

```python
from decision_schema.compat import is_compatible, get_current_version

version = get_current_version()
if is_compatible(version, expected_major=0, min_minor=1, max_minor=1):
    print("Schema version is compatible")
```

## Integration with Other Cores

### MDM Engine

MDM Engine produces `Proposal`:

```python
from decision_schema.types import Proposal
# MDM generates proposal
proposal = Proposal(action=Action.ACT, confidence=0.8, ...)
```

### Decision Modulation Core

DMC consumes `Proposal` and produces `FinalDecision`:

```python
from decision_schema.types import Proposal, FinalDecision
# DMC modulates proposal
final_action, mismatch = modulate(proposal, policy, context)
```

### Evaluation Core

Evaluation core reads `PacketV2` traces:

```python
from decision_schema.packet_v2 import PacketV2
packet = PacketV2.from_dict(json.loads(line))
```

## Version Pinning

Pin schema version in your `pyproject.toml`:

```toml
dependencies = ["decision-schema>=0.1,<0.2"]
```

This ensures compatibility with `0.1.x` versions but prevents upgrades to `0.2.0+` (which may include deprecations).

## Migration from Legacy Types

If migrating from deprecated aliases:

```python
# Old (deprecated)
proposal = Proposal(action=Action.QUOTE, bid_quote=0.49, ...)

# New
proposal = Proposal(
    action=Action.ACT,
    params={"bid": 0.49, "ask": 0.51, "size": 1.0},
)
```

See `docs/DEPRECATION_PLAN.md` for detailed migration guide.
