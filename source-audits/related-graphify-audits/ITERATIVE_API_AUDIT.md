# Iterative API Audit - Graphify v0.9.61

Target repo: `C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61`
Commit: `fe66389083369c3159aa391117185c8f58b4d07c`
Asgard API Auditor: `0.8.0` installed at `C:\repos\proveedores\asgard-api-auditor`

## Iterations

### v1 - Official Asgard broad audit

Artifacts: `C:\repos\proveedores\graphify-asgard-audit\v1-official-audit`

New finding: Asgard returned `PARTIAL`, not complete. The broad scan was polluted by fixture/example code and reported unsupported/dynamic surfaces from non-runtime files.

### v2 - Official Asgard runtime-scope audit

Artifacts: `C:\repos\proveedores\graphify-asgard-audit\v2-runtime-scope`

New finding: On runtime scope, Asgard generated `paths: {}` and selected no supported API detector. This is a detector coverage gap, not proof that Graphify has no API.

### v3 - Static route and server inspection

New findings:

- Graphify exposes a Starlette MCP Streamable HTTP route through `_build_http_app`, defaulting to `/mcp`.
- The route is configurable with `--path`.
- Auth is optional; `--api-key` / `GRAPHIFY_API_KEY` enables either `Authorization: Bearer <key>` or `X-API-Key`.
- Binding `0.0.0.0` without auth warns but does not fail closed.

### v4 - Dynamic MCP contract inventory

New findings:

- The single HTTP route exposes 10 MCP tools: `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.
- The server exposes 6 MCP resources: `graphify://report`, `graphify://stats`, `graphify://god-nodes`, `graphify://surprises`, `graphify://audit`, `graphify://questions`.
- Stateful mode requires `mcp-session-id` after initialization; stateless mode does not return or require a session id.
- `DELETE /mcp` is accepted for session lifecycle.

### v5 - Documentation and behavioral edge checks

New findings:

- README lists only 7 MCP tools and omits `get_community`, `god_nodes`, and `graph_stats`.
- README omits all MCP resource URIs.
- README omits the per-tool argument schemas, including `project_path`.
- `POST /mcp/` returns a `307` redirect to `/mcp` when redirects are disabled, despite comments describing no trailing-slash redirect.
- `X-API-Key` takes precedence over `Authorization`; a wrong `X-API-Key` causes 401 even if Bearer is correct.
- Bearer token whitespace is stripped, while `X-API-Key` whitespace is not.

### v6 - Security/delegated audit

New findings:

- `project_path` lets any MCP client select an arbitrary local project path containing `graphify-out/graph.json`, with the server process permissions.
- PR tools execute `gh` and `git worktree` through the server host and can expose PR metadata, authors, CI/review status, changed files, and local worktree paths.
- Supplying `--api-key` places the secret in process argv; the environment variable is safer.
- Shared HTTP examples use Bearer over plain HTTP unless the operator adds TLS/proxying externally.
- Unknown tool names and generic execution failures are returned as successful MCP results (`isError=false`).
- A pure multi-project server can use `project_path` for tools, but `resources/read` always selects the missing default graph and returns a JSON-RPC error.
- DNS-rebinding protection rejects standard bracketed IPv6 Host forms like `[::1]:8080`.
- Package metadata allows `mcp>=1,<3`, but the lockfile pins `mcp 1.29.0`, so the mcp 2.x branch is not covered by the frozen CI install.

### v7 - API-client / outbound integration scan

New findings:

- Graphify consumes external APIs via SDKs rather than literal HTTP clients: OpenAI-compatible APIs, Azure OpenAI, Anthropic, AWS Bedrock, and GitHub CLI.
- Asgard runtime inventory reports no HTTP clients because these SDK/subprocess integrations are outside its supported literal-client detector model.

### v8 - Bandit API-module scan

New findings: none. Bandit reported no high-severity issues. Medium findings only reinforced the already-known wildcard-bind exposure.

### v9 - Mechanical contract/docs/Asgard comparison and targeted tests

New findings: none. The comparison only confirmed prior documentation omissions and the empty Asgard OpenAPI. Targeted tests passed.

Stop criterion met at that point: v8 and v9 added no new findings.

### v10 - MCP argument fuzzing

New findings:

- Tool input schemas are advertised but not enforced as schema validation before handler execution. Missing required fields, wrong scalar types, and invalid numeric strings generally return HTTP 200 with text such as `Error executing ...` and `isError=false`.
- `depth` is capped to 6, but there is no minimum bound: negative or unusual budgets are accepted into output trimming paths.
- Extra arguments are accepted silently by tools such as `graph_stats`.

### v11 - Current dependency vulnerability audit

New findings: none for the Graphify API stack. `pip-audit` found vulnerabilities in the auditor host's `pip` package, but no vulnerabilities in `mcp`, `starlette`, `uvicorn`, `httpx/httpx2`, `anyio`, or Graphify's HTTP/MCP runtime dependencies.

Artifact: `C:\repos\proveedores\graphify-asgard-audit\v11-pip-audit-current.json`

### v12 - Explicit mcp 1.x compatibility check

New findings: none. A separate venv with `mcp==1.29.0` and `starlette==1.6.0` passed `tests\test_serve_http.py`, matching the local mcp 2.2.0 behavior already exercised.

Artifact: `C:\repos\proveedores\graphify-asgard-audit\mcp129-venv`

Final stop criterion met: v11 and v12 added no new Graphify API findings after the v10 fuzzing additions.

## Verification

- `python -m pytest tests\test_serve_http.py -q`: 30 passed.
- `python -m pytest tests\test_serve_http.py tests\test_prs.py -q`: 82 passed.
- Targeted MCP tests: 6 passed.
- Dynamic TestClient probes confirmed tools/resources, auth matrix, session behavior, wildcard host behavior, trailing-slash redirect, project_path behavior, and IPv6 Host behavior.
- `mcp==1.29.0` isolated venv: `tests\test_serve_http.py` passed, 30 passed.
