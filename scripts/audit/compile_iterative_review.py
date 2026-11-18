"""Compile reviewed deltas and a semantic, cumulative iteration ledger."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT/'knowledge/reviews/iterative-20261118'
MASTER = 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707'
PERU = '95fe9a4c3b3cddd84be922cc0e1eb9c88603df62'
BASELINE = '3822900b6d54d99ccf854bec43005a208e2a9694'


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))


def write(path, data):
    (ROOT/path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def fingerprint(records):
    payload = {'baseline_knowledge_commit': BASELINE, 'deltas': sorted(records, key=lambda r: r['id'])}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--close', action='store_true', help='Requires both completed zero-delta closure reviews.')
    args = parser.parse_args()
    transaction = read('knowledge/reviews/iterative-20261118/transactions-delta.json')['items']
    contract = read('knowledge/reviews/iterative-20261118/contracts-delta.json')['deltas']
    records = []

    def add(identifier, classification, version, title, statement, evidence, origin, scope, validation):
        records.append({'id': identifier, 'classification': classification, 'first_version': version,
            'title': title, 'statement': statement, 'scope': scope, 'origin': origin,
            'evidence': [{k: v for k, v in e.items() if k in {'path', 'line_start', 'line_end', 'commit'}}
                         for e in evidence if e.get('commit') in {MASTER, PERU}],
            'validation': validation, 'production_status': 'UNVERIFIED', 'canonical': False})

    sec = next(f for f in read('knowledge/general/security-findings.json')['findings'] if f['id'] == 'SEC-015')
    add('SEC-015', 'new_finding', 1, sec['title'], sec['summary'],
        [dict(e, commit=MASTER) for e in sec['evidence']], 'report-query-contract.md', 'master', sec['validation_result'])
    ast = read('source-audits/master/2026-11-18/iterative/sql-ast-summary.json')
    add('IMP-AST-001', 'improvement', 2, 'Separar nombres léxicos, tablas en AST y esquema físico',
        '394 fragmentos: 227 AST MySQL, 167 sin resolver; 100 nombres AST frente a 134 léxicos, cinco adicionales. Las ausencias del subconjunto no prueban ausencia de tablas.',
        [], 'source-audits/master/2026-11-18/iterative/sql-ast-summary.json', 'master',
        {'parser': ast['parser_version'], 'negative_controls': ast['negative_controls'],
         'source_references': 'source-audits/master/2026-11-18/iterative/sql-ast-references.csv'})
    for i, item in enumerate(transaction[:10], 1):
        add(f'OPS-{i:03d}' if i <= 7 else f'IMP-T{i:03d}', item['classification'], 3,
            item['title'], item['impact'], item['evidence'], item['id'], item['scope'], item['validation'])
    for item in contract[:4]:
        identifier = {'TEMP-C1': 'IMP-C1', 'TEMP-C2': 'IMP-C2', 'TEMP-C3': 'VAR-001', 'TEMP-C4': 'OPS-008'}[item['id']]
        add(identifier, item['classification'], 4, item['titleSpanish'], item['correction'],
            item['evidence'], item['id'], item['scope'], item['validation'])
    add('OPS-009', 'new_finding', 5, 'La rama mostrartabla omite un argumento obligatorio del listado',
        'El controlador pasa un argumento a getListaEmbarques, que requiere dos; PHP 8.4 rechaza la firma antes del cuerpo. El handler AJAX alternativo pasa los argumentos. Despliegue y PHP 5.4 sin comprobar.',
        [{'path': 'index_archivos/embarques/embarquesController.php', 'line_start': 18, 'line_end': 20, 'commit': MASTER},
         {'path': 'index_archivos/embarques/EmbarqueClass.php', 'line_start': 129, 'line_end': 135, 'commit': MASTER},
         {'path': 'index_archivos/embarques/ajax/listaEmbarques.php', 'line_start': 40, 'line_end': 42, 'commit': MASTER}],
        'static-arity-review.json', 'master', '279 PHP tokenizados; 542 llamadas resueltas. Tres controles del censo y tres pruebas aisladas de firma; cuerpo sustituido por centinela.')
    precision_review = read('knowledge/reviews/iterative-20261118/closure-transactions.json')
    for precision in precision_review['improvements']:
        add(precision['id'], 'improvement', 6, precision['title'],
            precision['observation']+' '+precision['action'], precision['source_evidence'],
            'closure-transactions.json', precision['related_known_ids'],
            {'technique': precision_review['technique'], 'check': precision['validation_check'],
             'dedup': precision['dedup_rationale']})
    remote = read('source-audits/master/2026-11-18/iterative/remote-refs-observation.json')
    add('IMP-SCOPE-001', 'improvement', 7, 'Distinguir la comparación Perú fijada del nuevo HEAD remoto',
        'Master auditado continúa vigente. La comparación Perú conserva '+PERU+'; su remoto avanzó a '+remote['peru_remote_observed']+' y cambió tres archivos. Se registra actualidad sin atribuir la auditoría fijada a ese nuevo pin.',
        [], 'source-audits/master/2026-11-18/iterative/remote-refs-observation.json', 'audit_provenance',
        {'kind': 'git_remote_ref_and_tree_metadata',
         'observed_master_pin': remote['master_remote_observed'],
         'observed_peru_pin': remote['peru_remote_observed'],
         'changed_paths_vs_comparison_pin': remote['changed_paths_vs_comparison_pin'],
         'limitation': 'New Peru head is not semantically audited; no production or browser/navigation review.'})
    repair_review = read('knowledge/reviews/iterative-20261118/closure-repair-obligations.json')
    for precision in repair_review['improvements']:
        add(precision['id'], 'improvement', 8, precision['title'],
            'TO-BE propuesto, condicionado a política y representación: '+precision['observation']+' '+precision['proposed_rule_TO_BE'],
            precision['source_evidence'], 'closure-repair-obligations.json', precision['related_known_ids'],
            {'technique': repair_review['technique'], 'checks': precision['validation_check_ids'],
             'dedup': precision['dedup_rationale'], 'condition': precision['condition']})
    branch_review = read('knowledge/reviews/iterative-20261118/closure-branch-obligations.json')
    for precision in branch_review['improvements']:
        add(precision['id'], 'improvement', 9, precision['title'], precision['correction'],
            precision['source_evidence'], 'closure-branch-obligations.json', 'pinned_master_vs_peru_comparison',
            precision['validation'])
    accepted = {'schema_version': '1.0', 'baseline_knowledge_commit': BASELINE, 'master_commit': MASTER,
                'peru_commit': PERU, 'deltas': records,
                'counts': {'new_findings': sum(r['classification'] == 'new_finding' for r in records),
                           'improvements': sum(r['classification'] == 'improvement' for r in records)},
                'materiality': 'Only new supported behavior or substantive correction/qualification. Timestamps, formatting, repeated tests and unchanged risk restatements are not deltas.'}
    write('knowledge/reviews/iterative-20261118/accepted-deltas.json', accepted)
    techniques = [
        'Contratos de consulta completa con despacho aislado',
        'AST MySQL contrastado con inventario léxico y controles negativos',
        'Inyección de fallos, intercalado sintético y permutaciones de invariantes',
        'Diferencial de contratos M/P, callbacks sin transporte y matrices de representación',
        'Censo de llamadas/firma mediante tokens PHP y fronteras de aridad',
        precision_review['technique'],
        'Verificación remota de referencias y diferencia de árbol para actualidad del alcance',
        repair_review['technique'],
        branch_review['technique'],
    ]
    iterations, cumulative = [], []
    previous = fingerprint([])
    for version, technique in enumerate(techniques, 1):
        delta = [r for r in records if r['first_version'] == version]
        cumulative += delta
        current = fingerprint(cumulative)
        iterations.append({'version': version, 'technique': technique, 'status': 'completed',
            'new_findings': [r['id'] for r in delta if r['classification'] == 'new_finding'],
            'improvements': [r['id'] for r in delta if r['classification'] == 'improvement'],
            'before_semantic_sha256': previous, 'after_semantic_sha256': current,
            'cumulative_delta_count': len(cumulative)})
        previous = current
    closures = []
    if args.close:
        for name in ['closure-semantic-mutations.json', 'closure-inference-boundaries.json']:
            closure = read('knowledge/reviews/iterative-20261118/'+name)
            if closure.get('new_findings') != [] or closure.get('improvements') != []:
                raise ValueError('Closure review not zero-delta: '+name)
            if not closure.get('technique'):
                raise ValueError('Closure lacks a real review technique: '+name)
            if not closure.get('checks') or any(c.get('status') not in {'completed', 'pass'} for c in closure['checks']):
                raise ValueError('Closure has unfinished checks: '+name)
            if any('not yet executed' in str(v).lower() for v in closure.get('limitations', [])):
                raise ValueError('Closure is an unexecuted staging record: '+name)
            closures.append(closure)
            iterations.append({'version': len(iterations)+1, 'technique': closure['technique'],
                'status': 'completed', 'new_findings': [], 'improvements': [],
                'review_artifact': 'knowledge/reviews/iterative-20261118/'+name,
                'before_semantic_sha256': previous, 'after_semantic_sha256': previous,
                'cumulative_delta_count': len(cumulative)})
    ledger = {'schema_version': '1.0', 'baseline_knowledge_commit': BASELINE, 'source_commit': MASTER,
        'source_unchanged': True, 'semantic_state_definition': 'Baseline commit plus cumulative accepted-deltas records, canonical sorted JSON; excludes clerical metadata and audit logs.',
        'iterations': iterations, 'converged': args.close,
        'consecutive_zero_delta_passes': 2 if args.close else 0,
        'scope': 'Reviewed pinned static source and isolated contracts; not exhaustive production assurance.',
        'excluded_attempts': [{'technique': 'Delegated browser-output/navigation review',
            'status': 'rejected_automatic_safety_review_before_completion', 'reason': 'possible_cybersecurity_risk',
            'partial_artifacts': 'excluded_from_publication_and_convergence', 'counts_as_zero_delta': False}]}
    ledger['auxiliary_reviews_not_counted_as_final_streak'] = ['knowledge/reviews/iterative-20261118/closure-contracts.json: completed before version-6 precisions; retained as supporting evidence only.']
    ledger['auxiliary_reviews_not_counted_as_final_streak'].append('knowledge/reviews/iterative-20261118/closure-abstract-contracts.json: zero delta before version-9 branch precisions; retained as supporting evidence only.')
    version_root = REVIEW/'versions'
    version_root.mkdir(exist_ok=True)
    for iteration in iterations:
        state = {'baseline_knowledge_commit': BASELINE,
                 'deltas': sorted([r for r in records if r['first_version'] <= iteration['version']], key=lambda r: r['id'])}
        snapshot = version_root/f"audit-v{iteration['version']:02d}.json"
        snapshot.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        iteration['snapshot'] = snapshot.relative_to(ROOT).as_posix()
        iteration['snapshot_sha256'] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    write('knowledge/reviews/iterative-20261118/iterations.json', ledger)
    manifest = read('knowledge/manifest.json')
    manifest['knowledge_pack']['version'] = '0.3.0'
    manifest['audits']['iterative'] = {'baseline_knowledge_commit': BASELINE, 'documentation': 'knowledge/reviews/iterative-20261118/README.md',
        'accepted_deltas': 'knowledge/reviews/iterative-20261118/accepted-deltas.json',
        'ledger': 'knowledge/reviews/iterative-20261118/iterations.json', 'counts': accepted['counts'],
        'converged_in_reviewed_scope': args.close, 'consecutive_zero_delta_passes': ledger['consecutive_zero_delta_passes'],
        'application_source_modified': False, 'overall_coverage': 'PARTIAL'}
    manifest['repository']['comparison_remote_observed'] = remote['peru_remote_observed']
    manifest['repository']['comparison_freshness'] = 'pinned_comparison_not_latest_peru_head'
    write('knowledge/manifest.json', manifest)
    lines = [
        '# Revisión iterativa: cambios frente a la auditoría anterior', '',
        'Fecha: 18-11-2026. Knowledge 0.3.0. Comparación con la [auditoría anterior](https://github.com/lluisfont/asgard-proveedores-knowledge/commit/'+BASELINE+').', '',
        'El código fuente sigue en master `'+MASTER+'`; contraste Perú `'+PERU+'`. No hay cambios de aplicación ni correcciones desplegadas. Se amplía el conocimiento del mismo código.', '',
        '**Delta aceptado: '+str(accepted['counts']['new_findings'])+' hallazgos nuevos y '+str(accepted['counts']['improvements'])+' mejoras sustantivas de documentación.** Diez hallazgos se refieren a master (uno de seguridad y nueve operativos); uno corresponde específicamente al consumidor de inventario de Perú. Las coincidencias con Perú no certifican iguales datos/configuración.', '',
        ('**Cierre alcanzado:** las pasadas 10 y 11 no aportan nuevos hallazgos ni mejoras; mantienen la misma huella semántica que la versión 9.' if args.close else '**Revisión abierta:** las nueve pasadas iniciales aportaron novedades; todavía no se declara convergencia.'), '',
        'El cierre se limita al alcance estático y los contratos aislados revisados. No certifica ausencia de defectos ni cierra los riesgos de producción.', '',
        '## Qué ha cambiado', '',
        '| ID | Cambio frente al informe anterior |', '| --- | --- |',
    ]
    lines += ['| '+r['id']+' | '+r['title'].replace('|', '\\|')+' |' for r in records]
    lines += [
        '', 'Los hallazgos se sustentan en [aceptaciones estructuradas](accepted-deltas.json), [registro operativo](../../general/operational-findings.md), [SEC-015](report-query-contract.md), [contratos API revisados](../../general/api-reference.md), [variante Perú](../../variants/peru.md) y [glosario](../../glossary/business-glossary.md). Las propuestas iniciales conservan sus IDs temporales para poder revisar deduplicación y rechazos; su aceptación está registrada en [transacciones](transaction-integration.json) y [contratos](contract-integration.json).', '',
        'Seguridad pasa de 14 a 15 hallazgos (ocho P1, siete P2); los nueve operativos se mantienen en un registro separado (dos P1, siete P2). No se suman marcas automáticas como vulnerabilidades. Se mantienen 81 conceptos de negocio, ahora con el estado de viaje mejor descrito y evidencias adicionales; no se inflan los recuentos con sinónimos o códigos.', '',
        'El modelo de datos diferencia 134 nombres léxicos históricos, 100 nombres en AST MySQL y el esquema físico aún no verificado. De 394 fragmentos, 227 se interpretan y 167 quedan sin resolver. Cinco nombres AST no estaban en el inventario léxico. Los 39 no reproducidos no se eliminan como inexistentes. Los 20 candidatos raw de consumo API se conservan como historial; los POST reales y el falso PUT se corrigen mediante un overlay revisado.', '',
        'Las reglas, procesos, manual, pruebas e índices enlazan las ampliaciones. Bolivia/master, Perú y el SQL local candidato siguen separados. El DDL histórico de Perú no se convierte en esquema general.', '',
        '**Actualidad de ramas:** la verificación remota confirma master en el pin auditado, pero Perú avanzó a `'+remote['peru_remote_observed']+'` durante el trabajo. Tres archivos difieren respecto al pin de comparación. [Observación reproducible de referencias](../../../source-audits/master/2026-11-18/iterative/remote-refs-observation.json). No se presenta este informe como auditoría de ese nuevo HEAD de Perú. Esta precisión de procedencia es IMP-SCOPE-001 y constituye la versión 7 con mejora.', '',
        '## Pasadas y criterio de parada', '',
        '| Versión | Técnica adicional | Nuevos | Mejoras |', '| --- | --- | ---: | ---: |',
    ]
    lines += ['| '+str(i['version'])+' | '+str(i['technique']).replace('|', '\\|')+' | '+str(len(i['new_findings']))+' | '+str(len(i['improvements']))+' |' for i in iterations]
    lines += [
        '', 'El [registro completo](iterations.json) conserva las huellas antes/después y los [snapshots acumulativos de cada versión](versions/audit-v01.json). Se compara el conjunto acumulado de afirmaciones aceptadas y sus evidencias, sin fechas ni nuevos archivos de log. Los últimos snapshots sin delta tienen el mismo contenido y hash de archivo. Repetir un test o reformular un riesgo conocido no cuenta como mejora. Cualquier delta sustantivo reinicia el contador.', '',
        'Las técnicas combinan contrato de consulta completa, AST SQL, fallos programados, intercalado sintético, permutaciones de eventos, diferencias M/P, tipos PHP/JavaScript y un censo de aridad por tokens PHP. El último detectó OPS-009 y reinició el contador. Después, la revisión por modelos relacionales, postcondiciones y contraejemplos aportó tres precisiones más: DELETE correcto no garantiza filas borradas; importa la primera coincidencia del evento 26; y el detalle de pedidos devuelve NULL incluso en éxito. Es la versión 6 con novedades y reinicia otra vez el contador. Los cierres posteriores contrastan obligaciones entre ramas y la suficiencia lógica de las recomendaciones.', '',
        'La versión 8 detecta dos mejoras de las recomendaciones: separar actualizaciones efectivas, no-op permitido y ausencia de coincidencia; y conservar IDs numéricos válidos recibidos como texto al corregir pertenencia. Son TO-BE condicionadas, sin convertirlas en política aprobada ni otro defecto. También reinician el contador. La revisión final usa contraste entre ramas y análisis abstracto de contratos, posterior a esas aceptaciones.', '',
        'La versión 9 añade cuatro diferencias por rama: intento de registro EDP en la ruta masiva; fecha que ordena el historial; uso de referencia al resolver lugar; y origen de fecha/hora del temporal. Se integran en el [registro de obligaciones entre ramas](branch-obligations.md). La revisión abstracta anterior dio cero deltas, pero se descarta para el cierre final porque precede a estas cuatro precisiones. Tras integrarlas, el contador vuelve a cero y se realizan mutaciones semánticas documentales y una auditoría de límites de inferencia.', '',
        '## Evidencia y comprobaciones', '',
        '- [Reportes](../../../source-audits/master/2026-11-18/iterative/report-contract-probes.json): 3/3 contratos reproducidos sin DB.',
        '- [Transacciones](../../../source-audits/master/2026-11-18/iterative/transaction-probes.json): 34/34 comportamientos reproducidos, incluidos 15 controles negativos.',
        '- [Contratos](../../../source-audits/master/2026-11-18/iterative/contract-consistency-probes.json): tipos, callbacks registrados sin transporte, 32 combinaciones de resumen y 11 representaciones por rama.',
        '- [Aridad estática](../../../source-audits/master/2026-11-18/iterative/static-arity-review.json): 279 PHP, 460 declaraciones, 542 llamadas resueltas, tres candidatos; dos ya conocidos y OPS-009 nuevo. Tres controles del analizador.',
        '- [Firma aislada](../../../source-audits/master/2026-11-18/iterative/arity-contract-probes.json): 3/3; cuerpo sustituido por un centinela. No prueba el cuerpo real ni el PHP 5.4 declarado.',
        '- [AST SQL](../../../source-audits/master/2026-11-18/iterative/sql-ast-summary.json): tres controles negativos. No se guarda SQL literal ni se ejecutan consultas.',
    ]
    if args.close:
        lines += ['- Cierres sin delta posteriores a todas las precisiones: [mutaciones semánticas documentales](closure-semantic-mutations.md), [límites de inferencia](closure-inference-boundaries.md).']
    lines += ['- [Revisión por postcondiciones y modelos relacionales](closure-transactions.md): nueve comprobaciones; aporta CLR-IMP-001..003. La [revisión auxiliar de contratos y tipos](closure-contracts.md) se conserva como apoyo y no se usa como cierre posterior a esas precisiones.']
    lines += ['- [Obligaciones de reparación frente a éxitos válidos](closure-repair-obligations.md): aporta RPR-IMP-001/002; tampoco se usa como pasada sin novedades.']
    lines += ['- [Obligaciones diferenciales entre ramas](closure-branch-obligations.md): aporta BR-IMP-001..004. [Revisión abstracta auxiliar](closure-abstract-contracts.md): cero deltas antes de las cuatro precisiones de rama; no cuenta en el cierre posterior.']
    lines += [
        '- [Validación actual](../../snapshots/current/knowledge-validation.json), [integridad de transferencia histórica](../../snapshots/current/transfer-validation.json) y [receta de reproducción](../../operations/reproduce-audit.md).', '',
        'Las pruebas que reproducen un defecto pasan cuando confirman el comportamiento esperado por la auditoría; esto no aprueba ese comportamiento para negocio. No hubo bootstrap de aplicación, peticiones de aplicación, sesiones persistentes, datos reales, SQL ni mutaciones de fuente.', '',
        '## Límites y revisión excluida', '',
        'El estado global continúa **PARTIAL**: faltan correspondencia del DDL con el despliegue, privilegios y datos, runtime real, submódulos, autorización por entorno, concurrencia real y aprobación de negocio. El esquema local candidato conserva procedencia/país sin confirmar. Los efectos persistentes de fallos dependen de autocommit, restricciones y manejo de errores no comprobados.', '',
        'La revisión delegada de salidas al navegador/navegación fue rechazada por la revisión automática de seguridad por posible riesgo de ciberseguridad antes de completarse. Sus artefactos parciales no se publican, no se integran y no cuentan como pasada sin novedades. El auditor nativo ASGARD sigue bloqueado por AppControl; no se eludió el bloqueo.', '',
    ]
    (REVIEW/'README.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'counts': accepted['counts'], 'passes': len(iterations), 'converged': args.close}))


if __name__ == '__main__':
    main()
