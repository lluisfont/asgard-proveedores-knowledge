"""Reproducible static inventory of pinned Proveedores branches; never executes app code."""

import argparse
import csv
import gzip
import hashlib
import importlib.util
import io
import json
import re
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


EXCLUDE = {'.git', '.brownfield', 'graphify-out', 'node_modules', 'vendor', 'PHPExcel',
           'MPDF57', 'PDFMerger', 'jqwidgetsVer', 'jqwidgets', 'spreadsjs', 'datatables',
           'datatables_old', 'datatable', 'bootstrap4', 'bootstrap', 'fontawesome',
           'jquery-ui', 'jqGrid', 'php-jwt-5.2.0', 'Carbon', 'carbon', '.vscode'}
LIBRARY_NAMES = ('jquery', 'bootstrap', 'select2', 'sweetalert', 'moment', 'popper',
                 'leaflet', 'ckeditor', 'modernizr', 'kendo', 'ext-all', 'vue.min', 'vue.js')
TOKEN = re.compile(r'(?:SG\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{20,}|AIza[\w-]{30,}|gh[pousr]_[\w]{20,}|github_pat_[\w]{30,}|sk-(?:proj-)?[\w-]{20,}|AKIA[A-Z0-9]{16}|eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}|[ps]k\.eyJ[\w.-]{20,})')
PARAM = re.compile(r"\$_(GET|POST|REQUEST|FILES|SESSION|COOKIE)\s*\[\s*['\"]([^'\"]+)['\"]\s*\]")
TABLE = re.compile(r'\b(FROM|JOIN|INTO|UPDATE|DELETE\s+FROM)\s+`?([A-Za-z_]\w*)`?', re.I)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(source, *args):
    return subprocess.run(['git', '-C', str(source), *args], capture_output=True, check=True).stdout


def tree(source, ref):
    result = {}
    for entry in git(source, 'ls-tree', '-rz', ref).split(b'\0'):
        if not entry:
            continue
        metadata, path = entry.split(b'\t', 1)
        mode, kind, blob = metadata.decode().split()
        result[path.decode('utf-8')] = {'mode': mode, 'kind': kind, 'blob': blob}
    return result


def own(path):
    p = Path(path)
    return not any(part in EXCLUDE for part in p.parts) and not (
        p.suffix == '.js' and ('.min.' in p.name or any(name in p.name.lower() for name in LIBRARY_NAMES)))


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(obj, ensure_ascii=False, indent=2) + '\n'
    path.write_text(TOKEN.sub('[REDACTED]', content), encoding='utf-8')


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(TOKEN.sub('[REDACTED]', stream.getvalue()), encoding='utf-8')


def collect(source, target):
    out = target / 'source-audits/master/2026-11-18'
    master_ref = git(source, 'rev-parse', 'master').decode().strip()
    peru_ref = git(source, 'rev-parse', 'origin/master_peru').decode().strip()
    master, peru = tree(source, 'master'), tree(source, 'origin/master_peru')
    if git(source, 'rev-parse', 'HEAD').decode().strip() != master_ref:
        raise ValueError('Audited checkout is not the pinned master')
    inventory, params, tables, secrets, includes = [], [], [], [], []
    table_usage = defaultdict(lambda: {'reads': [], 'writes': []})
    sources = []
    for name, meta in sorted(master.items()):
        path = source / name
        in_scope = own(name)
        raw = path.read_bytes() if meta['kind'] == 'blob' and path.is_file() else None
        if raw is not None:
            blob_hash = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            # Git on Windows can check out CRLF; verify normalized bytes against the Git blob.
            if blob_hash != meta['blob']:
                normalized = raw.replace(b'\r\n', b'\n')
                normalized_hash = hashlib.sha1(b'blob ' + str(len(normalized)).encode() + b'\0' + normalized).hexdigest()
                if normalized_hash != meta['blob']:
                    canonical = git(source, 'show', master_ref + ':' + name)
                    if normalized != canonical.replace(b'\r\n', b'\n'):
                        raise ValueError('Tracked source modified: ' + name)
        inventory.append({'path': name, **meta, 'bytes': len(raw) if raw is not None else None,
                          'sha256_checkout': digest(raw) if raw is not None else None,
                          'scope': 'first_party_review' if in_scope else 'dependency_or_asset_excluded'})
        if raw is None or not in_scope or path.suffix not in {'.php', '.js'}:
            continue
        sources.append(path)
        lines = raw.decode('utf-8-sig', errors='replace').splitlines()
        for line_no, line in enumerate(lines, 1):
            if line.strip().startswith(('//', '*', '<!--')):
                continue
            for match in PARAM.finditer(line):
                params.append({'path': name, 'line': line_no, 'kind': match.group(1), 'name': match.group(2),
                               'evidence_id': 'REQ-' + digest(f'{master_ref}:{name}:{line_no}:{match.group(0)}'.encode())[:14]})
            for match in TABLE.finditer(line):
                # Only retain table references in lines containing an SQL literal/SQL variable.
                if not re.search(r'(?i)(select|query|sql|update|insert|delete|join)', line):
                    continue
                table = match.group(2)
                if table.lower() in {'set', 'select', 'values', 'function', 'new', 'this'}:
                    continue
                usage = 'writes' if match.group(1).upper() in {'INTO', 'UPDATE', 'DELETE FROM'} else 'reads'
                reference = {'path': name, 'line': line_no, 'table': table, 'usage': usage,
                             'confidence': 'static_sql_token_candidate',
                             'evidence_id': 'SQLREF-' + digest(f'{master_ref}:{name}:{line_no}:{table}:{usage}'.encode())[:14]}
                tables.append(reference)
                table_usage[table][usage].append({'path': name, 'line': line_no})
            if TOKEN.search(line):
                secrets.append({'path': name, 'line': line_no, 'kind': 'credential_token_literal',
                                'value': '[REDACTED]', 'action': 'rotate_and_externalize'})
    write_csv(out / 'inventory.csv', inventory, ['path','mode','kind','blob','bytes','sha256_checkout','scope'])
    write_csv(out / 'request-fields.csv', params, ['path','line','kind','name','evidence_id'])
    write_csv(out / 'sql-references.csv', tables, ['path','line','table','usage','confidence','evidence_id'])
    write_json(out / 'secret-locations.json', secrets)
    write_json(out / 'table-usage.json', {'schema_status': 'not_supplied',
        'warning': 'SQL tokens in static source are candidates, not verified physical tables, foreign keys or column types.',
        'tables': [{'name': k, **v} for k, v in sorted(table_usage.items())]})
    changes = []
    for name in sorted(master.keys() | peru.keys()):
        a, b = master.get(name), peru.get(name)
        status = 'identical_blob' if a and b and a['blob'] == b['blob'] else 'changed_blob' if a and b else 'master_only' if a else 'peru_only'
        if status == 'changed_blob' and (a['kind'] == 'commit' or b['kind'] == 'commit'):
            status = 'changed_gitlink'
        changes.append({'path': name, 'status': status, 'master_blob': a['blob'] if a else '',
                        'peru_blob': b['blob'] if b else '', 'first_party_candidate': own(name)})
    write_csv(out / 'branch-comparison.csv', changes, ['path','status','master_blob','peru_blob','first_party_candidate'])
    write_json(out / 'branch-comparison.json', {'master_commit': master_ref, 'peru_commit': peru_ref,
        'counts': dict(Counter(c['status'] for c in changes)),
        'first_party_counts': dict(Counter(c['status'] for c in changes if c['first_party_candidate'])),
        'warning': 'Equal blobs demonstrate equal source bytes only, not equal deployment configuration or business behavior.'})
    php_files = [path for path in sources if path.suffix == '.php']
    php_version = subprocess.run(['php', '-n', '-v'], capture_output=True, text=True).stdout.splitlines()[0]
    def lint(path):
        result = subprocess.run(['php', '-n', '-d', 'short_open_tag=1', '-l', str(path)], capture_output=True, text=True)
        message = (result.stdout + result.stderr).replace(str(source), '<source>').strip()
        return {'path': path.relative_to(source).as_posix(), 'exit_code': result.returncode,
                'status': 'pass' if result.returncode == 0 else 'fail',
                'message': TOKEN.sub('[REDACTED]', message) if result.returncode else ''}
    with ThreadPoolExecutor(max_workers=4) as pool:
        lint_rows = list(pool.map(lint, php_files))
    write_json(out / 'php-lint.json', {'runtime': php_version, 'short_open_tag': True,
        'executed_application': False, 'files': len(lint_rows), 'failed': sum(r['status']=='fail' for r in lint_rows),
        'results': lint_rows, 'warning': 'Syntax check under local PHP only. Dockerfile declares PHP 5.4; deployment/runtime/DB remain unverified.'})
    summary = {'repository': 'https://github.com/KPO-Group/proveedores', 'branch': 'master', 'commit': master_ref,
        'peru_commit': peru_ref, 'audit_date': '2026-11-18', 'tracked_entries': len(master),
        'first_party_code_files': len(sources), 'php_files_linted': len(php_files),
        'php_lint_failures': sum(r['status']=='fail' for r in lint_rows),
        'request_field_references': len(params), 'sql_token_references': len(tables),
        'table_candidates': len(table_usage), 'credential_literal_locations': len(secrets),
        'database_schema': 'not_versioned_in_master', 'submodules': [i for i in inventory if i['kind']=='commit'],
        'native_asgard': {'status': 'not_executed', 'reason': 'Windows Application Control blocked installed executable'},
        'runtime_validation': 'not_executed_missing_deployment_environment', 'source_writes': 'audit_tool_metadata_only'}
    write_json(out / 'audit-summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


def graph(source, target):
    from graphify.extract import extract
    from graphify.build import build
    from graphify.export import to_json
    tracked = tree(source, 'master')
    paths = [source / p for p in tracked if own(p) and Path(p).suffix in {'.php', '.js'}]
    print('Graphify local AST extraction: ' + str(len(paths)) + ' first-party candidate files; no semantic API calls', flush=True)
    extraction = extract(paths, root=source, parallel=True, max_workers=2)
    print('Graphify building graph', flush=True)
    graph_data = build([extraction], directed=True, root=source, dedup=False)
    import networkx as nx
    communities = {i:list(c) for i,c in enumerate(nx.community.louvain_communities(graph_data.to_undirected(), seed=42))}
    out = target / 'source-audits/master/2026-11-18/graphify'
    out.mkdir(parents=True, exist_ok=True)
    graph_path = out / 'graph.json'
    to_json(graph_data, communities, str(graph_path), built_at_commit=git(source,'rev-parse','master').decode().strip())
    raw = graph_path.read_text(encoding='utf-8')
    sanitized = TOKEN.sub('[REDACTED]', raw)
    # Graph extraction may carry line context; credentials are removed before persistence to Git.
    graph_path.write_text(sanitized, encoding='utf-8')
    summary = {'tool': 'graphifyy', 'mode': 'local_ast_code_only', 'files': len(paths),
        'nodes': graph_data.number_of_nodes(), 'edges': graph_data.number_of_edges(), 'communities': len(communities),
        'input_tokens': 0, 'output_tokens': 0, 'semantic_extraction': False,
        'extraction_warnings': extraction.get('errors', extraction.get('warnings', [])),
        'coverage_note': 'Direct PHP scripts often yield only a file node. Use the request, SQL and endpoint catalogs as complementary evidence; symbol extraction alone is not behavioral coverage.'}
    write_json(out / 'summary.json', summary)
    graph_path.with_suffix('.json.gz').write_bytes(gzip.compress(sanitized.encode('utf-8'),mtime=0))
    graph_path.unlink()
    print(json.dumps(summary, ensure_ascii=False, indent=2),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['collect','graph'])
    parser.add_argument('--source', required=True)
    parser.add_argument('--target', default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args()
    source = Path(args.source).resolve()
    if git(source, 'rev-parse', 'master').decode().strip() != 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707':
        raise ValueError('This audit profile is pinned to master a8ce2c23; create a new dated profile for another commit')
    if git(source, 'rev-parse', 'origin/master_peru').decode().strip() != '95fe9a4c3b3cddd84be922cc0e1eb9c88603df62':
        raise ValueError('This audit profile requires the pinned master_peru comparison')
    globals()[args.mode](source, Path(args.target).resolve())
