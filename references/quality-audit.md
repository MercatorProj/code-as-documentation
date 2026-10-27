# Quality audit and redundancy cleanup

## Principle

An audit collects evidence and proposes fixes; it is never an excuse to rewrite the
site. Static checks surface candidates only - a keyword hit is not, by itself, a
proven factual error.

## Procedure

1. Fix scope and baseline; read Git state; never clobber existing changes.
2. Inventory docs against core source, schemas, config, and tests; decide what
   should have coverage.
3. Run the bundled scripts where the environment allows:
   - `python scripts/check_doc_links.py <root>`: local links, reference-style links,
     heading anchors.
   - `python scripts/audit_docs.py <root>`: empty pages, missing headings, placeholder
     candidates.
   - `python scripts/check_frontmatter.py <root>`: title/status validation.
4. Verify high-risk facts manually: install/run commands, core flows, API paths and
   fields, config defaults, permission boundaries, data models, version compatibility.
5. Check diagrams, navigation, duplicated explanations, orphan pages, expired drafts,
   and the provenance of generated docs.
6. Record per finding: file, location, evidence, impact, priority, suggested fix.
   Static results require human review.
7. Fix factual errors, key paths, and contract gaps first; formatting and polish
   last. Re-run the relevant checks after fixing and report what remains unverified.

## Redundancy cleanup

Right-sizing is part of every audit. Produce a disposition list (keep / merge /
move / archive / delete / undecided) per `references/structure-and-taxonomy.md`,
covering second copies of facts, orphans, stubs, stale drafts, and hand-maintained
generated output. Deletion and consolidation
are major actions. The disposition decision tree, the delete-versus-archive
boundary, and the evidence requirements live in `references/doc-cleanup.md`; run
`scripts/find_cleanup_candidates.py` for the mechanical first pass, then apply its
gates: propose, approve, execute in batches, and re-run link and navigation checks. A
smaller, accurate doc set beats a larger, complete-looking one.

## Severity scale

- **P0:** content could cause a high-risk security, data, or operational incident,
  or a key execution step is dangerously wrong.
- **P1:** core startup, usage, deployment, permission, or interface instructions are
  wrong; primary flows will fail.
- **P2:** clearly outdated, broken links, key topic missing, or important terminology
  contradicted.
- **P3:** layout, duplication, low-risk readability, non-critical index issues.

When a report format needs status categories instead, use `error` (requested
deliverable broken), `warning` (likely defect or maintainability risk), `review`
(semantic/authority question for a person), `info` (optional improvement).

## Auto-fix boundaries

Directly fixable when low-risk: spelling, an unambiguous dead relative link (unique
target, no file move needed), duplicate index entries, confirmed path typos.

Confirmation required: deleting pages, large-scale reorganization, changing product
semantics, rewriting history, inferring unknown API behavior, changing URLs that
external links depend on, swapping the generation toolchain.

## Report requirements

Every audit report (`templates/audit-report.md`) states: scope and baseline; finding
counts by severity (verified findings only); locatable evidence; suggested fixes and
whether each needs confirmation; checks actually executed with results; and what was
not run or verified, and why. Never phrase "no findings" as "the docs are fully
correct" - state scan scope and coverage limits instead.
