"""Validate semantic deltas, closure evidence and the cumulative convergence ledger."""

import hashlib
import json
from pathlib import Path


def validate(root, cite):
    def read(relative):
        return json.loads((root/relative).read_text(encoding='utf-8-sig'))
    prefix = 'knowledge/reviews/iterative-20261118/'
    accepted = read(prefix+'accepted-deltas.json')
    ledger = read(prefix+'iterations.json')
    records = accepted['deltas']
    by_id = {r['id']: r for r in records}
    if len(by_id) != len(records):
        raise ValueError('Duplicate accepted delta ID')
    for record in records:
        if record['classification'] not in {'new_finding', 'improvement'} or not record['statement']:
            raise ValueError('Unsupported accepted delta')
        for e in record['evidence']:
            cite(e['commit'], e['path'], e['line_start'], e['line_end'])
    counts = {kind: sum(r['classification'] == value for r in records)
              for kind, value in [('new_findings', 'new_finding'), ('improvements', 'improvement')]}
    if counts != accepted['counts']:
        raise ValueError('Delta counts disagree')

    def fingerprint(items):
        payload = {'baseline_knowledge_commit': accepted['baseline_knowledge_commit'],
                   'deltas': sorted(items, key=lambda r: r['id'])}
        return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    cumulative, prior, streak = [], fingerprint([]), 0
    for version, iteration in enumerate(ledger['iterations'], 1):
        ids = iteration['new_findings']+iteration['improvements']
        if iteration['version'] != version or iteration['status'] != 'completed':
            raise ValueError('Incomplete or unordered iteration')
        expected = [r for r in records if r['first_version'] == version]
        if set(ids) != {r['id'] for r in expected}:
            raise ValueError('Unrecorded delta or duplicate iteration')
        cumulative += expected
        after = fingerprint(cumulative)
        if iteration['before_semantic_sha256'] != prior or iteration['after_semantic_sha256'] != after:
            raise ValueError('Semantic iteration fingerprint mismatch')
        snapshot_path = root/iteration['snapshot']
        snapshot = read(iteration['snapshot'])
        if snapshot['baseline_knowledge_commit'] != accepted['baseline_knowledge_commit'] or snapshot['deltas'] != sorted(cumulative, key=lambda r: r['id']):
            raise ValueError('Version snapshot differs from cumulative accepted records')
        if hashlib.sha256(snapshot_path.read_bytes()).hexdigest() != iteration['snapshot_sha256']:
            raise ValueError('Version snapshot file hash differs')
        streak = streak+1 if not ids else 0
        if not ids:
            closure = read(iteration['review_artifact'])
            if closure['new_findings'] or closure['improvements'] or not closure.get('technique'):
                raise ValueError('Closure review not independently zero-delta')
            if not closure.get('checks') or any(c.get('status') not in {'completed', 'pass'} for c in closure['checks']):
                raise ValueError('Closure checks not completed')
            if str(closure.get('status', '')).startswith('STAGED'):
                raise ValueError('Closure still staged')
        prior = after
    if len(cumulative) != len(records) or streak < 2 or not ledger['converged']:
        raise ValueError('Two consecutive zero-delta completed reviews not yet established')
    if ledger['consecutive_zero_delta_passes'] != streak:
        raise ValueError('Wrong convergence streak')

    operations = read('knowledge/general/operational-findings.json')
    for key, classification in [('findings', 'new_finding'), ('improvements', 'improvement')]:
        for item in operations[key]:
            if item['id'] not in by_id or by_id[item['id']]['classification'] != classification:
                raise ValueError('Operational registry and accepted deltas disagree: '+item['id'])
    # Evidence may nest beneath findings or documentary improvements.
    def walk(value):
        if isinstance(value, dict):
            if all(k in value for k in ['commit', 'path', 'line_start', 'line_end']):
                if value['commit'] in {accepted['master_commit'], accepted['peru_commit']}:
                    cite(value['commit'], value['path'], value['line_start'], value['line_end'])
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(operations)
    walk(read(prefix+'contract-integration.json'))
    walk(read(prefix+'branch-obligations.json'))
    for closure in ['closure-semantic-mutations.json', 'closure-inference-boundaries.json']:
        walk(read(prefix+closure))
    for item in read('source-audits/master/2026-11-18/iterative/sql-ast-fragments.json')['fragments']:
        cite(accepted['master_commit'], item['path'], item['line_start'], item['line_end'])
    probe_root = 'source-audits/master/2026-11-18/iterative/'
    for file in ['report-contract-probes.json', 'arity-contract-probes.json', 'transaction-probes.json']:
        probe = read(probe_root+file)
        probe = probe.get('summary', probe)
        if probe['passed'] != probe['total']:
            raise ValueError('Iterative probe failure: '+file)
    contracts = read(probe_root+'contract-consistency-probes.json')
    if contracts['checks_passed'] is not True:
        raise ValueError('Contract checks failed')
    for file in ['sql-ast-summary.json', 'static-arity-review.json']:
        if any(c['status'] != 'pass' for c in read(probe_root+file)['negative_controls']):
            raise ValueError('Parser control failure')
    for file in ['scripts/audit/browser_context_probes.py', probe_root+'browser-context-probes.json']:
        if (root/file).exists():
            raise ValueError('Incomplete rejected review artifact must not be published')
    return {**counts, 'completed_passes': len(ledger['iterations']),
            'consecutive_zero_delta_passes': streak, 'semantic_sha256': prior,
            'coverage': 'PARTIAL', 'production_validation': 'UNVERIFIED'}
