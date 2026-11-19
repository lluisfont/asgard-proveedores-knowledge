"""Close the Peru HEAD provenance pass against the generated parent snapshot."""

import copy
import hashlib
import json
from pathlib import Path

from compile_peru_head_review import FOLDER, ROOT, prepare_inputs


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_parent(actual, expected, documents):
    require(actual == expected, 'Accepted registry differs from its reviewed source normalization')
    require(actual['counts'] == {'new_findings': 4, 'improvements': 8}, 'Unexpected accepted counts')
    require(actual['peru_head'] == '2a179e2e6472d5705d031665ecbc90c3d806edec', 'Unexpected Peru HEAD pin')
    require(actual['previous_peru'] == '95fe9a4c3b3cddd84be922cc0e1eb9c88603df62', 'Unexpected P95 pin')
    require(actual['master_reference'] == 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707', 'Unexpected master reference')
    require(actual['canonical'] is False and actual['coverage'] == 'PARTIAL', 'Trust boundary changed')
    ids = {record['id'] for record in actual['deltas']}
    require(len(ids) == 12, 'Expected twelve unique accepted records')
    for name, text in documents.items():
        missing = sorted(record_id for record_id in ids if record_id not in text)
        require(not missing, f'{name} omits accepted IDs: {missing}')
        require('PARTIAL' in text and 'a44f4ed' in text, f'{name} omits coverage/master boundary')


def main():
    expected, _ = prepare_inputs()
    accepted_path = FOLDER/'accepted-deltas.json'
    actual = json.loads(accepted_path.read_text(encoding='utf-8-sig'))
    parent_paths = {
        'review_readme': FOLDER/'README.md',
        'variant_page': ROOT/'knowledge/variants/peru-head-20261119.md',
        'accepted_registry': accepted_path,
    }
    documents = {name: path.read_text(encoding='utf-8-sig') for name, path in parent_paths.items() if path.suffix == '.md'}
    validate_parent(actual, expected, documents)

    mutations = []
    cases = []
    value = copy.deepcopy(actual); value['deltas'][0]['classification'] = 'improvement'; cases.append(('classification', value))
    value = copy.deepcopy(actual); value['deltas'][0]['origin_id'] = 'TEMP-PH003'; cases.append(('origin_id', value))
    value = copy.deepcopy(actual); value['peru_head'] = actual['previous_peru']; cases.append(('peru_head_pin', value))
    value = copy.deepcopy(actual); value['deltas'][0]['evidence'][0]['line_start'] += 1; cases.append(('evidence_range', value))
    value = copy.deepcopy(actual); value['deltas'].pop(); cases.append(('record_count', value))
    value = copy.deepcopy(actual); value['canonical'] = True; cases.append(('canonical_boundary', value))
    for name, mutated in cases:
        rejected = False
        try:
            validate_parent(mutated, expected, documents)
        except ValueError:
            rejected = True
        require(rejected, f'Mutation was not rejected: {name}')
        mutations.append({'id': name, 'status': 'rejected'})

    closure_path = FOLDER/'closure-provenance.json'
    closure = json.loads(closure_path.read_text(encoding='utf-8-sig'))
    closure['status'] = 'completed'
    closure['review_sequence']['parent_integrated_snapshot_available'] = True
    closure['review_sequence']['post_parent_integration_closure_completed'] = True
    closure['delta_assessment'] = 'No additional material delta was found after reverse-tracing the twelve published records to the report and carry-forward sources.'
    closure['zero_delta_pass_eligible'] = True
    closure['global_convergence_claimed'] = False
    closure['next_action'] = 'Preserve the immutable pins and PARTIAL boundary. A new source head requires a new dated profile.'
    closure['parent_snapshot'] = [
        {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path)}
        for path in parent_paths.values()
    ]
    closure['mutation_controls']['parent_snapshot_mutations_applied'] = True
    closure['mutation_controls']['parent_snapshot_mutations'] = mutations
    pending_results = {
        'CP-PENDING-1': 'Parent README, Peru HEAD page and accepted registry fixed by SHA256.',
        'CP-PENDING-2': '12/12 published IDs reverse-traced to their reviewed origin records with pins and evidence unchanged.',
        'CP-PENDING-3': '6/6 deliberate parent-registry mutations rejected: classification, origin, pin, range, count and canonical boundary.',
    }
    for check in closure['checks']:
        if check['id'] in pending_results:
            check['status'] = 'completed'
            check['result'] = pending_results[check['id']]
            check.pop('pending', None)
    require(all(check.get('status') in {'completed', 'pass'} for check in closure['checks']), 'Closure still has incomplete checks')
    closure_path.write_text(json.dumps(closure,ensure_ascii=False,indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'status':'completed','accepted':actual['counts'],'parent_mutations_rejected':len(mutations)}))


if __name__ == '__main__':
    main()
