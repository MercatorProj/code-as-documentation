# Documentation governance policy

> Status: draft | Owner: to be assigned | Last verified: YYYY-MM-DD

## 1. Goals and scope

- Goal: documentation accurately reflects actual code, interface contracts,
  configuration, and operational behavior, and stays no larger than it needs to be.
- In scope: `<to fill>`
- Out of scope for now: `<to fill>`

## 2. Source-of-truth precedence

1. Current implementation, migrations, executable configuration, and executed tests.
2. Designated machine-readable contracts (OpenAPI, JSON Schema, Pydantic, protobuf).
3. ADRs, for decision rationale; they never override current implementation facts.
4. Architecture pages, tutorials, README, and other explanatory documents.
5. Discussions, chat logs, and unverified design drafts.

On conflict, record the conflict and the evidence; never pick one story to hide the
difference.

## 3. Documentation tiers

| Tier | Content | Update requirement |
|---|---|---|
| L0 | README, project entry, run/deploy/recovery instructions | Must sync when usage is affected |
| L1 | Architecture, flows, module boundaries, data flow, ADRs | Sync on architecture/dependency/key-decision change |
| L2 | API, data model, config, event, permission contracts | Must sync on contract change, or regenerate |
| L3 | Tutorials, design background, examples, historical records | Judge impact; misleading facts must not survive |

## 4. Right-sizing and change rules

- Every code change starts with a documentation impact analysis before edits.
- Prefer deleting or merging a redundant page over updating a second copy in place.
- Semantic doc changes must be reviewable; mark uncertain content as needs-review,
  never guess.
- Bulk directory changes, mass moves and deletions, and historical rewrites require
  explicit confirmation first.
- Generated files carry their generator and regeneration method; never hand-edit
  generated output.
- Checks run manually by default; no CI, hooks, scheduled jobs, or external
  publishing without authorization.

## 5. Minimum verification

- Internal links and navigation targets.
- Code paths, symbols, config names, and API examples still exist and verify.
- Mermaid syntax or build check when tooling exists; note limits otherwise.
- Local site build if a site exists; never publish by default.

## 6. Exceptions and review

- Exceptions: <to fill>
- Semantic-change reviewer/process: <to fill>
- Approver for major directory changes: <to fill>
