# Code as Documentation Skill

Version: `2.2.0`

Skill name: `code-as-documentation`. A standalone, single-entry,
English-language skill that implements a code-as-documentation policy for any
repository. It is an independent package and does not replace or require any other
skill package.

Its doctrine: implementation is the evidence, prose exists only where code
cannot speak, and the doc set is kept just right - redundant,
orphaned, and stale pages are cleaned up instead of accumulated.

## Package contents

```text
code-as-documentation/
|-- SKILL.md                    entry point: invariants, right-sizing, routing, protocol
|-- references/
|   |-- code-sync-method.md         drift detection, finding classes, confidence, where knowledge lives
|   |-- structure-and-taxonomy.md   information architecture, naming, migration safety and gates
|   |-- architecture-and-adr.md     evidence-based architecture pages and decision records
|   |-- contracts.md                API / data model / config / event contract checklists
|   |-- release-docs.md             changelogs, release notes, upgrade and compatibility guides
|   |-- quality-audit.md            audit method, severities, redundancy cleanup, auto-fix bounds
|   `-- site-delivery.md            VitePress preview, build, offline packaging
|-- scripts/                     standard-library only, read-only by default
|   |-- inventory_docs.py           CSV inventory of documentation-like files
|   |-- check_doc_links.py          local Markdown links, reference-style links, heading anchors
|   |-- audit_docs.py               empty pages, missing headings, placeholder candidates
|   |-- check_frontmatter.py        title/status frontmatter validation
|   `-- check_governance_map.py     path check for .governance/docs.yml
|-- templates/
|   |-- docs-governance.example.yml project governance config (copy to .governance/docs.yml)
|   |-- documentation-policy.md     governance policy skeleton
|   |-- documentation-map.md        doc-to-source mapping table
|   |-- migration-plan.md           path mapping, validation plan, rollback
|   |-- change-impact.md            code-change documentation impact record
|   |-- adr.md                      architecture decision record
|   |-- audit-report.md             quality audit report
|   `-- AGENTS.md                   optional persistent repo rules (review before installing)
|-- examples/
|   `-- sample-docs-map.yml         worked mapping example
|-- CHANGELOG.md
`-- LICENSE
```

## Install

Copy this directory into your agent skill discovery location (for example
`.agents/skills/` in the project, or a user-level skills directory). No build step,
no third-party dependencies; Python 3.9+ is needed only for the scripts.

Optionally review and adapt `templates/AGENTS.md` into the repository root so the
code-change-triggers-doc-analysis rule persists without depending on memory.

## Usage

Invoke the skill for a task such as:

- "inventory the current docs and find redundancy"
- "plan a documentation restructure"
- "compare docs with the changes on this branch and sync them"
- "audit the docs before release"
- "build an offline VitePress site"

The SKILL.md routing table maps each request to one reference file; read-only steps
always run before any file modification.

## Script examples

```bash
python scripts/inventory_docs.py . --out artifacts/documentation-governance/inventory.csv
python scripts/check_doc_links.py docs
python scripts/audit_docs.py . --strict
python scripts/check_frontmatter.py docs
python scripts/check_governance_map.py .governance/docs.yml
python scripts/find_cleanup_candidates.py . --out artifacts/documentation-governance/cleanup.csv
```

All scripts are read-only, use the standard library, and never modify source files.
The link checker is a best-effort static check, not a replacement for a site build.

## Design limits

This skill does not make product decisions, approve requirements, refactor business
logic, or guarantee semantic equivalence between code and prose. It provides
traceability, evidence-based drift detection, right-sizing and cleanup
recommendations, mechanical validation, and review workflows. Publishing, CI/CD,
hooks, and scheduled automation are out of scope unless explicitly requested.
