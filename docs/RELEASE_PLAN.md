<!--
Decision Ecosystem — decision-schema
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Release Plan

## Versioning Policy

### 0.x Versions

**Minor increments** (`0.1.0` → `0.2.0`):
- May include deprecations (with warnings)
- May add new types or fields
- Must maintain backward compatibility at Python API level
- Compatibility checks use minor version range (e.g., `min_minor=1, max_minor=1`)

**Patch increments** (`0.1.0` → `0.1.1`):
- Bug fixes only
- Documentation updates
- No deprecations
- No API changes

### 1.x+ Versions

**Major increments** (`0.x.0` → `1.0.0`):
- Breaking changes allowed
- Deprecated features removed (aliases, legacy fields, re-exports)
- All cores must update dependency range

**Minor/Patch increments** (`1.0.0` → `1.1.0`):
- Backward compatible (additive changes only)
- Compatibility checks use major version only

## Deprecation Enforcement Timeline

As defined in `docs/DEPRECATION_PLAN.md`:

| Version | Action Aliases | Legacy Fields | Re-exports |
|---------|----------------|---------------|------------|
| **0.1.x** | ✅ Available, no warnings | ✅ Available, no warnings | ✅ Available, no warnings |
| **0.2.x** | ⚠️ Available with warnings | ⚠️ Available with warnings | ✅ Available, no warnings |
| **0.3.x** | ⚠️ Available with warnings | ⚠️ Available with warnings | ⚠️ Available with warnings |
| **1.0.0** | ❌ Removed | ❌ Removed | ❌ Removed |

## Warnings Policy in CI

### Default Tests

- **DeprecationWarning**: Not treated as error
- Tests run normally, warnings are logged but don't fail builds
- Allows gradual migration without breaking CI

### Optional Strict Pipeline

- Enable `warnings-as-errors` for deprecation warnings:
  ```bash
  pytest -W error::DeprecationWarning
  ```
- Use in separate CI job (e.g., `ci-strict.yml`)
- Fails build if deprecated features are used
- Useful for catching migration issues early

## Release Checklist Template

### Pre-Release

- [ ] Update `decision_schema/version.py` (`__version__`)
- [ ] Update `ECOSYSTEM_CONTRACT_MATRIX.md` if minor version changes
- [ ] Review `CHANGELOG.md` (create if missing)
- [ ] Run all tests: `pytest tests/`
- [ ] Verify contract matrix still correct
- [ ] Check for secret leaks: `gitleaks detect` (if available)

### Release Notes Template

```markdown
## Version X.Y.Z

### Added
- [List new features]

### Changed
- [List changes]

### Deprecated
- [List deprecations]

### Removed
- [List removals (only in major versions)]

### Fixed
- [List bug fixes]
```

### Post-Release

- [ ] Tag release: `git tag vX.Y.Z`
- [ ] Push tag: `git push origin vX.Y.Z`
- [ ] Update dependent cores (if breaking changes)
- [ ] Monitor compatibility test failures in dependent cores

## Version Bump Examples

### Patch Release (0.1.0 → 0.1.1)

- Bug fix in `compat.py`
- No deprecations
- No API changes
- All cores remain compatible

### Minor Release (0.1.0 → 0.2.0)

- Enable deprecation warnings for aliases/legacy fields
- Update `ECOSYSTEM_CONTRACT_MATRIX.md`: `max_minor=2`
- Dependent cores update: `>=0.2,<0.3` (optional, can stay on 0.1.x)
- Compatibility checks: `expected_minor=2` (for cores that upgrade)

### Major Release (0.3.0 → 1.0.0)

- Remove deprecated aliases, legacy fields, re-exports
- Update `ECOSYSTEM_CONTRACT_MATRIX.md`: `expected_major=1`
- All dependent cores **must** update: `>=1.0,<2.0`
- Breaking change: compatibility checks use `expected_major=1`

## CI/CD Integration

### Compatibility Test

Each dependent core should run compatibility test in CI:

```yaml
- name: Check schema compatibility
  run: |
    python -c "from eval_calibration_core.contracts import check_schema_compatibility; check_schema_compatibility()"
```

### Version Matrix Test

Test against multiple schema versions (if needed):

```yaml
- name: Test compatibility
  strategy:
    matrix:
      schema_version: ["0.1.0", "0.2.0"]
  run: |
    pip install decision-schema==${{ matrix.schema_version }}
    pytest tests/test_contract_compat.py
```
