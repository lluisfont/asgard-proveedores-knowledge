from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from starlette.testclient import TestClient


REPO = Path(r"C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61")
sys.path.insert(0, str(REPO))

from graphify import serve as serve_mod  # noqa: E402


HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "edge-probe", "version": "1"},
    },
}


def graph(path: Path, label: str, nodes: int = 1) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({
            "directed": True,
            "nodes": [
                {"id": f"{label}-{i}", "label": f"{label} {i}", "community": 0}
                for i in range(nodes)
            ],
            "edges": [],
        }),
        encoding="utf-8",
    )
    return path


def init_session(client: TestClient, headers: dict | None = None) -> dict:
    resp = client.post("/mcp", headers=headers or HEADERS, json=INIT)
    return {**(headers or HEADERS), "mcp-session-id": resp.headers.get("mcp-session-id", "")}


def call_tool(client: TestClient, headers: dict, name: str, arguments: dict) -> tuple[int, str]:
    resp = client.post(
        "/mcp",
        headers=headers,
        json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
    )
    text = ""
    try:
        result = resp.json().get("result", {})
        content = result.get("content") or []
        if content:
            text = content[0].get("text", "")
    except Exception:
        text = resp.text[:200]
    return resp.status_code, text


def main() -> int:
    out = Path(r"C:\repos\proveedores\graphify-asgard-audit")
    default_graph = graph(out / "edge-default" / "graph.json", "DefaultGraph", 2)
    external_project = out / "outside-project"
    graph(external_project / "graphify-out" / "graph.json", "ExternalProject", 7)

    results: dict[str, object] = {}

    app = serve_mod._build_http_app(str(default_graph), api_key="k", json_response=True)
    with TestClient(app, base_url="http://127.0.0.1") as client:
        results["auth_missing_get_mcp"] = client.get("/mcp").status_code
        results["auth_missing_delete_mcp"] = client.delete("/mcp").status_code
        results["auth_wrong_x_api_key_correct_bearer"] = client.post(
            "/mcp",
            headers={**HEADERS, "X-API-Key": "wrong", "Authorization": "Bearer k"},
            json=INIT,
        ).status_code
        results["auth_correct_x_api_key_wrong_bearer"] = client.post(
            "/mcp",
            headers={**HEADERS, "X-API-Key": "k", "Authorization": "Bearer wrong"},
            json=INIT,
        ).status_code
        ok_headers = init_session(client, {**HEADERS, "Authorization": "Bearer k"})
        client.post("/mcp", headers=ok_headers, json={"jsonrpc": "2.0", "method": "notifications/initialized"})
        status, text = call_tool(client, ok_headers, "graph_stats", {"project_path": str(external_project)})
        results["external_project_path_status"] = status
        results["external_project_path_text"] = text

    host_app = serve_mod._build_http_app(str(default_graph), host="127.0.0.1", port=8080, json_response=True)
    with TestClient(host_app, base_url="http://evil.example") as client:
        results["bad_host_status"] = client.post("/mcp", headers=HEADERS, json=INIT).status_code
        results["bad_host_body"] = client.post("/mcp", headers=HEADERS, json=INIT).text[:160]

    wildcard_app = serve_mod._build_http_app(str(default_graph), host="0.0.0.0", port=8080, json_response=True)
    with TestClient(wildcard_app, base_url="http://evil.example") as client:
        results["wildcard_host_status"] = client.post("/mcp", headers=HEADERS, json=INIT).status_code

    previous = os.environ.get("GRAPHIFY_MAX_CONTEXTS")
    try:
        os.environ["GRAPHIFY_MAX_CONTEXTS"] = "0"
        results["max_contexts_zero"] = serve_mod._max_server_contexts()
        os.environ["GRAPHIFY_MAX_CONTEXTS"] = "bogus"
        results["max_contexts_bogus"] = serve_mod._max_server_contexts()
    finally:
        if previous is None:
            os.environ.pop("GRAPHIFY_MAX_CONTEXTS", None)
        else:
            os.environ["GRAPHIFY_MAX_CONTEXTS"] = previous

    output = out / "mcp-edge-probe-results.json"
    output.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
