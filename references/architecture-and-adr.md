# Architecture documentation and decision records

## Goal

Explain what the system consists of, where the boundaries are, how requests and data
flow, and why key decisions hold. Architecture pages describe the current
implementation; future proposals get their own clearly labeled documents.

## Evidence requirements

- Trace the real structure first: entry points, dependency manifests, routing/
  controllers, service layer, data layer, tasks/messages, configuration, tests.
- Every module boundary, arrow, external dependency, and persistence relationship
  needs code, config, or runtime evidence.
- Mark unprovable relationships as inferred/needs-review; never add arrows to make a
  diagram look complete.
- Distinguish in diagrams: current implementation, target design, historical state.

## When to update

Update architecture pages when modules are added/split/merged, core request paths,
async tasks, event flows, or data ownership change, key external systems, storage,
caches, or queues appear, security boundaries, permission checks, or transaction/
consistency policy change, or a decision with long-term impact is made. Pure local
details and cosmetic renames usually need no ADR and no architecture edit.

## Diagrams

Pick the simplest diagram that answers the question; never pad pages with diagrams:

- system context: system, actors, external systems, responsibility boundaries;
- container/runtime units: web, workers, databases, brokers as deployed blocks;
- component: key modules, interfaces, dependency direction;
- sequence: one concrete scenario with success and failure branches;
- data flow: sources, transformations, persistence, downstream consumers;
- state: state machines, transition conditions, rejection paths, side effects.

Mermaid is the default text diagram format unless the project has a standard. Keep
naming consistent with source code; do not let layout directives dominate.

## ADR practice

1. Write an ADR only when there is a non-obvious trade-off, long-term impact, or a
   need to reconstruct the decision later. Not every change deserves one.
2. Record background, constraints, candidate options, the choice, trade-offs, risks,
   consequences, and how to verify. Use `templates/adr.md`; adopt an existing repo
   ADR format instead if one exists.
3. Statuses: `proposed`, `accepted`, `deprecated`, `superseded`. A draft ADR is not
   an implemented fact; update status and link code/PR/test evidence when it lands.
4. ADRs explain why this was chosen; architecture pages explain how it works now.
   Cross-link them so an old ADR never masquerades as current state. When a decision
   is replaced, keep the history and mark the supersession; do not overwrite.

## Suggested page structure

System goals and non-goals; boundaries and external dependencies; module
responsibilities, dependencies, data ownership; key scenario flows; quality
attributes and constraints; deployment shape when relevant; known limitations and
open questions; index of related ADRs and source paths.

## Quality checks

Diagrams and prose must not contradict each other. Arrow direction and sync/async
semantics are explicit. Mark data writers, sources of truth, and transaction
boundaries. Judge error paths, retries, idempotency, and permissions only with
evidence; do not assume. Keep Mermaid renderable and run the build when tooling
exists.
