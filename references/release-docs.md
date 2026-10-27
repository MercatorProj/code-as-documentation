# Release and version documentation

## Principle

Release notes record verifiable user impact. They are not a mechanical splice of
commit titles and not marketing copy. Write only what changed relative to a stated
baseline.

## Procedure

1. Establish version, audience, and the baseline version/commit. If unspecified,
   identify candidates from tags, branches, version files, and the working tree, and
   state your assumptions. Never treat the whole Git history as this release.
2. Compare scope: `git log`, `git diff`, version files, migrations, feature flags,
   interface schemas, tests, confirmed issues/PRs.
3. Classify changes: added, behavior changed, fixed, performance/observability,
   compatibility/deprecation, security, internal maintenance.
4. Explain user impact, enablement steps, limits, and required actions. Do not leak
   sensitive fix details or secrets.
5. Verify breaking changes specifically: field deletion/rename, default changes,
   database migrations, config changes, API behavior changes, minimum dependency
   bumps.
6. Update the existing CHANGELOG/release notes/upgrade guide; follow repository
   conventions. Do not create a parallel release-record system.
7. Evidence-check every command, migration step, rollback note, and compatibility
   claim. Mark unverified steps "unverified"; they are not executable instructions.
8. Check version numbers, dates, links, and the docs-site entry; report anything you
   could not confirm.

## Format

Group by reader impact: Added (capability and how to enable), Changed (existing
behavior), Fixed, Deprecated/Removed, Migration/Upgrade (prerequisites and steps),
Known issues. The project's existing format wins. Internal refactors with no user
impact stay out of user-facing notes but may go into a developer changelog.

## Compatibility and upgrade sections

- State affected version ranges, prerequisites, backup needs, data migration,
  downtime, and rollback risk.
- Never claim backward compatibility without contract checks, tests, or solid
  evidence.
- When the baseline is uncertain, mark the scope assumption explicitly.
