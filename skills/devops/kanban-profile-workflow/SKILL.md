---
name: kanban-profile-workflow
description: Public multi-profile Kanban workflow conventions.
version: 0.1.0
---
# Kanban Profile Workflow

Use Kanban for durable cross-profile work. Keep PM, builder, orchestrator, reviewer, and publisher responsibilities separate. Generated public artifacts must be independently validated before publication.

## Concrete Dependencies Instead of Stranded Blocking

When a publisher/release profile is waiting on concrete Kanban work, do not leave the waiting task in `blocked` as the normal state. Create or identify the remediation, reviewer, approval, install/update, docs, or other unblocker task; link that task as a parent dependency of the waiting publisher/release task; then return the publisher task to todo/ready so the board can re-dispatch it automatically when all parents are GREEN/done.

Use `blocked` only for external/manual blockers where no concrete Kanban task exists yet, such as missing credentials, unknown authority, unavailable repo/distribution, or human approval that has not yet been captured as a task. If an external/manual blocker can be represented as an unblocker Kanban task, create or link that task instead of stranding downstream work.

This preserves Software Factory role boundaries: PM/orchestrator routes durable work, builders edit source, reviewers gate, publishers publish authorized public artifacts, installer/profile-mutation tasks perform installs or runtime profile updates, and docs tasks produce release notes/documentation.
