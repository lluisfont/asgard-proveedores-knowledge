# Brownfield Iterative Audit - Graphify v0.9.61

Target repo: `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61`

Brownfield kit: `C:\repos\proveedores\Brownfield-Refactor-Analyst`

Brownfield version: 0.2.3

Run date: 2026-09-14

## Installation And Baseline

- Installed `brownfield-refactor-kit` from local clone in editable mode.
- Brownfield kit self-tests: 38 passed, 1 skipped.
- Installed `.brownfield/` into Graphify with `technical-language=English` and `business-language=Spanish`.
- `verify-config`: valid.
- `seed-baseline`: completed.
- `semantic-reconstruct`: completed.
- `graphify-import`: imported `GRAPH_REPORT.md` and `graph.json`; `graph.html` was missing from disk at import time.
- `package`: produced `.brownfield\releases\brownfield_checkpoint_20260914_170536_329908Z.zip`.

## Brownfield Metrics

- Inventory: 913 files, 26,129,026 bytes.
- Evidence: 541 records.
- Evidence by kind:
  - permission: 11
  - route: 1
  - secret_candidate: 126
  - sql_query: 6
  - state_transition: 13
  - transaction: 384
- Data dictionary: 14 tables, 28 columns, 5 relations, 14 indexes, 19 constraints, 13 database objects.
- Process map: 1 route, 6 non-HTTP candidates, 11 components, 31 nodes, 27 edges.
- Completeness after semantic pass: 11.62%.
- Status: `INCOMPLETE_BASELINE`, as expected for a deterministic seed baseline.

## Iteration Log

### Iteration 1 - Deterministic Brownfield Baseline

New findings:

1. The Brownfield baseline is polluted by prior audit/build artifacts:
   - `bandit_v0961.json`
   - `pyright_v0961.json`
   - `pip_audit_v0961.json`
   - `dist_audit/`
   - `dist_audit_iter/`
   - `graphifyy.egg-info/`
   - wheel/tarball artifacts

2. Brownfield treats documentation examples as source evidence. Example: `CHANGELOG.md` line 785 became route `GET /`.

3. Brownfield flags many secret candidates from documentation or variable names. Most are not leaked secrets, but they create triage noise unless the scope is filtered.

### Iteration 2 - Data Dictionary And Process Map Review

New findings:

4. The generated data dictionary is mostly fixture-driven, not product-driven. Tables such as `users`, `orders`, `customers`, `accounts`, `Sales.Customer`, and `Sales.SalesOrder` come from `tests/fixtures/*.sql`.

5. The semantic glossary therefore infers a fake business domain (`general-business-data`) for a code analysis library. This is useful as a warning: Brownfield must be configured differently for library repos with test fixtures.

6. `database_sources` was empty in `.brownfield/config/project.yaml`, yet Brownfield still discovered 7 SQL files under tests/fixtures. For this repo, SQL fixture discovery should probably be excluded from canonical business/data reconstruction.

### Iteration 3 - Runtime-Only Evidence Filter

New findings:

7. After excluding docs/tests/generated artifacts, Brownfield still reports 58 runtime secret candidates. Most are parameter names (`api_key`, `password`, `token`), but they highlight sensitive paths that need policy review.

8. A real CLI exposure remains: graph database export accepts `--password` for Neo4j/FalkorDB. The CLI warns that env vars are preferred, but skills/docs still show `--password PASSWORD` examples.
   - `graphify/cli.py:2822-2824`
   - `graphify/cli.py:2883-2884`
   - `graphify/skills/*/references/exports.md:26`

### Iteration 4 - Brownfield Verifier/Final-Auditor Checklist

New findings:

9. Brownfield requires verification claims to cite primary evidence and rejects analyst narrative as evidence. Current generated artifacts remain `INFERRED_DRAFT_REVIEW_REQUIRED`; they should not be treated as canonical repo facts.

10. `graphify-import` expects `graph.html`, but it was absent from `graphify-out/` at import time. It imported `GRAPH_REPORT.md` and `graph.json` only. This is not a Brownfield failure, but the architecture evidence package lacks the interactive graph artifact.

### Iteration 5 - Packaging And Revalidation

New findings: none.

Confirmations:

- Brownfield package command completed and verified ZIP integrity.
- `verify-state` remained valid.
- `verify-config` remained valid.

### Iteration 6 - Convergence Pass

New findings: none.

Stop criterion met: two consecutive iterations added no new findings.

## Consolidated Findings

### B1 - Brownfield scope is too broad for this repo

Severity: Medium for audit reliability.

The default Brownfield install scans the whole repository (`source_roots: [.]`) and excludes only `.git`, `.brownfield`, `node_modules`, `vendor`, `.venv`, and `graphify-out`. In this checkout, prior audit outputs and build artifacts were included as current source. This can distort inventory metrics, secret-candidate counts, and baseline hashes.

Recommended fix: configure Brownfield excludes for generated/audit outputs before treating results as canonical. Suggested additions: `build`, `dist`, `dist_audit`, `dist_audit_iter`, `*.egg-info`, `bandit_*.json`, `pyright_*.json`, `pip_audit_*.json`, `.pytest_cache`.

### B2 - Test fixtures are promoted into business/data artifacts

Severity: Medium for Brownfield-derived conclusions.

SQL fixtures under `tests/fixtures/` are parsed into tables, constraints and business glossary terms. This produces plausible but wrong business entities (`Users`, `Orders`, `Customers`, etc.) for a code analysis library.

Recommended fix: either exclude `tests/fixtures/*.sql` from Brownfield data archaeology for this repo, or mark them explicitly as fixture-only sources.

### B3 - Documentation examples are detected as live routes/secrets

Severity: Low/Medium for audit triage.

Brownfield detected `GET /` in `CHANGELOG.md` as a route and treated README/translation examples as secret candidates. These are mostly false positives, but they can drown real findings.

Recommended fix: exclude high-volume documentation from deterministic route/security extraction, or add a mode that treats docs as examples rather than runtime evidence.

### B4 - CLI password flag remains documented and accepted

Severity: Low/Medium security hygiene.

Graphify allows `graphify export neo4j/falkordb --password ...`, which can expose credentials via shell history or process argv. The code prefers env vars, but the explicit flag still overrides them, and installed skill docs recommend `--password PASSWORD`.

Recommended fix: update all skill/reference examples to use `NEO4J_PASSWORD` / `FALKORDB_PASSWORD`, and consider deprecating or warning more strongly on `--password`.

### B5 - Graphify architecture package imported without `graph.html`

Severity: Low.

Brownfield imported `GRAPH_REPORT.md` and `graph.json`, but not `graph.html` because the file was absent from `graphify-out/` during import. The release package therefore lacks the interactive visualization.

Recommended fix: regenerate `graph.html` before `brownfield graphify-import` when the visual artifact is needed.

## Notes

- Brownfield findings are evidence-routing findings first. They should not replace the earlier code/security audit findings.
- Brownfield is strongest here as a methodology and traceability tool, but its default source scope is tuned for legacy product repositories, not test-heavy developer tooling libraries.
- The best next improvement is to rerun Brownfield from a clean checkout with a narrowed `.brownfield/config/project.yaml`.
