# Repository documentation rules

## Code and documentation evolve together

- Before changing code, identify which user-facing behavior, architecture, data
  model, API, configuration, or operating procedure may be affected.
- After changing code, update the affected documentation when the change alters
  documented behavior or a documented contract. If no doc change is needed, be ready
  to explain why.
- Treat implementation code, migrations, executable configuration, tests, and
  designated machine-readable contracts as evidence. Do not invent behavior to fill
  documentation gaps.
- Do not describe planned behavior as implemented. Mark unresolved facts as
  needs-review and state what evidence is missing.
- Prefer generated API/schema references when a reliable source and generator exist.
  Update the source contract, not only its generated output.
- Keep documentation just right: do not add pages that restate code, and remove or
  merge redundant pages instead of maintaining second copies.
- When code is deleted or a feature removed, delete or archive its documentation in
  the same change; docs must not outlive what they describe.
- Keep temporary documents (drafts, notes, scratch work) in the agreed scratch
  location, dated and marked as draft, never linked into published navigation, and
  promoted, archived, or deleted when they expire.

## Safe change policy

- Inspect current documentation, repository conventions, and Git status before
  editing. Preserve existing user changes.
- Keep changes scoped and reviewable. Never use a documentation task as cover for
  refactoring unrelated code.
- Do not delete or bulk-move docs, rename major directories, replace the docs
  engine, or rewrite historical records without explicit confirmation.
- Do not add CI/CD, Git hooks, scheduled jobs, external publishing, or automatic
  commits unless explicitly requested.

## Verification

- Check internal links and navigation after documentation moves or edits.
- Verify examples, identifiers, commands, API fields, and configuration keys against
  their actual sources.
- Run relevant existing tests, schema checks, and local documentation builds when
  feasible. Report what actually ran and what could not be verified.
- End each substantive change with a concise summary of code facts, docs updated,
  checks run, and open questions.

## Suggested skill

Use the repository-installed code-as-documentation skill for inventories, drift sync,
restructures, audits, contracts, ADRs, release notes, and site delivery.
