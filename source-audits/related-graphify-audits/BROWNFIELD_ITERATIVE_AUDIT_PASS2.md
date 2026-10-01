# Graphify Brownfield Iterative Audit - Pass 2

Target repository: `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61`

Brownfield tool: `C:\repos\proveedores\Brownfield-Refactor-Analyst`

Date: 2026-09-14

## Scope

This pass continues the previous Brownfield/Graphify audit and only records findings that were not already present in `BROWNFIELD_ITERATIVE_AUDIT.md`.

Stop criterion used: continue trying different techniques until two consecutive iterations do not add a new finding.

## Techniques Used

1. Brownfield state/config verification after seed, semantic reconstruction, Graphify import, completeness and packaging.
2. Brownfield inventory vs `git ls-files` comparison.
3. Brownfield release ZIP structure and duplicate payload analysis.
4. Release artifact extension/content validation.
5. Process-map validation against real Graphify CLI/MCP source surfaces.
6. Graphify graph queries over `graphify-out/graph.json`.
7. Static security review using prior Bandit/Pyright/Pip-audit outputs plus focused source inspection.
8. Focused regression tests for MCP HTTP, CLI help and manifest ingestion.
9. Final TODO/FIXME and release consistency control passes.

## Iteration Log

### Iteration 1 - Brownfield State Traceability

New finding found: `PROJECT_STATE.json` remains partially unconfigured after successful Brownfield runs.

Evidence:

- `.brownfield/PROJECT_STATE.json` reports `"project": "UNCONFIGURED"`.
- `.brownfield/PROJECT_STATE.json` reports `"repository_commit": null`.
- After later commands, state still reports `"last_completed_step": "seed_baseline"` and `"current_phase": "business_validation"`.
- The repo is a Git checkout, so a commit anchor is available.

### Iteration 2 - Inventory vs Git Reality

New finding found: Brownfield inventory includes untracked/generated local files.

Evidence:

- Brownfield inventory files: `913`.
- Git tracked files: `890`.
- Inventory entries not tracked by Git: `28`.
- Top untracked groups included by Brownfield:
  - `.ruff_cache`: 10
  - `graphifyy.egg-info`: 6
  - `.pytest_cache`: 5
  - `dist_audit`: 2
  - `dist_audit_iter`: 2
  - `bandit_v0961.json`, `pip_audit_v0961.json`, `pyright_v0961.json`: 1 each

### Iteration 3 - Release Package Payload

New finding found: Brownfield duplicates very large Graphify artifacts in the checkpoint package and maps data files into misleading report names.

Evidence from latest checkpoint ZIP:

- ZIP entries: `393`.
- ZIP size: about `4.0 MB`.
- Largest uncompressed payload is copied three times:
  - `work/graphify/graph.json`
  - `work/release/engineering-analysis/architecture/GRAPHIFY_GRAPH.json`
  - `work/release/traceability/verification/GRAPHIFY_GRAPH.json`
- Each copy of `GRAPHIFY_GRAPH.json` is about `17.2 MB` uncompressed.
- Brownfield source mapping copies `work/evidence/evidence.jsonl` into `engineering-analysis/behavior/STATE_MACHINE_CATALOG.md`.

### Iteration 4 - Release Artifact Content Validation

New finding found: Brownfield emits at least seven `.md` release artifacts whose first line is CSV or JSONL, and validation/package commands do not reject them.

Evidence:

- `.brownfield/work/release/business-analysis/domain-model/BUSINESS_ENTITY_CATALOG.md` starts with CSV header.
- `.brownfield/work/release/business-analysis/processes/PROCESS_CATALOG.md` starts with CSV header.
- `.brownfield/work/release/engineering-analysis/behavior/STATE_MACHINE_CATALOG.md` starts with a JSON evidence object.
- `.brownfield/work/release/engineering-analysis/data/CONSTRAINT_CATALOG.md` starts with CSV header.
- `.brownfield/work/release/engineering-analysis/data/DATABASE_OBJECTS_CATALOG.md` starts with CSV header.
- `.brownfield/work/release/engineering-analysis/data/INDEX_CATALOG.md` starts with CSV header.
- `.brownfield/work/release/engineering-analysis/data/RELATIONSHIP_CATALOG.md` starts with CSV header.
- `brownfield verify-state` and `brownfield package` still succeeded.

### Iteration 5 - Process Map Accuracy

New finding found: Brownfield process mapping misclassifies documentation/tests/modules as business processes and misses the real command surface.

Evidence:

- Brownfield process candidates:
  - `GET /` from `CHANGELOG.md:785`.
  - `CLI_COMMAND` candidate in `docs/docker-mcp-sqlite.md`.
  - `EVENT_CONSUMER` candidate in `graphify/exporters/html.py`.
  - `QUEUE_WORKER` candidate in `graphify/prs.py`.
  - `CLI_COMMAND` candidate in `graphify/security.py`.
  - `EVENT_CONSUMER` candidate in `graphify/serve.py`.
  - `CLI_COMMAND` candidate in `tests/test_labeling.py`.
- Six of seven process candidates have empty `evidence_ids`.
- Brownfield's non-HTTP classifier is token-based: it returns `SCHEDULED_TASK`, `EVENT_CONSUMER`, `QUEUE_WORKER`, or `CLI_COMMAND` if words such as `consumer`, `listener`, `worker`, `queue`, `command`, `cli`, or `argparse` appear in a file name or content.
- Actual Graphify CLI dispatch in `graphify/cli.py` exposes 42 command/subcommand strings by direct `cmd == ...` matching.

### Iteration 6 - MCP Surface Omission

New finding found: Brownfield does not model Graphify's MCP tools/resources as public interfaces.

Evidence:

- `graphify/serve.py` defines 10 MCP tools:
  - `get_community`
  - `get_neighbors`
  - `get_node`
  - `get_pr_impact`
  - `god_nodes`
  - `graph_stats`
  - `list_prs`
  - `query_graph`
  - `shortest_path`
  - `triage_prs`
- `graphify/serve.py` defines 6 MCP resources:
  - `graphify://audit`
  - `graphify://god-nodes`
  - `graphify://questions`
  - `graphify://report`
  - `graphify://stats`
  - `graphify://surprises`
- Brownfield interface output remained the generic process map with 1 route and 6 non-HTTP candidates, without a first-class MCP/API catalog.

### Iteration 7 - XML Parser Hardening

New finding found: `graphify/manifest_ingest.py` parses Maven `pom.xml` with `xml.etree.ElementTree.fromstring` without the defensive DOCTYPE/ENTITY guard used in `graphify/extract.py`.

Evidence:

- `graphify/manifest_ingest.py` imports `xml.etree.ElementTree as ET`.
- `_parse_pom()` calls `ET.fromstring(text)` directly after namespace string replacement.
- `graphify/extract.py` has `_project_xml_is_safe()` and rejects XML with `DOCTYPE` or `ENTITY` before its own `ET.fromstring` calls.
- Bandit also flagged `graphify/manifest_ingest.py:290` as `B314`.

Risk:

- Graphify ingests package manifests from arbitrary target repos/corpora. Maven POMs are therefore attacker-controlled input in normal use.
- The existing defensive pattern in `extract.py` should be reused here or replaced with `defusedxml`.

### Iteration 8 - Dependency and Focused Tests

No new finding.

Evidence:

- `pip_audit_v0961.json` reported no vulnerabilities for inspected dependencies.
- Focused tests passed:
  - `tests/test_manifest_ingest.py`
  - `tests/test_serve_http.py`
  - `tests/test_cli_help.py`
- Result: `44 passed, 1 warning`.

### Iteration 9 - Debt Marker and Consistency Control

No new finding.

Evidence:

- `TODO/FIXME/BUG/follow-up` scan mostly returned tests, documentation, translated docs, and explicit regression comments.
- Release consistency scan repeated the seven `.md` content-format mismatches already found in Iteration 4.

Stop criterion met: Iterations 8 and 9 did not produce new findings.

## Consolidated New Findings

### BF-P2-01 - Brownfield State Is Not Commit-Anchored

Severity: Medium

Brownfield leaves the project as `UNCONFIGURED`, `repository_commit` as `null`, and `last_completed_step` as `seed_baseline` even after later successful commands. This weakens audit reproducibility because the checkpoint cannot be tied to a precise Git commit or true lifecycle state.

### BF-P2-02 - Brownfield Inventory Includes Generated/Untracked Files

Severity: Medium

Brownfield included 28 untracked/generated files in its inventory, including caches, build metadata, distribution audit folders, and previous audit JSON outputs. This contaminates baseline analysis and can make later diffs noisy or non-reproducible.

### BF-P2-03 - Brownfield Release Package Duplicates Large Graph Artifacts

Severity: Low/Medium

The checkpoint contains three uncompressed copies of the same large `graph.json` payload under different paths. This is inefficient and can become operationally painful on larger repos.

### BF-P2-04 - Brownfield Release Emits Mislabelled `.md` Artifacts

Severity: Medium

Seven release files use `.md` names but contain CSV or JSONL content. This undermines human review and downstream automation that trusts file extensions.

### BF-P2-05 - Brownfield Process Map Has False Positives and Interface Omissions

Severity: High

Brownfield classifies docs/tests/modules as process candidates based on keyword matches while missing the real Graphify command surface. The mismatch is material: Brownfield reports 1 route and 6 non-HTTP candidates, while the CLI dispatch alone exposes 42 command/subcommand strings.

### BF-P2-06 - Brownfield Does Not Catalog MCP API Surface

Severity: High

Graphify exposes a real MCP API surface with 10 tools and 6 resources, but Brownfield does not model these as first-class interfaces. For this repo, that means the main runtime integration surface is absent from the Brownfield audit output.

### G-P2-01 - Maven POM Parsing Lacks XML Entity/DOCTYPE Guard

Severity: Medium

`graphify/manifest_ingest.py` parses `pom.xml` using `ET.fromstring(text)` without applying the XML safety guard already present in `graphify/extract.py`. Since manifests are loaded from arbitrary analyzed repos, this should be hardened with the same `DOCTYPE`/`ENTITY` rejection or `defusedxml`.

## Verification

- Brownfield installed and executed against the target repo.
- Brownfield commands exercised: `verify-config`, `verify-state`, `status`, `seed-baseline`, `semantic-reconstruct`, `graphify-import`, `completeness-report`, `package`.
- Graphify query executed against `graphify-out/graph.json`: graph contained `13,712` nodes; query traversed BFS depth 2 and was truncated at a `6,000` token budget.
- Focused Graphify tests passed: `44 passed, 1 warning`.
- Brownfield tool self-tests previously passed: `38 passed, 1 skipped`.
