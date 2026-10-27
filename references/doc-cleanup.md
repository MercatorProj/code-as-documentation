# Documentation cleanup (pruning)

## Principle

Cleanup is a first-class governance activity, not housekeeping. Under
code-as-documentation the default stance is not "what docs should we write" but
"what entitles this document to exist". Prose earns its place only by carrying
knowledge the code cannot express: why (rationale, constraints, trade-offs),
how-to (procedures not inferable from source), composition (boundaries, data flow),
and business meaning. A page that restates code is a second copy that will drift;
its default disposition is deletion, not update.

## Existence test

Ask of every document; any unanswered question makes it a candidate:

1. Who reads it (audience)?
2. What single task does it accomplish for that reader?
3. Where is its source of truth (code, schema, migration, ADR)?
4. What change triggers a review of it?

Brutal follow-up: if this page vanished, would any reader be misled? No - delete.
Yes, but the content is wrong - it is worse than absence; fix or delete now.

## Decision procedure

1. Inventory and classify. Run the existence test across the scope. Produce a
   disposition per document: keep / merge / move / archive / delete / undecided.
2. Gather evidence per candidate:
   - doc-side: inbound links, navigation membership, placeholder/stub status,
     duplicate bodies, status/frontmatter, last substantive change in Git history;
   - code-side: does the documented feature/interface still exist? Do backtick
     source paths in the page resolve? Does `.governance/docs.yml` still map it?
   `scripts/find_cleanup_candidates.py` produces the mechanical first pass; every
   static candidate requires human review.
3. Apply the disposition table below. Deletion, archiving, and bulk consolidation
   are major actions: present the list with evidence, get approval, execute in
   bounded batches.
4. Verify after each batch: re-run link checks, confirm navigation and indexes no
   longer reference removed pages, rebuild the site when configured, and confirm
   unrelated working-tree changes are untouched.
5. Report: disposition list with outcomes, evidence kept, checks run, and anything
   left undecided.

## Disposition table

| Candidate | Default disposition | Notes |
|---|---|---|
| Second copy of a fact the code or another page already carries | delete, or reduce to a one-line summary linking the canonical page | Never update a second copy in place |
| Orphan page (no inbound link, not an entry point) | decide by existence test; usually delete or merge | Check external references before deleting |
| Empty, stub, or placeholder-only page | delete | A stub misleads readers into expecting content |
| Stale draft or superseded design written in present tense | archive with explicit status, or delete if valueless | Deprecated pages must never look like recommended practice |
| Hand-maintained generated output | delete; regenerate from the source contract | Fix the generator, never the artifact |
| Overlapping pages for the same task and audience | merge into the canonical page | The absorbed page is removed, not left as a stub |
| Documentation for deleted code or removed features | delete in the same change that deletes the code | Docs must not outlive what they describe |
| Plan or proposal described as if shipped | rewrite with explicit proposed status, or move out of the published tree | Never present-tense for unimplemented behavior |
| Externally referenced or historically valuable | archive instead of delete | Uncertain external usage always favors archive |

## Delete versus archive

Delete when the page is provably orphaned or redundant and its content exists
elsewhere (code, canonical page, history). Archive when external references might
exist, when the content records why an earlier design was replaced, or when the
project treats history as an asset. Archived pages carry status: archived, leave
the published navigation, and state what superseded them.

## Lifecycle symmetry

- Code deleted, feature removed, flag retired: its documentation dies in the same
  change - deleted, or archived if history matters.
- Behavior changed: documentation updates within the same change; impact analysis
  precedes the merge, not follows the release.
- Unimplemented work: proposed/planned wording only, never present tense.
- Generated output: regenerated from source; hand edits are drift by definition.

## Anti-patterns to hunt

- Documentation written for coverage metrics instead of reader tasks.
- Changelogs spliced mechanically from commit titles.
- Keeping a page because "we wrote it" rather than because a reader needs it.
- The same fact maintained in prose, in comments, and in a wiki simultaneously.
- Measuring documentation quality by volume.

## Temporary and working documents

Scratch material (drafts, meeting notes, personal notes, WIP summaries) is
documentation debt with a timer on it. It is allowed, but only under contract:

- Location: keep temporary documents in the repository's agreed scratch location
  (for example `docs/scratch/` or `notes/`); never scatter them through the
  published tree.
- Naming: prefix with a date and mark the working status, for example
  `2026-10-27-topic-draft.md`. A name is the cheapest status label a file can carry.
- Frontmatter: `status: draft` plus a real owner and `last_reviewed`; a draft
  without a review date is already a defect.
- Publication boundary: never link scratch pages from navigation, sidebars, or
  canonical pages except as explicitly labeled unverified drafts; exclude them
  from site builds and offline packages.
- Time to live: every draft has an expiry (default 90 days since last review).
  On expiry the disposition procedure applies with three outcomes:
  - promote: it passes the existence test, is rewritten to standard, and moves
    into the proper taxonomy section;
  - archive: it records context worth keeping; mark it archived and state why;
  - delete: nobody missed it; that is the most common and healthiest outcome.
- Mass accumulation is a smell: a scratch directory that only grows means reviews
  are not happening; schedule a sweep.

## Report format

Use the redundancy cleanup section of `templates/audit-report.md`. Each row states:
document, disposition, doc-side evidence, code-side evidence, canonical page when
merging, and approval status. Counts in the summary include only reviewed findings;
static candidates are listed separately until confirmed.
