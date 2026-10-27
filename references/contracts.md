# Interface, data model, and configuration contracts

## Purpose

Stop the "one copy in docs, one in code, one at runtime" drift. Put structured
contracts where they can be validated or generated; write explanatory content in
human-readable pages. Never hand-maintain generated output.

## Identify the authoritative source first

Judge per project; never force a tool:

- HTTP API: routes/controllers, request/response DTOs, OpenAPI, serialization and
  validation code.
- Data model: ORM models, DDL/migrations, constraints, indexes, enums, transaction
  behavior.
- Configuration: defaults, environment parsing, config schema, deploy templates,
  startup code.
- Events/messages: message definitions, producers, consumers, versioning, retry and
  idempotency implementation.
- Permissions: actual rules, middleware, policies, role definitions, tests.

When candidates disagree, list the differences with evidence; do not silently crown
one as authoritative.

## Field checklists

**API:** method, path, purpose, auth requirements; path/query/body fields with type,
required, default, constraints, example; response shape, pagination, sorting, empty
semantics; errors, status codes, retryability, idempotency (only when evidenced);
version, compatibility, deprecation policy, permission-sensitive fields.

**Data model:** business meaning, keys, relations, cardinality, delete behavior;
nullability, defaults, unique/check constraints, indexes; states and legal
transitions; computed/audit fields, retention or masking (confirmed against
implementation); migration path and backward-compatibility impact.

**Configuration:** key, type, default, required, allowed range; source precedence,
environment variable, sensitivity; activation timing (startup/reload) and validation
command. Examples use fictional values; never emit secrets, tokens, personal data,
or real credentials.

**Events:** name, producers, consumers, schema, version; delivery guarantees only
when the mechanism proves them; ordering, duplication, retry, dead-letter,
idempotency semantics; recovery after failure.

## Generation strategy

If an OpenAPI/Schema generation chain exists, change its source or generator, never
the generated output. Do not introduce a new toolchain "for automation" without the
user accepting the dependency and maintenance cost. Generated field tables are fine;
business explanation, trade-offs, and operational guidance stay human-maintained.

## Compatibility review

Classify every interface/field change: added, deprecated, removed, semantics
changed, constraint tightened, default changed, error handling changed. Assess
callers, persisted data, migration, release ordering, and rollback per class. When
the caller inventory is unknown, write exactly that; never claim compatibility
without evidence.

## Delivery

Report contract sources, before/after deltas, affected pages, compatibility
conclusions with evidence, verification commands and results, and open items. Use
"passes / compatible / verified" only when actually verified.
