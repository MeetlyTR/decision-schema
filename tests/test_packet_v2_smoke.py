# Decision Ecosystem — decision-schema
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Smoke tests for PacketV2."""

from decision_schema.packet_v2 import PacketV2
from decision_schema.version import __version__


def test_packet_v2_creation() -> None:
    """Verify PacketV2 can be instantiated."""
    packet = PacketV2(
        run_id="test-run",
        step=42,
        input={"key": "value"},
        external={"data": "test"},
        mdm={"proposal": "test"},
        final_action={"action": "ACT"},
        latency_ms=5,
    )
    assert packet.run_id == "test-run"
    assert packet.step == 42
    assert packet.latency_ms == 5
    assert packet.schema_version == __version__


def test_packet_v2_to_dict() -> None:
    """Verify PacketV2 serialization."""
    packet = PacketV2(
        run_id="test-run",
        step=1,
        input={},
        external={},
        mdm={},
        final_action={},
        latency_ms=10,
    )
    data = packet.to_dict()
    assert data["run_id"] == "test-run"
    assert data["step"] == 1
    assert data["latency_ms"] == 10
    assert data["schema_version"] == __version__


def test_packet_v2_from_dict() -> None:
    """Verify PacketV2 deserialization."""
    data = {
        "run_id": "test-run",
        "step": 1,
        "input": {},
        "external": {},
        "mdm": {},
        "final_action": {},
        "latency_ms": 10,
        "schema_version": "0.1.0",
    }
    packet = PacketV2.from_dict(data)
    assert packet.run_id == "test-run"
    assert packet.step == 1
    assert packet.schema_version == "0.1.0"


def test_packet_v2_from_dict_missing_version() -> None:
    """Verify PacketV2 uses current version if schema_version missing."""
    data = {
        "run_id": "test-run",
        "step": 1,
        "input": {},
        "external": {},
        "mdm": {},
        "final_action": {},
        "latency_ms": 10,
    }
    packet = PacketV2.from_dict(data)
    assert packet.schema_version == __version__
