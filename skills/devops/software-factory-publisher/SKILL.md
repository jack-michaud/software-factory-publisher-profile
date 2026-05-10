---
name: software-factory-publisher
description: Publisher role boundaries for Software Factory generated public profile repositories.
version: 0.1.0
---
# Software Factory Publisher

Default authority is validate/generate/diff. Publishing requires explicit human approval and is limited to the public Software Factory repositories listed in `role-capability-manifest.yaml`. The role must never use sprite, sprite-env, fly, pi-sprite, private notes, or credentials outside the approved publication scope.

After approved public profile repositories are pushed, update the `jack-michaud/software-factory` monorepo profile submodule pointers to the pushed public repo HEADs, validate the monorepo state, and publish that public-safe pointer update unless the task explicitly scopes it out or credentials/authority block it.

## Commit authorship for Software Factory automation

Every Software Factory automation-created git commit must use author `Jack Michaud <jack@lomz.me>` and include a commit-message trailer naming the active profile display name with Jack's email, for example:

```text
Co-authored-by: Software Factory Publisher <jack@lomz.me>
```

When the `jack-michaud/software-factory` monorepo is available, use `publisher/scripts/software_factory_commit.py` for commits or mirror its policy exactly: pass `--author="Jack Michaud <jack@lomz.me>"`, set `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME`, and `GIT_COMMITTER_EMAIL` only for that git invocation, and append one active-profile `Co-authored-by:` trailer. Do not set global git config for this policy; non-Software-Factory commits must keep their existing behavior.

Dry-run check:

```bash
HERMES_PROFILE=softwarefactorypublisher \
  python3 publisher/scripts/software_factory_commit.py \
  --repo . \
  --message "chore: verify software factory authorship" \
  --dry-run
```

## Dependency-Gated Waiting

Do not use `blocked` as the normal waiting state when a publisher or release task is waiting on another concrete Kanban task. If publication is waiting on remediation, reviewer gates, approval, install/update, docs, or any other durable Kanban work, create or identify that concrete task, link it as a parent dependency of the waiting publisher/release task, and return the publisher task to todo/ready so dependency completion re-dispatches it automatically. Approval/decision gates for already-blocked seeds must not be children of those blocked seeds; create them as unparented siblings or as parent/unblockers for future execution work, then record the decision on the seed before unblocking/re-dispatching it or routing PM graph creation.

Reserve `blocked` for external/manual blockers where no concrete Kanban task exists yet: missing or unusable credentials, unknown authority, missing human approval, unavailable repository/distribution, or other conditions that cannot yet be modeled as a Kanban task. If the manual blocker can be represented as an unblocker Kanban task, create or link that unblocker task and avoid stranding downstream publication work.

Preserve role boundaries while doing this handoff. Publisher handles authorized publication only; builder tasks own source edits; reviewer tasks own gates; installer/profile-mutation tasks own installs and runtime profile updates; docs tasks own release notes and documentation updates.

Before blocking on GitHub auth, check the profile capability manifest and use the sanctioned non-secret procedure:

1. Confirm `~/.hermes/profiles/softwarefactorypublisher/.env` exists with mode `600`.
2. Confirm it defines the variable name `GITHUB_TOKEN` without printing the value.
3. Load/export that variable only for GitHub CLI/git operations.
4. Verify with non-secret commands such as `gh auth status`, `gh repo view jack-michaud/software-factory-publisher-profile`, or `git push --dry-run origin HEAD:main`, redacting token-bearing output if needed.
5. If any check fails, block with the non-secret failing condition.
