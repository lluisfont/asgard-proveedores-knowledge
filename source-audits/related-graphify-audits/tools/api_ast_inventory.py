from __future__ import annotations

import ast
import json
import re
import sys
import tomllib
from pathlib import Path


URL_RE = re.compile(r"https?://[^\s'\"<>`)]+")


def literal(node: ast.AST):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Call):
        return dotted(node.func)
    return ""


def iter_py(root: Path):
    ignored = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        "graphify-out",
        ".brownfield",
        "build",
        "dist_audit",
        "dist_audit_iter",
        "dist_audit_pass3",
        "tests",
        "worked",
    }
    for path in root.rglob("*.py"):
        if any(part in ignored for part in path.parts):
            continue
        yield path


class Inventory(ast.NodeVisitor):
    def __init__(self, path: Path, rel: str):
        self.path = path
        self.rel = rel
        self.tools = []
        self.resources = []
        self.routes = []
        self.env_vars = []
        self.subprocesses = []
        self.imports = []
        self.urls = []
        self.dynamic_fetches = []
        self.server_callbacks = []

    def loc(self, node: ast.AST) -> dict:
        return {"path": self.rel, "line": getattr(node, "lineno", None)}

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            root = alias.name.split(".")[0]
            if root in {"urllib", "yt_dlp", "neo4j", "falkordb", "psycopg", "openai", "anthropic", "boto3"}:
                self.imports.append({**self.loc(node), "module": alias.name})
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        root = module.split(".")[0]
        if root in {"urllib", "yt_dlp", "neo4j", "falkordb", "psycopg", "openai", "anthropic", "boto3"}:
            self.imports.append({**self.loc(node), "module": module})
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, str):
            for match in URL_RE.findall(node.value):
                self.urls.append({**self.loc(node), "url": match})
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        name = dotted(node.func)
        if name.endswith("types.Tool") or name == "Tool":
            item = {**self.loc(node)}
            for kw in node.keywords:
                if kw.arg in {"name", "description", "inputSchema"}:
                    item[kw.arg] = literal(kw.value)
            self.tools.append(item)
        elif name.endswith("types.Resource") or name == "Resource":
            item = {**self.loc(node)}
            for kw in node.keywords:
                if kw.arg in {"uri", "name", "description", "mimeType"}:
                    item[kw.arg] = literal(kw.value)
            self.resources.append(item)
        elif name.endswith("Route") or name == "Route":
            item = {**self.loc(node), "call": name}
            if node.args:
                item["path_arg"] = literal(node.args[0])
            for kw in node.keywords:
                if kw.arg in {"path", "endpoint", "methods"}:
                    item[kw.arg] = literal(kw.value) or dotted(kw.value)
            self.routes.append(item)
        elif name in {"os.environ.get", "environ.get"}:
            if node.args:
                key = literal(node.args[0])
                if isinstance(key, str):
                    self.env_vars.append({**self.loc(node), "name": key, "access": "get"})
        elif name in {"subprocess.run", "subprocess.Popen"} or name.endswith(".subprocess.run"):
            cmd = literal(node.args[0]) if node.args else None
            self.subprocesses.append({**self.loc(node), "call": name, "command": cmd})
        elif name in {"safe_fetch", "safe_fetch_text", "validate_url"} or name.endswith(".safe_fetch") or name.endswith(".safe_fetch_text"):
            arg = literal(node.args[0]) if node.args else None
            self.dynamic_fetches.append({**self.loc(node), "call": name, "url_arg": arg or ast.unparse(node.args[0]) if node.args else None})
        elif name.endswith("Server") or name == "Server":
            callbacks = {}
            for kw in node.keywords:
                if kw.arg and kw.arg.startswith("on_"):
                    callbacks[kw.arg] = dotted(kw.value)
            if callbacks:
                self.server_callbacks.append({**self.loc(node), "callbacks": callbacks})
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        base = dotted(node.value)
        if base in {"os.environ", "environ"}:
            key = literal(node.slice)
            if isinstance(key, str):
                self.env_vars.append({**self.loc(node), "name": key, "access": "subscript"})
        self.generic_visit(node)


def summarize_pyproject(root: Path) -> dict:
    path = root / "pyproject.toml"
    if not path.exists():
        return {}
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    project = data.get("project", {})
    return {
        "dependencies": project.get("dependencies", []),
        "optional_dependencies": project.get("optional-dependencies", {}),
        "scripts": project.get("scripts", {}),
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: api_ast_inventory.py <repo-root> <output-json>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    result = {
        "repo": str(root),
        "tools": [],
        "resources": [],
        "routes": [],
        "env_vars": [],
        "subprocesses": [],
        "imports": [],
        "urls": [],
        "dynamic_fetches": [],
        "server_callbacks": [],
        "pyproject": summarize_pyproject(root),
    }
    for path in iter_py(root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except Exception as exc:
            result.setdefault("parse_errors", []).append({"path": str(path), "error": str(exc)})
            continue
        inv = Inventory(path, path.relative_to(root).as_posix())
        inv.visit(tree)
        for key in ("tools", "resources", "routes", "env_vars", "subprocesses", "imports", "urls", "dynamic_fetches", "server_callbacks"):
            result[key].extend(getattr(inv, key))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "tools": len(result["tools"]),
        "resources": len(result["resources"]),
        "routes": len(result["routes"]),
        "env_vars": len(result["env_vars"]),
        "subprocesses": len(result["subprocesses"]),
        "imports": len(result["imports"]),
        "urls": len(result["urls"]),
        "dynamic_fetches": len(result["dynamic_fetches"]),
        "server_callbacks": len(result["server_callbacks"]),
        "output": str(out),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
