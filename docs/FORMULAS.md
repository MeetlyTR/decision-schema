<!--
Decision Ecosystem — decision-schema
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Decision Schema Formulas

## Version Compatibility

### SemVer Compatibility Check

For **0.x versions**, compatibility requires major match AND minor within range:

```
is_compatible(schema_version, expected_major, min_minor, max_minor)
```

**Formula**:
- Parse `schema_version` → `(major, minor, patch)`
- If `major != expected_major` → incompatible
- If `major == 0` and `minor < min_minor` → incompatible
- If `major == 0` and `minor > max_minor` → incompatible
- Otherwise → compatible

**Example**:
- `is_compatible("0.1.0", 0, min_minor=1, max_minor=1)` → `True`
- `is_compatible("0.2.0", 0, min_minor=1, max_minor=1)` → `False`
- `is_compatible("1.0.0", 0, min_minor=1, max_minor=1)` → `False`

For **1.x+ versions**, only major version matters (minor/patch are backward compatible).

## Type Validation

### Proposal Confidence Clamp

```
confidence ∈ [0.0, 1.0]
```

If `confidence < 0.0` or `confidence > 1.0` → raise `ValueError`.

### Action Enum Values

Valid actions (schema 0.2.0+):
- `HOLD`: No action
- `ACT`: Generic action
- `EXIT`: Generic exit
- `CANCEL`: Generic cancel
- `STOP`: Emergency stop

## Packet Versioning

### Packet Format vs Schema Contract

Two independent version fields:
- `packet_version`: Packet format version (e.g., "2")
- `schema_version`: Schema contract version (e.g., "0.1.0")

These can evolve independently:
- Packet format changes → bump `packet_version`
- Schema contract changes → bump `schema_version`

## Deprecation Timeline

### Version-Based Warnings

- **v0.1.x**: No warnings (aliases/legacy fields available)
- **v0.2.x**: `DeprecationWarning` for aliases and legacy fields
- **v0.3.x**: `DeprecationWarning` for re-exports
- **v1.0.0**: Aliases, legacy fields, and re-exports removed

### Warning Formula

```python
if minor_version >= 2:
    emit DeprecationWarning for aliases/legacy_fields
if minor_version >= 3:
    emit DeprecationWarning for re_exports
```
