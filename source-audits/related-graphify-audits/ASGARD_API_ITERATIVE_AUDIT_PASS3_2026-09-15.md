# Graphify API audit - iterative pass 3

Target repo: `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61`  
Auditor: `asgard-api-auditor 0.8.0` plus manual Graphify/static/dynamic probes  
Date: 2026-09-15  
Commit under audit: `fe66389083369c3159aa391117185c8f58b4d07c`  
Repo state: dirty before this pass; generated audit artifacts were kept outside the target repo where possible.

## Stopping rule

The loop stopped after two consecutive closure iterations produced no new verified API findings:

- V24: product-scope Asgard rerun after excluding tests/docs/worked/build artifacts produced no exposed or consumed endpoints and only the same coverage blocker: no supported detector selected.
- V25: targeted runtime grep over `serve.py`, `security.py`, `llm.py`, `prs.py`, `google_workspace.py`, `pg_introspect.py`, `transcribe.py`, `exporters/graphdb.py`, `querylog.py`, `README.md`, and `pyproject.toml` only restated already catalogued surfaces.

## Iterative versions and deltas

### V20 - Dynamic host/auth probe

Technique: in-process Starlette TestClient against `_build_http_app`, using synthetic graphs and hostile/edge headers.

New findings:

1. The API-key middleware protects GET and DELETE on `/mcp`, not only POST. Missing auth returned 401 for both.
2. When both auth headers are present, `X-API-Key` takes precedence over `Authorization: Bearer`. A wrong `X-API-Key` with a correct bearer token returned 401; a correct `X-API-Key` with a wrong bearer token returned 200.
3. The Host-header guard rejects `Host: evil.example` with 421 when the server is bound to `127.0.0.1`.
4. Binding to `0.0.0.0` disables the Host-header allowlist and accepts the same hostile Host header. This matches the code's documented wildcard behavior, but it is a deployment-sensitive edge.

Evidence:

- Probe script: `C:\repos\proveedores\graphify-asgard-audit\tools\mcp_edge_probe.py`
- Results: `C:\repos\proveedores\graphify-asgard-audit\mcp-edge-probe-results.json`
- Source: `graphify/serve.py:2366`, `graphify/serve.py:2407`, `graphify/serve.py:2453`, `graphify/serve.py:2480`
- Docs: `README.md:484`, `README.md:496`, `README.md:498`, `README.md:504`

### V21 - Multi-project `project_path` behavior

Technique: synthetic external graph outside the target repo and MCP `graph_stats` call with `project_path`.

New findings:

5. Every MCP tool advertises optional `project_path`; authenticated clients can select an absolute local project directory and make the server load `<project_path>/graphify-out/graph.json`.
6. This is real runtime behavior, not only schema: the probe loaded a graph from `C:\repos\proveedores\graphify-asgard-audit\outside-project\graphify-out\graph.json` and returned its node stats.
7. The cache is bounded by `GRAPHIFY_MAX_CONTEXTS`; invalid values fall back to 8 and values below 1 clamp to 1. The probe confirmed `bogus -> 8` and `0 -> 1`.

Impact:

- In single-user localhost mode this is useful multi-project behavior.
- On a shared HTTP MCP server it means the API key grants read access to any graphify project path readable by the process, unless deployment isolates the process or clients are fully trusted.

Evidence:

- Probe result: `"external_project_path_status": 200`, `"external_project_path_text": "Nodes: 7..."`
- Source: `graphify/serve.py:107`, `graphify/serve.py:1769`, `graphify/serve.py:1792`, `graphify/serve.py:1937`, `tests/test_serve_http.py:203`, `tests/test_serve_http.py:217`
- Docs: `README.md:557`

### V22 - MCP error contract probe

Technique: dynamic JSON-RPC calls for unknown tools, bad `project_path`, invalid integer args, negative ranges, and unknown resources.

New findings:

8. Unknown tool calls return HTTP 200 and a normal MCP tool result text (`Unknown tool: ...`) with `isError: false`.
9. Bad `project_path` and bad integer conversion inside tools also return HTTP 200 and normal tool content (`Error executing ...`) with `isError: false`.
10. Unknown resources behave differently: `resources/read` returns a JSON-RPC error envelope (`error.message = Unknown resource...`), still over HTTP 200.
11. Only `ToolError` paths are machine-readable as `isError: true`; existing tests prove this for PR tools, but generic tool failures do not share that contract.

Impact:

- MCP clients that rely on `isError` may treat failed tool calls as successful textual answers.
- API compatibility docs should distinguish tool-result errors, JSON-RPC errors, and `ToolError` isError semantics.

Evidence:

- Probe script: `C:\repos\proveedores\graphify-asgard-audit\tools\mcp_error_budget_probe.py`
- Results: `C:\repos\proveedores\graphify-asgard-audit\mcp-error-budget-probe-results.json`
- Source: `graphify/serve.py:2267`, `graphify/serve.py:2277`, `graphify/serve.py:2297`, `graphify/serve.py:2307`
- Tests: `tests/test_serve_http.py:368`, `tests/test_serve_http.py:390`

### V23 - Argument range and budget fuzzing

Technique: same MCP dynamic probe with negative and zero values for `depth`, `token_budget`, and `max_hops`.

New findings:

12. `query_graph.depth` is capped above at 6, but not clamped below. `depth=-3` is accepted and reported as `Traversal: BFS depth=-3`, returning only seed nodes.
13. `get_community.token_budget=-5` is accepted and produces an odd truncation message: `showing 20 of 21 lines (~-5-token budget)`, i.e. negative budget creates misleading accounting rather than validation failure.
14. `shortest_path.max_hops=0` and `max_hops=-1` are accepted and return `Path exceeds max_hops=...`, instead of a schema/range error.

Impact:

- These are not direct security bugs, but they are API contract quality issues. The input schema says "Traversal depth (1-6)" yet runtime accepts negative values.
- Fix direction: add `minimum`/`maximum` to schemas where supported and enforce runtime clamps/errors consistently.

Evidence:

- Results: `C:\repos\proveedores\graphify-asgard-audit\mcp-error-budget-probe-results.json`
- Source: `graphify/serve.py:1962`, `graphify/serve.py:1963`, `graphify/serve.py:2042`, `graphify/serve.py:2061`, `graphify/serve.py:1625`

### V24 - Asgard full-repo vs product-scope comparison

Technique: rerun Asgard twice, first on the whole repo with exclusions for generated/build artifacts, then on a stricter product scope excluding tests/docs/worked.

New findings:

15. Full-repo Asgard output is contaminated by fixtures and examples: it reports unsupported ASP.NET Core, Django, NestJS, Angular HttpClient, .NET HttpClient, fetch, and SSE blockers even though these are not the Graphify product API surface.
16. Product-scope Asgard output drops those framework/client blockers and still reports 0 proven exposed endpoints, 0 consumed endpoints, and `no_supported_api_detector_selected`.
17. Therefore Asgard v0.8.0 should be treated as a fail-closed coverage signal for this repo, not as an authoritative API inventory. It lacks a detector for Graphify's Starlette-hosted MCP Streamable HTTP endpoint and OpenAI-compatible SDK consumption patterns.

Evidence:

- Full repo Asgard: `C:\repos\proveedores\graphify-asgard-audit\asgard-pass3\audit-report.md`
- Product-scope Asgard: `C:\repos\proveedores\graphify-asgard-audit\asgard-pass3-product-scope\audit-report.md`
- Product-scope finding: `no_supported_api_detector_selected`

### V25 - Runtime integration inventory closure

Technique: targeted literal/static search across runtime modules and docs, compared against Graphify graph queries.

No new findings beyond the existing inventory. Confirmed surfaces:

- Exposed API: Starlette/MCP Streamable HTTP mounted at configurable path, default `/mcp`; methods GET/POST/DELETE are delegated to MCP session manager.
- Auth: optional shared API key, accepted through `Authorization: Bearer <key>` or `X-API-Key`.
- Resources: `graphify://report`, `graphify://stats`, `graphify://god-nodes`, `graphify://surprises`, `graphify://audit`, `graphify://questions`.
- Tools: `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.
- Consumed HTTP/content APIs: generic URL ingestion through `safe_fetch`, Twitter/X oEmbed, arXiv abstract fetch, YouTube/video download via `yt-dlp`.
- Provider SDK/API integrations: OpenAI-compatible providers, Anthropic, Azure OpenAI, Bedrock, Ollama, DeepSeek, Kimi/Moonshot, Gemini.
- Local/CLI integrations: `gh` for PR tools, `gws` for Google Workspace export.
- Database integrations: PostgreSQL introspection, Neo4j export/push, FalkorDB export/push.

Evidence:

- `graphify/security.py:21`, `graphify/security.py:22`, `graphify/security.py:32`, `graphify/security.py:69`, `graphify/security.py:103`, `graphify/security.py:180`, `graphify/security.py:195`, `graphify/security.py:231`, `graphify/security.py:258`
- `graphify/ingest.py:86`, `graphify/ingest.py:110`, `graphify/ingest.py:215`, `graphify/ingest.py:229`
- `graphify/llm.py:62`, `graphify/llm.py:103`, `graphify/llm.py:119`, `graphify/llm.py:129`, `graphify/llm.py:154`, `graphify/llm.py:171`, `graphify/llm.py:1389`, `graphify/llm.py:1502`, `graphify/llm.py:1824`, `graphify/llm.py:1881`, `graphify/llm.py:1898`, `graphify/llm.py:3032`, `graphify/llm.py:3101`
- `graphify/prs.py:144`, `graphify/prs.py:240`, `graphify/prs.py:637`, `graphify/prs.py:651`
- `graphify/google_workspace.py:95`, `graphify/google_workspace.py:110`
- `graphify/pg_introspect.py:22`
- `graphify/transcribe.py:34`, `graphify/transcribe.py:58`, `graphify/transcribe.py:83`
- `graphify/exporters/graphdb.py:40`, `graphify/exporters/graphdb.py:134`
- `graphify/querylog.py:17`, `graphify/querylog.py:35`

## Consolidated prioritized findings from this pass

### P1 - Shared HTTP MCP plus `project_path` grants broad graph-file read capability

Authenticated clients can pass an absolute `project_path` and the server will load that project's `graphify-out/graph.json`. This is by design for multi-project MCP, but it is a material API/security boundary in shared deployments. Binding to `0.0.0.0` is documented and disables the Host allowlist, so API-key possession becomes the main control.

Recommendation: document this as a trust boundary; consider an allowlist/root constraint for `project_path` in HTTP mode, especially when `host=0.0.0.0`.

### P2 - MCP tool error semantics are inconsistent

Unknown tools, bad project paths, and generic handler exceptions return normal tool results with `isError` false/absent. PR-specific `ToolError` returns `isError: true`; resources use JSON-RPC error envelopes.

Recommendation: convert unknown tools and generic handler failures to `ToolError` or equivalent `CallToolResult(isError=True)` in the mcp 2.x path, and add regression tests for bad `project_path` and invalid args.

### P2 - Numeric argument ranges are documented but not enforced

`depth` is described as 1-6 but accepts negative values; `token_budget` accepts negative values and produces misleading truncation; `max_hops` accepts 0/negative.

Recommendation: enforce runtime validation and add schema `minimum`/`maximum` where applicable.

### P2 - Asgard v0.8.0 cannot be used as the final API inventory for this repo

Asgard emits a validated but partial artifact set. In full-repo scope it is polluted by fixtures; in product scope it reports no supported detector selected. It misses the real Starlette/MCP API and most SDK/CLI integration surfaces.

Recommendation: use Asgard output as a fail-closed coverage artifact only, then maintain the Graphify-specific API inventory manually or add dedicated Asgard detectors for Starlette MCP and Python SDK clients.

### P3 - Query logging can persist full graph responses when explicitly enabled

`GRAPHIFY_QUERY_LOG_RESPONSES=1` records full query responses to plaintext JSONL under the configured/default log path. It is opt-in and documented, but responses can include proprietary graph labels and source locations.

Recommendation: keep opt-in posture, document retention/security expectations, and consider redaction controls for shared developer machines.

## Verification run

- `python C:\repos\proveedores\graphify-asgard-audit\tools\mcp_edge_probe.py` - passed and wrote `mcp-edge-probe-results.json`.
- `python C:\repos\proveedores\graphify-asgard-audit\tools\mcp_error_budget_probe.py` - passed and wrote `mcp-error-budget-probe-results.json`.
- `python -m pytest tests\test_serve_http.py::test_pr_tool_failure_sets_iserror tests\test_serve_http.py::test_normal_tool_result_is_not_iserror -q` - `2 passed, 1 warning`.
- `asgard-api-auditor audit ... --allow-dirty ... --output C:\repos\proveedores\graphify-asgard-audit\asgard-pass3` - completed with `partial`.
- `asgard-api-auditor audit ... product scope ... --output C:\repos\proveedores\graphify-asgard-audit\asgard-pass3-product-scope` - completed with `partial`.

## Suggested next fixes

1. Add runtime validators for MCP numeric args and align schemas.
2. Make MCP generic failures and unknown tools return machine-readable `isError: true`.
3. Add an HTTP-mode `project_path` allowlist/root option or stronger documentation warning.
4. Extend Asgard with detectors for Starlette MCP Streamable HTTP and Python SDK consumers.
