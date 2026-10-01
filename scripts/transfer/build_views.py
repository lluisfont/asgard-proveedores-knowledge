"""Build navigable evidence views from the exported audit tables."""

import csv
import gzip
import io
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BF = 'source-audits/brownfield/reports/'
API = 'source-audits/api/'


def text(path):
    p = ROOT / path
    data = p.read_bytes() if p.exists() else gzip.decompress(Path(str(p) + '.gz').read_bytes())
    return data.decode('utf-8-sig')


def rows(path):
    return list(csv.DictReader(io.StringIO(text(path))))


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def table(headers, values):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |'] +
                     ['| ' + ' | '.join(cell(v) for v in row) + ' |' for row in values])


def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.rstrip() + '\n', encoding='utf-8')


def main():
    endpoints = rows(BF + 'custom/http_endpoint_catalog.csv')
    domains = rows(BF + 'semantic_flow_analysis/DOMAIN_FLOW_SEMANTIC_SUMMARY.csv')
    risks = rows(API + 'api-deep-iterative/endpoint_deep_risks.csv')
    tables = rows(BF + 'data_dictionary/tables.csv')
    comparison = json.loads(text('knowledge/snapshots/current/audited-source-comparison.json'))
    grouped = Counter()
    for endpoint in endpoints:
        parts = endpoint['handler'].split('/')
        group = parts[1] if len(parts) > 2 and parts[0] == 'index_archivos' else '(raiz)'
        grouped[group] += 1
    write('knowledge/product/business-domains.md', '# Dominios y superficie candidata\n\n'
          'Agrupaciones tecnicas extraidas del catalogo PHP/AJAX historico. Los nombres de carpetas '
          'no confirman limites de negocio. Fuente: `source-audits/brownfield/reports/custom/http_endpoint_catalog.csv`.\n\n' +
          table(['Grupo de handlers', 'Candidatos'], sorted(grouped.items(), key=lambda x: (-x[1], x[0]))) +
          '\n\nReconstruccion semantica Brownfield, pendiente de revision humana:\n\n' +
          table(['Dominio candidato', 'Procesos', 'Tablas', 'Campos', 'Estado'],
                [(d['domain'], d['process_count'], d['table_count'], d['field_count'], d['validation_status']) for d in domains]) +
          '\n\nFuente: `source-audits/brownfield/reports/semantic_flow_analysis/DOMAIN_FLOW_SEMANTIC_SUMMARY.csv`. '
          'Las definiciones completas permanecen en los mapas, glosario y diccionarios originales.')
    write('knowledge/crosswalk/screens-endpoints-tables.md', '# Pantallas, endpoints y tablas\n\n'
          'Cruce estatico historico. `caller_sources` procede del catalogo aumentado; una referencia '
          'no demuestra que la ruta este desplegada ni que su autorizacion sea correcta. '
          'Fuente: `source-audits/brownfield/reports/custom/http_endpoint_catalog.csv`.\n\n' +
          table(['Handler / fuente', 'Metodo inferido', 'Callers detectados', 'Tablas leidas', 'Tablas escritas', 'Confianza'],
                [(e['handler'], e['method'], e['caller_sources'], e['tables_read'], e['tables_written'], e['confidence']) for e in endpoints]))
    write('knowledge/crosswalk/endpoints-services-sql.md', '# Endpoints, servicios y SQL\n\n'
          'Cada fila conserva la ruta, el handler y las senales estaticas originales. Las senales '
          'son candidatos de riesgo; requieren revisar includes, controles compartidos y ejecucion. '
          'Fuente: `source-audits/api/api-deep-iterative/endpoint_deep_risks.csv`.\n\n' +
          table(['Riesgo ID', 'Handler', 'Metodo', 'Tablas', 'Senales', 'Evidencia'],
                [(r['risk_id'], r['handler'], r['method'], r['tables'], r['flags'], r['evidence']) for r in risks]) +
          '\n\nLos contratos de servicios externos y las ubicaciones de consumo se conservan '
          'en `source-audits/api/asgard-api-audit-augmented/consumed_api_augmented.csv`. '
          'Las constantes de base sin resolver permanecen marcadas `UNRESOLVED_CONST`.')
    permissions = [json.loads(line) for line in text(BF + 'evidence/evidence.jsonl').splitlines() if line.strip()]
    permissions = [e for e in permissions if e.get('kind') == 'permission']
    write('knowledge/crosswalk/modules-permissions-clients.md', '# Modulos, permisos y clientes\n\n'
          'El extractor solo identifico las siguientes senales de permisos. No constituyen una '
          'matriz completa de roles, tenants o clientes. Fuente: '
          '`source-audits/brownfield/reports/evidence/evidence.jsonl`.\n\n' +
          table(['Evidencia ID', 'Fuente', 'Linea', 'Observacion', 'Confianza'],
                [(e['evidence_id'], e['source'], e['line_start'], e['observation'], e['confidence']) for e in permissions]) +
          '\n\nLa asignacion real rol-cliente-modulo queda `unknown` hasta revisar las reglas '
          'de acceso y el contexto de despliegue. Los candidatos de endpoint se encuentran '
          'en `screens-endpoints-tables.md`.')
    flags = Counter(flag for r in risks for flag in r['flags'].split(';') if flag)
    write('knowledge/crosswalk/risks-unresolved.md', '# Riesgos y decisiones pendientes\n\n'
          'El baseline es `INCOMPLETE_BASELINE`, sin confirmacion humana ni commit Git auditado. '
          'La API nativa es `partial`; el catalogo aumentado es estatico. '\
          'La comparacion del inventario auditado con el checkout actual devuelve:\n\n' +
          table(['Resultado SHA256', 'Archivos'], sorted(comparison['counts'].items())) +
          '\n\nFuente: `knowledge/snapshots/current/audited-source-comparison.json`. '
          'Esta comparacion no incluye archivos adicionales ni demuestra cobertura del dump SQL actual.\n\n' +
          table(['Familia de senales API', 'Filas candidatas'], flags.most_common()) +
          '\n\nFuente: `source-audits/api/api-deep-iterative/endpoint_deep_risks.csv`. '
          'La falta de una senal local de auth o CSRF no demuestra ausencia de un control compartido. '
          'SQL taint, IDOR, uploads y rutas de archivo requieren validacion contextual.\n\n'
          'Las semanticas de negocio, las relaciones inferidas, los borradores de release '
          'y los defectos funcionales siguen pendientes. Las auditorias de la herramienta Graphify '
          'estan en `source-audits/related-graphify-audits/` y no deben mezclarse con Proveedores.')
    used = [t for t in tables if t['usage_status'] == 'USED']
    write('knowledge/product/data-model-guide.md', '# Guia del modelo de datos\n\n'
          'Se conserva el modelo fisico extraido del SQL historico. Las descripciones de negocio '
          'son inferencias, no definiciones confirmadas. Fuente: '
          '`source-audits/brownfield/reports/data_dictionary/tables.csv`.\n\n' +
          table(['Tabla usada', 'Evidencia ID', 'Fuente', 'Linea', 'Lecturas', 'Escrituras', 'Validacion'],
                [(t['table'], t['evidence_id'], t['source'], t['line'], t['read_references'], t['write_references'], t['validation_status']) for t in used]) +
          '\n\nEl catalogo completo incluye tambien tablas sin uso encontrado. Consultar '
          '`DATA_DICTIONARY.md`, `SEMANTIC_DATA_DICTIONARY.md` y sus versiones JSON, CSV y XLSX '
          'en la carpeta de auditoria. No se exportan registros del dump de produccion.')
    write('knowledge/product/user-manual-source.md', '# Fuentes para manuales de usuario\n\n'
          'Los manuales deben apoyarse en rutas y secuencias verificadas, conservando los IDs de '
          'evidencia. Actualmente existen mapas tecnicos y borradores pendientes de validacion.\n\n'
          '- Procesos y componentes: `source-audits/brownfield/reports/process_maps/`.\n'
          '- Pantallas y rutas candidatas: `knowledge/crosswalk/screens-endpoints-tables.md`.\n'
          '- Terminos: `source-audits/brownfield/reports/business_glossary/`.\n'
          '- UI y casos de uso candidatos: `source-audits/brownfield/reports/release/business-analysis/`.\n\n'
          'La secuencia real, los roles autorizados, las excepciones y las variantes por cliente '
          'requieren validacion humana antes de publicar instrucciones operativas.')
    print('Generated evidence views for ' + str(len(endpoints)) + ' endpoint candidates and ' + str(len(tables)) + ' tables')


if __name__ == '__main__':
    main()
