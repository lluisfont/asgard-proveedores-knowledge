"""Hash all current audit payloads; generated index is deliberately outside the indexed subtree."""

import gzip
import hashlib
import json
from pathlib import Path


def main():
    root=Path(__file__).resolve().parents[2]
    records=[]
    paths=[]
    for directory in ('source-audits/master/2026-11-18','source-audits/master/2026-11-19','source-audits/local-schema-candidate/2026-11-18','source-audits/peru/2026-11-19'):
        paths.extend((root/directory).rglob('*'))
    for path in sorted(paths):
        if not path.is_file():
            continue
        stored=path.read_bytes()
        payload=gzip.decompress(stored) if path.suffix=='.gz' else stored
        records.append({'path':path.relative_to(root).as_posix(),
                        'export_sha256':hashlib.sha256(payload).hexdigest(),
                        'stored_sha256':hashlib.sha256(stored).hexdigest(),
                        'compression':'gzip' if path.suffix=='.gz' else None,
                        'bytes':len(payload),'stored_bytes':len(stored)})
    result={'schema_version':'1.0','source_commit':'a8ce2c23dead8552d2c4699e4a9b9134f7a18707',
            'entries':records,'note':'Integrity of the current static evidence snapshot, not validation of runtime behavior.'}
    peru_summary=root/'source-audits/peru/2026-11-19/summary.json'
    if peru_summary.exists():
        summary=json.loads(peru_summary.read_text(encoding='utf-8-sig'))
        result['source_commits']={'master_reference':summary['master_reference_commit'],
            'master_head':'a44f4ed69470f1bc00c800e592eadfce1bac6053',
            'peru_previous':summary['previous_peru_commit'],'peru_head':summary['source_commit']}
    (root/'knowledge/current-artifacts.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Indexed '+str(len(records))+' current audit payloads')


if __name__=='__main__':
    main()
