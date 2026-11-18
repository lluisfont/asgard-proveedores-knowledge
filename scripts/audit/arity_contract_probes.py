"""Check the extracted signature with a sentinel body; no app body is evaluated."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from collect_master import git, write_json
from security_probes import extract_method, run_php


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    args = parser.parse_args()
    root = Path(args.source).resolve()
    commit = git(root, 'rev-parse', 'HEAD').decode().strip()
    if commit != 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707':
        raise ValueError('Wrong source pin')
    path = 'index_archivos/embarques/EmbarqueClass.php'
    content = (root/path).read_text(encoding='utf-8-sig')
    php = shutil.which('php')
    method = extract_method(php, content, 'getListaEmbarques')
    signature = method.split('{', 1)[0]
    body = 'class AuditFixture { public static '+signature+'{return "signature_satisfied";}}'
    body += '''
$cases=[];
foreach([1,2,5] as $n) {
    try { $v=call_user_func_array(['AuditFixture','getListaEmbarques'],array_fill(0,$n,0)); }
    catch(ArgumentCountError $e) { $v='ArgumentCountError'; }
    $cases[]=['arguments'=>$n,'actual'=>$v];
}
echo json_encode(['php_version'=>PHP_VERSION,'cases'=>$cases]);
'''
    result = json.loads(run_php(php, body))
    expected = ['ArgumentCountError', 'signature_satisfied', 'signature_satisfied']
    for case, value in zip(result['cases'], expected):
        case['expected'] = value
        case['status'] = 'pass' if case['actual'] == value else 'fail'
    result.update({'source_commit': commit, 'path': path,
        'source_normalized_sha256': hashlib.sha256(content.replace('\r\n', '\n').encode()).hexdigest(),
        'technique': 'source_signature_only_sentinel_body_boundary_check',
        'body_adaptation': 'Entire application method body replaced with a constant sentinel; only original parameter signature tested.',
        'passed': sum(c['status'] == 'pass' for c in result['cases']), 'total': len(expected),
        'application_body_executed': False, 'database_access': False, 'network_access': False,
        'limitation': 'PHP 8.4 CLI signature behavior only; does not execute the controller or prove production reachability.'})
    output = Path(__file__).resolve().parents[2]/'source-audits/master/2026-11-18/iterative/arity-contract-probes.json'
    write_json(output, result)
    print(json.dumps({k: result[k] for k in ['php_version', 'passed', 'total']}))


if __name__ == '__main__':
    main()
