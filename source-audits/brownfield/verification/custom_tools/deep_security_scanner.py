#!/usr/bin/env python3
"""Heuristic security scanner for legacy PHP + MySQL dump.

This complements Brownfield/Graphify with targeted checks Brownfield does not
currently produce as completed findings for this codebase.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
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
    "bootstrap-filestyle",
    "fontawesome",
    "jqGrid",
    "Carbon",
    "carbon",
    "php-jwt-5.2.0",
    "php",
}

SUPERGLOBAL_RE = re.compile(r"\$_(GET|POST|REQUEST|COOKIE|FILES)\s*\[\s*['\"]([^'\"]+)['\"]\s*\]")
MYSQL_QUERY_RE = re.compile(r"\b(mysql_query|mysqli_query|\$[A-Za-z_][A-Za-z0-9_]*\s*->\s*(?:query|exec))\s*\(", re.I)
PREPARE_RE = re.compile(r"->\s*prepare\s*\(", re.I)
ESCAPE_RE = re.compile(r"mysql_real_escape_string|mysqli_real_escape_string|addslashes|intval\s*\(|filter_input\s*\(", re.I)
SQL_WORD_RE = re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|CALL|REPLACE)\b", re.I)
SINK_RE = re.compile(r"\b(shell_exec|system|passthru|exec|eval|unserialize|preg_replace\s*\([^)]*/e|assert)\s*\(", re.I)
INCLUDE_VAR_RE = re.compile(r"\b(include|include_once|require|require_once)\s*\(?\s*\$", re.I)
UPLOAD_MOVE_RE = re.compile(r"\b(move_uploaded_file|copy)\s*\(", re.I)
CLIENT_FILENAME_RE = re.compile(r"\$_FILES\s*\[[^\]]+\]\s*\[\s*['\"]name['\"]\s*\]", re.I)
EXT_ALLOW_RE = re.compile(r"pathinfo|extension|in_array\s*\(|preg_match\s*\([^)]*(?:jpg|jpeg|png|pdf|xls|xlsx|doc|docx|csv)", re.I)
MIME_RE = re.compile(r"finfo_|mime_content_type|\[\s*['\"]type['\"]\s*\]", re.I)
SIZE_RE = re.compile(r"\[\s*['\"]size['\"]\s*\]|MAX_FILE_SIZE", re.I)
RANDOM_NAME_RE = re.compile(r"uniqid|random_bytes|openssl_random_pseudo_bytes|md5\s*\(\s*time|sha1\s*\(\s*time", re.I)
CSRF_RE = re.compile(r"csrf|xsrf|nonce|_token", re.I)
AUTH_RE = re.compile(r"permisos\.php|\$_SESSION|session_start|idusuarioaccesoproveedor|login", re.I)
SIMPLE_ROUTINE_RE = re.compile(r"\bCREATE\s+(?:DEFINER=`[^`]+`@`[^`]+`\s+)?(PROCEDURE|FUNCTION)\s+`([^`]+)`", re.I)


def excluded(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        parts = path.parts
    return any(part in EXCLUDE_SEGMENTS for part in parts)


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def context(lines: list[str], line_no: int, radius: int = 8) -> str:
    start = max(0, line_no - radius - 1)
    end = min(len(lines), line_no + radius)
    return "\n".join(lines[start:end])


def assigned_superglobal_vars(text: str) -> set[str]:
    vars_found: set[str] = set()
    for match in re.finditer(r"(\$[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\$_(?:GET|POST|REQUEST|COOKIE)\s*\[[^\]]+\])", text):
        vars_found.add(match.group(1))
    return vars_found


def scan_php(root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    sql_rows: list[dict[str, str]] = []
    upload_rows: list[dict[str, str]] = []
    sink_rows: list[dict[str, str]] = []

    for path in sorted(root.rglob("*.php")):
        if excluded(path, root):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        tainted_vars = assigned_superglobal_vars(text)

        for line_no, line in enumerate(lines, start=1):
            window = context(lines, line_no)
            if MYSQL_QUERY_RE.search(line):
                superglobals = SUPERGLOBAL_RE.findall(window)
                variables = sorted(v for v in tainted_vars if re.search(re.escape(v) + r"\b", window))
                direct_risk = bool(superglobals or variables)
                legacy = "mysql_query" in line
                if direct_risk or legacy or SQL_WORD_RE.search(window):
                    sql_rows.append(
                        {
                            "file": rel(path, root),
                            "line": str(line_no),
                            "sink": MYSQL_QUERY_RE.search(line).group(1) if MYSQL_QUERY_RE.search(line) else "query",
                            "superglobals_in_context": ";".join(f"{scope}.{key}" for scope, key in superglobals),
                            "tainted_vars_in_context": ";".join(variables),
                            "escape_signal": str(bool(ESCAPE_RE.search(window))).lower(),
                            "prepare_signal": str(bool(PREPARE_RE.search(window))).lower(),
                            "risk": "tainted_sql" if direct_risk and not ESCAPE_RE.search(window) else ("legacy_mysql_api" if legacy else "review_sql"),
                            "snippet": line.strip()[:220],
                        }
                    )

            sink_match = SINK_RE.search(line)
            if sink_match or INCLUDE_VAR_RE.search(line):
                superglobals = SUPERGLOBAL_RE.findall(window)
                variables = sorted(v for v in tainted_vars if re.search(re.escape(v) + r"\b", window))
                sink_rows.append(
                    {
                        "file": rel(path, root),
                        "line": str(line_no),
                        "sink": sink_match.group(1) if sink_match else "dynamic_include",
                        "superglobals_in_context": ";".join(f"{scope}.{key}" for scope, key in superglobals),
                        "tainted_vars_in_context": ";".join(variables),
                        "risk": "tainted_sink" if superglobals or variables else "dangerous_sink",
                        "snippet": line.strip()[:220],
                    }
                )

        if "$_FILES" in text or UPLOAD_MOVE_RE.search(text):
            flags: list[str] = []
            if not EXT_ALLOW_RE.search(text):
                flags.append("NO_EXTENSION_ALLOWLIST_SIGNAL")
            if not MIME_RE.search(text):
                flags.append("NO_MIME_CHECK_SIGNAL")
            if not SIZE_RE.search(text):
                flags.append("NO_SIZE_LIMIT_SIGNAL")
            if CLIENT_FILENAME_RE.search(text) and not RANDOM_NAME_RE.search(text):
                flags.append("CLIENT_FILENAME_USED_WITHOUT_RANDOMIZATION_SIGNAL")
            if not CSRF_RE.search(text):
                flags.append("NO_CSRF_SIGNAL")
            if not AUTH_RE.search(text):
                flags.append("NO_AUTH_SIGNAL")
            if "copy(" in text:
                flags.append("COPY_USED_FOR_UPLOAD")
            upload_rows.append(
                {
                    "file": rel(path, root),
                    "file_params": ";".join(sorted(set(key for scope, key in SUPERGLOBAL_RE.findall(text) if scope == "FILES"))),
                    "move_or_copy_signal": str(bool(UPLOAD_MOVE_RE.search(text))).lower(),
                    "flags": ";".join(sorted(set(flags))),
                }
            )

    return sql_rows, upload_rows, sink_rows


def scan_sql_dump(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    dumps = sorted(root.glob("*.sql"))
    for dump in dumps:
        try:
            text = dump.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        current_kind = ""
        current_name = ""
        current_start = 0
        buffer: list[str] = []

        def flush(end_line: int) -> None:
            nonlocal buffer, current_kind, current_name, current_start
            if not current_name:
                return
            body = "\n".join(buffer)
            flags: list[str] = []
            if re.search(r"\bPREPARE\b|\bEXECUTE\b", body, re.I):
                flags.append("DYNAMIC_SQL")
            if re.search(r"\bCONCAT\s*\(", body, re.I):
                flags.append("SQL_STRING_CONCAT")
            if re.search(r"\bSTART\s+TRANSACTION\b|\bCOMMIT\b|\bROLLBACK\b", body, re.I):
                flags.append("EXPLICIT_TRANSACTION")
            if re.search(r"\bDROP\s+TABLE\b|\bTRUNCATE\s+TABLE\b|DELETE\s+FROM\s+\w+\s*;", body, re.I):
                flags.append("DESTRUCTIVE_SQL")
            if re.search(r"\bCREATE\s+TEMPORARY\s+TABLE\b", body, re.I):
                flags.append("TEMP_TABLE")
            if flags:
                rows.append(
                    {
                        "file": dump.name,
                        "routine": current_name,
                        "kind": current_kind,
                        "start_line": str(current_start),
                        "end_line": str(end_line),
                        "flags": ";".join(sorted(set(flags))),
                    }
                )

        for idx, line in enumerate(lines, start=1):
            match = SIMPLE_ROUTINE_RE.search(line)
            if match:
                flush(idx - 1)
                current_kind = match.group(1).upper()
                current_name = match.group(2)
                current_start = idx
                buffer = [line]
                continue
            if current_name:
                buffer.append(line)
                if line.strip().endswith("*/;") or line.strip() == "END ;;":
                    flush(idx)
                    current_kind = ""
                    current_name = ""
                    current_start = 0
                    buffer = []
        flush(len(lines))
    return rows


def write_markdown(path: Path, sql_rows: list[dict[str, str]], upload_rows: list[dict[str, str]], sink_rows: list[dict[str, str]], routine_rows: list[dict[str, str]]) -> None:
    sql_by_risk = Counter(row["risk"] for row in sql_rows)
    upload_flag_counts = Counter(flag for row in upload_rows for flag in row["flags"].split(";") if flag)
    sink_by_name = Counter(row["sink"] for row in sink_rows)
    routine_flag_counts = Counter(flag for row in routine_rows for flag in row["flags"].split(";") if flag)

    lines = [
        "# Deep Security Findings - augmented pass",
        "",
        "Status: REVIEW_REQUIRED",
        "",
        "This pass adds targeted PHP and SQL-dump checks on top of Brownfield's baseline.",
        "",
        "## Summary",
        "",
        f"- SQL sink findings: {len(sql_rows)}",
        f"- Upload handling findings: {len(upload_rows)}",
        f"- Dangerous PHP sink findings: {len(sink_rows)}",
        f"- SQL routine risk findings: {len(routine_rows)}",
        "",
        "## SQL sink risk counts",
        "",
        "| Risk | Count |",
        "| --- | ---: |",
    ]
    for name, count in sql_by_risk.most_common():
        lines.append(f"| `{name}` | {count} |")

    lines.extend(["", "## Upload flags", "", "| Flag | Count |", "| --- | ---: |"])
    for name, count in upload_flag_counts.most_common():
        lines.append(f"| `{name}` | {count} |")

    lines.extend(["", "## Dangerous sink counts", "", "| Sink | Count |", "| --- | ---: |"])
    for name, count in sink_by_name.most_common():
        lines.append(f"| `{name}` | {count} |")

    lines.extend(["", "## SQL routine flags", "", "| Flag | Count |", "| --- | ---: |"])
    for name, count in routine_flag_counts.most_common():
        lines.append(f"| `{name}` | {count} |")

    lines.extend(["", "## Highest priority SQL sinks", "", "| File | Line | Risk | Signal |", "| --- | ---: | --- | --- |"])
    priority = [row for row in sql_rows if row["risk"] == "tainted_sql"][:40]
    for row in priority:
        signal = row["superglobals_in_context"] or row["tainted_vars_in_context"] or row["snippet"]
        lines.append(f"| `{row['file']}` | {row['line']} | `{row['risk']}` | `{signal}` |")

    lines.extend(["", "## Upload files needing review", "", "| File | Flags |", "| --- | --- |"])
    for row in sorted(upload_rows, key=lambda r: len(r["flags"].split(";")), reverse=True)[:40]:
        lines.append(f"| `{row['file']}` | `{row['flags']}` |")

    lines.extend(["", "## SQL routines needing review", "", "| Routine | Kind | Lines | Flags |", "| --- | --- | --- | --- |"])
    for row in routine_rows[:60]:
        lines.append(f"| `{row['routine']}` | `{row['kind']}` | {row['start_line']}-{row['end_line']} | `{row['flags']}` |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    sql_rows, upload_rows, sink_rows = scan_php(root)
    routine_rows = scan_sql_dump(root)
    out = root / ".brownfield" / "work" / "custom"
    write_csv(
        out / "sql_taint_findings.csv",
        sql_rows,
        ["file", "line", "sink", "superglobals_in_context", "tainted_vars_in_context", "escape_signal", "prepare_signal", "risk", "snippet"],
    )
    write_csv(out / "upload_security_findings.csv", upload_rows, ["file", "file_params", "move_or_copy_signal", "flags"])
    write_csv(out / "dangerous_php_sinks.csv", sink_rows, ["file", "line", "sink", "superglobals_in_context", "tainted_vars_in_context", "risk", "snippet"])
    write_csv(out / "sql_routine_risks.csv", routine_rows, ["file", "routine", "kind", "start_line", "end_line", "flags"])
    write_markdown(out / "DEEP_SECURITY_FINDINGS.md", sql_rows, upload_rows, sink_rows, routine_rows)

    release_security = root / ".brownfield" / "work" / "release" / "engineering-analysis" / "security" / "SECURITY_FINDINGS.md"
    write_markdown(release_security, sql_rows, upload_rows, sink_rows, routine_rows)

    summary = {
        "sql_sink_findings": len(sql_rows),
        "upload_findings": len(upload_rows),
        "dangerous_php_sink_findings": len(sink_rows),
        "sql_routine_risk_findings": len(routine_rows),
        "output": str(out / "DEEP_SECURITY_FINDINGS.md"),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
