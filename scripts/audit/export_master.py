"""Export current audit payloads without copying application code or historical assumptions."""

import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

from collect_master import TOKEN, git, write_json, write_csv, digest, own


def sanitize(data, suffix):
    if suffix == '.xlsx':
        output = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(data)) as src, zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                blob = src.read(item.filename)
                if item.filename.endswith(('.xml','.rels')):
                    blob = TOKEN.sub('[REDACTED]',blob.decode('utf-8')).encode('utf-8')
                dst.writestr(item,blob)
        return output.getvalue()
    text = data.decode('utf-8-sig')
    return TOKEN.sub('[REDACTED]',text).encode('utf-8')


def export(source,target):
    out = target/'source-audits/master/2026-11-18'
    records=[]
    # Import deterministic evidence and explicitly generated candidate catalogs, not seeded release templates.
    for folder in ('inventory','evidence','data_dictionary','process_maps','semantic_flow_analysis',
                   'business_glossary','completeness','custom'):
        root = source/'.brownfield/work'/folder
        for path in sorted(root.rglob('*')):
            if not path.is_file():
                continue
            raw=path.read_bytes()
            payload=sanitize(raw,path.suffix.lower())
            dest=out/'brownfield'/folder/path.relative_to(root)
            dest.parent.mkdir(parents=True,exist_ok=True)
            compression=None
            if len(payload)>1000000 and path.suffix!='.xlsx':
                dest=dest.with_name(dest.name+'.gz')
                dest.write_bytes(gzip.compress(payload,mtime=0))
                compression='gzip'
            else:
                dest.write_bytes(payload)
            records.append({'source_path':path.relative_to(source).as_posix(),
                'path':dest.relative_to(target).as_posix(),'source_sha256':digest(raw),
                'export_sha256':digest(payload),'compression':compression,'bytes':len(payload)})
    for relative in ('.brownfield/PROJECT_STATE.json','.brownfield/config/project.yaml'):
        path=source/relative
        dest=out/'brownfield'/path.name
        payload=sanitize(path.read_bytes(),path.suffix)
        dest.write_bytes(payload)
        records.append({'source_path':relative,'path':dest.relative_to(target).as_posix(),
            'source_sha256':digest(path.read_bytes()),'export_sha256':digest(payload),'compression':None,'bytes':len(payload)})
    write_json(out/'export-manifest.json',{'entries':records,
        'note':'Seeded release placeholders omitted from this current export. Original Peru release artifacts remain historical.',
        'source_commit':git(source,'rev-parse','master').decode().strip()})
    old_manifest=target/'knowledge/manifest.json'
    old=json.loads(old_manifest.read_text(encoding='utf-8-sig'))
    history=target/'knowledge/history/manifest-20261001.json'
    if not history.exists():
        write_json(history,old)
    summary=json.loads((out/'audit-summary.json').read_text(encoding='utf-8'))
    graph_path=out/'graphify/summary.json'
    graph=json.loads(graph_path.read_text(encoding='utf-8'))
    graph.update({'symbol_less_warning_files':319,
        'coverage_note':'319 of 545 selected files yielded no symbols beyond a file node. Endpoint/request/SQL catalogs complement this AST representation.'})
    write_json(graph_path,graph)
    # The legacy augmentation has no native findings input: make that absence explicit, never zero-API success.
    write_json(out/'native-api-execution.json',summary['native_asgard'])
    manifest={
        'repository':{'name':'asgard-proveedores','url':'https://github.com/KPO-Group/proveedores',
            'branch':'master','current_head':summary['commit'],'audited_commit':summary['commit'],
            'current_checkout':str(source),'functional_paths':['src','index_archivos','index.php','info.php',
                '.htaccess','.env-example.php','Dockerfile','package.json'],
            'comparison_branch':'master_peru','comparison_commit':summary['peru_commit']},
        'knowledge_pack':{'version':'0.2.0','generated_at':'2026-11-18','generated_by':
            'convertidor-knowledge plus pinned master audit and evidence review',
            'mode':'embedded-and-standalone','primary_scope':'master_with_explicit_country_variants'},
        'audits':{'graphify':{'status':'local_ast_only','source_path':'source-audits/master/2026-11-18/graphify',**graph},
            'brownfield':{'status':'INCOMPLETE_BASELINE','evidence_count':1091,'canonical':False,
                'source_path':'source-audits/master/2026-11-18/brownfield'},
            'api':{'status':'static_augmented_review','native_status':'not_executed_application_control',
                'endpoint_candidates':241,'consumed_call_candidates':20,
                'source_path':'source-audits/master/2026-11-18/brownfield/custom'}},
        'variants':{'bolivia':{'source_branch':'master','status':'country_specific_behavior_observed',
                            'documentation':'knowledge/variants/bolivia.md'},
                    'peru':{'source_branch':'master_peru','commit':summary['peru_commit'],
                            'status':'current_source_comparison_and_historical_database_evidence',
                            'documentation':'knowledge/variants/peru.md'}},
        'coverage':{'source_snapshot':'pinned_and_hashed','static_audit':'performed','database_schema':'missing_for_master',
            'runtime':'not_verified','deployed_roles_and_tenants':'not_verified','submodules':'not_audited',
            'human_business_approval':'pending','overall':'PARTIAL'},
        'history':{'peru_manifest':'knowledge/history/manifest-20261001.json',
                   'peru_export_manifest':'knowledge/transfer-artifacts.json',
                   'historical_graph':'source-audits/graphify/graph.json.gz',
                   'related_graphify_tool_audits':'source-audits/related-graphify-audits'},
        'trust_policy':old.get('trust_policy',{})}
    write_json(old_manifest,manifest)
    write_json(target/'knowledge/graph-summary.json',{
        'nodes':graph['nodes'],'edges':graph['edges'],'community_count':graph['communities'],
        'includes_third_party':'possible_residual_dependencies','dependency_exclusion_is_best_effort':True,
        'full_graph':'source-audits/master/2026-11-18/graphify/graph.json.gz',
        'historical_peru_graph':'source-audits/graphify/graph.json.gz'})
    # Table references are not a fabricated physical database dictionary.
    tables=json.loads((out/'table-usage.json').read_text(encoding='utf-8'))['tables']
    lines=['# Referencias de datos observadas en master','','Estado: candidatos de referencias SQL, sin DDL de master.',
           'Tipos, claves, relaciones e invariantes fisicas quedan desconocidos.','','| Tabla candidata | Lecturas | Escrituras | Fuentes de ejemplo |','| --- | ---: | ---: | --- |']
    for table in tables:
        refs=table['reads']+table['writes']
        examples='; '.join(f"{r['path']}:{r['line']}" for r in refs[:3])
        lines.append(f"| `{table['name']}` | {len(table['reads'])} | {len(table['writes'])} | {examples} |")
    page=target/'knowledge/general/table-reference.md'
    page.parent.mkdir(parents=True,exist_ok=True)
    page.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'exported_current_payloads':len(records),'summary':summary},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--target',default=str(Path(__file__).resolve().parents[2]))
    args=parser.parse_args()
    export(Path(args.source).resolve(),Path(args.target).resolve())
