# Code and documentation synchronization method

## Principle

Detect and explain drift; do not equate "code differs from docs" with "docs are
wrong". Determine the authority for each claim before proposing a change. "Code as
documentation" does not mean more comments: it means the implementation is the
verifiable fact and necessary explanation follows the change. Read the code and the
change evidence before editing anything; never infer unverified behavior from file
names, variable names, or plausibility.

## Where knowledge lives

- Near the code: docstrings and comments for stable contracts, invariants, why and
  constraints, and failure conditions. Not line-by-line narration of obvious code.
- Guides: how a user or operator completes a task.
- Architecture pages: how the system is composed, boundaries, data flow.
- Schemas and reference pages: field and interface contracts, ideally generated.
- When a change invalidates a comment, update it; when the implementation is
  self-explanatory and the doc adds no independent value, remove the doc instead of
  maintaining a second copy.

## Inputs

- User-stated change, `git status`, `git diff`, a baseline commit, or named files.
- Relevant source, schemas, tests, configs, and current docs.
- Source-to-document mappings from `.governance/docs.yml`.
- Requirement, issue, or decision identifiers where present.

## Procedure

1. Establish the change boundary. Separate this change from pre-existing working-tree
   edits, generated files, and unrelated files. Record per change: path, symbol or
   interface, behavior delta, evidence, tests.
2. Extract concrete facts: API signatures, schema fields, config keys, commands,
   routes, module boundaries, behavior evidenced by tests.
3. Match changes to docs via explicit mappings first, then links, symbol references,
   filenames, and semantic search.
4. Build an impact table: source change, affected claim/doc, evidence, finding class,
   confidence, proposed action.
5. Classify each finding:
   - `mechanical`: path, name, field, signature, command, or generated reference
     checkable deterministically.
   - `semantic`: meaning, workflow, intent, acceptance criteria, or architectural
     rationale; review required.
   - `conflict`: authoritative sources disagree; a decision is required.
   - `unknown`: insufficient evidence; investigate or ask.
6. Confidence: high for exact symbol/schema/command mismatch against a direct source;
   medium when linkage exists but interpretation is required; low for name- or
   similarity-based inference. Never auto-fix medium/low-confidence semantic findings.
7. Propose minimal edits. Apply authorized mechanical fixes; present semantic edits
   as diffs for review. Never alter business code to make docs look consistent unless
   separately requested.
8. Re-search edited symbols, config names, field names, and old terms for missed
   references. Re-run link checks, schema/example validation, and the local site
   build when available. State plainly what could not run.
9. Report using `templates/change-impact.md`: code facts, affected docs (changed /
   no change needed / pending confirmation), verification and results, remaining
   differences.

## Common traps

- A code implementation may be a bug, not a new requirement.
- Tests describe current expected behavior but may themselves be wrong or stale.
- A schema defines types without explaining business meaning.
- Generated API docs can be structurally correct yet omit usage caveats.
- No detected drift is not proof of semantic consistency.

If the change is not yet implemented, document it as planned/proposed, never as an
existing capability.
