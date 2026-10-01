#!/usr/bin/env python3
"""Data-model integrity scanner for Brownfield outputs."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


SENSITIVE_RE = re.compile(
    r"(contrasena|password|pass|master_pass|token|secret|correo|email|mail|telefono|celular|nit|username|usuario|ip|2fa|codigo)",
    re.I,
)
FK_LIKE_RE = re.compile(r"(^id[A-Za-z_].+|.+_id$|created_by|updated_by|deleted_by|idusuario|idcliente|idproveedor|operador_id|embarque_id)", re.I)
COPY_TEMP_RE = re.compile(r"(^tmp_|_tmp|_copy|copy\d*$|_bk$|bk$|backup|respaldo)", re.I)
CRITICAL_TABLES = {
    "prov_usuarioaccesoproveedor",
    "dav_codigos_2fa",
    "dav_reseteos_passswords_proveedores",
    "master_pass",
    "tck_location",
    "tck_asignacion_viaje",
}


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


def index_map(rows: list[dict[str, str]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        table = row.get("table", "")
        cols = row.get("columns", "")
        for col in re.findall(r'"([^"]+)"', cols):
            out[table].add(col)
    return out


def relation_map(rows: list[dict[str, str]]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    outgoing: dict[str, set[str]] = defaultdict(set)
    incoming: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        ft = row.get("from_table", "")
        fc = row.get("from_column", "")
        tt = row.get("to_table", "")
        tc = row.get("to_column", "")
        if ft and fc:
            outgoing[ft].add(fc)
        if tt and tc:
            incoming[tt].add(tc)
    return outgoing, incoming


def scan(root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    dd = root / ".brownfield" / "work" / "data_dictionary"
    columns = read_csv(dd / "columns.csv")
    tables = read_csv(dd / "tables.csv")
    indexes = read_csv(dd / "indexes.csv")
    relations = read_csv(dd / "relations.csv")

    indexed = index_map(indexes)
    outgoing, incoming = relation_map(relations)

    sensitivity_rows: list[dict[str, str]] = []
    fk_gap_rows: list[dict[str, str]] = []
    table_rows: list[dict[str, str]] = []

    for col in columns:
        table = col.get("table", "")
        name = col.get("column", "")
        if SENSITIVE_RE.search(name):
            flags: list[str] = []
            if col.get("sensitivity", "UNKNOWN") == "UNKNOWN":
                flags.append("SENSITIVITY_UNKNOWN")
            if col.get("nullable") != "NO":
                flags.append("SENSITIVE_FIELD_NULLABLE")
            if name not in indexed.get(table, set()) and re.search(r"(token|codigo|username|correo|email|master_pass|contrasena|password)", name, re.I):
                flags.append("NO_INDEX_ON_AUTH_OR_TOKEN_FIELD")
            sensitivity_rows.append(
                {
                    "table": table,
                    "column": name,
                    "data_type": col.get("data_type", ""),
                    "nullable": col.get("nullable", ""),
                    "sensitivity": col.get("sensitivity", ""),
                    "indexed": str(name in indexed.get(table, set())).lower(),
                    "flags": ";".join(flags),
                    "line": col.get("line", ""),
                }
            )

        if FK_LIKE_RE.search(name) and col.get("key_role") != "PRIMARY_KEY" and name not in outgoing.get(table, set()):
            fk_gap_rows.append(
                {
                    "table": table,
                    "column": name,
                    "data_type": col.get("data_type", ""),
                    "indexed": str(name in indexed.get(table, set())).lower(),
                    "usage_status": "",
                    "flags": "FK_LIKE_COLUMN_WITHOUT_DECLARED_RELATION",
                    "line": col.get("line", ""),
                }
            )

    usage_by_table = {row.get("table", ""): row.get("usage_status", "") for row in tables}
    for row in fk_gap_rows:
        row["usage_status"] = usage_by_table.get(row["table"], "")

    for table in tables:
        name = table.get("table", "")
        flags: list[str] = []
        if name in CRITICAL_TABLES and not outgoing.get(name) and not incoming.get(name):
            flags.append("CRITICAL_TABLE_WITHOUT_DECLARED_RELATIONS")
        if COPY_TEMP_RE.search(name):
            flags.append("TEMP_COPY_OR_BACKUP_TABLE")
        if table.get("usage_status") == "NO_USAGE_FOUND":
            flags.append("NO_CODE_USAGE_FOUND")
        if flags:
            table_rows.append(
                {
                    "table": name,
                    "usage_status": table.get("usage_status", ""),
                    "read_refs": table.get("read_references", ""),
                    "write_refs": table.get("write_references", ""),
                    "declared_fk_out": str(len(outgoing.get(name, set()))),
                    "declared_fk_in": str(len(incoming.get(name, set()))),
                    "flags": ";".join(flags),
                }
            )

    return sensitivity_rows, fk_gap_rows, table_rows


def write_markdown(path: Path, sensitivity_rows: list[dict[str, str]], fk_gap_rows: list[dict[str, str]], table_rows: list[dict[str, str]]) -> None:
    sens_flags = Counter(flag for row in sensitivity_rows for flag in row["flags"].split(";") if flag)
    fk_used = [row for row in fk_gap_rows if row["usage_status"] == "USED"]
    table_flags = Counter(flag for row in table_rows for flag in row["flags"].split(";") if flag)
    critical = [row for row in table_rows if "CRITICAL_TABLE_WITHOUT_DECLARED_RELATIONS" in row["flags"]]

    lines = [
        "# Data Model Integrity Findings - augmented pass",
        "",
        "Status: REVIEW_REQUIRED",
        "",
        "This pass inspects Brownfield's data dictionary for security and integrity gaps that the baseline leaves unclassified.",
        "",
        "## Summary",
        "",
        f"- Sensitive-name columns: {len(sensitivity_rows)}",
        f"- FK-like columns without declared relation: {len(fk_gap_rows)}",
        f"- FK-like columns without declared relation in USED tables: {len(fk_used)}",
        f"- Table-level integrity findings: {len(table_rows)}",
        f"- Critical tables without declared relations: {len(critical)}",
        "",
        "## Sensitive field flags",
        "",
        "| Flag | Count |",
        "| --- | ---: |",
    ]
    for name, count in sens_flags.most_common():
        lines.append(f"| `{name}` | {count} |")

    lines.extend(["", "## Table flags", "", "| Flag | Count |", "| --- | ---: |"])
    for name, count in table_flags.most_common():
        lines.append(f"| `{name}` | {count} |")

    lines.extend(["", "## Critical tables without declared relations", "", "| Table | Usage | Read refs | Write refs |", "| --- | --- | ---: | ---: |"])
    for row in critical:
        lines.append(f"| `{row['table']}` | `{row['usage_status']}` | {row['read_refs'] or 0} | {row['write_refs'] or 0} |")

    lines.extend(["", "## Highest density sensitive tables", "", "| Table | Sensitive columns |", "| --- | ---: |"])
    by_table = Counter(row["table"] for row in sensitivity_rows)
    for table, count in by_table.most_common(40):
        lines.append(f"| `{table}` | {count} |")

    lines.extend(["", "## USED tables with FK-like gaps", "", "| Table | Column | Indexed | Line |", "| --- | --- | --- | ---: |"])
    for row in fk_used[:60]:
        lines.append(f"| `{row['table']}` | `{row['column']}` | `{row['indexed']}` | {row['line']} |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out = root / ".brownfield" / "work" / "custom"

    sensitivity_rows, fk_gap_rows, table_rows = scan(root)
    write_csv(out / "sensitive_column_findings.csv", sensitivity_rows, ["table", "column", "data_type", "nullable", "sensitivity", "indexed", "flags", "line"])
    write_csv(out / "fk_gap_findings.csv", fk_gap_rows, ["table", "column", "data_type", "indexed", "usage_status", "flags", "line"])
    write_csv(out / "table_integrity_findings.csv", table_rows, ["table", "usage_status", "read_refs", "write_refs", "declared_fk_out", "declared_fk_in", "flags"])
    write_markdown(out / "DATA_MODEL_INTEGRITY_FINDINGS.md", sensitivity_rows, fk_gap_rows, table_rows)

    release_data = root / ".brownfield" / "work" / "release" / "engineering-analysis" / "data" / "DATA_QUALITY_FINDINGS.md"
    write_markdown(release_data, sensitivity_rows, fk_gap_rows, table_rows)

    summary = {
        "sensitive_name_columns": len(sensitivity_rows),
        "fk_like_columns_without_declared_relation": len(fk_gap_rows),
        "table_integrity_findings": len(table_rows),
        "output": str(out / "DATA_MODEL_INTEGRITY_FINDINGS.md"),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
