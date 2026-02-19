# Decision Ecosystem — decision-schema
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""PacketV2 dataclass and serialization for end-to-end tracing."""

from dataclasses import asdict, dataclass, field
from typing import Any

from decision_schema.version import __version__


@dataclass
class PacketV2:
    """
    Single-step packet: input -> external -> mdm -> final_action + latency + mismatch.

    Used for end-to-end tracing and audit logging.
    Schema version is included for compatibility checks.
    """

    run_id: str
    step: int
    input: dict[str, Any]
    external: dict[str, Any]
    mdm: dict[str, Any]
    final_action: dict[str, Any]
    latency_ms: int
    mismatch: dict[str, Any] | None = None
    schema_version: str = field(
        default_factory=lambda: __version__
    )  # Schema version for compatibility

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize for JSONL; no secrets (external/input must be pre-redacted).

        Returns:
            Dictionary representation suitable for JSON serialization.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PacketV2":
        """
        Deserialize from dictionary.

        Args:
            data: Dictionary representation from JSON.

        Returns:
            PacketV2 instance.
        """
        # Extract schema_version if present, otherwise use current version
        schema_version = data.pop("schema_version", __version__)
        return cls(schema_version=schema_version, **data)
