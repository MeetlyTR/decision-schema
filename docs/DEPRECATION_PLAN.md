<!--
Decision Ecosystem — decision-schema
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Deprecation Plan

## Schema 0.2.0 (contract cleanup)

As of **0.2.0**, the contract is domain-agnostic and no longer includes:

- **Action:** Only `HOLD`, `ACT`, `EXIT`, `CANCEL`, `STOP`. Legacy aliases `QUOTE`, `FLATTEN`, `CANCEL_ALL` have been **removed**.
- **Proposal / FinalDecision:** No legacy fields. Only `action`, `confidence`, `reasons`, `params`, etc. Legacy fields `bid_quote`, `ask_quote`, `size_usd`, `post_only` have been **removed**.
- **Aliases:** `TradeProposal` and `FinalAction` have been **removed**. Use `Proposal` and `FinalDecision` only.

## Migrating from 0.1.x to 0.2.x

- Use `Proposal(..., params={...})` for any domain-specific data; use namespaced keys (e.g. `example_domain:key`).
- Use `Action.ACT` instead of `Action.QUOTE`, `Action.EXIT` instead of `Action.FLATTEN`, `Action.CANCEL` instead of `Action.CANCEL_ALL`.
- Import from `decision_schema.types` only (no re-exports from other packages).

**Example-domain migration examples** (e.g. legacy bid/ask/quote mappings) are documented only under:

- `docs/examples/example_domain_legacy_migration.md`

Core docs and contract remain free of domain vocabulary.

## Version pinning

- For 0.2.x: `decision-schema>=0.2,<0.3`
- See `ECOSYSTEM_CONTRACT_MATRIX.md` for core compatibility.
