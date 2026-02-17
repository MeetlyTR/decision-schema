"""Smoke tests for core types (schema 0.2.0+)."""

import pytest

from decision_schema.types import Action, Proposal, FinalDecision, MismatchInfo


def test_action_enum() -> None:
    """Verify Action enum values (domain-agnostic only)."""
    assert Action.HOLD == "HOLD"
    assert Action.ACT == "ACT"
    assert Action.EXIT == "EXIT"
    assert Action.CANCEL == "CANCEL"
    assert Action.STOP == "STOP"


def test_proposal_creation() -> None:
    """Verify Proposal can be instantiated."""
    proposal = Proposal(
        action=Action.ACT,
        confidence=0.8,
        reasons=["anomaly_signal"],
        params={"example_domain:constraint_id": "C-17"},
    )
    assert proposal.action == Action.ACT
    assert proposal.confidence == 0.8
    assert proposal.reasons == ["anomaly_signal"]
    assert proposal.params == {"example_domain:constraint_id": "C-17"}


def test_proposal_confidence_validation() -> None:
    """Verify Proposal validates confidence range."""
    with pytest.raises(ValueError):
        Proposal(action=Action.ACT, confidence=1.5)
    with pytest.raises(ValueError):
        Proposal(action=Action.ACT, confidence=-0.1)


def test_proposal_to_params() -> None:
    """Verify to_params returns copy of params."""
    proposal = Proposal(action=Action.ACT, confidence=0.5, params={"a": 1})
    p = proposal.to_params()
    assert p == {"a": 1}
    p["a"] = 2
    assert proposal.params == {"a": 1}


def test_final_decision_creation() -> None:
    """Verify FinalDecision can be instantiated."""
    mismatch = MismatchInfo(flags=["test"], reason_codes=["code"])
    decision = FinalDecision(
        action=Action.ACT,
        allowed=True,
        reasons=["approved"],
        mismatch=mismatch,
    )
    assert decision.action == Action.ACT
    assert decision.allowed is True
    assert decision.mismatch == mismatch


def test_mismatch_info_creation() -> None:
    """Verify MismatchInfo can be instantiated."""
    mismatch = MismatchInfo(
        flags=["flag1"],
        reason_codes=["code1"],
        throttle_refresh_ms=1000,
    )
    assert mismatch.flags == ["flag1"]
    assert mismatch.reason_codes == ["code1"]
    assert mismatch.throttle_refresh_ms == 1000
