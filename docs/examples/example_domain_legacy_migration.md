# Example Domain Only: Legacy Migration (0.1 → 0.2)

**This document is for illustration only.** It shows how one might map legacy domain-specific fields to the 0.2.0 contract. The contract itself does not prescribe these keys.

## Example: Mapping legacy action aliases

```python
# Old (0.1.x) — example domain only
proposal = Proposal(action=Action.QUOTE, ...)

# New (0.2.0+)
proposal = Proposal(action=Action.ACT, ...)
```

## Example: Mapping legacy fields to params

```python
# Old (0.1.x) — example domain only
proposal = Proposal(
    action=Action.ACT,
    bid_quote=0.49,
    ask_quote=0.51,
    size_usd=1.0,
    post_only=True,
)

# New (0.2.0+) — use params with namespaced or generic keys
proposal = Proposal(
    action=Action.ACT,
    confidence=0.8,
    reasons=[],
    params={
        "example_domain:bid": 0.49,
        "example_domain:ask": 0.51,
        "example_domain:size": 1.0,
        "example_domain:post_only": True,
    },
)
```

Domain-specific keys MUST be namespaced in your adapter; the core contract does not define them.
