# Role Capability Readiness Checklist

A Software Factory profile distribution is not ready for installation, update, or publication unless its role capability manifest is present and answers every item below.

## Required manifest fields

- [ ] `schema_version`
- [ ] `role`
- [ ] `profile_distribution`
- [ ] `purpose`
- [ ] `role_authority.summary`
- [ ] `role_authority.allowed_mutation_targets` with explicit scoped targets, or an explicit empty list with rationale
- [ ] `role_authority.explicitly_not_allowed`
- [ ] `credentials` with non-secret variable names/locations only
- [ ] `canonical_workspaces`
- [ ] `completion_contract.done_when`
- [ ] `completion_contract.handoff_when`
- [ ] `completion_contract.block_when`
- [ ] `readiness_smoke_tests`

## Review questions

- [ ] Does the manifest distinguish scoped authority from no authority?
- [ ] Are allowed mutation targets specific enough that the worker knows what it may mutate?
- [ ] Are credential paths and environment variable names documented without values?
- [ ] Is the canonical source repository documented?
- [ ] Is task completion different from handoff/block?
- [ ] Are smoke tests runnable without printing secrets?
- [ ] Does `SOUL.md` point to the manifest as the source of role-specific authority?
- [ ] Does `distribution.yaml` include the manifest, checklist, and validation scripts as distribution-owned files?
