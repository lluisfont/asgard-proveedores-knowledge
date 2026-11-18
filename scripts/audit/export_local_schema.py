"""Export only structural DDL metadata from an explicitly unauthoritative local schema candidate."""

import argparse
import gzip
import json
from pathlib import Path

from collect_master import digest, write_json, write_csv


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--parsed-root',required=True)
    parser.add_argument('--original',required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    parsed=Path(args.parsed_root).resolve()
    original=Path(args.original).resolve()
    if digest(original.read_bytes())!='a0833cde6629ac2d458dad6faaa17df4c61af19401eacad59e4bc4400aa5d1e5':
        raise ValueError('This candidate profile is pinned to the local asgard.sql fingerprint observed on 2026-11-18')
    candidate=parsed/'asgard.sql'
    if digest(original.read_bytes())!=digest(candidate.read_bytes()):
        raise ValueError('Parsed SQL copy does not match the local source')
    full=json.loads((parsed/'.brownfield/work/data_dictionary/data_dictionary.json').read_text(encoding='utf-8'))
    schemas={
        'tables':['table','source','line','evidence_id'],
        'columns':['table','column','data_type','nullable','key_role','source','line','evidence_id'],
        'relations':['from_table','from_column','to_table','to_column','relation_type','constraint_name','on_delete','on_update','source','line','evidence_id'],
        'indexes':['table','index_name','index_type','columns','source','line','evidence_id'],
        'constraints':['table','constraint_name','constraint_type','columns','referenced_table','referenced_columns','on_delete','on_update','source','line','evidence_id'],
        'database_objects':['object_type','object_name','source','line','evidence_id']}
    exported={name:[{key:row.get(key,'') for key in keys} for row in full[name]] for name,keys in schemas.items()}
    out=root/'source-audits/local-schema-candidate/2026-11-18'
    out.mkdir(parents=True,exist_ok=True)
    for name,keys in schemas.items():
        write_csv(out/(name+'.csv'),exported[name],keys)
    payload=json.dumps(exported,ensure_ascii=False,indent=2).encode('utf-8')
    (out/'structure.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    table_names={row['table'].lower() for row in exported['tables']}
    master=json.loads((root/'source-audits/master/2026-11-18/table-usage.json').read_text(encoding='utf-8'))['tables']
    matched=[row['name'] for row in master if row['name'].lower() in table_names]
    unmatched=[row['name'] for row in master if row['name'].lower() not in table_names]
    summary={'status':'LOCAL_SCHEMA_CANDIDATE_UNVERIFIED','source_file':original.name,
        'source_sha256':digest(original.read_bytes()),'source_bytes':original.stat().st_size,
        'header_schema_name':'asgard','header_environment_label':'Asgard_dev','header_export_date':'2026-07-23',
        'country':'unknown','git_commit':None,'matches_master_deployment':'not_verified',
        'counts':{name:len(records) for name,records in exported.items()},
        'master_reference_candidates_found_in_local_schema':len(matched),
        'master_reference_candidates_unmatched':unmatched,
        'unmatched_names_do_not_prove_missing_tables':True,
        'note':'Matching names is not proof of compatible columns, deployed schema, business meaning or country. Unmatched candidates may include temporary/view names or lexical false positives (for example FROM inside TRIM). No INSERT data, credentials, defaults, server address or routine bodies are exported.'}
    write_json(out/'summary.json',summary)
    lines=['# Diccionario estructural SQL local candidato','','Estado: LOCAL_SCHEMA_CANDIDATE_UNVERIFIED.',
           '', 'Fuente local: asgard.sql, dump etiquetado Asgard_dev/asgard con fecha 2026-07-23. '
           'No esta versionado en los commits auditados. Pais y correspondencia con master/Peru sin confirmar.',
           '',f"Extraccion Brownfield: {len(exported['tables'])} tablas, {len(exported['columns'])} columnas, "
           f"{len(exported['relations'])} relaciones declaradas, {len(exported['indexes'])} indices y "
           f"{len(exported['database_objects'])} objetos SQL.",
           '',f'{len(matched)} de {len(master)} nombres candidatos usados por master aparecen en este DDL. '
           'Eso demuestra coincidencia nominal, no compatibilidad completa ni autoridad del esquema.',
           '', '## Catalogos','','- [Tablas](../../source-audits/local-schema-candidate/2026-11-18/tables.csv).',
           '- [Columnas y tipos](../../source-audits/local-schema-candidate/2026-11-18/columns.csv).',
           '- [Relaciones declaradas](../../source-audits/local-schema-candidate/2026-11-18/relations.csv).',
           '- [Indices](../../source-audits/local-schema-candidate/2026-11-18/indexes.csv).',
           '- [Constraints](../../source-audits/local-schema-candidate/2026-11-18/constraints.csv).',
           '- [Funciones/procedimientos](../../source-audits/local-schema-candidate/2026-11-18/database_objects.csv).',
           '- [Estructura JSON comprimida](../../source-audits/local-schema-candidate/2026-11-18/structure.json.gz).',
           '- [Procedencia y hash](../../source-audits/local-schema-candidate/2026-11-18/summary.json).',
           '', 'Se conservan lineas e IDs de evidencia del archivo local para revisar cada declaracion. '
           'No se publican registros INSERT, valores por defecto, direcciones de servidor ni cuerpos '
           'de rutinas. Las definiciones de negocio revisadas estan en el glosario; los nombres SQL '
           'no se convierten automaticamente en terminos validados.',
           '', '## Pendiente de confirmar','',
           'Confirmar propietario, entorno y version de este dump y contrastar columnas, indices, '
           'rutinas y catalogos contra la base usada por cada commit desplegado. Hasta entonces '
           'este perfil se mantiene separado tanto del esquema historico de Peru como del modelo '
           'general basado en consultas de master.']
    (root/'knowledge/general/local-schema-candidate.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    manifest_path=root/'knowledge/manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['audits']['local_schema_candidate']={'status':summary['status'],'source_sha256':summary['source_sha256'],
        'documentation':'knowledge/general/local-schema-candidate.md','counts':summary['counts'],
        'country':'unknown','master_deployment_correspondence':'not_verified'}
    write_json(manifest_path,manifest)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
