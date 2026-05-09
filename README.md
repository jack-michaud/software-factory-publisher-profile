# softwarefactorypublisher profile

This is the source-controlled role distribution root for current Hermes. It is generated/maintained from the Software Factory profiles monorepo prototype and includes a role capability manifest so publisher workers know their scoped repository-publication authority and credential procedure.

Install locally for testing:

```bash
hermes profile install /path/to/software-factory-profiles/profiles/publisher --name softwarefactorypublisher-monorepo-test --yes
```

Role boundary: Validates, generates, diffs, and publishes generated public profile repos only after explicit human approval; never mutates sprites. `role-capability-manifest.yaml` is the source of truth for scoped mutation targets, credential loading, canonical repositories, and completion-vs-handoff/block criteria.

## Safe GitHub authentication

The installed runtime profile may have a profile-local credential file at `~/.hermes/profiles/softwarefactorypublisher/.env` with mode `600`. The only sanctioned variable name for publication is `GITHUB_TOKEN`.

Publisher workers may load/export `GITHUB_TOKEN` for GitHub CLI and git operations when a task explicitly approves repository publication. They must not print the variable value, must not show token-bearing remote URLs, and must redact command output if needed.

Non-secret verification commands:

```bash
scripts/github_auth_smoke_test.sh --check-env-only
scripts/github_auth_smoke_test.sh
# or, manually after loading the token without echoing it:
gh auth status
gh repo view jack-michaud/software-factory-publisher-profile
git push --dry-run origin HEAD:main
```

If the credential file is missing, `GITHUB_TOKEN` is absent/empty, file mode is not `600`, or GitHub verification fails, block with that non-secret fact instead of claiming the profile is not configured.

## Generated public repository shape

This root is current-Hermes-compatible: `distribution.yaml` is at repository root.

Install after publication:

```bash
hermes profile install https://github.com/jack-michaud/software-factory-publisher-profile.git --name softwarefactorypublisher
```

Update after publication:

```bash
hermes profile update softwarefactorypublisher --yes
```

Public/private boundary: credentials, runtime state, logs, memories, sessions, Kanban DB/workspaces, sprite credentials, SSH keys, OAuth tokens, API keys, and private Obsidian notes are not included.

## Publication provenance

Version: v0.1.0
Source of truth: https://github.com/jack-michaud/software-factory
Source tag: profiles/v0.1.0
Source commit: 63035a90746ab304b7e8c5f231d9d89c2106e9d8
Generated manifest: GENERATED_METADATA.json
License: MPL-2.0

This repository is generated. File issues and feature requests on https://github.com/jack-michaud/software-factory rather than editing this generated repository directly.
