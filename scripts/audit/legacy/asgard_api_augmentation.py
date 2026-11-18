#!/usr/bin/env python3
"""Augment asgard-api-auditor output for legacy PHP file-routed APIs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


EXCLUDE_SEGMENTS = {
    ".git",
    ".brownfield",
    "graphify-out",
    "node_modules",
    "vendor",
    "PHPExcel",
    "MPDF57",
    "PDFMerger",
    "jqwidgetsVer",
    "jqwidgets",
    "spreadsjs",
    "datatables",
    "datatable",
    "datatables_old",
    "fontawesome",
    "jqGrid",
    "carbon",
    "Carbon",
    "php-jwt-5.2.0",
}

EXCLUDE_FILE_MARKERS = {
    ".min.js",
    "ext-all",
    "kendo",
    "jquery",
    "bootstrap",
    "select2",
    "sweetalert",
    "moment",
    "popper",
    "chart",
    "ckeditor",
    "plugins",
    "assets/vendor",
    "vue-google-maps",
    "vue-json-excel",
    "vue-draggable",
    "vue.draggable",
    "leaflet",
    "geosearch",
    "magnific-popup",
    "fvalidate",
    "loadingoverlay",
    "modernizr",
    "grid.locale-",
    "resetpassword/js/vue.js",
}

STATIC_URL_SUFFIXES = (
    ".css",
    ".js",
    ".map",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".pdf",
    ".dtd",
)

HTTP_URL_RE = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+")
PHP_CONST_RE = re.compile(r"define\s*\(\s*['\"]([A-Z0-9_]*(?:API|URL|URI|HOST|FILES)[A-Z0-9_]*)['\"]\s*,\s*([^;]+?)\s*\)", re.I)
CONST_API_CALL_RE = re.compile(r"(?P<constant>[A-Z0-9_]*(?:API|URL)[A-Z0-9_]*)\s*(?:\.\s*|\+\s*)['\"](?P<path>[^'\"]+)['\"]")
PHP_ECHO_CONST_URL_RE = re.compile(r"<\?=\s*(?P<constant>[A-Z0-9_]*(?:API|URL)[A-Z0-9_]*)\s*\?>\s*(?P<path>[^'\",\s]*)")
PHP_ECHO_CONST_LONG_RE = re.compile(r"<\?(?:php\s+)?echo\s+(?P<constant>[A-Z0-9_]*(?:API|URL|FILES)[A-Z0-9_]*)\s*;?\s*\?>\s*(?P<path>[^'\",\s]*)")
LOCAL_CONST_URL_ASSIGN_RE = re.compile(r"(?P<var>\$[A-Za-z_]\w*)\s*=\s*(?P<constant>[A-Z0-9_]*(?:API|URL)[A-Z0-9_]*)\s*(?:\.\s*|\+\s*)['\"](?P<path>[^'\"]+)['\"]")
GUZZLE_CREATE_RE = re.compile(r"createRequest\s*\(\s*['\"](?P<method>[A-Z]+)['\"]\s*,\s*(?P<target>\$[A-Za-z_]\w*|[A-Z0-9_]+(?:\s*\.\s*['\"][^'\"]+['\"])?)", re.I)
RESPONSE_STATUS_RE = re.compile(r"\b(http_response_code|header\s*\(\s*['\"]HTTP/|->withStatus\s*\()", re.I)
JSON_OUT_RE = re.compile(r"json_encode|Content-Type:\s*application/json", re.I)
REDIRECT_RE = re.compile(r"header\s*\(\s*['\"]Location:", re.I)
MYSQL_ERROR_RE = re.compile(r"mysql_error\s*\(|or\s+die\s*\(", re.I)
HTTP_CLIENT_CONTEXT_RE = re.compile(r"fetch\s*\(|axios\.|axios\s*\(|\$\.(?:ajax|get|post)|curl_setopt|CURLOPT_URL|createRequest|url\s*:|action\s*=|api|geocode|sendgrid|tracking|documents", re.I)


def excluded(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        parts = path.parts
    rel_lower = "/".join(parts).lower()
    return any(part in EXCLUDE_SEGMENTS for part in parts) or any(marker in rel_lower for marker in EXCLUDE_FILE_MARKERS)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def stable_id(*parts: str) -> str:
    return "aug_" + hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:20]


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def scan_constants(root: Path) -> dict[str, str]:
    constants: dict[str, str] = {}
    for path in sorted(root.rglob("*.php")) + sorted(root.glob(".env*.php")):
        if excluded(path, root):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for name, expr in PHP_CONST_RE.findall(text):
            url = HTTP_URL_RE.search(expr)
            if url:
                constants[name] = url.group(0).rstrip("'\"),")
    return constants


def normalize_join(base: str, suffix_path: str) -> str:
    base = base.rstrip("/")
    suffix_path = suffix_path.lstrip()
    if suffix_path and not suffix_path.startswith(("/", "?", "#")):
        suffix_path = "/" + suffix_path
    return base + suffix_path


def is_likely_api_url(url: str, line: str) -> bool:
    lowered_url = url.lower().rstrip("'\"),;")
    lowered_line = line.lower()
    if lowered_url in {"http://", "https://"}:
        return False
    try:
        parsed = urlparse(lowered_url)
    except ValueError:
        return False
    host = parsed.netloc
    if any(marker in host for marker in ("w3.org", "github.com", "fonts.googleapis.com", "cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com", "v2.vuejs.org")):
        return False
    if host == "maps.google.com" and "/mapfiles/" in parsed.path:
        return False
    if lowered_url.endswith(STATIC_URL_SUFFIXES) and "maps.googleapis.com/maps/api/js" not in lowered_url:
        return False
    if any(marker in lowered_line for marker in ("<script", "<link", "xmlns", "doctype", "license")) and "maps.googleapis.com/maps/api/js" not in lowered_url:
        return False
    if any(marker in lowered_url for marker in ("api.", "/api/", "maps.googleapis.com/maps/api", "sendgrid.com/v3", "developer1.kpogroup", "api-documents", "ip-api.com/json")):
        return True
    if HTTP_CLIENT_CONTEXT_RE.search(line):
        return True
    return False


def extract_file_var_targets(text: str, constants: dict[str, str]) -> dict[str, dict[str, str]]:
    targets: dict[str, dict[str, str]] = {}
    for line_no, line in enumerate(text.splitlines(), start=1):
        match = LOCAL_CONST_URL_ASSIGN_RE.search(line)
        if not match:
            continue
        const = match.group("constant")
        suffix_path = match.group("path")
        targets[match.group("var")] = {
            "url": normalize_join(constants.get(const, f"UNRESOLVED_CONST:{const}"), suffix_path),
            "constant": const,
            "line": str(line_no),
            "base_source": "local_var_constant_concat",
        }
    return targets


def method_from_match_or_line(match_method: str | None, line: str) -> str:
    return match_method.upper() if match_method else infer_method(line)


def scan_consumed(root: Path, constants: dict[str, str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for suffix in ("*.php", "*.js"):
        for path in sorted(root.rglob(suffix)):
            if excluded(path, root):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            var_targets = extract_file_var_targets(text, constants)
            lines = text.splitlines()
            for line_no, line in enumerate(lines, start=1):
                context_block = "\n".join(lines[max(0, line_no - 1): min(len(lines), line_no + 12)])
                for url in HTTP_URL_RE.findall(line):
                    url = url.rstrip("'\"),;")
                    if not is_likely_api_url(url, line):
                        continue
                    rows.append(
                        {
                            "endpoint_id": stable_id("direct", url, str(line_no), rel(path, root)),
                            "method": infer_method(line),
                            "url": url,
                            "base_source": "literal_url",
                            "constant": "",
                            "file": rel(path, root),
                            "line": str(line_no),
                            "risk_flags": consumed_flags(url, context_block),
                        }
                    )
                for match in CONST_API_CALL_RE.finditer(line):
                    const = match.group("constant")
                    suffix_path = match.group("path")
                    if not HTTP_CLIENT_CONTEXT_RE.search(line) and suffix_path == "":
                        continue
                    rows.append(
                        {
                            "endpoint_id": stable_id("constant", const, suffix_path, str(line_no), rel(path, root)),
                            "method": infer_method(line),
                            "url": normalize_join(constants.get(const, f"UNRESOLVED_CONST:{const}"), suffix_path),
                            "base_source": "constant_concat",
                            "constant": const,
                            "file": rel(path, root),
                            "line": str(line_no),
                            "risk_flags": consumed_flags(constants.get(const, ""), context_block) + (";UNRESOLVED_BASE_CONSTANT" if const not in constants else ""),
                        }
                    )
                for match in PHP_ECHO_CONST_URL_RE.finditer(line):
                    const = match.group("constant")
                    suffix_path = match.group("path")
                    if not HTTP_CLIENT_CONTEXT_RE.search(line) and suffix_path == "":
                        continue
                    rows.append(
                        {
                            "endpoint_id": stable_id("php_echo_constant", const, suffix_path, str(line_no), rel(path, root)),
                            "method": infer_method(line),
                            "url": normalize_join(constants.get(const, f"UNRESOLVED_CONST:{const}"), suffix_path),
                            "base_source": "php_echo_constant",
                            "constant": const,
                            "file": rel(path, root),
                            "line": str(line_no),
                            "risk_flags": consumed_flags(constants.get(const, ""), context_block) + (";UNRESOLVED_BASE_CONSTANT" if const not in constants else ""),
                        }
                    )
                for match in PHP_ECHO_CONST_LONG_RE.finditer(line):
                    const = match.group("constant")
                    suffix_path = match.group("path")
                    if not HTTP_CLIENT_CONTEXT_RE.search(line) and suffix_path == "":
                        continue
                    rows.append(
                        {
                            "endpoint_id": stable_id("php_echo_constant_long", const, suffix_path, str(line_no), rel(path, root)),
                            "method": infer_method(line),
                            "url": normalize_join(constants.get(const, f"UNRESOLVED_CONST:{const}"), suffix_path),
                            "base_source": "php_echo_constant",
                            "constant": const,
                            "file": rel(path, root),
                            "line": str(line_no),
                            "risk_flags": consumed_flags(constants.get(const, ""), context_block) + (";UNRESOLVED_BASE_CONSTANT" if const not in constants else ""),
                        }
                    )
                for match in GUZZLE_CREATE_RE.finditer(line):
                    target = match.group("target").replace(" ", "")
                    const_match = CONST_API_CALL_RE.search(target)
                    if const_match:
                        const = const_match.group("constant")
                        endpoint_url = normalize_join(constants.get(const, f"UNRESOLVED_CONST:{const}"), const_match.group("path"))
                        row_const = const
                        source = "guzzle_create_request_constant_concat"
                    elif target in var_targets:
                        endpoint_url = var_targets[target]["url"]
                        row_const = var_targets[target]["constant"]
                        source = "guzzle_create_request_local_var"
                    else:
                        endpoint_url = f"UNRESOLVED_DYNAMIC:{target}"
                        row_const = ""
                        source = "guzzle_create_request_dynamic"
                    rows.append(
                        {
                            "endpoint_id": stable_id("guzzle", endpoint_url, str(line_no), rel(path, root)),
                            "method": method_from_match_or_line(match.group("method"), line),
                            "url": endpoint_url,
                            "base_source": source,
                            "constant": row_const,
                            "file": rel(path, root),
                            "line": str(line_no),
                            "risk_flags": consumed_flags(endpoint_url, context_block) + (";UNRESOLVED_BASE_CONSTANT" if endpoint_url.startswith("UNRESOLVED_CONST:") else ""),
                        }
                    )
    return dedupe_consumed(rows)


def infer_method(line: str) -> str:
    low = line.lower()
    if "post" in low or "type: 'post'" in low or 'type: "post"' in low or "method: 'post'" in low or 'method: "post"' in low:
        return "POST"
    if "put" in low:
        return "PUT"
    if "delete" in low:
        return "DELETE"
    return "GET_OR_UNKNOWN"


def consumed_flags(url: str, line: str) -> str:
    flags: list[str] = []
    if url.startswith("http://"):
        flags.append("PLAINTEXT_HTTP")
    if "key=" in line.lower() or "token" in line.lower() or "authorization" in line.lower():
        flags.append("CREDENTIAL_OR_KEY_IN_CALL")
    if "verify' => false" in line.lower() or '"verify" => false' in line.lower():
        flags.append("TLS_VERIFY_DISABLED")
    if "UNRESOLVED_CONST:" in url:
        flags.append("UNRESOLVED_BASE_CONSTANT")
    return ";".join(sorted(set(flags)))


def dedupe_consumed(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], dict[str, str]] = {}
    evidence: defaultdict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        row["risk_flags"] = ";".join(sorted({flag for flag in row["risk_flags"].split(";") if flag}))
        key = (row["method"], row["url"])
        evidence[key].add(f"{row['file']}:{row['line']}")
        if key not in grouped:
            grouped[key] = row
            continue
        merged_flags = sorted({flag for flag in (grouped[key]["risk_flags"] + ";" + row["risk_flags"]).split(";") if flag})
        grouped[key]["risk_flags"] = ";".join(merged_flags)
        if not grouped[key]["constant"] and row["constant"]:
            grouped[key]["constant"] = row["constant"]
        if row["base_source"] not in grouped[key]["base_source"].split(";"):
            grouped[key]["base_source"] += ";" + row["base_source"]
    out = []
    for key in sorted(grouped):
        row = grouped[key]
        ordered_evidence = sorted(evidence[key])
        samples = ordered_evidence[:10]
        row["evidence_count"] = str(len(ordered_evidence))
        row["evidence_samples"] = ";".join(samples)
        out.append(row)
    return out


def response_profile(root: Path, handler: str) -> dict[str, str]:
    path = root / handler
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        text = ""
    return {
        "json_response_signal": str(bool(JSON_OUT_RE.search(text))).lower(),
        "explicit_status_signal": str(bool(RESPONSE_STATUS_RE.search(text))).lower(),
        "redirect_signal": str(bool(REDIRECT_RE.search(text))).lower(),
        "mysql_error_leak_signal": str(bool(MYSQL_ERROR_RE.search(text))).lower(),
    }


def provider_catalog(root: Path, endpoint_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    providers: list[dict[str, object]] = []
    for row in endpoint_rows:
        methods = [m for m in row["method"].split("|") if m and m != "GET_OR_INCLUDE"] or ["GET"]
        profile = response_profile(root, row["handler"])
        providers.append(
            {
                "endpoint_id": stable_id("provider", row["route"], row["method"]),
                "direction": "exposed",
                "route": row["route"],
                "handler": row["handler"],
                "methods": methods,
                "route_strength": row.get("route_strength", ""),
                "auth_signal": row.get("auth_signal", ""),
                "csrf_signal": row.get("csrf_signal", ""),
                "json_signal": row.get("json_signal", ""),
                "upload_signal": row.get("upload_signal", ""),
                "download_signal": row.get("download_signal", ""),
                "tables_read": split_semicolon(row.get("tables_read", "")),
                "tables_written": split_semicolon(row.get("tables_written", "")),
                "params": {
                    "get": split_semicolon(row.get("params_get", "")),
                    "post": split_semicolon(row.get("params_post", "")),
                    "request": split_semicolon(row.get("params_request", "")),
                    "files": split_semicolon(row.get("params_files", "")),
                },
                "caller_refs": int(row.get("caller_refs") or 0),
                "caller_sources": split_semicolon(row.get("caller_sources", "")),
                "risk_flags": split_semicolon(row.get("risk_flags", "")),
                "response_profile": profile,
                "confidence": "augmented_file_route",
            }
        )
    return providers


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def write_openapi(path: Path, providers: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "openapi: 3.0.3",
        "info:",
        "  title: proveedores-master_peru augmented file-routed API",
        "  version: 0.1.0",
        "  description: Provisional OpenAPI generated from PHP direct-route evidence; review required.",
        "paths:",
    ]
    for ep in providers:
        route = str(ep["route"])
        if not route.startswith("/"):
            route = "/" + route
        lines.append(f"  {json.dumps(route)}:")
        for method in ep["methods"]:
            m = str(method).lower()
            if m == "request":
                m = "post"
            lines.extend(
                [
                    f"    {m}:",
                    f"      operationId: {ep['endpoint_id']}_{m}",
                    "      summary: Provisional PHP file route",
                    "      x-asgard-augmented-confidence: augmented_file_route",
                    f"      x-handler: {json.dumps(ep['handler'])}",
                    f"      x-route-strength: {json.dumps(ep['route_strength'])}",
                    f"      x-caller-refs: {ep['caller_refs']}",
                    f"      x-risk-flags: {json.dumps(ep['risk_flags'])}",
                    "      responses:",
                    "        '200':",
                    "          description: Response observed from legacy PHP route; schema not proven.",
                ]
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_security_matrix(path: Path, providers: list[dict[str, object]]) -> None:
    rows: list[dict[str, str]] = []
    for ep in providers:
        prof = ep["response_profile"]  # type: ignore[index]
        rows.append(
            {
                "route": str(ep["route"]),
                "methods": "|".join(ep["methods"]),  # type: ignore[arg-type]
                "handler": str(ep["handler"]),
                "auth_signal": str(ep["auth_signal"]),
                "csrf_signal": str(ep["csrf_signal"]),
                "caller_refs": str(ep["caller_refs"]),
                "json_response_signal": prof["json_response_signal"],  # type: ignore[index]
                "explicit_status_signal": prof["explicit_status_signal"],  # type: ignore[index]
                "mysql_error_leak_signal": prof["mysql_error_leak_signal"],  # type: ignore[index]
                "tables_written": ";".join(ep["tables_written"]),  # type: ignore[arg-type]
                "risk_flags": ";".join(ep["risk_flags"]),  # type: ignore[arg-type]
            }
        )
    write_csv(
        path,
        rows,
        [
            "route",
            "methods",
            "handler",
            "auth_signal",
            "csrf_signal",
            "caller_refs",
            "json_response_signal",
            "explicit_status_signal",
            "mysql_error_leak_signal",
            "tables_written",
            "risk_flags",
        ],
    )


def write_markdown(path: Path, native: dict[str, object], providers: list[dict[str, object]], consumed: list[dict[str, str]]) -> None:
    native_supplied = bool(native)
    native_endpoints = native.get("endpoints", []) if isinstance(native.get("endpoints"), list) else []
    exposed = [ep for ep in native_endpoints if ep.get("direction") == "exposed"]
    native_consumed = [ep for ep in native_endpoints if ep.get("direction") == "consumed"]
    by_strength = Counter(str(ep["route_strength"]) for ep in providers)
    by_group = Counter(str(ep["route"]).split("/")[2] if str(ep["route"]).startswith("/index_archivos/") and len(str(ep["route"]).split("/")) > 2 else "(root)" for ep in providers)
    consumed_flags = Counter(flag for row in consumed for flag in row["risk_flags"].split(";") if flag)
    no_status = [ep for ep in providers if ep["response_profile"]["explicit_status_signal"] == "false"]  # type: ignore[index]
    mysql_error = [ep for ep in providers if ep["response_profile"]["mysql_error_leak_signal"] == "true"]  # type: ignore[index]
    active_write = [ep for ep in providers if ep["caller_refs"] and ep["tables_written"]]  # type: ignore[truthy-function]
    upload_or_import = [ep for ep in providers if "FILE_UPLOAD_OR_IMPORT" in ep["risk_flags"]]  # type: ignore[operator]

    lines = [
        "# ASGARD API Auditor - augmented iterative audit",
        "",
        "Status: REVIEW_REQUIRED",
        "",
        "Static augmentation for a legacy PHP file-routed application. Native findings are included only when an actual native findings file was supplied.",
        "",
        "## Native ASGARD result",
        "",
        f"- Status: `{native.get('status', 'not_executed_no_findings_supplied')}`",
        f"- Native exposed endpoints: {len(exposed) if native_supplied else 'not measured'}",
        f"- Native consumed endpoints: {len(native_consumed) if native_supplied else 'not measured'}",
        f"- Native unresolved items: {len(native.get('unresolved', [])) if native_supplied and isinstance(native.get('unresolved'), list) else 'not measured'}",
        "",
        "## Augmented provider surface",
        "",
        f"- PHP/AJAX exposed endpoint candidates: {len(providers)}",
        f"- Endpoints referenced by frontend/PHP callers: {sum(1 for ep in providers if int(ep['caller_refs']))}",
        f"- Endpoints writing database tables: {sum(1 for ep in providers if ep['tables_written'])}",
        f"- Active caller + DB-write endpoints: {len(active_write)}",
        f"- Endpoints with upload/import signal: {len(upload_or_import)}",
        f"- Endpoints without explicit status-code signal: {len(no_status)}",
        f"- Endpoints with `mysql_error()` / `die()` leak signal: {len(mysql_error)}",
        "",
        "## Provider route strength",
        "",
        "| Strength | Count |",
        "| --- | ---: |",
    ]
    for name, count in by_strength.most_common():
        lines.append(f"| `{name}` | {count} |")

    lines.extend(["", "## Provider groups", "", "| Group | Count |", "| --- | ---: |"])
    for name, count in by_group.most_common():
        lines.append(f"| `{name}` | {count} |")

    lines.extend(["", "## Augmented consumed API surface", "", f"- Consumed call candidates: {len(consumed)}", "", "| Flag | Count |", "| --- | ---: |"])
    for name, count in consumed_flags.most_common():
        lines.append(f"| `{name}` | {count} |")

    lines.extend(["", "## Consumed calls", "", "| Method | URL | Evidence count | Evidence samples | Flags |", "| --- | --- | ---: | --- | --- |"])
    for row in consumed[:60]:
        lines.append(f"| `{row['method']}` | `{row['url']}` | {row.get('evidence_count', '1')} | `{row.get('evidence_samples', row['file'] + ':' + row['line'])}` | `{row['risk_flags']}` |")

    lines.extend(["", "## Active DB-writing API candidates", "", "| Route | Methods | Callers | Tables written | Flags |", "| --- | --- | ---: | --- | --- |"])
    for ep in active_write[:80]:
        lines.append(
            f"| `{ep['route']}` | `{'|'.join(ep['methods'])}` | {ep['caller_refs']} | `{' ; '.join(ep['tables_written'])}` | `{' ; '.join(ep['risk_flags'])}` |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--native-findings", default=".brownfield/work/custom/asgard-api-audit-v2/findings.json")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out = root / ".brownfield" / "work" / "custom" / "asgard-api-audit-augmented"
    native_path = root / args.native_findings
    native = json.loads(native_path.read_text(encoding="utf-8")) if native_path.exists() else {}

    endpoint_rows = read_csv(root / ".brownfield" / "work" / "custom" / "http_endpoint_catalog.csv")
    constants = scan_constants(root)
    consumed = scan_consumed(root, constants)
    providers = provider_catalog(root, endpoint_rows)

    out.mkdir(parents=True, exist_ok=True)
    (out / "api-catalog.augmented.json").write_text(
        json.dumps(
            {
                "schema_version": "augmented-0.1",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "native_findings": str(native_path) if native_path.exists() else None,
                "native_status": native.get("status", "not_executed_no_findings_supplied"),
                "constants_resolved": constants,
                "providers": providers,
                "consumed": consumed,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    write_csv(out / "consumed_api_augmented.csv", consumed, ["endpoint_id", "method", "url", "base_source", "constant", "file", "line", "evidence_count", "evidence_samples", "risk_flags"])
    write_security_matrix(out / "api_endpoint_security_matrix.csv", providers)
    write_openapi(out / "openapi.augmented.yaml", providers)
    write_markdown(out / "ASGARD_API_AUDIT_AUGMENTED.md", native, providers, consumed)

    summary = {
        "native_status": native.get("status", "not_executed_no_findings_supplied"),
        "native_endpoints": len(native.get("endpoints", [])) if isinstance(native.get("endpoints"), list) else None,
        "augmented_provider_endpoints": len(providers),
        "augmented_consumed_calls": len(consumed),
        "output": str(out),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
