# softwarefactorypublisher profile

This is a local-installable role distribution root for current Hermes. It is generated/maintained from the Software Factory profiles monorepo prototype.

Install locally for testing:

```bash
hermes profile install /path/to/software-factory-profiles/profiles/publisher --name softwarefactorypublisher-monorepo-test --yes
```

Role boundary: Validates, generates, diffs, and publishes generated public profile repos only after explicit human approval; never mutates sprites.

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
