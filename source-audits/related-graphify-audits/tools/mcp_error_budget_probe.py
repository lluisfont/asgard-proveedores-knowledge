from __future__ import annotations

import json
import os
import sys
from pathlib import Path


TARGET = Path(r"C:\Users\GMKtek-1\.graphify\repos\Graphify-Labs\graphify-v0.9.61")
OUT = Path(r"C:\repos\proveedores\graphify-asgard-audit")


def _write_graph(path: Path, node_count: int = 20) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nodes = [
        {
            "id": f"n{i}",
            "label": f"Node{i}",
            "community": 0,
            "source_file": f"src/file_{i}.py",
            "source_location": f"L{i}",
        }
        for i in range(node_count)
    ]
    edges = [
        {
            "source": f"n{i}",
            "target": f"n{i + 1}",
            "relation": "calls",
            "confidence": "EXTRACTED",
            "source_file": f"src/file_{i}.py",
            "source_location": f"L{i}",
        }
        for i in range(node_count - 1)
    ]
    path.write_text(
        json.dumps({"directed": True, "nodes": nodes, "edges": edges}),
        encoding="utf-8",
    )


def _init_session(client):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "probe", "version": "0"},
        },
    }
    resp = client.post("/mcp", headers=headers, json=body)
    resp.raise_for_status()
    sid = resp.headers.get("mcp-session-id")
    if sid:
        headers["mcp-session-id"] = sid
    return headers


def _call(client, headers, method, params, rid):
    resp = client.post(
        "/mcp",
        headers=headers,
        json={"jsonrpc": "2.0", "id": rid, "method": method, "params": params},
    )
    try:
        body = resp.json()
    except Exception:
        body = resp.text
    return {"status": resp.status_code, "body": body}


def _text(result):
    try:
        return result["body"]["result"]["content"][0]["text"]
    except Exception:
        return None


def _is_error(result):
    try:
        return result["body"]["result"].get("isError")
    except Exception:
        return None


def main() -> None:
    sys.path.insert(0, str(TARGET))
    os.chdir(TARGET)

    from starlette.testclient import TestClient
    from graphify import serve as serve_mod

    graph_path = OUT / "edge-errors" / "graph.json"
    _write_graph(graph_path)
    missing_project = OUT / "missing-project"

    app = serve_mod._build_http_app(str(graph_path), json_response=True)
    results = {}
    with TestClient(app, base_url="http://127.0.0.1") as client:
        headers = _init_session(client)
        cases = {
            "unknown_tool": (
                "tools/call",
                {"name": "definitely_not_a_tool", "arguments": {}},
            ),
            "bad_project_path": (
                "tools/call",
                {
                    "name": "graph_stats",
                    "arguments": {"project_path": str(missing_project)},
                },
            ),
            "bad_depth_string": (
                "tools/call",
                {
                    "name": "query_graph",
                    "arguments": {"question": "Node", "depth": "bogus"},
                },
            ),
            "negative_depth": (
                "tools/call",
                {
                    "name": "query_graph",
                    "arguments": {"question": "Node0", "depth": -3},
                },
            ),
            "negative_token_budget": (
                "tools/call",
                {
                    "name": "get_community",
                    "arguments": {"community_id": 0, "token_budget": -5},
                },
            ),
            "zero_max_hops": (
                "tools/call",
                {
                    "name": "shortest_path",
                    "arguments": {"source": "Node0", "target": "Node2", "max_hops": 0},
                },
            ),
            "negative_max_hops": (
                "tools/call",
                {
                    "name": "shortest_path",
                    "arguments": {"source": "Node0", "target": "Node2", "max_hops": -1},
                },
            ),
            "unknown_resource": (
                "resources/read",
                {"uri": "graphify://does-not-exist"},
            ),
        }
        for idx, (name, (method, params)) in enumerate(cases.items(), 2):
            raw = _call(client, headers, method, params, idx)
            results[name] = {
                "status": raw["status"],
                "isError": _is_error(raw),
                "text": _text(raw),
                "jsonrpc_error": raw["body"].get("error") if isinstance(raw["body"], dict) else None,
            }

    out_path = OUT / "mcp-error-budget-probe-results.json"
    out_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
