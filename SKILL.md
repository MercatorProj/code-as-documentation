---
name: code-as-documentation
description: >
  Govern project documentation as an engineering asset under a code-as-documentation
  policy: inventory and right-size docs, clean up redundant, orphaned, and stale pages,
  map every document to its authoritative code/spec source, detect and resolve drift
  with confidence-graded findings, record architecture decisions and interface
  contracts, validate links and metadata with local scripts, deliver a local VitePress
  site with offline packaging, and prepare release notes. Use when a user asks to
  organize, audit, synchronize, migrate, prune, document, or package project
  documentation. Do not use as a substitute for product decisions,
  business-domain approval, or code refactoring.
metadata:
  version: 2.2.0
  license: MIT
  topics: [documentation, governance, code-as-documentation, vitepress]
---

# Code as Documentation

## Mission

Maintain a documentation system that is discoverable, verifiable, and no larger than
the project needs. Implementation code, migrations, executable configuration, schemas,
and tests are the evidence of behavior; prose exists only where code cannot speak:
why decisions were made, how to run and operate the system, and contracts readers
cannot infer by reading source. Markdown and Git are the default source of record;
VitePress is a presentation layer, never the authoritative store.

## Core invariants

1. Inspect before editing. Identify the repository root, project guidance
   (`AGENTS.md`, `CONTRIBUTING.md`), existing docs conventions, package scripts,
   VitePress configuration, and Git working-tree state. Do not assume tools are
   installed or that a clean-looking directory has no untracked changes.
2. Code is evidence, docs follow. Runtime behavior and tests prove what the system
   does; they do not prove what it should do. A conflict between requirements and
   implementation is reported, never silently adjudicated.
3. Authority is explicit per information type. See the authority model below. When
   two candidate authorities disagree, record both with evidence and ask.
4. Right-size every page. Documentation must be just right, not as detailed as
   possible. See the right-sizing doctrine.
5. One fact, one home. Duplicated prose is drift waiting to happen. Summarize and
   link to the canonical page instead of copying it.
6. Preserve user work. Distinguish pre-existing working-tree changes from changes
   made by this task. Never reset, clean, overwrite, or discard unrelated changes.
7. Plan before migration. Show current path to proposed path, reason, affected
   references, risks, and rollback before bulk moves, renames, deletions, or
   replacement of existing site configuration.
8. Separate facts from inference. Mark unverified claims `needs-review` and name
   the missing evidence. Never describe planned behavior as implemented.
9. Validate after changes, report honestly. Distinguish `passed`, `failed`,
   `not run`, and `not applicable`. "No findings" is not "fully correct".
10. Manual and local by default. No Git hooks, CI/CD, scheduled jobs, uploads, or
    external publication unless separately requested. Build is not publish; offline
    packaging is not deployment.
11. The skill must work without VitePress. Inventory, mapping, drift analysis,
    pruning, and validation run independently of any site.

## Right-sizing doctrine

Ask of every existing or proposed page:

- Does it carry knowledge the code cannot (rationale, constraints, procedure,
  composition, business meaning)? If not, it is a redundancy candidate.
- Does it duplicate a fact kept elsewhere? Reduce to a short summary plus a link to
  the canonical page, or delete it.
- Does it serve one primary task for one audience? Split an oversized grab-bag page;
  merge a fragment that has no independent reason to exist.
- Does it have a purpose, audience, authority, and review trigger? If none can be
  named, propose archiving or deletion.

Redundancy candidates to hunt during any audit or sync: second copies of API/config
facts, orphan pages unreachable from navigation, stale drafts presented as current,
empty or placeholder-only files, generated output maintained by hand, and superseded
designs that still read as present tense. Deletion, consolidation, and bulk cleanup
follow the decision procedure in `references/doc-cleanup.md`: propose the list
with evidence, get confirmation, then execute in bounded batches and verify links.

## Authority model

- **Canonical source:** the single source of truth for a claim or artifact (code,
  schema, migration, ADR, or a designated contract such as OpenAPI).
- **Derived content:** generated from a canonical source; always name the generator
  and the regeneration command. Fix the source, not the output.
- **Supporting explanation:** human-maintained rationale, procedures, tutorials.
- **Status:** `draft`, `active`, `needs-review`, `deprecated`, `archived`.
- **Owner and review trigger:** record only when real; never invent an owner.

Precedence when sources disagree: (1) implementation, migrations, executable config,
tests; (2) designated machine-readable contracts; (3) ADRs for why; (4) guides and
diagrams; (5) discussions and unverified drafts. Record the conflict; do not sync one
side into the other on your own authority.

Introduce frontmatter and status labels for new or actively maintained documents
first; migrate legacy documents incrementally.

## Action classes

- **Read-only:** inventory, audit, link scan, drift analysis, migration planning.
  Proceed freely; change nothing.
- **Low-risk and reversible:** add a missing index entry, fix an unambiguous broken
  local link, write a report to an agreed location. Allowed when the request clearly
  asks for fixes.
- **Major:** bulk moves/renames, deletion or consolidation of documents, authority or
  policy changes, navigation restructuring, replacing site config, installing
  dependencies, changing manifests, packaging for an unclear audience. Present a
  concise plan and wait for approval.

## Task routing

Read the referenced file in `references/` before executing. Choose the narrowest
task that satisfies the request.

| Request | Reference |
|---|---|
| Establish or upgrade governance, first adoption | this file + `templates/documentation-policy.md` |
| Inventory what exists | `scripts/inventory_docs.py` + read-only protocol below |
| Restructure, migrate, prune, or reorganize docs | `references/structure-and-taxonomy.md` |
| Compare docs with code changes; sync after a change | `references/code-sync-method.md` |
| Architecture pages, diagrams, ADRs | `references/architecture-and-adr.md` |
| API, data model, config, event contracts | `references/contracts.md` |
| Quality audit, drift sweep | `references/quality-audit.md` |
| Prune or clean up redundant docs | `references/doc-cleanup.md` |
| Changelog, release notes, upgrade guide | `references/release-docs.md` |
| VitePress setup, preview, build, offline delivery | `references/site-delivery.md` |

## Execution protocol

### A. Establish context

Inspect the repository per invariant 1. Read `.governance/docs.yml` if present. Note
existing docs conventions and reuse them where workable; do not build a parallel
system when the project already has one.

### B. Classify and plan

Assign the request to an action class. For read-only work, produce evidence and
recommendations. For low-risk work, edit directly. For major work, produce a plan
(migration map, cleanup list, or contract change summary) and ask.

### C. Apply and verify

Execute in bounded batches, checking the diff each batch. Record path changes in a
migration map. Run the relevant scripts and any project build; state plainly what
could not run and why. Summarize changed files, checks run and their real results,
unresolved decisions, and next actions.

## Project configuration

When useful, create `.governance/docs.yml` from `templates/docs-governance.example.yml`.
It is project-specific configuration, not a mandatory schema. It records doc roots,
exclusions, site settings, automation mode (always `manual` by default), and the
source-to-document mappings used by `scripts/check_governance_map.py` and the sync
method. Keep generated inventories and reports out of the canonical docs tree; never
let generated output become an authority without an explicit rule.

## Tooling rules

- Scripts are standard-library only, read-only by default, return non-zero on
  validation failures, and print what they checked.
- Report outputs go to a user-approved location; suggest `artifacts/documentation-governance/`
  only after confirming it does not clash with project conventions.
- Use local links and local assets in offline deliverables; declare any remote
  dependency instead of hiding it.
- Do not claim PDF export, single-file bundling, or full portability unless tested,
  with limitations stated.

## Definition of done

The task is complete only when the response reports: what changed (or that it was
read-only); key files and decisions; validation actually performed and results;
unresolved conflicts, risks, and checks not run; and how to preview, build, or
package locally when relevant.
