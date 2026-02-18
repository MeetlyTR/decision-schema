<!--
Decision Ecosystem — decision-schema
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Security Policy

## Public Repository Security

This repository is intended for public release. **No secrets, keys, or sensitive data should be committed.**

### What to Never Commit

- API keys, private keys, secrets
- Environment files (`.env`, `.env.local`, `.env.*`)
- Credentials files (`*.secrets*`, `secrets*.yaml`)
- Run artifacts (`runs/`, `traces/`, `*.log`)

### Git History

**⚠️ WARNING**: If this repository's git history contains secrets or sensitive data, do NOT rewrite history automatically. Instead:

1. Add this warning section (done)
2. Rotate any exposed credentials immediately
3. Consider using `git filter-branch` or BFG Repo-Cleaner only after careful review
4. Document any known exposures in this file

### .gitignore

The `.gitignore` file includes:
- `.env*`, `*.local`, `*.secrets*`
- `runs/`, `traces/`, `*.log`
- `*.egg-info/`, `__pycache__/`, `.pytest_cache/`

### Secret Scanning

**Pre-push checks** (recommended):

- Use [gitleaks](https://github.com/gitleaks/gitleaks) or [trufflehog](https://github.com/trufflesecurity/trufflehog) to scan commits before pushing
- Example: `gitleaks detect --source . --verbose`
- Add to pre-commit hook or CI pipeline

**GitHub Security Settings**:

- Enable [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning) (automatically scans for secrets in code)
- Enable [Dependabot](https://docs.github.com/en/code-security/dependabot) for dependency vulnerability alerts
- Review security alerts regularly

### Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public issue
2. Contact the maintainers privately
3. Provide details about the vulnerability
4. Allow time for a fix before public disclosure
