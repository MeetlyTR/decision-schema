"""Smoke tests for core types."""

import pytest

from decision_schema.types import Action, Proposal, FinalDecision, MismatchInfo


def test_action_enum() -> None:
    """Verify Action enum values."""
    assert Action.HOLD == "HOLD"
    assert Action.ACT == "ACT"
    assert Action.EXIT == "EXIT"
    assert Action.CANCEL == "CANCEL"
    assert Action.STOP == "STOP"


def test_action_backward_compat() -> None:
    """Verify backward compatibility aliases."""
    assert Action.QUOTE == Action.ACT
    assert Action.FLATTEN == Action.EXIT
    assert Action.CANCEL_ALL == Action.CANCEL


def test_proposal_creation() -> None:
    """Verify Proposal can be instantiated."""
    proposal = Proposal(
        action=Action.ACT,
        confidence=0.8,
        reasons=["test"],
        params={"value": 100},
    )
    assert proposal.action == Action.ACT
    assert proposal.confidence == 0.8
    assert proposal.reasons == ["test"]
    assert proposal.params == {"value": 100}


def test_proposal_confidence_validation() -> None:
    """Verify Proposal validates confidence range."""
    with pytest.raises(ValueError):
        Proposal(action=Action.ACT, confidence=1.5)
    
    with pytest.raises(ValueError):
        Proposal(action=Action.ACT, confidence=-0.1)


def test_proposal_empty_reasons() -> None:
    """Verify Proposal handles empty reasons."""
    proposal = Proposal(action=Action.HOLD, confidence=0.5)
    assert proposal.reasons == []  # Empty list is valid


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
    assert decision.reasons == ["approved"]
    assert decision.mismatch == mismatch


def test_mismatch_info_creation() -> None:
    """Verify MismatchInfo can be instantiated."""
    mismatch = MismatchInfo(
        flags=["flag1", "flag2"],
        reason_codes=["code1"],
        throttle_refresh_ms=1000,
    )
    assert mismatch.flags == ["flag1", "flag2"]
    assert mismatch.reason_codes == ["code1"]
    assert mismatch.throttle_refresh_ms == 1000


def test_backward_compat_aliases() -> None:
    """Verify backward compatibility aliases work."""
    from decision_schema.types import TradeProposal, FinalAction
    
    # TradeProposal should be Proposal
    assert TradeProposal is Proposal
    
    # FinalAction should be FinalDecision
    assert FinalAction is FinalDecision
