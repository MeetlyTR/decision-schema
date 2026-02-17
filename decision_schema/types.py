"""Core types: Action enum, Proposal, FinalDecision, MismatchInfo."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Action(str, Enum):
    """
    High-level action from MDM / after DMC modulation.
    
    Generic action types that work across domains.
    
    **Deprecation plan for aliases**:
    - v0.1.x: Aliases available, no warnings
    - v0.2.x: Aliases available with DeprecationWarning
    - v1.0.0: Aliases removed (stable contract)
    """

    HOLD = "HOLD"
    ACT = "ACT"  # Generic action
    EXIT = "EXIT"  # Generic exit
    CANCEL = "CANCEL"  # Generic cancel
    STOP = "STOP"

    # LEGACY ALIASES (deprecated, will be removed in v1.0.0)
    # Use ACT, EXIT, CANCEL instead
    QUOTE = "ACT"  # Deprecated: use ACT
    FLATTEN = "EXIT"  # Deprecated: use EXIT
    CANCEL_ALL = "CANCEL"  # Deprecated: use CANCEL
    
    def __new__(cls, value: str):
        """Create enum member, emit deprecation warning for legacy aliases in v0.2+."""
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._name_ = None  # Will be set by EnumMeta
        return obj
    
    def __init__(self, value: str):
        """Emit deprecation warning for legacy aliases in v0.2+."""
        # EnumMeta sets _name_ after __new__, so check here
        if hasattr(self, "_name_") and self._name_ in ("QUOTE", "FLATTEN", "CANCEL_ALL"):
            import warnings
            # Only warn in v0.2+ (check version at runtime)
            from decision_schema.version import __version__
            version_parts = __version__.split(".")
            if len(version_parts) >= 2:
                minor = int(version_parts[1])
                if minor >= 2:
                    warnings.warn(
                        f"Action.{self._name_} is deprecated. Use Action.{self.value} instead. "
                        "Will be removed in schema v1.0.0.",
                        DeprecationWarning,
                        stacklevel=3,
                    )


@dataclass
class Proposal:
    """
    MDM output: proposed action and parameters.
    
    Generic proposal that can be used across domains (trading, operations, etc.).
    
    **Domain-agnostic design**: Use `params` dict for domain-specific fields.
    Legacy fields (`bid_quote`, `ask_quote`, `size_usd`, `post_only`) are deprecated
    and will be removed in schema v1.0.0.
    """

    action: Action
    confidence: float  # [0.0, 1.0]
    reasons: list[str] = field(default_factory=list)
    params: dict[str, Any] | None = None  # Generic parameters (domain-specific fields go here)
    run_id: str | None = None
    features_summary: dict[str, Any] = field(default_factory=dict)  # Optional feature summary
    
    # LEGACY FIELDS (deprecated, will be removed in v1.0.0)
    # Use params dict instead: params={"bid": ..., "ask": ..., "size": ..., "post_only": ...}
    bid_quote: float | None = field(default=None, metadata={"deprecated": True, "since": "0.1.0", "removed": "1.0.0"})
    ask_quote: float | None = field(default=None, metadata={"deprecated": True, "since": "0.1.0", "removed": "1.0.0"})
    size_usd: float | None = field(default=None, metadata={"deprecated": True, "since": "0.1.0", "removed": "1.0.0"})
    post_only: bool = field(default=True, metadata={"deprecated": True, "since": "0.1.0", "removed": "1.0.0"})

    def __post_init__(self) -> None:
        """Validate proposal fields."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0.0, 1.0], got {self.confidence}")
        if not self.reasons:
            self.reasons = []
        # Sync params dict with legacy fields if params is None but legacy fields are set
        if self.params is None and (self.bid_quote is not None or self.ask_quote is not None or self.size_usd is not None):
            import warnings
            warnings.warn(
                "Legacy fields (bid_quote, ask_quote, size_usd, post_only) are deprecated. "
                "Use params dict instead. Will be removed in schema v1.0.0.",
                DeprecationWarning,
                stacklevel=2,
            )
            self.params = {
                "bid": self.bid_quote,  # Use generic "bid" instead of "bid_quote"
                "ask": self.ask_quote,  # Use generic "ask" instead of "ask_quote"
                "size": self.size_usd,  # Use generic "size" instead of "size_usd"
                "post_only": self.post_only,
            }
    
    def to_params(self) -> dict[str, Any]:
        """
        Normalize proposal to params dict (domain-agnostic).
        
        Returns:
            Normalized params dict (legacy fields converted to generic keys).
        """
        if self.params is not None:
            return self.params.copy()
        # Convert legacy fields to generic params
        params: dict[str, Any] = {}
        if self.bid_quote is not None:
            params["bid"] = self.bid_quote
        if self.ask_quote is not None:
            params["ask"] = self.ask_quote
        if self.size_usd is not None:
            params["size"] = self.size_usd
        if self.post_only is not None:
            params["post_only"] = self.post_only
        return params


@dataclass
class MismatchInfo:
    """
    Guard/modulation mismatch flags and reason codes.
    
    Used when a proposal is rejected or modified by guards/modulation layer.
    """

    flags: list[str] = field(default_factory=list)
    reason_codes: list[str] = field(default_factory=list)
    throttle_refresh_ms: int | None = None  # Suggested refresh delay
    metadata: dict[str, Any] | None = None  # Additional context

    def __post_init__(self) -> None:
        """Validate mismatch info."""
        if not self.flags:
            self.flags = []
        if not self.reason_codes:
            self.reason_codes = []


@dataclass
class FinalDecision:
    """
    Post-modulation action: possibly clamped or overridden.
    
    Generic final decision after risk/modulation layer processing.
    
    **Domain-agnostic design**: Use `params` dict for domain-specific fields.
    Legacy fields (`bid_quote`, `ask_quote`, `size_usd`, `post_only`) are deprecated
    and will be removed in schema v1.0.0.
    """

    action: Action
    allowed: bool = True  # Whether action is allowed
    reasons: list[str] = field(default_factory=list)
    mismatch: MismatchInfo | None = None  # Guard failure info if any
    throttle_ms: int | None = None  # Throttle delay hint
    cooldown_ms: int | None = None  # Cooldown delay hint
    params: dict[str, Any] | None = None  # Generic parameters (domain-specific fields go here)
    
    # LEGACY FIELDS (deprecated, will be removed in v1.0.0)
    # Use params dict instead: params={"bid": ..., "ask": ..., "size": ..., "post_only": ...}
    bid_quote: float | None = field(default=None, metadata={"deprecated": True, "since": "0.1.0", "removed": "1.0.0"})
    ask_quote: float | None = field(default=None, metadata={"deprecated": True, "since": "0.1.0", "removed": "1.0.0"})
    size_usd: float | None = field(default=None, metadata={"deprecated": True, "since": "0.1.0", "removed": "1.0.0"})
    post_only: bool = field(default=True, metadata={"deprecated": True, "since": "0.1.0", "removed": "1.0.0"})

    def __post_init__(self) -> None:
        """Validate final decision."""
        if not self.reasons:
            self.reasons = []
        # Sync params dict with legacy fields if params is None but legacy fields are set
        if self.params is None and (self.bid_quote is not None or self.ask_quote is not None or self.size_usd is not None):
            import warnings
            warnings.warn(
                "Legacy fields (bid_quote, ask_quote, size_usd, post_only) are deprecated. "
                "Use params dict instead. Will be removed in schema v1.0.0.",
                DeprecationWarning,
                stacklevel=2,
            )
            self.params = {
                "bid": self.bid_quote,  # Use generic "bid" instead of "bid_quote"
                "ask": self.ask_quote,  # Use generic "ask" instead of "ask_quote"
                "size": self.size_usd,  # Use generic "size" instead of "size_usd"
                "post_only": self.post_only,
            }
    
    def to_params(self) -> dict[str, Any]:
        """
        Normalize decision to params dict (domain-agnostic).
        
        Returns:
            Normalized params dict (legacy fields converted to generic keys).
        """
        if self.params is not None:
            return self.params.copy()
        # Convert legacy fields to generic params
        params: dict[str, Any] = {}
        if self.bid_quote is not None:
            params["bid"] = self.bid_quote
        if self.ask_quote is not None:
            params["ask"] = self.ask_quote
        if self.size_usd is not None:
            params["size"] = self.size_usd
        if self.post_only is not None:
            params["post_only"] = self.post_only
        return params


# Backward compatibility aliases (for smooth transition)
TradeProposal = Proposal  # Alias for backward compatibility
FinalAction = FinalDecision  # Alias for backward compatibility


# Validation helpers
def clamp_confidence(confidence: float) -> float:
    """Clamp confidence to [0.0, 1.0]."""
    return max(0.0, min(1.0, confidence))


def ensure_non_empty_reasons(reasons: list[str] | None) -> list[str]:
    """Ensure reasons list is non-empty (return ['unknown'] if empty)."""
    if not reasons:
        return ["unknown"]
    return reasons
