#!/usr/bin/env python3
"""Detect direct PHP/AJAX endpoints missed by Brownfield.

The legacy app routes many requests by public PHP file path instead of framework
route declarations. Brownfield's deterministic route extractor reports zero HTTP
routes for that style, so this companion scanner creates an evidence-backed
endpoint catalog from file paths, superglobals, includes, output calls and SQL
data-flow edges.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


EXCLUDE_SEGMENTS = {
    ".git",
    ".brownfield",
    "node_modules",
    "vendor",
    "graphify-out",
    "PHPExcel",
    "MPDF57",
    "jqwidgetsVer",
    "jqwidgets",
    "spreadsjs",
    "datatables",
    "datatables_old",
    "datatable",
    "PDFMerger",
    "bootstrap4",
    "fontawesome",
}

SUPERGLOBAL_RE = re.compile(r"\$_(GET|POST|REQUEST|FILES|COOKIE|SESSION)\s*\[\s*['\"]([^'\"]+)['\"]\s*\]")
INCLUDE_RE = re.compile(r"\b(?:include|include_once|require|require_once)\s*\(?\s*['\"]([^'\"]+)['\"]", re.I)
CLASS_RE = re.compile(r"^\s*(?:abstract\s+|final\s+)?class\s+\w+", re.M)
FUNCTION_RE = re.compile(r"^\s*function\s+\w+", re.M)
SQL_RE = re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|CALL|TRUNCATE|DROP|ALTER|CREATE)\b", re.I)
OUTPUT_RE = re.compile(r"\b(echo|print|json_encode|header\s*\(|readfile|fpassthru)\b", re.I)
CALLER_RE = re.compile(
    r"(?P<kind>url\s*:|\.load\s*\(|\$\.(?:post|get)\s*\(|fetch\s*\(|action\s*=)\s*['\"](?P<url>[^'\"]+?\.php(?:\?[^'\"]*)?)",
    re.I,
)
DESTRUCTIVE_RE = re.compile(
    r"\b(delete|eliminar|borrar|remove|destroy|anular|cancel|update|actualizar|guardar|insert|reset|duplicar|reasignar)\b",
    re.I,
)
UPLOAD_RE = re.compile(r"\$_FILES|move_uploaded_file|upload|carga\s*masiva|excel|xlsx|xls", re.I)
DOWNLOAD_RE = re.compile(r"readfile|fpassthru|Content-Disposition|generar_excel|export|download|descargar", re.I)
AUTH_RE = re.compile(r"permisos\.php|\$_SESSION|session_start|idusuario|usuarioaccesoproveedor|login|logout", re.I)
CSRF_RE = re.compile(r"csrf|nonce|xsrf|_token", re.I)
JSON_RE = re.compile(r"json_encode|Content-Type:\s*application/json", re.I)


def relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def excluded(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        parts = path.parts
    return any(part in EXCLUDE_SEGMENTS for part in parts)


def load_process_edges(root: Path) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    edge_file = root / ".brownfield" / "work" / "process_maps" / "process_edges.csv"
    reads: dict[str, set[str]] = defaultdict(set)
    writes: dict[str, set[str]] = defaultdict(set)
    if not edge_file.exists():
        return reads, writes

    with edge_file.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            source = row.get("from", "")
            target = row.get("to", "")
            typ = row.get("type", "")
            if not source.startswith("FILE:") or not target.startswith("DATA:"):
                continue
            file_path = source.removeprefix("FILE:").replace("\\", "/")
            table = target.removeprefix("DATA:")
            if typ == "reads":
                reads[file_path].add(table)
            elif typ == "writes":
                writes[file_path].add(table)
    return reads, writes


def scan_callers(root: Path) -> list[dict[str, str]]:
    callers: list[dict[str, str]] = []
    for suffix in ("*.php", "*.js"):
        for path in sorted(root.rglob(suffix)):
            if excluded(path, root):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            lines = text.splitlines()
            for line_no, line in enumerate(lines, start=1):
                for match in CALLER_RE.finditer(line):
                    callers.append(
                        {
                            "caller": relpath(path, root),
                            "line": str(line_no),
                            "kind": match.group("kind").strip(),
                            "url": match.group("url"),
                        }
                    )
    return callers


def clean_url(url: str) -> str:
    cleaned = url.split("?", 1)[0].split("#", 1)[0].replace("\\", "/").strip()
    while cleaned.startswith("../"):
        cleaned = cleaned[3:]
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned.lstrip("/").lower()


def caller_index(rows: list[dict[str, str]], callers: list[dict[str, str]]) -> dict[str, list[str]]:
    by_route: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        handler = row["handler"].lower()
        route = row["route"].lstrip("/").lower()
        for caller in callers:
            url = clean_url(caller["url"])
            if not url:
                continue
            if handler.endswith(url) or route.endswith(url):
                by_route[row["route"]].append(f"{caller['caller']}:{caller['line']}")
    return by_route


def unmatched_callers(rows: list[dict[str, str]], callers: list[dict[str, str]]) -> list[dict[str, str]]:
    unmatched: list[dict[str, str]] = []
    route_keys = [(row["handler"].lower(), row["route"].lstrip("/").lower()) for row in rows]
    for caller in callers:
        url = clean_url(caller["url"])
        if not url:
            continue
        if not any(handler.endswith(url) or route.endswith(url) for handler, route in route_keys):
            unmatched.append(caller)
    return unmatched


def is_endpoint_candidate(path: Path, text: str) -> bool:
    parts = [p.lower() for p in path.parts]
    name = path.name.lower()
    has_superglobal = bool(SUPERGLOBAL_RE.search(text))
    has_output = bool(OUTPUT_RE.search(text))
    is_ajax = "ajax" in parts or "ajaxasignacion" in parts
    is_page = name in {"index.php", "login.php", "logout.php"} or not (CLASS_RE.search(text) and not has_output)
    is_api_like = JSON_RE.search(text) or UPLOAD_RE.search(text) or DOWNLOAD_RE.search(text)
    return bool(is_ajax or (has_superglobal and has_output) or (is_page and (has_output or has_superglobal or is_api_like)))


def route_strength(path: Path, text: str) -> str:
    parts = [p.lower() for p in path.parts]
    name = path.name.lower()
    has_superglobal = bool(SUPERGLOBAL_RE.search(text))
    has_output = bool(OUTPUT_RE.search(text))
    if "ajax" in parts or "ajaxasignacion" in parts:
        return "strong_ajax_endpoint"
    if has_superglobal and has_output:
        return "strong_direct_endpoint"
    if name in {"index.php", "login.php", "logout.php"}:
        return "strong_page_endpoint"
    if CLASS_RE.search(text):
        return "public_php_logic_candidate"
    return "public_php_page_candidate"


def likely_third_party(path: Path) -> bool:
    rel = path.as_posix().lower()
    markers = [
        "/php-jwt-",
        "/bootstrap-filestyle/test/",
        "/libs/carbon/",
        "/libs/pdo/",
        "/libs/php/",
    ]
    return any(marker in rel for marker in markers)


def classify_methods(params: dict[str, set[str]]) -> str:
    methods: list[str] = []
    if params["POST"] or params["FILES"]:
        methods.append("POST")
    if params["GET"]:
        methods.append("GET")
    if params["REQUEST"]:
        methods.append("REQUEST")
    if not methods:
        methods.append("GET_OR_INCLUDE")
    return "|".join(methods)


def risk_flags(text: str, params: dict[str, set[str]], tables_written: set[str], path: str) -> list[str]:
    flags: list[str] = []
    if not CSRF_RE.search(text) and (params["POST"] or params["REQUEST"] or params["FILES"]):
        flags.append("POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL")
    if tables_written and not CSRF_RE.search(text):
        flags.append("DB_WRITE_WITHOUT_CSRF_SIGNAL")
    if DESTRUCTIVE_RE.search(path) or DESTRUCTIVE_RE.search(text):
        flags.append("DESTRUCTIVE_OR_MUTATING_ACTION")
    if UPLOAD_RE.search(text) or params["FILES"]:
        flags.append("FILE_UPLOAD_OR_IMPORT")
    if DOWNLOAD_RE.search(text):
        flags.append("FILE_DOWNLOAD_OR_EXPORT")
    if SQL_RE.search(text) and "prepare(" not in text.lower():
        flags.append("RAW_SQL_SIGNAL")
    if not AUTH_RE.search(text):
        flags.append("NO_LOCAL_AUTH_SIGNAL")
    if JSON_RE.search(text):
        flags.append("JSON_ENDPOINT")
    return sorted(set(flags))


def scan(root: Path) -> list[dict[str, str]]:
    reads, writes = load_process_edges(root)
    rows: list[dict[str, str]] = []

    for path in sorted(root.rglob("*.php")):
        if excluded(path, root):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not is_endpoint_candidate(path, text):
            continue

        rel = relpath(path, root)
        params: dict[str, set[str]] = defaultdict(set)
        for scope, key in SUPERGLOBAL_RE.findall(text):
            params[scope].add(key)
        includes = sorted(set(INCLUDE_RE.findall(text)))
        read_tables = sorted(reads.get(rel, set()))
        write_tables = sorted(writes.get(rel, set()))
        flags = risk_flags(text, params, set(write_tables), rel)

        rows.append(
            {
                "route": "/" + rel,
                "handler": rel,
                "route_strength": route_strength(path, text),
                "likely_third_party": str(likely_third_party(path)).lower(),
                "method": classify_methods(params),
                "params_get": ";".join(sorted(params["GET"])),
                "params_post": ";".join(sorted(params["POST"])),
                "params_request": ";".join(sorted(params["REQUEST"])),
                "params_files": ";".join(sorted(params["FILES"])),
                "uses_session": str("SESSION" in params or bool(re.search(r"\$_SESSION|session_start", text, re.I))).lower(),
                "auth_signal": "permisos.php" if re.search(r"permisos\.php", text, re.I) else ("session_or_login" if AUTH_RE.search(text) else ""),
                "csrf_signal": str(bool(CSRF_RE.search(text))).lower(),
                "json_signal": str(bool(JSON_RE.search(text))).lower(),
                "upload_signal": str(bool(UPLOAD_RE.search(text) or params["FILES"])).lower(),
                "download_signal": str(bool(DOWNLOAD_RE.search(text))).lower(),
                "sql_signal": str(bool(SQL_RE.search(text))).lower(),
                "tables_read": ";".join(read_tables),
                "tables_written": ";".join(write_tables),
                "includes": ";".join(includes),
                "caller_refs": "0",
                "caller_sources": "",
                "risk_flags": ";".join(flags),
                "confidence": "inferred_file_route",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "route",
        "handler",
        "route_strength",
        "likely_third_party",
        "method",
        "params_get",
        "params_post",
        "params_request",
        "params_files",
        "uses_session",
        "auth_signal",
        "csrf_signal",
        "json_signal",
        "upload_signal",
        "download_signal",
        "sql_signal",
        "tables_read",
        "tables_written",
        "includes",
        "caller_refs",
        "caller_sources",
        "risk_flags",
        "confidence",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_callers_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["caller", "line", "kind", "url"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def endpoint_group(handler: str) -> str:
    parts = handler.split("/")
    if len(parts) >= 3 and parts[0] == "index_archivos":
        return parts[1]
    if len(parts) >= 2:
        return parts[0]
    return "(root)"


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    by_group = Counter(endpoint_group(row["handler"]) for row in rows)
    by_strength = Counter(row["route_strength"] for row in rows)
    caller_linked = [r for r in rows if r.get("caller_refs") and r["caller_refs"] != "0"]
    post_without_csrf = [r for r in rows if "POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL" in r["risk_flags"]]
    db_write_without_csrf = [r for r in rows if "DB_WRITE_WITHOUT_CSRF_SIGNAL" in r["risk_flags"]]
    upload_routes = [r for r in rows if r["upload_signal"] == "true"]
    no_auth = [r for r in rows if "NO_LOCAL_AUTH_SIGNAL" in r["risk_flags"]]

    lines = [
        "# HTTP Endpoint Catalog - PHP direct routes",
        "",
        "Status: AUGMENTED_DETERMINISTIC_SCAN",
        "",
        "Brownfield's native route extractor reports zero route declarations for this legacy codebase.",
        "This catalog corrects that blind spot by treating public PHP files and AJAX scripts as file-routed HTTP endpoints.",
        "",
        "## Summary",
        "",
        f"- Endpoint candidates: {len(rows)}",
        f"- Strong AJAX endpoints: {by_strength['strong_ajax_endpoint']}",
        f"- Strong direct endpoints: {by_strength['strong_direct_endpoint']}",
        f"- Public PHP logic candidates: {by_strength['public_php_logic_candidate']}",
        f"- Likely third-party/test endpoints: {sum(r['likely_third_party'] == 'true' for r in rows)}",
        f"- Endpoints referenced by frontend/PHP callers: {len(caller_linked)}",
        f"- POST/REQUEST endpoints without local CSRF signal: {len(post_without_csrf)}",
        f"- DB-writing endpoints without local CSRF signal: {len(db_write_without_csrf)}",
        f"- Upload/import endpoints: {len(upload_routes)}",
        f"- Endpoints without local auth/session signal: {len(no_auth)}",
        "",
        "## Endpoint groups",
        "",
        "| Group | Endpoints |",
        "| --- | ---: |",
    ]
    for group, count in by_group.most_common():
        lines.append(f"| `{group}` | {count} |")

    lines.extend(
        [
            "",
            "## Highest risk candidates",
            "",
            "| Route | Method | Caller refs | Tables written | Flags |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    def score(row: dict[str, str]) -> int:
        return len(row["risk_flags"].split(";")) + (3 if row["tables_written"] else 0) + (2 if row["upload_signal"] == "true" else 0)

    for row in sorted(rows, key=score, reverse=True)[:40]:
        lines.append(
            "| `{}` | `{}` | {} | `{}` | `{}` |".format(
                row["route"],
                row["method"],
                row.get("caller_refs", "0"),
                row["tables_written"] or "",
                row["risk_flags"],
            )
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `auth_signal` is local evidence only. Included files may enforce authorization indirectly.",
            "- `csrf_signal` is based on token naming patterns. Absence is a review finding, not final proof of exploitability.",
            "- Table reads/writes are imported from Brownfield process edges when available.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_route_matrix(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "route",
                "handler",
                "method",
                "confidence",
                "route_strength",
                "likely_third_party",
                "auth_signal",
                "csrf_signal",
                "tables_read",
                "tables_written",
                "caller_refs",
                "caller_sources",
                "risk_flags",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in writer.fieldnames})


def write_findings(path: Path, rows: list[dict[str, str]], unmatched: list[dict[str, str]]) -> None:
    counters = {
        "post_without_csrf": sum("POST_OR_REQUEST_WITHOUT_CSRF_SIGNAL" in r["risk_flags"] for r in rows),
        "db_write_without_csrf": sum("DB_WRITE_WITHOUT_CSRF_SIGNAL" in r["risk_flags"] for r in rows),
        "upload_routes": sum(r["upload_signal"] == "true" for r in rows),
        "no_auth": sum("NO_LOCAL_AUTH_SIGNAL" in r["risk_flags"] for r in rows),
        "json_routes": sum(r["json_signal"] == "true" for r in rows),
    }
    lines = [
        "# Endpoint Findings - augmented pass",
        "",
        "Status: REVIEW_REQUIRED",
        "",
        "New findings produced after correcting Brownfield's zero-route blind spot:",
        "",
        f"- Direct PHP/AJAX endpoint candidates found: {len(rows)}",
        f"- Strong AJAX endpoint candidates: {sum(r['route_strength'] == 'strong_ajax_endpoint' for r in rows)}",
        f"- Strong direct endpoint candidates: {sum(r['route_strength'] == 'strong_direct_endpoint' for r in rows)}",
        f"- Public PHP logic candidates exposed under webroot: {sum(r['route_strength'] == 'public_php_logic_candidate' for r in rows)}",
        f"- Likely third-party/test candidates to exclude or block at web server: {sum(r['likely_third_party'] == 'true' for r in rows)}",
        f"- Endpoint candidates referenced by frontend/PHP callers: {sum(r.get('caller_refs', '0') != '0' for r in rows)}",
        f"- PHP caller references not matched to scanned endpoint candidates: {len(unmatched)}",
        f"- POST/REQUEST endpoints without local CSRF signal: {counters['post_without_csrf']}",
        f"- DB-writing endpoints without local CSRF signal: {counters['db_write_without_csrf']}",
        f"- Upload/import endpoints requiring file validation review: {counters['upload_routes']}",
        f"- JSON endpoints: {counters['json_routes']}",
        f"- Endpoints without local auth/session evidence: {counters['no_auth']}",
        "",
        "Top corrective action: use this catalog instead of Brownfield's native zero-route output when auditing HTTP exposure.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_unmatched_callers(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["caller", "line", "kind", "url"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    rows = scan(root)
    callers = scan_callers(root)
    refs = caller_index(rows, callers)
    unmatched = unmatched_callers(rows, callers)
    for row in rows:
        sources = sorted(set(refs.get(row["route"], [])))
        row["caller_refs"] = str(len(sources))
        row["caller_sources"] = ";".join(sources[:25])
    custom_dir = root / ".brownfield" / "work" / "custom"
    write_csv(custom_dir / "http_endpoint_catalog.csv", rows)
    write_callers_csv(custom_dir / "frontend_endpoint_callers.csv", callers)
    write_unmatched_callers(custom_dir / "unmatched_php_callers.csv", unmatched)
    write_markdown(custom_dir / "HTTP_ENDPOINT_CATALOG_AUGMENTED.md", rows)
    write_findings(custom_dir / "ENDPOINT_FINDINGS_AUGMENTED.md", rows, unmatched)

    release_dir = root / ".brownfield" / "work" / "release" / "engineering-analysis" / "interfaces"
    write_markdown(release_dir / "HTTP_ENDPOINT_CATALOG.md", rows)
    write_route_matrix(release_dir / "ROUTE_TO_HANDLER_MATRIX.csv", rows)

    summary = {
        "endpoint_candidates": len(rows),
        "frontend_php_call_references": len(callers),
        "endpoints_with_caller_references": sum(row.get("caller_refs", "0") != "0" for row in rows),
        "unmatched_php_call_references": len(unmatched),
        "output_dir": str(custom_dir),
        "release_http_catalog": str(release_dir / "HTTP_ENDPOINT_CATALOG.md"),
        "release_route_matrix": str(release_dir / "ROUTE_TO_HANDLER_MATRIX.csv"),
    }
    (custom_dir / "endpoint_scan_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
