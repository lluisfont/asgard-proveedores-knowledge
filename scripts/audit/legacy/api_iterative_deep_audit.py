#!/usr/bin/env python3
"""Extra API audit passes for legacy PHP endpoint catalogs."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ENDPOINT_CATALOG = Path(".brownfield/work/custom/http_endpoint_catalog.csv")
ASGARD_CONSUMED = Path(".brownfield/work/custom/asgard-api-audit-augmented/consumed_api_augmented.csv")
DANGEROUS_SINKS = Path(".brownfield/work/custom/dangerous_php_sinks.csv")
UPLOAD_FINDINGS = Path(".brownfield/work/custom/upload_security_findings.csv")
SQL_TAINT_FINDINGS = Path(".brownfield/work/custom/sql_taint_findings.csv")
SENSITIVE_COLUMNS = Path(".brownfield/work/custom/sensitive_column_findings.csv")
FK_GAPS = Path(".brownfield/work/custom/fk_gap_findings.csv")

IDOR_PARAM_RE = re.compile(r"(^id|id$|embarque|viaje|proveedor|cliente|operador|transportista|usuario|documento|archivo|pedido|orden|journey|location)", re.I)
OWNERSHIP_RE = re.compile(r"(_SESSION|idusuario|idproveedor|idoperador|idcliente|proveedor_id|cliente_id|created_by|updated_by|alcance|scope)", re.I)
PATH_SINK_RE = re.compile(r"\b(readfile|fopen|file_get_contents|unlink|copy|rename|move_uploaded_file|ZipArchive|Content-Disposition|download)\b", re.I)
PATH_PARAM_RE = re.compile(r"(archivo|file|path|ruta|documento|nombre|adjunto|xls|excel|pdf|zip)", re.I)
PASSWORD_PARAM_RE = re.compile(r"(password|passwd|pwd|pass|contrasena|contrase|clave)", re.I)
AUTH_INCLUDE_RE = re.compile(r"(veriflogin|permisos|validar|session_start|_SESSION)", re.I)
WEAK_METHOD_RE = re.compile(r"^(POST|REQUEST|POST\|GET|POST\|REQUEST|POST\|GET\|REQUEST)$")
DEV_EGRESS_RE = re.compile(r"(dev|developer|181\.188\.187\.222|http://)", re.I)
SECRET_RE = re.compile(r"(token|secret|password|passwd|pwd|key|Authorization|Bearer|AIza|SG\.)", re.I)
TABLE_RE = re.compile(r"\b(?:FROM|JOIN|UPDATE|INTO|DELETE\s+FROM)\s+`?([A-Za-z0-9_]+)`?", re.I)


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


def file_text(root: Path, handler: str) -> str:
    try:
        return (root / handler).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def stable_id(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


def split(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def endpoint_params(row: dict[str, str]) -> list[str]:
    params: list[str] = []
    for field in ("params_get", "params_post", "params_request", "params_files"):
        params.extend(split(row.get(field, "")))
    return sorted(set(params))


def risk_score(flags: list[str]) -> int:
    weights = {
        "DB_WRITE": 30,
        "NO_CSRF": 25,
        "NO_LOCAL_AUTH": 20,
        "CALLER_REFERENCED": 12,
        "IDOR_CANDIDATE": 20,
        "PATH_TRAVERSAL_CANDIDATE": 20,
        "DANGEROUS_SINK": 30,
        "UPLOAD_IMPORT": 18,
        "SENSITIVE_TABLE_ACCESS": 16,
        "FK_GAP_TABLE_ACCESS": 10,
        "DEV_OR_PLAINTEXT_EGRESS": 12,
        "SECRET_IN_CONTEXT": 14,
        "TLS_VERIFY_DISABLED": 16,
        "UNRESOLVED_BASE_CONSTANT": 10,
        "SQL_TAINT": 28,
        "LEGACY_MYSQL_API": 12,
        "PASSWORD_CHANGE_NO_LOCAL_AUTH": 26,
    }
    return sum(weights.get(flag, 0) for flag in flags)


def endpoint_deep_rows(
    root: Path,
    endpoints: list[dict[str, str]],
    sink_by_file: dict[str, list[dict[str, str]]],
    sql_by_file: dict[str, list[dict[str, str]]],
    upload_by_file: set[str],
    sensitive_tables: set[str],
    fk_gap_tables: set[str],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for ep in endpoints:
        handler = ep["handler"]
        text = file_text(root, handler)
        params = endpoint_params(ep)
        tables = set(split(ep.get("tables_read", "")) + split(ep.get("tables_written", "")))
        text_tables = set(TABLE_RE.findall(text))
        all_tables = tables | text_tables
        idor_params = [p for p in params if IDOR_PARAM_RE.search(p)]
        path_params = [p for p in params if PATH_PARAM_RE.search(p)]
        has_ownership = bool(OWNERSHIP_RE.search(text))
        has_auth_include = bool(AUTH_INCLUDE_RE.search(text)) or ep.get("auth_signal") not in ("", "none")
        has_path_sink = bool(PATH_SINK_RE.search(text))
        flags: list[str] = []
        if ep.get("tables_written"):
            flags.append("DB_WRITE")
        if WEAK_METHOD_RE.search(ep.get("method", "")) and ep.get("csrf_signal") != "true":
            flags.append("NO_CSRF")
        if not has_auth_include or "NO_LOCAL_AUTH_SIGNAL" in ep.get("risk_flags", ""):
            flags.append("NO_LOCAL_AUTH")
        if int(ep.get("caller_refs") or 0) > 0:
            flags.append("CALLER_REFERENCED")
        if idor_params and not has_ownership:
            flags.append("IDOR_CANDIDATE")
        if path_params and has_path_sink:
            flags.append("PATH_TRAVERSAL_CANDIDATE")
        if handler in sink_by_file:
            flags.append("DANGEROUS_SINK")
        sql_risks = {row.get("risk", "") for row in sql_by_file.get(handler, [])}
        if "tainted_sql" in sql_risks:
            flags.append("SQL_TAINT")
        if "legacy_mysql_api" in sql_risks:
            flags.append("LEGACY_MYSQL_API")
        if any(PASSWORD_PARAM_RE.search(p) for p in params) and ("NO_LOCAL_AUTH" in flags or "NO_CSRF" in flags):
            flags.append("PASSWORD_CHANGE_NO_LOCAL_AUTH")
        if "FILE_UPLOAD_OR_IMPORT" in ep.get("risk_flags", "") or handler in upload_by_file:
            flags.append("UPLOAD_IMPORT")
        if all_tables & sensitive_tables:
            flags.append("SENSITIVE_TABLE_ACCESS")
        if all_tables & fk_gap_tables:
            flags.append("FK_GAP_TABLE_ACCESS")
        if not flags:
            continue
        rows.append(
            {
                "risk_id": "api_deep_" + stable_id(ep["route"], ",".join(flags)),
                "route": ep["route"],
                "handler": handler,
                "method": ep.get("method", ""),
                "caller_refs": ep.get("caller_refs", "0"),
                "tables": ";".join(sorted(all_tables)),
                "idor_params": ";".join(idor_params),
                "path_params": ";".join(path_params),
                "flags": ";".join(flags),
                "risk_score": str(risk_score(flags)),
                "evidence": summarize_evidence(ep, sink_by_file.get(handler, []), sql_by_file.get(handler, [])),
            }
        )
    return sorted(rows, key=lambda row: (-int(row["risk_score"]), row["route"]))


def summarize_evidence(ep: dict[str, str], sinks: list[dict[str, str]], sql_risks: list[dict[str, str]]) -> str:
    parts: list[str] = []
    if ep.get("risk_flags"):
        parts.append(ep["risk_flags"])
    for sink in sinks[:2]:
        parts.append(f"{sink.get('sink')}@L{sink.get('line')}")
    for row in sql_risks[:2]:
        parts.append(f"{row.get('risk')}:{row.get('sink')}@L{row.get('line')}")
    return " | ".join(parts)[:600]


def consumer_deep_rows(consumed: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in consumed:
        flags: list[str] = []
        url = row.get("url", "")
        source_flags = row.get("risk_flags", "")
        if DEV_EGRESS_RE.search(url):
            flags.append("DEV_OR_PLAINTEXT_EGRESS")
        if "UNRESOLVED_BASE_CONSTANT" in source_flags:
            flags.append("UNRESOLVED_BASE_CONSTANT")
        if "TLS_VERIFY_DISABLED" in source_flags:
            flags.append("TLS_VERIFY_DISABLED")
        if SECRET_RE.search(url + " " + source_flags + " " + row.get("constant", "")):
            flags.append("SECRET_IN_CONTEXT")
        if not flags:
            continue
        rows.append(
            {
                "risk_id": "api_consumer_" + stable_id(row.get("method", ""), url, ",".join(flags)),
                "method": row.get("method", ""),
                "url": url,
                "base_source": row.get("base_source", ""),
                "constant": row.get("constant", ""),
                "evidence_count": row.get("evidence_count", "1"),
                "evidence_samples": row.get("evidence_samples", ""),
                "flags": ";".join(flags),
                "risk_score": str(risk_score(flags)),
            }
        )
    return sorted(rows, key=lambda row: (-int(row["risk_score"]), row["url"]))


def write_markdown(path: Path, endpoint_rows: list[dict[str, str]], consumer_rows: list[dict[str, str]]) -> None:
    flag_counts = Counter(flag for row in endpoint_rows for flag in row["flags"].split(";") if flag)
    consumer_flag_counts = Counter(flag for row in consumer_rows for flag in row["flags"].split(";") if flag)
    top_endpoint_rows = endpoint_rows[:30]
    top_consumer_rows = consumer_rows[:30]
    lines = [
        "# API Deep Iterative Findings",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Summary",
        "",
        f"- Endpoint risk rows: {len(endpoint_rows)}",
        f"- Consumer risk rows: {len(consumer_rows)}",
        f"- High endpoint risk rows (score >= 80): {sum(int(row['risk_score']) >= 80 for row in endpoint_rows)}",
        f"- High consumer risk rows (score >= 40): {sum(int(row['risk_score']) >= 40 for row in consumer_rows)}",
        "",
        "## Endpoint Risk Families",
        "",
        "| Family | Count |",
        "| --- | ---: |",
    ]
    for flag, count in flag_counts.most_common():
        lines.append(f"| `{flag}` | {count} |")
    lines.extend(["", "## Consumer Risk Families", "", "| Family | Count |", "| --- | ---: |"])
    for flag, count in consumer_flag_counts.most_common():
        lines.append(f"| `{flag}` | {count} |")
    lines.extend(["", "## Top Endpoint Risks", "", "| Score | Route | Method | Flags | Evidence |", "| ---: | --- | --- | --- | --- |"])
    for row in top_endpoint_rows:
        lines.append(f"| {row['risk_score']} | `{row['route']}` | `{row['method']}` | `{row['flags']}` | `{row['evidence']}` |")
    lines.extend(["", "## Top Consumer Risks", "", "| Score | Method | URL | Flags | Evidence |", "| ---: | --- | --- | --- | --- |"])
    for row in top_consumer_rows:
        lines.append(f"| {row['risk_score']} | `{row['method']}` | `{row['url']}` | `{row['flags']}` | `{row['evidence_samples']}` |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    root = Path(".").resolve()
    endpoints = read_csv(ENDPOINT_CATALOG)
    consumed = read_csv(ASGARD_CONSUMED)
    dangerous = read_csv(DANGEROUS_SINKS)
    uploads = read_csv(UPLOAD_FINDINGS)
    sql_taint = read_csv(SQL_TAINT_FINDINGS)
    sensitive = read_csv(SENSITIVE_COLUMNS)
    fk_gaps = read_csv(FK_GAPS)
    sink_by_file: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in dangerous:
        sink_by_file[row["file"]].append(row)
    sql_by_file: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in sql_taint:
        sql_by_file[row["file"]].append(row)
    upload_by_file = {row["file"] for row in uploads}
    sensitive_tables = {row["table"] for row in sensitive}
    fk_gap_tables = {row["table"] for row in fk_gaps if row.get("usage_status") == "USED"}
    endpoint_rows = endpoint_deep_rows(root, endpoints, sink_by_file, sql_by_file, upload_by_file, sensitive_tables, fk_gap_tables)
    consumer_rows = consumer_deep_rows(consumed)
    out = root / ".brownfield" / "work" / "custom" / "api-deep-iterative"
    out.mkdir(parents=True, exist_ok=True)
    endpoint_fields = ["risk_id", "route", "handler", "method", "caller_refs", "tables", "idor_params", "path_params", "flags", "risk_score", "evidence"]
    consumer_fields = ["risk_id", "method", "url", "base_source", "constant", "evidence_count", "evidence_samples", "flags", "risk_score"]
    write_csv(out / "endpoint_deep_risks.csv", endpoint_rows, endpoint_fields)
    write_csv(out / "consumer_deep_risks.csv", consumer_rows, consumer_fields)
    write_markdown(out / "API_DEEP_ITERATIVE_FINDINGS.md", endpoint_rows, consumer_rows)
    summary = {
        "endpoint_risk_rows": len(endpoint_rows),
        "consumer_risk_rows": len(consumer_rows),
        "endpoint_flags": Counter(flag for row in endpoint_rows for flag in row["flags"].split(";") if flag),
        "consumer_flags": Counter(flag for row in consumer_rows for flag in row["flags"].split(";") if flag),
        "output": str(out),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
