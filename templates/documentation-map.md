# Documentation-to-source mapping

Each row records the topic a document explains, its source of truth, the changes
that trigger an update, and how it is verified. Registering paths alone is not enough.

| Document path | Topic / audience | Source of truth (path/symbol) | Changes that trigger update | Verification | Status |
|---|---|---|---|---|---|
| README.md | Project overview / developers | pyproject.toml; src/... | Command, dependency, entry-point changes | Command check / quick start | pending |
| docs/architecture/... | Architecture / developers | src/...; config; ADRs | Module boundary, dependency, main-flow changes | Code tracing / diagram check | pending |
| docs/reference/... | API users | OpenAPI / schema / route implementation | Request, response, error-code changes | Schema / tests | pending |
