# Deprecation Plan

This document outlines the deprecation strategy for `decision-schema` to maintain a clean, domain-agnostic contract.

## Overview

As the schema evolves, certain features will be deprecated to keep the contract generic and domain-agnostic. This plan ensures smooth transitions and clear migration paths.

## Deprecation Timeline

### Version 0.1.x (Current)
- **Legacy aliases**: Available, no warnings
- **Legacy fields**: Available, no warnings
- **Re-exports**: Available, no warnings

### Version 0.2.x
- **Legacy aliases**: Available with `DeprecationWarning`
- **Legacy fields**: Available with `DeprecationWarning`
- **Re-exports**: Available, no warnings

### Version 0.3.x
- **Legacy aliases**: Available with `DeprecationWarning`
- **Legacy fields**: Available with `DeprecationWarning`
- **Re-exports**: Available with `DeprecationWarning`

### Version 1.0.0 (Stable)
- **Legacy aliases**: Removed
- **Legacy fields**: Removed
- **Re-exports**: Removed

## Deprecated Features

### 1. Action Enum Aliases

**Deprecated**: `Action.QUOTE`, `Action.FLATTEN`, `Action.CANCEL_ALL`

**Replacement**: `Action.ACT`, `Action.EXIT`, `Action.CANCEL`

**Reason**: Domain-specific names (QUOTE, FLATTEN) pollute the generic contract.

**Migration**:
```python
# Old (deprecated)
proposal = Proposal(action=Action.QUOTE, ...)

# New
proposal = Proposal(action=Action.ACT, ...)
```

### 2. Proposal/FinalDecision Legacy Fields

**Deprecated**: `bid_quote`, `ask_quote`, `size_usd`, `post_only` (direct fields)

**Replacement**: Use `params` dict with generic keys

**Reason**: Trading-specific field names (`*_usd`, `bid_quote`) make the contract domain-specific.

**Migration**:
```python
# Old (deprecated)
proposal = Proposal(
    action=Action.ACT,
    bid_quote=0.49,
    ask_quote=0.51,
    size_usd=1.0,
    post_only=True,
)

# New (domain-agnostic)
proposal = Proposal(
    action=Action.ACT,
    params={
        "bid": 0.49,      # Generic key, not "bid_quote"
        "ask": 0.51,      # Generic key, not "ask_quote"
        "size": 1.0,      # Generic key, not "size_usd"
        "post_only": True,
    },
)
```

**Helper method**: Use `proposal.to_params()` to normalize legacy fields to params dict.

### 3. Re-exports from `dmc_core.schema`

**Deprecated**: Importing from `dmc_core.schema`

**Replacement**: Import directly from `decision_schema`

**Reason**: Re-exports create confusion and prevent clear dependency tracking.

**Migration**:
```python
# Old (deprecated)
from dmc_core.schema import Proposal, FinalDecision

# New
from decision_schema.types import Proposal, FinalDecision
```

## Version Compatibility

### 0.x Versions

For `0.x` versions, minor version changes may include breaking changes. Use `is_compatible()` with minor version range:

```python
from decision_schema.compat import is_compatible

# Check if schema version is compatible with 0.1.x - 0.2.x range
assert is_compatible("0.1.5", expected_major=0, min_minor=1, max_minor=2)
```

### 1.x+ Versions

For `1.x+` versions, minor and patch changes are backward compatible. Only major version changes break compatibility:

```python
# Compatible: same major version
assert is_compatible("1.2.0", expected_major=1)  # True
assert is_compatible("1.5.3", expected_major=1)  # True

# Incompatible: different major version
assert is_compatible("2.0.0", expected_major=1)  # False
```

## Best Practices

1. **Use params dict**: Always use `params` dict for domain-specific fields
2. **Use generic Action values**: Use `ACT`, `EXIT`, `CANCEL` instead of domain-specific aliases
3. **Import from decision_schema**: Import directly from `decision_schema`, not re-exports
4. **Check compatibility**: Use `is_compatible()` when integrating with schema versions
5. **Monitor warnings**: Enable `DeprecationWarning` in your test suite to catch deprecated usage

## Testing Deprecation Warnings

```python
import warnings

# Capture deprecation warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    
    # Use deprecated feature
    proposal = Proposal(action=Action.QUOTE, bid_quote=0.49, ...)
    
    # Check warning was emitted
    assert len(w) > 0
    assert issubclass(w[0].category, DeprecationWarning)
```

## Questions?

If you have questions about the deprecation plan or need help migrating, please open an issue in the `decision-schema` repository.
