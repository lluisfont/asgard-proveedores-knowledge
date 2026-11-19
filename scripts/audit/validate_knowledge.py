"""Verify current evidence hashes, glossary schema, source references, formats and navigation."""

import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree

import jsonschema

from collect_master import TOKEN
from validate_iterative import validate as validate_iterative


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source')
    parser.add_argument('--peru-source')
    parser.add_argument('--peru-head-source')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    manifest=json.loads((root/'knowledge/manifest.json').read_text(encoding='utf-8-sig'))
    master=manifest['repository']['audited_commit']
    peru=manifest['repository']['comparison_commit']
    source_roots={master:Path(args.source).resolve() if args.source else None,
                  peru:Path(args.peru_source).resolve() if args.peru_source else None}
    peru_head=manifest['repository'].get('peru_audited_commit')
    if peru_head:
        source_roots[peru_head]=Path(args.peru_head_source).resolve() if args.peru_head_source else None
    for commit,source in source_roots.items():
        if source is None:
            continue
        actual=subprocess.run(['git','-C',str(source),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
        if actual!=commit:
            raise ValueError('Source checkout commit mismatch')
        changed=subprocess.run(['git','-C',str(source),'diff','--name-only','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
        if changed:
            raise ValueError('Tracked source changes invalidate reference verification')
    known_paths={master:set(),peru:set()}
    with (root/'source-audits/master/2026-11-18/branch-comparison.csv').open(encoding='utf-8',newline='') as file:
        for record in csv.DictReader(file):
            if record['master_blob']:
                known_paths[master].add(record['path'])
            if record['peru_blob']:
                known_paths[peru].add(record['path'])
    if peru_head:
        with (root/'source-audits/peru/2026-11-19/inventory.csv').open(encoding='utf-8-sig',newline='') as file:
            known_paths[peru_head]={row['path'] for row in csv.DictReader(file)}
    lines_cache={}
    citations=set()
    def cite(commit,path,start,end):
        if commit not in known_paths or path not in known_paths[commit]:
            raise ValueError('Source reference not in pinned tree: '+commit+':'+path)
        if start<1 or end<start:
            raise ValueError('Invalid source line range: '+path)
        source=source_roots[commit]
        if source:
            key=(commit,path)
            if key not in lines_cache:
                lines_cache[key]=len((source/path).read_text(encoding='utf-8-sig',errors='replace').splitlines())
            if end>lines_cache[key]:
                raise ValueError('Source line out of range: '+path+':'+str(end))
        citations.add((commit,path,start,end))
    glossary=json.loads((root/'knowledge/glossary/business-glossary.json').read_text(encoding='utf-8-sig'))
    if 'schema' in glossary:
        jsonschema.Draft202012Validator(glossary['schema']).validate(glossary)
    entries=glossary['entries']
    glossary_csv=list(csv.DictReader((root/'knowledge/glossary/business-glossary.csv').open(encoding='utf-8-sig',newline='')))
    if len(glossary_csv)!=len(entries):
        raise ValueError('Glossary CSV count differs from JSON')
    for entry,row in zip(entries,glossary_csv):
        if any(row[key]!=entry[key] for key in ['id','term','definition','scope','confidence']) or json.loads(row['evidence'])!=entry['evidence']:
            raise ValueError('Glossary CSV is stale: '+entry['id'])
    ids=set()
    for entry in entries:
        if entry['id'] in ids:
            raise ValueError('Duplicate glossary ID')
        ids.add(entry['id'])
        if not entry['definition'].strip() or len(entry['definition'])<30:
            raise ValueError('Missing substantive glossary definition')
        if entry['confidence'] not in {'observed','inferred','unknown'}:
            raise ValueError('Invalid confidence')
        evidence_commits=set()
        for evidence in entry['evidence']:
            commit=evidence['ref'].split('@')[-1]
            evidence_commits.add(commit)
            cite(commit,evidence['path'],evidence['line_start'],evidence['line_end'])
        if entry['scope']=='shared_evidence' and evidence_commits!={master,peru}:
            raise ValueError('Shared glossary claim lacks both pinned sources: '+entry['id'])
    current=json.loads((root/'knowledge/current-artifacts.json').read_text(encoding='utf-8'))
    for record in current['entries']:
        path=(root/record['path']).resolve()
        if not path.is_relative_to(root):
            raise ValueError('Unsafe artifact path')
        if path.name=='.env.php' or path.suffix in {'.sql','.php','.exe','.dll'}:
            raise ValueError('Application source, raw dump or executable must not be exported: '+record['path'])
        stored=path.read_bytes()
        payload=gzip.decompress(stored) if record['compression']=='gzip' else stored
        if hashlib.sha256(payload).hexdigest()!=record['export_sha256'] or hashlib.sha256(stored).hexdigest()!=record['stored_sha256']:
            raise ValueError('Current evidence hash mismatch: '+record['path'])
        if path.suffix=='.xlsx':
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                if archive.testzip():
                    raise ValueError('Broken workbook')
                for name in archive.namelist():
                    if name.endswith(('.xml','.rels')):
                        xml=archive.read(name)
                        ElementTree.fromstring(xml)
                        if TOKEN.search(xml.decode('utf-8')):
                            raise ValueError('Credential-shaped token in workbook: '+record['path'])
        else:
            text=payload.decode('utf-8-sig')
            if TOKEN.search(text):
                raise ValueError('Credential-shaped token in current evidence: '+record['path'])
            suffix=Path(path.stem).suffix if path.suffix=='.gz' else path.suffix
            if suffix=='.json':
                json.loads(text)
            elif suffix=='.jsonl':
                for line in text.splitlines():
                    if line.strip():
                        json.loads(line)
            elif suffix=='.csv':
                list(csv.reader(io.StringIO(text,newline=''),strict=True))
    link_pattern=re.compile(r'\[[^\]\n]*\]\(([^)\n]+)\)')
    source_pattern=re.compile(r'https://github\.com/KPO-Group/proveedores/blob/([0-9a-f]{40})/([^\s)#]+)#L(\d+)(?:-L(\d+))?')
    abbreviated_source_pattern=re.compile(r'\b(M|P2|P95|P):([^`\s;]+?):(L\d+(?:-L\d+)?(?:,L\d+(?:-L\d+)?)*)')
    installed_checkout=(root/'index.php').exists()
    documents=sorted((root/'knowledge').rglob('*.md'))
    if not installed_checkout:
        documents += [root/'README.md',root/'QUICK_START.md',root/'BUSINESS_GLOSSARY.md']
    # The historical transfer scope keeps source-era links; current docs must all resolve locally.
    documents=[p for p in documents if 'history' not in p.parts]
    local_links=0
    for path in documents:
        text=path.read_text(encoding='utf-8-sig')
        if TOKEN.search(text):
            raise ValueError('Credential-shaped token in documentation: '+str(path))
        for destination in link_pattern.findall(text):
            if destination.startswith(('https://','http://','mailto:','#')):
                continue
            destination=unquote(destination.split('#')[0])
            if destination and not (path.parent/destination).exists():
                raise ValueError('Broken local link: '+path.relative_to(root).as_posix()+': '+destination)
            local_links+=1
        for commit,source,start,end in source_pattern.findall(text):
            cite(commit,unquote(source),int(start),int(end or start))
        for branch,source,ranges in abbreviated_source_pattern.findall(text):
            for line_range in ranges.split(','):
                bounds=[int(v.removeprefix('L')) for v in line_range.split('-')]
                commit=master if branch=='M' else peru_head if branch=='P2' else peru
                cite(commit,source,bounds[0],bounds[-1])
    security=json.loads((root/'knowledge/general/security-findings.json').read_text(encoding='utf-8'))
    finding_ids=set()
    for finding in security['findings']:
        if finding['id'] in finding_ids or finding['commit']!=master:
            raise ValueError('Duplicate finding or wrong source commit')
        finding_ids.add(finding['id'])
        for evidence in finding['evidence']:
            cite(master,evidence['path'],evidence['line_start'],evidence['line_end'])
    dispositions=list(csv.DictReader((root/'knowledge/glossary/historical-candidates-disposition.csv').open(encoding='utf-8',newline='')))
    if len(dispositions)!=891 or len({r['id'] for r in dispositions})!=891:
        raise ValueError('Historical glossary candidates not fully accounted for')
    probes=json.loads((root/'source-audits/master/2026-11-18/guard-probes.json').read_text(encoding='utf-8'))
    if probes['passed']!=probes['total']:
        raise ValueError('Guard probe failure unresolved')
    security_probes=json.loads((root/'source-audits/master/2026-11-18/security-probes.json').read_text(encoding='utf-8'))
    if security_probes['passed']!=security_probes['total']:
        raise ValueError('Independent security probe failure unresolved')
    iterative=validate_iterative(root,cite) if (root/'knowledge/reviews/iterative-20261118/iterations.json').exists() else None
    peru_review=None
    if (root/'knowledge/reviews/peru-head-20261119/iterations.json').exists():
        from validate_peru_head import validate as validate_peru_head
        peru_review=validate_peru_head(root,cite)
    report={'status':'PASS','context':'installed_application_checkout' if installed_checkout else 'standalone_knowledge',
        'source_commit':master,'peru_commit':peru,
        'current_payloads_verified':len(current['entries']),'glossary_terms':len(entries),
        'reviewed_security_findings':len(finding_ids),
        'historical_candidates_accounted_for':len(dispositions),'documents_checked':len(documents),
        'local_links_checked':local_links,'distinct_pinned_source_citations':len(citations),
        'source_line_bounds_verified':all(source_roots.values()),'guard_cases_passed':probes['passed'],
        'independent_security_cases_passed':security_probes['passed'],
        'iterative_review':iterative,
        'peru_head_review':peru_review,
        'database_schema':'missing_for_master','runtime_end_to_end':'not_verified','business_approval':'pending',
        'overall_audit_coverage':'PARTIAL',
        'note':'PASS validates evidence integrity, structure and references. It does not certify business correctness or close security findings.'}
    (root/'knowledge/snapshots/current/knowledge-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    try:
        main()
    except Exception as error:
        print('Knowledge validation FAIL: '+str(error),file=sys.stderr)
        raise SystemExit(1)
