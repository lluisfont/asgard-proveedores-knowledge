"""Validate the separate Peru head audit without reinterpreting historic M/P evidence."""

import hashlib
import json


def validate(root,cite):
    def read(path):
        return json.loads((root/path).read_text(encoding='utf-8-sig'))
    prefix = 'knowledge/reviews/peru-head-20261119/'
    accepted = read(prefix+'accepted-deltas.json')
    ledger = read(prefix+'iterations.json')
    records = accepted['deltas']
    if accepted['peru_head'] != '2a179e2e6472d5705d031665ecbc90c3d806edec' or ledger['peru_head'] != accepted['peru_head']:
        raise ValueError('Unexpected Peru audit pin')
    counts = {'new_findings':sum(r['classification']=='new_finding' for r in records),
              'improvements':sum(r['classification']=='improvement' for r in records)}
    if counts != ledger['counts'] or len({r['id'] for r in records}) != len(records):
        raise ValueError('Peru delta classification/count mismatch')
    source_pins = {accepted['peru_head'],accepted['previous_peru'],accepted['master_reference']}
    def walk(value):
        if isinstance(value,dict):
            if all(k in value for k in ['commit','path','line_start','line_end']) and value['commit'] in source_pins:
                cite(value['commit'],value['path'],value['line_start'],value['line_end'])
            for v in value.values():walk(v)
        elif isinstance(value,list):
            for v in value:walk(v)
    walk(accepted)
    prior = None
    streak = 0
    for version, iteration in enumerate(ledger['iterations'],1):
        state = read(iteration['snapshot'])
        expected = {'baseline_knowledge_commit':accepted['baseline_knowledge_commit'],
                    'peru_head':accepted['peru_head'],'previous_peru':accepted['previous_peru'],
                    'master_reference':accepted['master_reference'],
                    'deltas':sorted([r for r in records if r['first_version']<=version],key=lambda r:r['id'])}
        if state != expected or iteration['version'] != version or iteration['status'] != 'completed':
            raise ValueError('Peru snapshot or receipt mismatch')
        canonical = json.dumps(state,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
        digest = hashlib.sha256(canonical).hexdigest()
        if digest != iteration['semantic_sha256'] or hashlib.sha256((root/iteration['snapshot']).read_bytes()).hexdigest()!=iteration['snapshot_sha256']:
            raise ValueError('Peru semantic/file hash mismatch')
        new = [r for r in records if r['first_version']==version]
        for key,kind in [('new_findings','new_finding'),('improvements','improvement')]:
            if set(iteration[key])!={r['id'] for r in new if r['classification']==kind}:
                raise ValueError('Peru pass delta mismatch')
        proof = read(iteration['artifact'])
        walk(proof)
        if not new:
            if prior!=digest or proof.get('new_findings')!=[] or proof.get('improvements')!=[] or not proof.get('checks'):
                raise ValueError('Invalid zero-delta Peru pass')
            if any(c.get('status') not in {'completed','pass'} for c in proof['checks']):
                raise ValueError('Peru closure check incomplete')
            streak+=1
        else:streak=0
        prior=digest
    if not ledger['converged'] or streak<2 or streak!=ledger['consecutive_zero_delta_passes']:
        raise ValueError('Peru convergence criterion not reached')
    summary=read('source-audits/peru/2026-11-19/summary.json')
    tree=read('source-audits/peru/2026-11-19/tree-comparison.json')
    if summary['source_commit']!=accepted['peru_head'] or tree['counts']!={'identical':10682,'changed':3}:
        raise ValueError('Peru profile tree/pin mismatch')
    return {**counts,'peru_head':accepted['peru_head'],'completed_passes':len(ledger['iterations']),
            'consecutive_zero_delta_passes':streak,'semantic_sha256':prior,'coverage':'PARTIAL'}
