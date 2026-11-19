"""Pinned Peru inventory, tree delta, lint and optional local Graphify AST. No app execution."""

import argparse
import gzip
import hashlib
import importlib.metadata
import json
import re
import subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from collect_master import TOKEN, git, own, tree, write_csv, write_json

HEAD = '2a179e2e6472d5705d031665ecbc90c3d806edec'
PREVIOUS = '95fe9a4c3b3cddd84be922cc0e1eb9c88603df62'
MASTER = 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707'
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'source-audits/peru/2026-11-19'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--graph', action='store_true')
    args = parser.parse_args()
    source = Path(args.source).resolve()
    if git(source, 'rev-parse', 'HEAD').decode().strip() != HEAD or git(source, 'diff', '--name-only', 'HEAD').strip():
        raise ValueError('Peru checkout must be clean at the pinned head')
    current, previous, master = (tree(source, pin) for pin in [HEAD, PREVIOUS, MASTER])
    changes = []
    inventory = []
    code = []
    for path, info in sorted(current.items()):
        raw = (source/path).read_bytes() if info['kind'] == 'blob' else None
        if raw is not None:
            normalized = raw.replace(b'\r\n', b'\n')
            hashes = {hashlib.sha1(b'blob '+str(len(value)).encode()+b'\0'+value).hexdigest()
                      for value in [raw, normalized]}
            if info['blob'] not in hashes:
                expected = git(source, 'show', HEAD+':'+path)
                if normalized != expected.replace(b'\r\n', b'\n'):
                    raise ValueError('Working bytes differ from Git: '+path)
        candidate = own(path) and Path(path).suffix in {'.php', '.js'}
        if candidate:
            code.append(source/path)
        inventory.append({'path': path, **info,
            'bytes': len(raw) if raw is not None else None,
            'sha256_normalized': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest() if raw is not None else None,
            'scope': 'code_candidate' if candidate else 'dependency_asset_or_other'})
    for path in sorted(previous.keys() | current.keys()):
        a, b = previous.get(path), current.get(path)
        status = 'identical' if a == b else 'changed' if a and b else 'added' if b else 'removed'
        changes.append({'path': path, 'status': status, 'previous_blob': a['blob'] if a else '',
                        'current_blob': b['blob'] if b else '', 'kind': (b or a)['kind']})
    write_csv(OUT/'inventory.csv', inventory, ['path','mode','kind','blob','bytes','sha256_normalized','scope'])
    write_csv(OUT/'tree-comparison.csv', changes, ['path','status','previous_blob','current_blob','kind'])
    write_json(OUT/'tree-comparison.json', {'previous_commit': PREVIOUS, 'current_commit': HEAD,
        'counts': dict(Counter(c['status'] for c in changes)),
        'changed_paths': [c['path'] for c in changes if c['status'] != 'identical'],
        'equal_blobs_are_not_runtime_proof': True})
    comparison = []
    for path in sorted(master.keys() | current.keys()):
        a, b = master.get(path), current.get(path)
        status = 'identical' if a == b else 'changed' if a and b else 'peru_only' if b else 'master_only'
        comparison.append({'path': path, 'status': status, 'master_blob': a['blob'] if a else '', 'peru_blob': b['blob'] if b else ''})
    write_csv(OUT/'master-peru-comparison.csv', comparison, ['path','status','master_blob','peru_blob'])
    php_paths = [p for p in code if p.suffix == '.php']
    def lint(path):
        result = subprocess.run(['php','-n','-d','short_open_tag=1','-l',str(path)],capture_output=True,text=True)
        message = result.stdout+result.stderr
        lines = [int(n) for n in re.findall(r'on line (\d+)', message)]
        category = ('nested_ternary_php8' if 'ternary' in message.lower() else 'syntax_or_compatibility_error') if result.returncode else 'parse_pass'
        return {'path': path.relative_to(source).as_posix(), 'exit_code': result.returncode,
                'status': 'pass' if result.returncode == 0 else 'fail', 'category': category, 'lines': sorted(set(lines))}
    with ThreadPoolExecutor(max_workers=4) as pool:
        lints = list(pool.map(lint, php_paths))
    php_version = subprocess.run(['php','-n','-v'],capture_output=True,text=True,check=True).stdout.splitlines()[0]
    write_json(OUT/'php-lint.json', {'source_commit': HEAD, 'runtime': php_version, 'short_open_tag': True,
        'total': len(lints), 'passed': sum(c['status'] == 'pass' for c in lints), 'results': lints,
        'application_executed': False, 'production_compatibility': 'not_verified'})
    summary = {'audit_date': '2026-11-19', 'timezone': 'Europe/Madrid', 'source_commit': HEAD,
        'previous_peru_commit': PREVIOUS, 'master_reference_commit': MASTER,
        'tracked_entries': len(current), 'code_candidates': len(code), 'tree_delta': dict(Counter(c['status'] for c in changes)),
        'master_comparison': dict(Counter(c['status'] for c in comparison)),
        'php_lint': {'total': len(lints), 'passed': sum(c['status'] == 'pass' for c in lints)},
        'database_access': False, 'application_executed': False,
        'native_asgard': 'not_executed_prior_appcontrol_block',
        'browser_output_navigation_security_review': 'excluded_prior_automatic_rejection_not_retried',
        'coverage': 'PARTIAL'}
    if args.graph:
        from graphify.extract import extract
        from graphify.build import build
        from graphify.export import to_json
        import networkx as nx
        extraction = extract(code, root=source, parallel=True, max_workers=2)
        graph = build([extraction], directed=True, root=source, dedup=False)
        communities = {i:list(c) for i,c in enumerate(nx.community.louvain_communities(graph.to_undirected(),seed=42))}
        folder = OUT/'graphify'
        folder.mkdir(parents=True, exist_ok=True)
        temporary = folder/'graph.json'
        to_json(graph, communities, str(temporary), built_at_commit=HEAD)
        data = json.loads(temporary.read_text(encoding='utf-8-sig'))
        # Keep only structural attributes; never export source snippets, docstrings or arbitrary values.
        allowed_node = {'id','label','community','file_type','source_file','source_location','norm_label','_origin'}
        allowed_edge = {'source','target','relation','confidence','confidence_score','source_file','source_location','weight','_origin'}
        data['nodes'] = [{k:v for k,v in n.items() if k in allowed_node} for n in data['nodes']]
        data['links'] = [{k:v for k,v in e.items() if k in allowed_edge} for e in data['links']]
        data['hyperedges'] = []
        payload = TOKEN.sub('[REDACTED]', json.dumps(data,ensure_ascii=False,sort_keys=True)).encode('utf-8')
        (folder/'graph.json.gz').write_bytes(gzip.compress(payload,mtime=0))
        temporary.unlink()
        counts = Counter(n.get('source_file') for n in data['nodes'])
        graph_summary = {'source_commit': HEAD, 'tool': 'graphifyy', 'version': importlib.metadata.version('graphifyy'),
            'mode': 'local_ast_structural_only', 'code_candidates': len(code), 'nodes': len(data['nodes']),
            'edges': len(data['links']), 'communities': len(communities),
            'single_node_source_files': sum(n == 1 for n in counts.values()),
            'input_tokens': 0, 'output_tokens': 0, 'semantic_extraction': False,
            'limitations': 'AST and equal blobs do not establish route execution, authorization, business policy or deployment.'}
        write_json(folder/'summary.json', graph_summary)
        summary['graphify'] = graph_summary
    write_json(OUT/'summary.json', summary)
    print(json.dumps(summary,ensure_ascii=True,indent=2))


if __name__ == '__main__':
    main()
