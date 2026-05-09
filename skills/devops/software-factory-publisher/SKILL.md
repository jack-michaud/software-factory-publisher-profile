---
name: software-factory-publisher
description: Publisher role boundaries for Software Factory generated public profile repositories.
version: 0.1.0
---
# Software Factory Publisher

Default authority is validate/generate/diff. Publishing requires explicit human approval and is limited to the public Software Factory profile repositories listed in `role-capability-manifest.yaml`. The role must never use sprite, sprite-env, fly, pi-sprite, private notes, or credentials outside the approved publication scope.

Before blocking on GitHub auth, check the profile capability manifest and use the sanctioned non-secret procedure:

1. Confirm `~/.hermes/profiles/softwarefactorypublisher/.env` exists with mode `600`.
2. Confirm it defines the variable name `GITHUB_TOKEN` without printing the value.
3. Load/export that variable only for GitHub CLI/git operations.
4. Verify with non-secret commands such as `gh auth status`, `gh repo view jack-michaud/software-factory-publisher-profile`, or `git push --dry-run origin HEAD:main`, redacting token-bearing output if needed.
5. If any check fails, block with the non-secret failing condition.
