# Changelog

## 2.2.0 - 2026-10-27

Temporary-document hygiene.

- `references/doc-cleanup.md` gains a "Temporary and working documents" section:
  agreed scratch location, dated naming, `status: draft` with owner and
  `last_reviewed`, publication boundary, and a 90-day default TTL with three
  expiry outcomes (promote / archive / delete).
- `scripts/find_cleanup_candidates.py` gains a `temp` category: backup artifacts,
  temporary/working and date-stamped names, drafts without a review date, and
  drafts whose `last_reviewed` exceeds `--max-age` (default 90 days).
- `references/site-delivery.md`: scratch and working directories are excluded from
  navigation and offline packages.
- `templates/AGENTS.md`: persistent rule for temporary-document placement and
  expiry.

## 2.1.0 - 2026-10-27

Strengthened documentation cleanup capability.

- New `references/doc-cleanup.md`: the pruning doctrine in one place - existence
  test, disposition table (keep/merge/move/archive/delete), delete-versus-archive
  boundary, lifecycle symmetry (deleted code kills its docs), and anti-patterns.
- New `scripts/find_cleanup_candidates.py` (read-only, standard library): detects
  orphan pages (Markdown links plus backtick path mentions), stub pages, dead
  source-code references, duplicate bodies, and plan-wording candidates; supports
  `--out` CSV and `--strict`.
- SKILL.md routing adds a dedicated "prune or clean up redundant docs" task;
  quality-audit and structure references now point to the shared decision tree
  instead of restating it.
- `templates/audit-report.md` cleanup table gains a code-side evidence column;
  `templates/AGENTS.md` adds the rule that deleted code takes its documentation
  with it.

## 2.0.0 - 2026-10-27

Initial release of this independent package. Its content is derived from and
credits `document-governance-skills` 1.0.0 and `documentation-governance` 1.0.1,
consolidated into a single English skill; content was deduplicated and nothing was
invented beyond the consolidation. The source packages remain independent and
are not superseded by this one.

### Added (from document-governance-skills)

- Domain depth previously locked inside sub-skills, now reachable from one routing
  table: `architecture-and-adr.md`, `contracts.md`, `release-docs.md`.
- Severity scale P0-P3 for audit findings.
- `templates/AGENTS.md` persistent repository rules, updated to reference this skill.
- `scripts/audit_docs.py` (placeholder and empty-page scan). The pack's
  `validate_skill_pack.py` became unnecessary with the single-skill layout and
  was dropped.

### Added (from documentation-governance)

- Finding classes (`mechanical` / `semantic` / `conflict` / `unknown`) and confidence
  levels in `references/code-sync-method.md`.
- `.governance/docs.yml` project configuration plus `check_governance_map.py`,
  `check_frontmatter.py`, and `inventory_docs.py` scripts.
- Migration safety gates, collision policy, and Git safety rules.
- `templates/migration-plan.md`, `templates/audit-report.md`, and an MIT `LICENSE`.

### Changed

- Right-sizing doctrine is now a core invariant: documentation is just right, not as
  detailed as possible; redundant, orphaned, and stale pages are cleanup targets.
- Link checker merged: fence-aware scanning and heading-anchor validation from the
  pack, reference-style links, `--ignore`, and directory-to-index resolution from the
  single skill.
- Eight workflows/sub-skills collapsed into one SKILL.md routing table over seven
  references; the duplicated change-impact, taxonomy, audit, and VitePress bodies
  were merged into single files.

### Removed

- The eight-skill split, `workflows/` layer, and duplicated templates, collapsed
  into one SKILL.md routing table.
- `templates/document-template.md`; frontmatter guidance now lives in
  `SKILL.md` and `references/structure-and-taxonomy.md`.
