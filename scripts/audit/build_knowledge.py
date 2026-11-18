"""Build current reader views while retaining explicitly scoped historical evidence."""

import argparse
import csv
import gzip
import io
import json
from collections import Counter
from pathlib import Path


ROOT=Path(__file__).resolve().parents[2]
AUDIT='source-audits/master/2026-11-18/'


def read(relative):
    path=ROOT/relative
    payload=path.read_bytes() if path.exists() else gzip.decompress(Path(str(path)+'.gz').read_bytes())
    return payload.decode('utf-8-sig')


def data(relative):
    return json.loads(read(relative))


def rows(relative):
    return list(csv.DictReader(io.StringIO(read(relative))))


def write(relative,content):
    path=ROOT/relative
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content.rstrip()+'\n',encoding='utf-8',newline='\n')


def table(headers,records):
    def cell(value):
        return str(value).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+
                     ['| '+' | '.join(cell(v) for v in record)+' |' for record in records])


CONTRACT_MASTER_PIN='a8ce2c23dead8552d2c4699e4a9b9134f7a18707'


def consumption_contract_overlay(consumed,commit):
    """IMP-C1: reviewed contracts supplement raw candidates without rewriting them.

    Match the pinned evidence exactly so a later extractor/source change requires
    review instead of silently carrying this correction onto a different input.
    """
    if commit != CONTRACT_MASTER_PIN:
        raise ValueError('IMP-C1 requires review for the new source commit')
    report='index_archivos/reportes/inventario-por-chasis.php'
    specs=[
        (report,'71','GET_OR_UNKNOWN','UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/buscar-chasis'),
        (report,'93','GET_OR_UNKNOWN','UNRESOLVED_CONST:URL_API/inventario/proveedores/reportes/resumen-inventario'),
        ('index_archivos/embarques/frames/items.php','43','PUT','UNRESOLVED_CONST:URL_API'),
    ]
    matched=[]
    for spec in specs:
        candidates=[r for r in consumed if (r['file'],str(r['line']),r['method'],r['url'])==spec]
        if len(candidates)!=1:
            raise ValueError('IMP-C1 raw candidate changed or is ambiguous: '+str(spec))
        matched.append(candidates[0]['endpoint_id'])
    return {
        'id':'IMP-C1','status':'accepted','raw_candidate_ids':matched,
        'contracts':[
            ('POST',specs[0][3],'chasis; Authorization',
             '`M:index_archivos/reportes/inventario-por-chasis.php:L68-L86`'),
            ('POST',specs[1][3],'chasis, tipo_inventario_id; Authorization',
             '`M:index_archivos/reportes/inventario-por-chasis.php:L89-L123`'),
            ('GET','UNRESOLVED_CONST:URL_API/proveedores/detalle-pedido/{idpedido}',
             'idpedido en ruta; Authorization',
             '`M:index_archivos/embarques/frames/items.php:L42-L44,L99-L107` → '
             '`M:index_archivos/embarques/js/datosEmbarques.js:L1-L17`'),
        ],
        'rejected':('PUT','UNRESOLVED_CONST:URL_API',
                    '`M:index_archivos/embarques/frames/items.php:L43`',
                    'Input oculto de configuracion; no es una llamada a la raiz. '
                    'La cadena activa termina en GET detalle-pedido/{idpedido}.'),
    }


def api_reference_content(summary,endpoints,consumed):
    overlay=consumption_contract_overlay(consumed,summary['commit'])
    header=('AS-IS estatico del commit `'+summary['commit']+'`, rama `master`. '
            'Los candidatos requieren verificar configuracion y despliegue.\n\n')
    return ('# Referencia API y contratos candidatos\n\n'+header+
        'La aplicacion usa scripts PHP directos y llamadas AJAX. El catalogo raw del extractor conserva '
        f'{len(endpoints)} candidatos de exposicion y **{len(consumed)} candidatos raw de consumo externo**. '
        'El conteo raw no es un numero de llamadas confirmadas. El overlay revisado IMP-C1 que sigue '
        'corrige tres atribuciones y enlaza un caller real; no modifica los CSV/JSON/OpenAPI originales. '
        'No son rutas probadas mediante un servidor HTTP. Las peticiones de fichero, includes y '
        'paginas HTML pueden aparecer como candidatos junto a handlers JSON.\n\n'
        'La auditoria nativa ASGARD no se ejecuto: Windows Application Control bloqueo el '
        'lanzador instalado. El catalogo procede de los escaneres de ampliacion y del cruce '
        'con las evidencias de Brownfield. Los antiguos ceros nativos de Peru no describen master.\n\n'
        '## Catalogos\n\n'
        '- [Handlers, callers y tablas](../crosswalk/screens-endpoints-tables.md).\n'
        '- [Campos de peticion observados](../../source-audits/master/2026-11-18/request-fields.csv).\n'
        '- [Catalogo JSON raw provisional](../../source-audits/master/2026-11-18/brownfield/custom/asgard-api-audit-augmented/api-catalog.augmented.json).\n'
        '- [OpenAPI raw provisional](../../source-audits/master/2026-11-18/brownfield/custom/asgard-api-audit-augmented/openapi.augmented.yaml).\n'
        '- [Riesgos por endpoint](../../source-audits/master/2026-11-18/brownfield/custom/api-deep-iterative/endpoint_deep_risks.csv).\n\n'
        '## Interpretacion de respuestas\n\n'
        'Un campo JSON `code` no acredita que el servidor devuelva ese estado HTTP. '
        'Los metodos y parametros se infieren de accesos a superglobales y callers; los '
        'parametros calculados, sus tipos completos y las ramas dinamicas requieren revision '
        'del handler. La autenticacion puede depender de includes y de la configuracion web. '
        'Las senales locales de CSRF, sesion o ausencia de ellas no sustituyen esa comprobacion.\n\n'
        '## Contratos revisados — IMP-C1 aceptada\n\n'
        'M fija el commit indicado en la cabecera. En los casos siguientes, esta lectura de fuente '
        'prevalece sobre la atribucion raw. Una base de URL sin resolver no impide leer el metodo '
        'ni los parametros del caller.\n\n'+
        table(['Metodo observado','Destino','Parametros/contexto','Evidencia fijada'],overlay['contracts'])+
        '\n\n'+table(['Atribucion raw rechazada','Destino raw','Evidencia','Correccion'],[
            (overlay['rejected'][0],overlay['rejected'][1],overlay['rejected'][2],overlay['rejected'][3])])+
        '\n\nLa ruta de detalle se obtiene siguiendo el input `url_pedidos`, la inclusion de '
        '`datosEmbarques.js` y la llamada a `ver_detalle_posiciones_pedido`. No se atribuye un PUT '
        'a la raiz por el mero valor de ese input. Las dos filas POST reemplazan metodo desconocido; '
        'el GET aporta el contrato real del caller antes confundido con configuracion. '
        'No se deduce un nuevo total de APIs verificadas a partir de este overlay parcial.\n\n'
        '## Candidatos raw de consumo externo (sin reconciliar)\n\n'
        f'Las **{len(consumed)} filas originales** se conservan a continuacion para trazabilidad. '
        'Incluyen las atribuciones corregidas o rechazadas arriba; su presencia en esta tabla '
        'no las rehabilita como contratos. Los catalogos enlazados tambien conservan esos candidatos raw.\n\n'+
        table(['Metodo raw candidato','Destino/configuracion raw','Fuente','Linea','Senales raw'],
              [(r['method'],r['url'],r['file'],r['line'],r['risk_flags']) for r in consumed])+
        '\n\nLas constantes UNRESOLVED_CONST permanecen sin valor. No se contactaron servicios '
        'ni se verificaron contratos externos. Las credenciales detectadas se redactan.\n\n'
        'Reproducir solo esta vista: `python -B scripts/audit/build_knowledge.py --view api-reference`. '
        'La generacion completa utiliza el mismo overlay. Registro: '
        '[integracion de contratos](../reviews/iterative-20261118/contract-integration.json).')


def build_api_reference():
    summary=data(AUDIT+'audit-summary.json')
    endpoints=rows(AUDIT+'brownfield/custom/http_endpoint_catalog.csv')
    consumed=rows(AUDIT+'brownfield/custom/asgard-api-audit-augmented/consumed_api_augmented.csv')
    write('knowledge/general/api-reference.md',api_reference_content(summary,endpoints,consumed))
    print(json.dumps({'view':'api-reference','raw_consumed_candidates':len(consumed),'overlay':'IMP-C1'}))


def glossary_csv_content(glossary):
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=['id','term','definition','scope','confidence','evidence'],lineterminator='\n')
    writer.writeheader()
    for entry in glossary['entries']:
        row={k:entry.get(k,'') for k in ['id','term','definition','scope','confidence']}
        row['evidence']=json.dumps(entry['evidence'],ensure_ascii=False)
        writer.writerow(row)
    return stream.getvalue()


def build_glossary_csv(glossary=None):
    if glossary is None:
        glossary=data('knowledge/glossary/business-glossary.json')
    write('knowledge/glossary/business-glossary.csv',glossary_csv_content(glossary))
    return len(glossary['entries'])


def build():
    summary=data(AUDIT+'audit-summary.json')
    endpoints=rows(AUDIT+'brownfield/custom/http_endpoint_catalog.csv')
    compared={row['path']:row for row in rows(AUDIT+'branch-comparison.csv')}
    header=('AS-IS estatico del commit `'+summary['commit']+'`, rama `master`. '
            'Los candidatos requieren verificar configuracion y despliegue.\n\n')
    by_group=Counter()
    for endpoint in endpoints:
        parts=endpoint['handler'].split('/')
        by_group[parts[1] if len(parts)>2 else '(raiz)']+=1
    write('knowledge/product/business-domains.md','# Dominios y modulos de Proveedores\n\n'+header+
          'Entradas principales: [procesos](../general/workflows.md), [actores](../general/actors-and-permissions.md), '
          '[reglas](../general/business-rules.md), [glosario de negocio](../glossary/business-glossary.md).\n\n'+
          table(['Grupo de handlers','Candidatos'],by_group.most_common())+
          '\n\nEstas agrupaciones son tecnicas; no equivalen a bounded contexts confirmados. '
          'Las diferencias por pais estan en [variantes](../variants/README.md). '
          'Las pantallas dedicadas de pedidos y preembarques de Peru no se incorporan como funciones universales de master; master ya contiene operaciones relacionadas con pedidos.')
    write('knowledge/crosswalk/screens-endpoints-tables.md','# Pantallas, endpoints y datos\n\n'+header+
          'Fuente: `source-audits/master/2026-11-18/brownfield/custom/http_endpoint_catalog.csv`. '
          'Tablas leidas/escritas son referencias estaticas de fichero. No se dispone de DDL master.\n\n'+
          table(['Handler','Metodo inferido','Callers','Lecturas','Escrituras','Comparacion Peru'],
                [(r['handler'],r['method'],r['caller_sources'],r['tables_read'],r['tables_written'],
                  compared.get(r['handler'],{}).get('status','unknown')) for r in endpoints]))
    write('knowledge/crosswalk/endpoints-services-sql.md','# Endpoints, servicios y SQL\n\n'+header+
          'Los contratos y riesgos de consumo se conservan en [referencia API](../general/api-reference.md). '
          'Las referencias SQL con linea de origen estan en '
          '`source-audits/master/2026-11-18/sql-references.csv`. Su extraccion por tokens '
          'es candidata y no acredita nombres fisicos ni resolucion completa de SQL dinamico.\n\n'+
          'Las clases, los servicios externos y los datos se explican en '
          '[arquitectura](../general/architecture.md), [integraciones](../general/integrations.md), '
          '[modelo de datos](../general/data-model.md) y [tablas candidatas](../general/table-reference.md).')
    permissions=[json.loads(line) for line in read(AUDIT+'brownfield/evidence/evidence.jsonl').splitlines() if line.strip()]
    permissions=[p for p in permissions if p['kind']=='permission']
    write('knowledge/crosswalk/modules-permissions-clients.md','# Modulos, permisos y clientes\n\n'+header+
          '[Actores y permisos](../general/actors-and-permissions.md) desarrolla los tipos de proveedor '
          'y el contexto de sesion observado. Las '+str(len(permissions))+' marcas heuristicas '
          'de permiso del extractor proceden de licencias/codigo de dependencias y no se usan '
          'como prueba de permisos de negocio. Las fuentes relevantes revisadas son:\n\n'+
          table(['Referencia','Fuente fijada','Control observado y limite'],[
              ('AUTH-M-01','`M:index_archivos/permisos.php:L1-L27`','Guardia compartida de sesion; terminacion de rechazo condicionada por runtime, ver SEC-005'),
              ('AUTH-M-02','`M:index_archivos/MenuClass.php:L25-L40`','Permisos de menu por usuario y modulo; no acredita autorizacion de cada handler'),
              ('AUTH-M-03','`M:src/core/users/application/Find/UserFind.php:L16-L61`','Tipo de proveedor y contexto de empresa; no equivale a una matriz de permisos'),
              ('AUTH-M-04','`M:index_archivos/tracking/guardia_imagen.php:L1-L5`','Sesion y validacion parcial de ruta; propiedad del recurso pendiente')]))
    write('knowledge/crosswalk/risks-unresolved.md','# Riesgos y pendientes actuales\n\n'+header+
          'La [ampliacion iterativa](../reviews/iterative-20261118/README.md) incorpora '
          '[defectos operativos](../general/operational-findings.md), SEC-015 y precisiones de contratos. '
          'Su cierre acotado no corrige la aplicacion ni valida el despliegue.\n\n'+
          'Consultar la [auditoria de seguridad](../general/security-audit.md), '
          'los [hallazgos estructurados](../general/security-findings.json), '
          'las [preguntas pendientes](../general/open-questions.md) y el '
          '[plan de pruebas](../general/testing.md).\n\n'
          'El resultado global sigue PARTIAL: falta el esquema SQL de master, no se verifico '
          'el despliegue, los submodulos ni la matriz de autorizacion efectiva. '
          'La auditoria nativa ASGARD esta bloqueada por Application Control; sus resultados '
          'no se sustituyen por una falsa ausencia de APIs. Las senales de escaner se separan '
          'de hallazgos revisados y no equivalen automaticamente a vulnerabilidades confirmadas.')
    write('knowledge/product/data-model-guide.md','# Guia del modelo de datos\n\n'
          'La fuente actual es [modelo de datos de master](../general/data-model.md) y '
          '[referencias SQL candidatas](../general/table-reference.md). El esquema fisico de master '
          'no esta versionado en el repositorio auditado.\n\n'
          'El antiguo diccionario de 1,055 tablas y 10,111 columnas procede del dump historico '
          'de Peru y se conserva como tal en `source-audits/brownfield/reports/data_dictionary/`. '
          'Sus tipos, claves, relaciones y procedimientos no se trasladan a master por suposicion.')
    write('knowledge/product/user-manual-source.md','# Manual de usuario y fuentes\n\n'
          'El [manual reconstruido de master](../general/user-manual.md) se apoya en pantallas y '
          'flujos observados. Los [procesos](../general/workflows.md), [reglas](../general/business-rules.md) '
          'y [variantes](../variants/README.md) aclaran precondiciones y diferencias. '
          'La revision de negocio y la prueba en el despliegue real siguen pendientes.')
    write('knowledge/product/requirements-analysis-guide.md','# Analisis de requisitos\n\n'
          'Usar la [guia actual de requisitos](../general/requirements-guide.md). Separar AS-IS '
          'observado, inferencias, defectos, preguntas pendientes y TO-BE. '
          'Citar commit, fichero y lineas y especificar alcance comun, master/Bolivia o Peru. '
          'Una funcion exclusiva de Peru no debe convertirse automaticamente en requisito de master.')
    build_api_reference()
    # Account for every historical candidate without pretending identifier expansion validates meaning.
    historical=rows('source-audits/brownfield/reports/business_glossary/BUSINESS_GLOSSARY.csv')
    table_refs={t['name'].lower():t for t in data(AUDIT+'table-usage.json')['tables']}
    dispositions=[]
    for index,entry in enumerate(historical,1):
        obj=entry['source_object'].strip('`')
        observed=table_refs.get(obj.lower())
        refs=(observed['reads']+observed['writes']) if observed else []
        dispositions.append({'id':f'LEGACY-{index:04d}','term':entry['term'],'source_object':obj,
            'category':entry['category'],'historical_validation':entry['validation_status'],
            'current_disposition':'master_reference_candidate_no_master_ddl' if observed else 'historical_candidate_no_master_reference_verified',
            'current_evidence':'; '.join(f"{r['path']}:{r['line']}" for r in refs[:5]),
            'decision':'physical_schema_and_business_meaning_require_review'})
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=list(dispositions[0]),lineterminator='\n')
    writer.writeheader();writer.writerows(dispositions)
    write('knowledge/glossary/historical-candidates-disposition.csv',stream.getvalue())
    glossary=data('knowledge/glossary/business-glossary.json')
    entries=glossary['entries']
    glossary_stats={'business_terms':len(entries),'historical_candidates_accounted_for':len(dispositions),
        'historical_dispositions':dict(Counter(r['current_disposition'] for r in dispositions)),
        'warning':'Reviewed business concepts and legacy physical identifiers are different inventories. No human approval or master physical schema is implied.'}
    write('knowledge/glossary/coverage.json',json.dumps(glossary_stats,ensure_ascii=False,indent=2))
    build_glossary_csv(glossary)
    write('BUSINESS_GLOSSARY.md','# Diccionario de negocio de Proveedores\n\n'
          f'El [glosario de negocio](knowledge/glossary/business-glossary.md) desarrolla {len(entries)} '
          'conceptos con definiciones en espanol, relaciones, alcance por variante y evidencia de codigo.\n\n'
          'Disponible tambien en [JSON](knowledge/glossary/business-glossary.json) y '
          '[CSV](knowledge/glossary/business-glossary.csv). Los 891 candidatos del extractor historico '
          'se conservan con [disposicion individual](knowledge/glossary/historical-candidates-disposition.csv). '
          'La revision basada en codigo no sustituye la aprobacion por responsables de negocio.')
    manifest=data('knowledge/manifest.json')
    manifest['knowledge_pack']['glossary']=glossary_stats
    write('knowledge/manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    old_map=ROOT/'knowledge/evidence-map.md'
    historical_map=ROOT/'knowledge/history/evidence-map-20261001.md'
    if not historical_map.exists():
        historical_map.write_text(old_map.read_text(encoding='utf-8-sig'),encoding='utf-8')
    write('knowledge/evidence-map.md','# Mapa de evidencias actual\n\n'+header+
          '| Area | Evidencia actual |\n| --- | --- |\n'
          '| Procedencia | [Alcance](audit-scope.md), [manifiesto](manifest.json), [hashes actuales](current-artifacts.json) |\n'
          '| Conceptos y reglas | [Glosario](glossary/business-glossary.md), [reglas](general/business-rules.md), [procesos](general/workflows.md) |\n'
          '| Variantes | [Bolivia](variants/bolivia.md), [Peru](variants/peru.md), [comparacion](variants/comparison.md) |\n'
          '| Fuente versionada | [Inventario](../source-audits/master/2026-11-18/inventory.csv), [diferencias](../source-audits/master/2026-11-18/branch-comparison.csv) |\n'
          '| Graphify | [Grafo comprimido](../source-audits/master/2026-11-18/graphify/graph.json.gz), [metricas](../source-audits/master/2026-11-18/graphify/summary.json) |\n'
          '| Brownfield | [Evidencias](../source-audits/master/2026-11-18/brownfield/evidence/summary.json), [mapa tecnico](../source-audits/master/2026-11-18/brownfield/process_maps/PROCESS_MAP.md) |\n'
          '| Datos | [Modelo](general/data-model.md), [candidatos SQL](general/table-reference.md), [referencias con linea](../source-audits/master/2026-11-18/sql-references.csv) |\n'
          '| API | [Referencia](general/api-reference.md), [campos](../source-audits/master/2026-11-18/request-fields.csv), [catalogo](../source-audits/master/2026-11-18/brownfield/custom/http_endpoint_catalog.csv) |\n'
          '| Seguridad | [Revision](general/security-audit.md), [hallazgos](general/security-findings.json) |\n'
          '| Ampliacion iterativa | [Deltas aceptados](reviews/iterative-20261118/accepted-deltas.json), [versiones](reviews/iterative-20261118/iterations.json), [defectos operativos](general/operational-findings.json) |\n'
          '| Verificaciones | [Validacion del paquete](snapshots/current/knowledge-validation.json), [lint](../source-audits/master/2026-11-18/php-lint.json), [guardas](../source-audits/master/2026-11-18/guard-probes.json) |\n'
          '| Limites | [Cobertura documental](documentation-coverage.md), [pendientes](general/open-questions.md) |\n'
          '| Historia Peru | [Mapa original](history/evidence-map-20261001.md), [transferencia](transfer-scope.md) |\n\n'
          'El DDL de Peru se conserva como historial, no como esquema de master. '
          'Los archivos no verificados en ejecucion, las inferencias y los controles de despliegue pendientes '
          'mantienen su estado explicito. Los hashes validan transporte, no correccion funcional.')
    print(json.dumps({'endpoint_candidates':len(endpoints),'glossary':glossary_stats},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--view',choices=['all','api-reference','glossary-csv'],default='all',
                        help='Regenerate only the requested view; default preserves the full build.')
    args=parser.parse_args()
    if args.view=='api-reference':
        build_api_reference()
    elif args.view=='glossary-csv':
        print(json.dumps({'view':'glossary-csv','entries':build_glossary_csv()}))
    else:
        build()
