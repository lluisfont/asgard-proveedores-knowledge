"""Idempotent structured overlays for the reviewed report contract and AST evidence."""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER = 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707'


def main():
    path = ROOT/'knowledge/general/security-findings.json'
    registry = json.loads(path.read_text(encoding='utf-8-sig'))
    finding = {
        'id': 'SEC-015', 'priority': 'P1',
        'title': 'El exportador acepta operaciones SQL completas del cliente',
        'cwe': ['CWE-89'], 'commit': MASTER,
        'source_status': 'SOURCE_CONFIRMED_QUERY_CONTRACT',
        'runtime_status': 'BOOTSTRAP_ACCESS_AND_DATABASE_PRIVILEGES_UNVERIFIED',
        'confidence': 'high',
        'validation_type': ['contract_based_extracted_source_with_database_substitutes'],
        'evidence': [
            {'path': 'index_archivos/reportes/reportecontrolol.php', 'line_start': 111, 'line_end': 118},
            {'path': 'index_archivos/reporteexcel/reporteexcel.php', 'line_start': 11, 'line_end': 25},
            {'path': 'index_archivos/reporteexcel/reporteexcel.php', 'line_start': 52, 'line_end': 58}],
        'trace': 'A hidden form submits complete SQL; POST query is split on xxx; auxiliary segments and then the first segment are passed verbatim to mysqli_query.',
        'trigger_preconditions': ['Reachable exporter with working bootstrap and applicable access', 'Usable database connection and grants permitting the selected operations'],
        'impact': 'Caller chooses operations and their order within effective database privileges; production impact and rows are unverified.',
        'recommendation': 'Select an authorized report query on the server by identifier, bind typed filters and enforce account scope; never accept complete SQL from the caller.',
        'validation_result': '3/3 isolated decoding/dispatch cases; memory substitutes only, no DB, HTTP or application bootstrap.',
        'reference_comparison': 'New master finding relative to knowledge baseline 3822900; not claimed as a newly introduced application regression. Peru exporter not independently assessed here.',
        'limitations': ['No anonymous reachability claim', 'No deployed privileges or rows inspected', 'Source control flow is not a deployment execution test'],
        'dedup': 'SEC-006 covers interpolation into fixed server SQL. This contract delegates the entire SQL operation and sequence to the client.',
        'summary': 'El cliente elige consultas completas y segmentos auxiliares. El impacto depende de acceso efectivo, bootstrap y privilegios SQL.'}
    registry['findings'] = [f for f in registry['findings'] if f['id'] != finding['id']] + [finding]
    priorities = Counter(f['priority'] for f in registry['findings'])
    registry['summary'] = {'total': len(registry['findings']), **dict(priorities)}
    registry['summary_text'] = 'Quince hallazgos de seguridad: ocho P1 y siete P2. Impacto en producción sin verificar; SEC-015 se incorpora en la revisión iterativa.'
    registry['iterative_review'] = {'baseline_knowledge_commit': '3822900b6d54d99ccf854bec43005a208e2a9694',
        'new_ids': ['SEC-015'], 'evidence': 'source-audits/master/2026-11-18/iterative/report-contract-probes.json',
        'documentation': 'knowledge/reviews/iterative-20261118/report-query-contract.md'}
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
