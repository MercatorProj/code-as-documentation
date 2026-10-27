# Structure, taxonomy, and migration safety

## Goals

Make documentation findable by task without imposing unnecessary structure. Readers
should reach the right document by task; maintainers should know where the
authoritative page for a topic lives. Structure serves readers, not tidiness.

## Suggested information architecture

```text
docs/
|-- index.md            landing page: what is this, where to start, what next
|-- getting-started/    install, quick start, dev environment
|-- guides/             task-oriented how-tos
|-- concepts/           domain concepts, terminology, business rules
|-- architecture/       boundaries, modules, data flows, deployment shape
|-- reference/          API, configuration, data model, commands
|-- decisions/          ADRs and key technical decisions
|-- operations/         run, troubleshoot, back up, recover
`-- releases/           version notes, migration, compatibility
```

This is a starting point, not a mandate. A small library may need only `index.md`
plus a few topic files. Respect the existing structure; compare migration benefit
against link breakage before changing anything. Keep storage (where files live),
knowledge model (how concepts relate), and navigation (how readers reach content)
distinct: one canonical file, many inbound links.

## Classification rules

Classify by primary purpose, not filename: product/requirements, architecture/design,
API/contracts, development, operations, decision records, project management records,
scratch (never published by default).

## File rules

- One page, one primary task or topic. Avoid a single oversized README grab-bag.
- Stable, readable, searchable names (kebab-case or repo convention). Never rename
  wholesale for style alone; avoid meaningless names like `final-v2.md`.
- Every new file must be discoverable from an index, navigation, or contextual link.
- A page must be nameable in one sentence: purpose, audience, authority. If it
  cannot, it is a merge/archive candidate.

## Redundancy and right-sizing sweep

During restructure or audit, produce a per-document disposition: keep, merge, move,
archive, delete, or undecided. Flag as candidates:

- second copies of facts whose canonical home is code, a schema, or another page;
- orphan pages unreachable from any index;
- empty, stub, or placeholder-only files;
- stale drafts and superseded designs still written in present tense;
- generated output maintained by hand;
- overlapping pages covering the same task for the same audience.

For duplicates: keep the canonical page, reduce the other to a short summary linking
to it, or delete with approval. The full disposition decision tree and the
delete-versus-archive boundary are in `references/doc-cleanup.md`. Never let a
deprecated page look like recommended practice.

## Risk classes

- Low: add a document or index without overwriting; fix an unambiguous broken local
  link; write a report to a confirmed path.
- Medium: change navigation or metadata across several files; rename a few files
  with fully understood references; additive site config changes. Confirm when intent
  is unclear or reversal is hard.
- High (approval required): bulk move/rename; delete, overwrite, consolidate, or
  replace documents; adjudicate conflicting requirements; replace site config,
  manifests, lockfiles, or build scripts; add dependencies; package for an audience
  with unclear access scope.

## Required migration plan

1. Inventory source paths and types.
2. Propose old-path-to-new-path mappings with reasons; every existing document is
   marked keep / merge / move / archive / delete / undecided.
3. Identify inbound and outbound links, images, code examples, Mermaid references,
   sidebar/nav entries, frontmatter, and external bookmarks at risk.
4. Identify collisions and files whose purpose or authority is uncertain.
5. State the rollback approach; prefer Git diff and a dedicated commit/branch over
   ad-hoc destructive operations.
6. Get approval, then move in bounded batches, updating references with exact-target
   resolution.
7. Re-run link, asset, metadata, navigation, and build checks; report unresolved
   references and exact affected paths.

## Collision policy

Never silently overwrite. If a destination exists, compare content and references;
recommend merge, keep-both, replace, or archive, and ask for the decision.

## Git safety

- Inspect `git status --short` before editing when Git is available.
- Preserve unrelated staged and unstaged changes; never run reset/clean/cleanup.
- Do not create commits unless requested.
- Record old path, new path, action, reason, references updated, and validation
  result in the migration map (`templates/migration-plan.md`).
