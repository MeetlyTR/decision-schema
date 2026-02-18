# Decision Ecosystem — decision-schema
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Core types: Action enum, Proposal, FinalDecision, MismatchInfo.

Contract is domain-agnostic. Domain-specific keys MUST use namespaced params
(e.g. example_domain:key). See docs/PARAMETER_INDEX.md.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Action(str, Enum):
    """
    High-level action from proposal layer / after modulation.

    Generic action types only. No domain vocabulary.
    """

    HOLD = "HOLD"
    ACT = "ACT"
    EXIT = "EXIT"
    CANCEL = "CANCEL"
    STOP = "STOP"


@dataclass
class Proposal:
    """
    Proposal layer output: proposed action and parameters.

    Domain-agnostic. Use params dict for any domain-specific data;
    keys should be namespaced (e.g. example_domain:constraint_id).
    """

    action: Action
    confidence: float  # [0.0, 1.0]
    reasons: list[str] = field(default_factory=list)
    params: dict[str, Any] | None = None
    run_id: str | None = None
    features_summary: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0.0, 1.0], got {self.confidence}")
        if not self.reasons:
            self.reasons = []

    def to_params(self) -> dict[str, Any]:
        """Return params dict (empty if None)."""
        return (self.params or {}).copy()


@dataclass
class MismatchInfo:
    """
    Guard/modulation mismatch flags and reason codes.
    """

    flags: list[str] = field(default_factory=list)
    reason_codes: list[str] = field(default_factory=list)
    throttle_refresh_ms: int | None = None
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.flags:
            self.flags = []
        if not self.reason_codes:
            self.reason_codes = []


@dataclass
class FinalDecision:
    """
    Post-modulation decision. Domain-agnostic.
    Use params dict for domain-specific fields (namespaced keys).
    """

    action: Action
    allowed: bool = True
    reasons: list[str] = field(default_factory=list)
    mismatch: MismatchInfo | None = None
    throttle_ms: int | None = None
    cooldown_ms: int | None = None
    params: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.reasons:
            self.reasons = []

    def to_params(self) -> dict[str, Any]:
        """Return params dict (empty if None)."""
        return (self.params or {}).copy()


def clamp_confidence(confidence: float) -> float:
    """Clamp confidence to [0.0, 1.0]."""
    return max(0.0, min(1.0, confidence))


def ensure_non_empty_reasons(reasons: list[str] | None) -> list[str]:
    """Ensure reasons list is non-empty."""
    if not reasons:
        return ["unknown"]
    return reasons
