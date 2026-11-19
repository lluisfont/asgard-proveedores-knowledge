"""Create immutable cumulative Peru audit versions from reviewed deltas and pass receipts."""

import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT/'knowledge/reviews/peru-head-20261119'

REPORT_MAPPING = {
    'PH-001': 'TEMP-PH002',
    'PH-002': 'TEMP-PH003',
    'PH-003': 'TEMP-PH004',
    'PH-004': 'TEMP-PH005',
    'PH-IMP-001': 'TEMP-PH001',
    'PH-IMP-002': 'TEMP-PH006',
    'PH-IMP-003': 'TEMP-PH007',
    'PH-IMP-004': 'TEMP-PH008',
    'PH-IMP-005': 'TEMP-PH010',
}
CF_MAPPING = {
    'PH-IMP-006': 'TEMP-CF001',
    'PH-IMP-007': 'TEMP-CF002',
    'PH-IMP-008': 'TEMP-CF003',
}


def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',', ':')).encode('utf-8')


def prepare_inputs():
    """Build the parent acceptance registry from the immutable child reviews."""
    report_path = FOLDER/'report-deltas.json'
    carry_path = FOLDER/'carryforward-deltas.json'
    report = json.loads(report_path.read_text(encoding='utf-8-sig'))
    carry = json.loads(carry_path.read_text(encoding='utf-8-sig'))
    report_items = {item['id']: item for item in report['items']}
    carry_items = {item['id']: item for item in carry['items']}
    records = []
    for version, mapping, items, origin in (
        (1, REPORT_MAPPING, report_items, report_path.relative_to(ROOT).as_posix()),
        (2, CF_MAPPING, carry_items, carry_path.relative_to(ROOT).as_posix()),
    ):
        for accepted_id, origin_id in mapping.items():
            record = copy.deepcopy(items[origin_id])
            source_classification = record['classification']
            record['id'] = accepted_id
            record['origin_id'] = origin_id
            record['origin_path'] = origin
            record['first_version'] = version
            record['classification'] = 'new_finding' if accepted_id.startswith('PH-') and not accepted_id.startswith('PH-IMP-') else 'improvement'
            record['origin_classification'] = source_classification
            record['canonical'] = False
            records.append(record)
    accepted = {
        'schema_version': '1.0',
        'baseline_knowledge_commit': '0c4bb99f076d6a8c18ae98375d6e154da6319922',
        'peru_head': '2a179e2e6472d5705d031665ecbc90c3d806edec',
        'previous_peru': '95fe9a4c3b3cddd84be922cc0e1eb9c88603df62',
        'master_reference': 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707',
        'deltas': records,
        'counts': {'new_findings': 4, 'improvements': 8},
        'materiality': 'Only new supported behavior or substantive knowledge correction. Equal blobs, repeated checks, timestamps and clerical edits alone are not new findings.',
        'coverage': 'PARTIAL',
        'canonical': False,
    }
    (FOLDER/'accepted-deltas.json').write_text(
        json.dumps(accepted,ensure_ascii=False,indent=2)+'\n', encoding='utf-8', newline='\n')
    passes = {'schema_version':'1.0','passes':[
        {'version':1,'technique':'Static report contract review with isolated probes','status':'completed',
         'new_findings':['PH-001','PH-002','PH-003','PH-004'],
         'improvements':['PH-IMP-001','PH-IMP-002','PH-IMP-003','PH-IMP-004','PH-IMP-005'],
         'artifact':'knowledge/reviews/peru-head-20261119/report-deltas.json'},
        {'version':2,'technique':'Git range carry-forward and provenance review','status':'completed',
         'new_findings':[],'improvements':['PH-IMP-006','PH-IMP-007','PH-IMP-008'],
         'artifact':'knowledge/reviews/peru-head-20261119/carryforward-deltas.json'},
        {'version':3,'technique':'SQL AST and metamorphic closure','status':'completed',
         'new_findings':[],'improvements':[],
         'artifact':'knowledge/reviews/peru-head-20261119/closure-sql.json'},
        {'version':4,'technique':'Reverse provenance closure on the published parent snapshot','status':'completed',
         'new_findings':[],'improvements':[],
         'artifact':'knowledge/reviews/peru-head-20261119/closure-provenance.json'},
    ]}
    (FOLDER/'passes.json').write_text(
        json.dumps(passes,ensure_ascii=False,indent=2)+'\n', encoding='utf-8', newline='\n')
    return accepted, passes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    accepted, prepared_passes = prepare_inputs()
    if args.prepare_only:
        print(json.dumps({'accepted':accepted['counts'],'passes':len(prepared_passes['passes'])}))
        return
    receipts = prepared_passes['passes']
    records = accepted['deltas']
    counts = {'new_findings': sum(r['classification'] == 'new_finding' for r in records),
              'improvements': sum(r['classification'] == 'improvement' for r in records)}
    if len({r['id'] for r in records}) != len(records):
        raise ValueError('Duplicate accepted delta')
    folder = FOLDER/'versions'
    folder.mkdir(exist_ok=True)
    prior = None
    iterations = []
    streak = 0
    for version, receipt in enumerate(receipts,1):
        if receipt['status'] != 'completed':
            raise ValueError('An incomplete or rejected review cannot count as a pass')
        items = [r for r in records if r['first_version'] <= version]
        delta = [r for r in records if r['first_version'] == version]
        if set(receipt['new_findings']) != {r['id'] for r in delta if r['classification'] == 'new_finding'} or set(receipt['improvements']) != {r['id'] for r in delta if r['classification'] == 'improvement'}:
            raise ValueError('Receipt and accepted deltas disagree')
        state = {'baseline_knowledge_commit': accepted['baseline_knowledge_commit'],
                 'peru_head': accepted['peru_head'], 'previous_peru': accepted['previous_peru'],
                 'master_reference': accepted['master_reference'], 'deltas': sorted(items,key=lambda r:r['id'])}
        digest = hashlib.sha256(canonical(state)).hexdigest()
        snapshot = folder/f'audit-v{version:02d}.json'
        snapshot.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        if not delta:
            proof = json.loads((ROOT/receipt['artifact']).read_text(encoding='utf-8-sig'))
            if proof.get('new_findings') != [] or proof.get('improvements') != [] or not proof.get('checks'):
                raise ValueError('Zero-delta receipt requires a completed exploratory review')
            if any(c.get('status') not in {'completed','pass'} for c in proof['checks']):
                raise ValueError('Review checks not completed')
            if prior != digest:
                raise ValueError('A declared zero-delta version changed the accepted state')
            streak += 1
        else:
            streak = 0
        iterations.append({'version':version, **receipt, 'semantic_sha256':digest,
            'snapshot':snapshot.relative_to(ROOT).as_posix(),
            'snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
            'consecutive_zero_delta_passes':streak})
        prior = digest
    if any(r['first_version'] > len(iterations) for r in records):
        raise ValueError('Accepted delta lacks a pass')
    ledger = {'schema_version':'1.0','audit_date':'2026-11-19','timezone':'Europe/Madrid',
        'baseline_knowledge_commit':accepted['baseline_knowledge_commit'],
        'peru_head':accepted['peru_head'],'previous_peru':accepted['previous_peru'],
        'master_reference':accepted['master_reference'], 'counts':counts,
        'iterations':iterations, 'consecutive_zero_delta_passes':streak, 'converged':streak>=2,
        'coverage':'PARTIAL','canonical':False,
        'materiality':'Only new supported behavior or substantive knowledge correction. Equal blobs, repeated checks, timestamps and clerical edits alone are not new findings.',
        'excluded_reviews':['Browser-output/navigation security review: prior automatic rejection; not retried or counted as zero.',
                            'Native ASGARD executable: prior AppControl block; not executed or bypassed.',
                            'New master remote head: outside this Peru audit; master reference stays immutable.']}
    (FOLDER/'iterations.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'counts':counts,'versions':len(iterations),'converged':ledger['converged'],'streak':streak}))


if __name__ == '__main__':
    main()
