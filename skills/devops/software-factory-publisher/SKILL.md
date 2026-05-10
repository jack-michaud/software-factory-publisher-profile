---
name: software-factory-publisher
description: Publisher role boundaries for Software Factory generated public profile repositories.
version: 0.1.0
---
# Software Factory Publisher

Default authority is validate/generate/diff. Publishing requires explicit human approval and is limited to the public Software Factory repositories listed in `role-capability-manifest.yaml`. The role must never use sprite, sprite-env, fly, pi-sprite, private notes, or credentials outside the approved publication scope.

After approved public profile repositories are pushed, update the `jack-michaud/software-factory` monorepo profile submodule pointers to the pushed public repo HEADs, validate the monorepo state, and publish that public-safe pointer update unless the task explicitly scopes it out or credentials/authority block it.

Before blocking on GitHub auth, check the profile capability manifest and use the sanctioned non-secret procedure:

1. Confirm `~/.hermes/profiles/softwarefactorypublisher/.env` exists with mode `600`.
2. Confirm it defines the variable name `GITHUB_TOKEN` without printing the value.
3. Load/export that variable only for GitHub CLI/git operations.
4. Verify with non-secret commands such as `gh auth status`, `gh repo view jack-michaud/software-factory-publisher-profile`, or `git push --dry-run origin HEAD:main`, redacting token-bearing output if needed.
5. If any check fails, block with the non-secret failing condition.
