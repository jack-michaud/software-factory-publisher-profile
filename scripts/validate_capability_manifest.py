#!/usr/bin/env python3
"""Validate Software Factory role capability manifests without printing secrets."""
from __future__ import annotations

import json
import pathlib
import sys

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(json.dumps({"passed": False, "error": f"PyYAML unavailable: {exc}"}, indent=2))
    sys.exit(2)

REQUIRED_TOP = [
    "schema_version",
    "role",
    "profile_distribution",
    "purpose",
    "role_authority",
    "credentials",
    "canonical_workspaces",
    "completion_contract",
    "readiness_smoke_tests",
]
REQUIRED_AUTHORITY = ["summary", "allowed_mutation_targets", "explicitly_not_allowed"]
REQUIRED_CONTRACT = ["done_when", "handoff_when", "block_when"]
FORBIDDEN_SECRET_KEYS = {"token", "secret", "password", "api_key", "private_key"}


def load_yaml(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def has_forbidden_secret_value(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key).lower()
            if key_text in FORBIDDEN_SECRET_KEYS and nested not in (None, "", [], {}):
                return True, f"secret-like key {key!r} has a value"
            bad, reason = has_forbidden_secret_value(nested)
            if bad:
                return True, reason
    elif isinstance(value, list):
        for nested in value:
            bad, reason = has_forbidden_secret_value(nested)
            if bad:
                return True, reason
    elif isinstance(value, str):
        compact = value.strip()
        if compact.startswith(("ghp_", "github_pat_", "sk-", "-----BEGIN")):
            return True, "credential-looking literal value present"
    return False, ""


def validate(root: pathlib.Path):
    manifest_path = root / "role-capability-manifest.yaml"
    findings = []
    if not manifest_path.exists():
        return {"passed": False, "findings": ["missing role-capability-manifest.yaml"]}
    data = load_yaml(manifest_path)
    if not isinstance(data, dict):
        return {"passed": False, "findings": ["manifest is not a mapping"]}

    for field in REQUIRED_TOP:
        if field not in data or data[field] in (None, "", [], {}):
            findings.append(f"missing/empty top-level field: {field}")

    authority = data.get("role_authority") or {}
    if not isinstance(authority, dict):
        findings.append("role_authority must be a mapping")
    else:
        for field in REQUIRED_AUTHORITY:
            if field not in authority or authority[field] in (None, "", [], {}):
                findings.append(f"missing/empty role_authority field: {field}")

    contract = data.get("completion_contract") or {}
    if not isinstance(contract, dict):
        findings.append("completion_contract must be a mapping")
    else:
        for field in REQUIRED_CONTRACT:
            if field not in contract or contract[field] in (None, "", [], {}):
                findings.append(f"missing/empty completion_contract field: {field}")

    tests = data.get("readiness_smoke_tests") or []
    if not isinstance(tests, list) or not all(isinstance(t, str) and t.strip() for t in tests):
        findings.append("readiness_smoke_tests must be a non-empty list of commands")

    bad, reason = has_forbidden_secret_value(data)
    if bad:
        findings.append(reason)

    soul = root / "SOUL.md"
    if not soul.exists() or "role-capability-manifest.yaml" not in soul.read_text(encoding="utf-8"):
        findings.append("SOUL.md must reference role-capability-manifest.yaml")

    checklist = root / "templates" / "role-capability-readiness-checklist.md"
    if not checklist.exists():
        findings.append("missing templates/role-capability-readiness-checklist.md")

    return {
        "passed": not findings,
        "manifest": str(manifest_path),
        "role": data.get("role"),
        "findings": findings,
    }


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    result = validate(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    sys.exit(0 if result.get("passed") else 1)


if __name__ == "__main__":
    main()
