"""Peru HEAD carry-forward: immutable Git metadata, bounded static dependencies.

Own metadata script; does not import/run ASGARD auditor or application code.
Only the three named sidecars may be written. --check compares in memory.
Python stdlib only; no network, database, subprocess shell, or compiled cache.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
from urllib.parse import unquote

K = '0c4bb99f076d6a8c18ae98375d6e154da6319922'
P = '95fe9a4c3b3cddd84be922cc0e1eb9c88603df62'
H = '2a179e2e6472d5705d031665ecbc90c3d806edec'
M = 'a8ce2c23dead8552d2c4699e4a9b9134f7a18707'
JS = 'index_archivos/embarques/js/datosEmbarques.js'
REPORTS = {
    'index_archivos/reportes/reportepreembarquenacional.php',
    'index_archivos/reportes/reportepreembarquenacionalquery.php',
}
OUTPUTS = (
    'source-audits/peru/2026-11-19/carryforward.json',
    'knowledge/reviews/peru-head-20261119/carryforward-deltas.json',
    'knowledge/reviews/peru-head-20261119/carryforward-deltas.md',
)
POLICY = {
    'date_client': '2026-11-19', 'timezone': 'Europe/Madrid',
    'sourcepins': {'P95': P, 'HEAD': H, 'M_historical': M, 'KB_baseline': K},
    'canonical': False, 'final_docs_or_manifest_updated': False,
    'network_database_application_execution': False,
    'asgard_auditor_or_python_workaround': False,
    'master_remote_a44': 'OUT_OF_SCOPE_NOT_RESOLVED',
    'exclusions': [
        'Dos PHP de reportes: solo blobs, modos y paths; semantica delegada a otro agente.',
        'Navegador, navegacion, salidas y JS de recarga: excluidos; no reintentados.',
        'datosEmbarques.js: solo hashes, rangos y solicitudes de negocio acotadas; sin callbacks de respuesta.',
        'Sin ejecucion PHP/JS, aplicacion, red, BD, submodulos, instalacion ni auditor nativo.',
        'Igualdad Git de todo el arbol no se cuenta como revision semantica de sus archivos.',
    ],
    'proof_semantics': {
        'blob': 'OID Git, modo y tipo por path; igualdad de bytes versionados, no de runtime.',
        'range': 'Lineas inclusivas; SHA256 de bytes crudos concatenados con finales de linea preservados.',
        'carry': 'Conserva evidencia historica local; no nueva aprobacion de negocio ni repeticion de probes.',
        'dependency': 'Un salto estatico; includes/scripts y contratos de negocio fijados. No grafo exhaustivo.',
    },
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pack(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


class Audit:
    def __init__(self, kb, source):
        self.kb, self.source = kb, source
        self.cache, self.proofs, self.proof_keys = {}, [], {}
        self.trees = {c: self.tree(source, c) for c in (P, H, M)}
        self.ktree = self.tree(kb, K)
        self.dependencies = []
        self.known = self.read_json('knowledge/reviews/iterative-20261118/accepted-deltas.json')

    @staticmethod
    def git(root, *args):
        return subprocess.run(
            ['git', '-c', 'core.quotepath=false', '-C', str(root), *args],
            check=True, capture_output=True, shell=False,
        ).stdout

    def tree(self, root, commit):
        raw = self.git(root, 'ls-tree', '-rz', '--full-tree', commit)
        result = {}
        for row in raw.split(b'\0'):
            if row:
                meta, path = row.split(b'\t', 1)
                mode, kind, oid = meta.decode().split()
                result[path.decode('utf-8')] = {'mode': mode, 'type': kind, 'blob': oid}
        return result

    def blob(self, commit, path, kb=False):
        if not kb and path in REPORTS:
            raise ValueError('Excluded report content: ' + path)
        key = (kb, commit, path)
        if key not in self.cache:
            root = self.kb if kb else self.source
            self.cache[key] = self.git(root, 'show', f'{commit}:{path}')
        return self.cache[key]

    def read_json(self, path):
        return json.loads(self.blob(K, path, True).decode('utf-8-sig'))

    def kbpin(self, path, pointer=None, line=None):
        result = {'repository': str(self.kb).replace('\\', '/'), 'commit': K,
                  'path': path, 'blob': self.ktree[path]['blob']}
        if pointer is not None:
            result['json_pointer'] = pointer
        if line is not None:
            result['line_start'] = result['line_end'] = line
        return result

    def proof(self, commit, path, start, end):
        key = (commit, path, start, end)
        if key in self.proof_keys:
            return self.proof_keys[key]
        pid = f'R{len(self.proofs) + 1:04d}'
        rec = {'id': pid, 'path': path, 'origin_commit': commit,
               'line_start': start, 'line_end': end, 'sourcepins': POLICY['sourcepins'],
               'comparison_role': ('P95_TO_HEAD' if commit == P else
                                   'M_HISTORICAL_TO_HEAD_NOT_AUTOMATIC_PERU_PROMOTION')}
        self.proof_keys[key] = pid
        self.proofs.append(rec)
        if path in REPORTS:
            rec['status'] = 'DELEGATED_REPORT_METADATA_ONLY'
            return pid
        if path not in self.trees[commit] or path not in self.trees[H]:
            rec['status'] = 'MISSING_PATH'
            return pid
        origin = self.blob(commit, path).splitlines(keepends=True)
        target = self.blob(H, path).splitlines(keepends=True)
        if not (1 <= start <= end <= len(origin)):
            rec['status'] = 'INVALID_ORIGIN_RANGE'
            return pid
        chunk = b''.join(origin[start-1:end])
        rec['origin_blob'] = self.trees[commit][path]['blob']
        rec['head_blob'] = self.trees[H][path]['blob']
        rec['origin_line_count'] = len(origin)
        rec['head_line_count'] = len(target)
        rec['range_sha256'] = sha(chunk)
        rec['whole_blob_equal'] = rec['origin_blob'] == rec['head_blob']
        if end <= len(target) and b''.join(target[start-1:end]) == chunk:
            a, b = start, end
            rec['mapping'] = 'SAME_LINES'
        else:
            length = end - start + 1
            matches = [i for i in range(len(target)-length+1)
                       if target[i] == origin[start-1] and b''.join(target[i:i+length]) == chunk]
            if len(matches) != 1:
                rec['status'] = 'REQUIRES_RANGE_REVIEW'
                rec['exact_match_count'] = len(matches)
                return pid
            a, b = matches[0]+1, matches[0]+length
            rec['mapping'] = 'UNIQUE_EXACT_RANGE_RELOCATED'
        rec.update(head_line_start=a, head_line_end=b,
                   head_range_sha256=sha(b''.join(target[a-1:b])), status='IDENTICAL_RANGE')
        return pid

    def evidence(self, values):
        result = []
        for e in values:
            commit = e.get('commit') or e.get('ref', '').split('@')[-1]
            if commit in (M, P):
                result.append(self.proof(commit, e['path'], int(e['line_start']), int(e['line_end'])))
        return list(dict.fromkeys(result))

    def row(self, item, group, doc, pointer, evidence):
        ids = self.evidence(evidence)
        pids = [i for i in ids if self.proofs[int(i[1:])-1]['origin_commit'] == P]
        result = {
            'id': item['id'], 'group': group, 'title': item.get('title', item.get('term')),
            'baseline_document': self.kbpin(doc, pointer),
            'evidence_proof_ids': ids, 'peru_proof_ids': pids,
            'status': 'P95_EVIDENCE_CARRIED_IDENTITY_ONLY' if pids else 'NO_ORIGINAL_P_EVIDENCE_NO_PROMOTION',
            'semantic_rereview_this_pass': False, 'probes_rerun': False,
            'original_scope': item.get('scope'),
            'retained_limits': 'Conserva confianza, AS-IS/RISK/TO-BE y limites del registro original; no cierre ni reparacion.',
        }
        if not pids:
            result['required_review'] = 'Atribucion Peru requiere evidencia propia/correspondencia contextual; igualdad M/HEAD no basta.'
        return result

    def citations(self):
        docs = sorted(p for p in self.ktree if p.endswith('.md') and
                      ((p.startswith('knowledge/') and '/history/' not in p) or
                       p in ('README.md', 'QUICK_START.md', 'BUSINESS_GLOSSARY.md')))
        full = re.compile(r'https://github\.com/KPO-Group/proveedores/blob/(' + P +
                          r')/([^\s)#]+)#L(\d+)(?:-L(\d+))?')
        short = re.compile(r'(?<![\w/])(?:M/)?P:([^`\s;]+?):(L\d+(?:-L\d+)?(?:,L\d+(?:-L\d+)?)*)')
        rows, apirows = [], []
        for doc in docs:
            text = self.blob(K, doc, True).decode('utf-8-sig')
            section = ''
            for n, line in enumerate(text.splitlines(), 1):
                if line.startswith('## '):
                    section = line[3:].strip()
                found = [(unquote(m[2]), int(m[3]), int(m[4] or m[3]), 'github_pinned')
                         for m in full.finditer(line)]
                for m in short.finditer(line):
                    for rg in m[2].split(','):
                        nums = [int(x.removeprefix('L')) for x in rg.split('-')]
                        found.append((unquote(m[1]), nums[0], nums[-1], 'P_abbreviated'))
                for path, start, end, kind in found:
                    rows.append({'id': f'CIT-P-{len(rows)+1:03d}',
                                 'document_pin': self.kbpin(doc, line=n), 'syntax': kind,
                                 'proof_id': self.proof(P, path, start, end),
                                 'semantic_rereview_this_pass': False})
                if doc in ('knowledge/general/integrations.md', 'knowledge/general/api-reference.md') and line.startswith('|'):
                    cells = [x.strip() for x in line.strip('|').split('|')]
                    if not cells or all(set(x) <= set(' -:') for x in cells):
                        continue
                    if cells[0] in ('Simbolo real', 'Integracion'):
                        continue
                    if doc.endswith('api-reference.md') and ('UNRESOLVED_' not in line and 'http' not in line):
                        continue
                    raw_candidate = section.startswith('Candidatos raw')
                    config = doc.endswith('integrations.md') and cells[0].startswith('`')
                    apirows.append({'id': f'API-DOC-{len(apirows)+1:03d}',
                                    'document_pin': self.kbpin(doc, line=n),
                                    'document_label': cells[0],
                                    'document_section': section,
                                    'documented_destination_or_context': cells[1],
                                    'raw_source_path': cells[2] if raw_candidate else None,
                                    'raw_source_line_M_not_P': int(cells[3]) if raw_candidate else None,
                                    'method_as_documented': cells[0] if doc.endswith('api-reference.md') else None,
                                    'excluded_browser_context': raw_candidate and any(s in cells[2] for s in ('guardar_asignacion.php', 'frames/rutas.php')),
                                    'P_proof_ids': list(dict.fromkeys(r['proof_id'] for r in rows
                                        if r['document_pin']['path'] == doc and r['document_pin']['line_start'] == n)),
                                    'status': ('KNOWN_RAW_CANDIDATE_NOT_CONTRACT' if raw_candidate else
                                               'REJECTED_RAW_ATTRIBUTION' if 'PUT' == cells[0] else
                                               'CONFIGURATION_CONTEXT_NOT_API_CALL' if config else
                                               'DOCUMENTED_CONTEXT_NOT_LIVE_VERIFIED'),
                                    'peru_promotion': False})
        return docs, rows, apirows

    def dependencies_for(self, path):
        """Literal one-hop include/script metadata only; never report bodies/callbacks."""
        if path in REPORTS or not path.endswith('.php'):
            return
        lines = self.blob(H, path).decode('utf-8', errors='replace').splitlines()
        patterns = [
            ('php_include_literal', re.compile(r'\b(?:include|require)(?:_once)?\s*\(?\s*[\'"]([^\'"]+)[\'"]')),
            ('script_include_metadata_only', re.compile(r'<script\b[^>]*\bsrc=[\'"]([^\'"?]+)', re.I)),
        ]
        for n, line in enumerate(lines, 1):
            for kind, regex in patterns:
                for match in regex.finditer(line):
                    target = match[1]
                    if re.match(r'\w+://', target):
                        continue
                    candidates = [posixpath.normpath(posixpath.join(posixpath.dirname(path), target)), target.lstrip('/')]
                    resolved = next((x for x in candidates if x in self.trees[H]), None)
                    self.dependencies.append({
                        'from': path, 'line_start': n, 'line_end': n, 'kind': kind,
                        'target_literal': target, 'to': resolved,
                        'source_proof_id': self.proof(P, path, n, n),
                        'target_P95': self.trees[P].get(resolved),
                        'target_HEAD': self.trees[H].get(resolved),
                        'status': ('CHANGED_DIRECT_DEPENDENCY' if resolved and self.trees[P].get(resolved) != self.trees[H].get(resolved)
                                   else 'UNCHANGED_DIRECT_DEPENDENCY' if resolved else 'UNRESOLVED_STATIC_INCLUDE'),
                        'execution_or_navigation_claim': False,
                    })

    def business_calls(self):
        # Deliberate allowlist: raw request/config ranges, no UI or done/fail callbacks.
        frame = 'index_archivos/embarques/frames/items.php'
        specs = [
            ('API-CF-001', 'GET', 'UNRESOLVED_CONST:URL_API/proveedores/detalle-pedido/{idpedido}',
             [(JS, 510, 521), (frame, 57, 57)], ['idpedido (ruta)', 'Authorization (simbolo tokenJWT)'], None),
            ('API-CF-002', 'POST', 'index_archivos/embarques/ajax/crear-viaje-desde-items.php',
             [(JS, 397, 405), (JS, 416, 421), (frame, 238, 238)],
             ['embarque_id', 'vins', 'origin_location_id', 'carrier_unit_id', 'driver_id',
              'schedule_date', 'schedule_time', 'destination_mappings'], 'index_archivos/embarques/ajax/crear-viaje-desde-items.php'),
            ('API-CF-003', 'GET', 'index_archivos/tracking/ajaxAsignacion/transporte.php',
             [(JS, 258, 258), (frame, 239, 239)], [], 'index_archivos/tracking/ajaxAsignacion/transporte.php'),
            ('API-CF-004', 'GET', 'index_archivos/tracking/ajaxAsignacion/origen.php',
             [(JS, 265, 265), (JS, 269, 269), (frame, 236, 236)], [], 'index_archivos/tracking/ajaxAsignacion/origen.php'),
            ('API-CF-005', 'GET', 'index_archivos/tracking/ajaxAsignacion/conductores.php?carrier_id={carrierBusinessId}',
             [(JS, 303, 303), (frame, 240, 240)], ['carrier_id (query)'], 'index_archivos/tracking/ajaxAsignacion/conductores.php'),
        ]
        result = []
        for ident, method, endpoint, ranges, fields, local in specs:
            proofs = [self.proof(P, *r) for r in ranges]
            result.append({'id': ident, 'method': method, 'endpoint': endpoint, 'fields': fields,
                           'evidence_proof_ids': proofs,
                           'status': 'REQUEST_RANGES_IDENTICAL_NOT_RESPONSE_OR_SERVICE_VALIDATION',
                           'local_handler': local, 'handler_P95': self.trees[P].get(local),
                           'handler_HEAD': self.trees[H].get(local),
                           'business_backend_review': False, 'response_navigation_output_review': False,
                           'known_context': ['IMP-C1'] if ident == 'API-CF-001' else ['BR-IMP-001', 'BR-IMP-003', 'BR-IMP-004']})
            if local:
                self.dependencies.append({'from': JS, 'to': local, 'kind': 'business_request_via_frame_config',
                    'source_proof_ids': proofs, 'target_P95': self.trees[P].get(local),
                    'target_HEAD': self.trees[H].get(local), 'status': 'UNCHANGED_DIRECT_DEPENDENCY',
                    'execution_or_navigation_claim': False})
        return result

    def changed_references(self):
        # Metadata projection: no source text of matching lines is exported or semantically analysed.
        result = []
        for changed in [JS, *sorted(REPORTS)]:
            needle = posixpath.basename(changed)
            raw = self.git(self.source, 'grep', '-l', '-F', needle, H, '--', '*.php', '*.js')
            for entry in raw.decode().splitlines():
                path = entry.split(':', 1)[1]
                if path in REPORTS:
                    result.append({'from': path, 'to': changed, 'status': 'DELEGATED_MATCH_METADATA_ONLY',
                                   'source_HEAD': self.trees[H][path]})
                    continue
                for n, line in enumerate(self.blob(H, path).splitlines(keepends=True), 1):
                    if needle.encode() in line:
                        result.append({'from': path, 'to': changed, 'line_start': n, 'line_end': n,
                                       'line_sha256': sha(line), 'proof_id': self.proof(P, path, n, n),
                                       'status': 'LEXICAL_REFERENCE_ONLY_NO_EXECUTION_CLAIM',
                                       'review_navigation_or_output': False})
        return result

    def build(self):
        for root, commit in ((self.kb, K), (self.source, H)):
            actual = self.git(root, 'rev-parse', 'HEAD').decode().strip()
            if actual != commit:
                raise ValueError(f'Pinned checkout mismatch: {root}: {actual}')
        allpaths = sorted(set(self.trees[P]) | set(self.trees[H]))
        unchanged = [p for p in allpaths if self.trees[P].get(p) == self.trees[H].get(p)]
        unchanged_set = set(unchanged)
        changed = [p for p in allpaths if p not in unchanged_set]
        assert set(changed) == {JS, *REPORTS}, changed
        diffs = [{'path': p, 'P95': self.trees[P].get(p), 'HEAD': self.trees[H].get(p),
                  'review': 'BOUNDED_BUSINESS_REQUEST_METADATA' if p == JS else 'DELEGATED_METADATA_ONLY'} for p in changed]
        # Only numeric hunk headers of JS; content and function-context text discarded.
        diff = self.git(self.source, 'diff', '--no-ext-diff', '--no-textconv', '--unified=0', P, H, '--', JS)
        hunks = [m.group(0).decode() for m in re.finditer(rb'^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@', diff, re.M)]
        matrix = []
        gdoc = 'knowledge/glossary/business-glossary.json'
        glossary = self.read_json(gdoc)
        assert len(glossary['entries']) == 81
        for i, entry in enumerate(glossary['entries']):
            matrix.append(self.row(entry, 'glossary', gdoc, f'/entries/{i}', entry['evidence']))
        odoc = 'knowledge/general/operational-findings.json'
        ops = self.read_json(odoc)
        for key, count in (('findings', 9), ('improvements', 8)):
            assert len(ops[key]) == count
            for i, entry in enumerate(ops[key]):
                matrix.append(self.row(entry, 'OPS' if key == 'findings' else 'operational_improvement',
                                       odoc, f'/{key}/{i}', entry['source_evidence']))
        bdoc = 'knowledge/reviews/iterative-20261118/branch-obligations.json'
        branch = self.read_json(bdoc)
        assert len(branch['improvements']) == 4
        for i, entry in enumerate(branch['improvements']):
            matrix.append(self.row(entry, 'branch_precision', bdoc, f'/improvements/{i}', entry['source_evidence']))
        i, var = next((i, x) for i, x in enumerate(self.known['deltas']) if x['id'] == 'VAR-001')
        matrix.append(self.row(var, 'VAR', 'knowledge/reviews/iterative-20261118/accepted-deltas.json',
                               f'/deltas/{i}', var['evidence']))
        docs, citations, apirows = self.citations()
        business = self.business_calls()
        references = self.changed_references()
        scoped_paths = sorted({r['path'] for r in self.proofs if r['origin_commit'] == P} |
                              {c['local_handler'] for c in business if c['local_handler']})
        for path in scoped_paths:
            self.dependencies_for(path)
        # Dependency graph is bounded to one hop from scoped PHP and the allowlisted JS calls.
        for row in matrix:
            ps = {self.proofs[int(i[1:])-1]['path'] for i in row['evidence_proof_ids']}
            deps = [i for i, d in enumerate(self.dependencies) if d['from'] in ps]
            refs = [i for i, r in enumerate(references) if r['from'] in ps]
            row['direct_dependency_indexes'] = deps
            row['changed_reference_indexes'] = refs
            row['boundary_status'] = ('CHANGED_REFERENCE_REQUIRES_SEPARATE_REVIEW' if refs else
                                      'NO_CHANGED_TARGET_IN_BOUNDED_DIRECT_DEPENDENCIES')
            row['boundary_limit'] = 'No acredita transitividad, rutas dinamicas, entorno ni contratos externos.'
        touched_docs = Counter(r['document_pin']['path'] for r in citations)
        statuses = Counter(r['status'] for r in self.proofs)
        pproofs = [r for r in self.proofs if r['origin_commit'] == P]
        assert all(r['status'] == 'IDENTICAL_RANGE' for r in pproofs), 'P range identity failed'
        groups = {g: dict(Counter(r['status'] for r in matrix if r['group'] == g))
                  for g in ('glossary', 'OPS', 'operational_improvement', 'branch_precision', 'VAR')}
        coverage = {
            'tree': {'P95_entries': len(self.trees[P]), 'HEAD_entries': len(self.trees[H]),
                     'identical_entries_mode_type_oid': len(unchanged), 'changed_paths': len(changed),
                     'P95_blobs': sum(x['type'] == 'blob' for x in self.trees[P].values()),
                     'HEAD_blobs': sum(x['type'] == 'blob' for x in self.trees[H].values()),
                     'P95_tree_oid': self.git(self.source, 'rev-parse', P+'^{tree}').decode().strip(),
                     'HEAD_tree_oid': self.git(self.source, 'rev-parse', H+'^{tree}').decode().strip(),
                     'identical_path_manifest_sha256': sha(('\n'.join(unchanged)+'\n').encode()),
                     'semantic_review_count_from_tree_equality': 0},
            'matrix_records': len(matrix), 'groups': groups,
            'proofs_total': len(self.proofs), 'proof_statuses': dict(statuses),
            'distinct_P95_ranges': len(pproofs),
            'range_statuses_by_origin': {
                'P95': dict(Counter(r['status'] for r in self.proofs if r['origin_commit'] == P)),
                'M_historical': dict(Counter(r['status'] for r in self.proofs if r['origin_commit'] == M)),
            },
            'md_documents_inventoried': len(docs), 'md_documents_with_P_citations': dict(touched_docs),
            'P_citation_occurrences_from_md': len(citations),
            'P_citation_distinct_ranges_from_md': len({x['proof_id'] for x in citations}),
            'md_citation_syntax': 'GitHub commit+Lx-Ly; P:path:Lx-Ly; M/P:path:Lx-Ly; inclusive; percent-decoded.',
            'md_citation_limit': 'No inference of bare filenames/ranges or unpinned prose; no blanket claim of all mentions resolved.',
            'excluded_md_history': sorted(p for p in self.ktree if p.startswith('knowledge/history/') and p.endswith('.md')),
            'source_audits_history': 'Outside documentary inventory; not traversed or promoted.',
            'api_document_rows': len(apirows), 'api_business_requests_bounded': len(business),
            'api_contract_status_counts': dict(Counter(x['status'] for x in apirows)),
            'raw_api_candidates_promoted_to_verified': 0,
            'direct_dependency_edges': len(self.dependencies),
            'dependency_status_counts': dict(Counter(x['status'] for x in self.dependencies)),
            'changed_path_lexical_references': len(references),
            'boundary_affected_matrix_rows': [r['id'] for r in matrix if r['changed_reference_indexes']],
            'source_paths_used_for_range_metadata': len({r['path'] for r in self.proofs}),
            'runtime_contract_or_semantic_global_closure': False,
        }
        data = {'schema_version': '1.0', 'registry_type': 'peru_HEAD_knowledge_revalidation_matrix',
                **POLICY, 'source_root': str(self.source).replace('\\', '/'),
                'knowledge_root': str(self.kb).replace('\\', '/'), 'coverage': coverage,
                'changed_paths': diffs, 'datosEmbarques_numeric_hunks_only': hunks,
                'matrix': matrix, 'range_proofs': self.proofs, 'source_citations_P_from_docs': citations,
                'md_document_inventory': [self.kbpin(p) for p in docs],
                'known_api_document_rows': apirows, 'bounded_business_requests': business,
                'direct_dependencies': self.dependencies, 'changed_path_reference_metadata': references}
        self.validate(data)
        return data

    def validate(self, data):
        assert len(data['matrix']) == 103
        assert len({r['id'] for r in data['matrix']}) == 103
        assert data['coverage']['groups']['glossary']['NO_ORIGINAL_P_EVIDENCE_NO_PROMOTION'] == 1
        assert data['coverage']['groups']['operational_improvement']['NO_ORIGINAL_P_EVIDENCE_NO_PROMOTION'] == 6
        for proof in self.proofs:
            if proof['status'] == 'IDENTICAL_RANGE':
                assert proof['range_sha256'] == proof['head_range_sha256']
        for request in data['bounded_business_requests']:
            assert all(self.proofs[int(i[1:])-1]['status'] == 'IDENTICAL_RANGE' for i in request['evidence_proof_ids'])
        assert all(k[2] not in REPORTS for k in self.cache if not k[0])
        assert sum(x['status'] == 'KNOWN_RAW_CANDIDATE_NOT_CONTRACT' for x in data['known_api_document_rows']) == 20


def deltas(audit, data):
    def source_evidence(ids):
        return [audit.proofs[int(i[1:])-1] for i in dict.fromkeys(ids)]
    calls = data['bounded_business_requests']
    items = [
        {'id': 'TEMP-CF001', 'classification': 'documentary_precision',
         'title': 'El blob JS cambia; cinco solicitudes de negocio conservan rangos exactos',
         'statement': 'En HEAD los cinco contratos de solicitud acotados siguen identicos: detalle GET/Authorization, creacion POST JSON y tres catalogos GET. Creacion P95 L416-L421 pasa a HEAD L409-L414; detalle P95 L510-L521 pasa a HEAD L505-L516. Configuracion del frame y cuatro handlers locales conservan blob. Solo se arrastra esta evidencia de solicitud; callbacks, resultados, recarga y navegacion siguen excluidos.',
         'evidence': source_evidence([i for c in calls for i in c['evidence_proof_ids']]),
         'related_known_ids': ['IMP-C1', 'BR-IMP-001', 'BR-IMP-003', 'BR-IMP-004'],
         'deduplication': 'IMP-C1 ya identifica el GET correcto en M; no se reabre como API nueva. Lo nuevo es la prueba P95/HEAD y sus rangos desplazados en el blob cambiado.',
         'new_independent_finding': False},
        {'id': 'TEMP-CF002', 'classification': 'documentary_precision',
         'title': 'Distinguir evidencia local estable de dependencia directa modificada',
         'statement': 'La matriz identifica por registro los frames/pantallas con referencias directas al JS cambiado. Sus blobs y citas pueden conservarse, pero esa igualdad no acredita el comportamiento compuesto. Las referencias a los reportes se inventarian sin leer sus cuerpos; sus cambios semanticos quedan en la tarea del otro agente. Los tres paths cambiados y sus vecinos no se convierten en una revision de todo el arbol.',
         'evidence': source_evidence([r['proof_id'] for r in data['changed_path_reference_metadata'] if 'proof_id' in r]),
         'changed_path_blob_evidence': data['changed_paths'],
         'affected_matrix_ids': data['coverage']['boundary_affected_matrix_rows'],
         'related_known_ids': ['IMP-SCOPE-001'],
         'deduplication': 'La observacion remota de tres paths ya era conocida; aporta ahora propagacion directa por registro y pruebas de blobs/rangos en HEAD, no un nuevo hallazgo de frescura.',
         'new_independent_finding': False},
        {'id': 'TEMP-CF003', 'classification': 'documentary_precision',
         'title': 'La revalidacion Peru conserva la procedencia de las mejoras citadas solo en M',
         'statement': '',
         'evidence': [r['baseline_document'] for r in data['matrix'] if not r['peru_proof_ids']],
         'related_known_ids': ['IMP-T008', 'IMP-T009', 'IMP-T010', 'CLR-IMP-001', 'RPR-IMP-001', 'RPR-IMP-002'],
         'deduplication': 'No altera los mecanismos conocidos ni abre OPS nuevas; documenta la cobertura y procedencia del traslado al HEAD solicitado.',
         'new_independent_finding': False},
    ]
    # Original-record provenance is separate from related OPS/BR evidence.
    no_p = [r['id'] for r in data['matrix'] if r['group'] == 'operational_improvement' and not r['peru_proof_ids']]
    items[2]['statement'] = (
        'De 81 conceptos, 80 tienen evidencia P95; parte-recepcion solo M. Las nueve OPS, VAR-001 y cuatro BR tienen evidencia P. '
        f'{len(no_p)} de ocho mejoras operativas solo citan M: ' + ', '.join(no_p) + '. '
        'Se registran coincidencias M/HEAD por rango cuando existen; no se promocionan a Peru ni se reutilizan lineas M como P. '
        'Las mejoras restantes con evidencia P conservan sus pins propios. Cualquier apoyo indirecto por un OPS/BR relacionado se mantiene separado del registro original.'
    )
    for item in items:
        item['sourcepins'] = POLICY['sourcepins']
        item['status'] = 'PROPOSED_FOR_COORDINATOR_INTEGRATION_NOT_CANONICAL'
    closure = {
        'status': 'PROPOSAL_NOT_EXECUTED_AFTER_INTEGRATION',
        'technique': 'Independent reverse traceability challenge with counterfactual mutations of in-memory evidence records; no application code.',
        'different_from_this_pass': 'Este pase construye identidad adelante P95->HEAD y dependencias de un salto. El cierre parte de cada afirmacion documental integrada, reconstruye su soporte hacia atras con git cat-file --batch, y desafia su suficiencia con mutaciones de metadatos.',
        'precondition': 'Coordinador integra novedades aceptadas y aporta sidecar del otro agente para los dos reportes; no ampliar exclusiones.',
        'steps': [
            'Fijar el commit o snapshot documental integrado y su digest, H/P95/K/M; no consultar master remoto a44.',
            'Para cada afirmacion integrada reconstruir claim->registro->rango->objeto Git usando un verificador independiente de este script y git cat-file --batch; calcular SHA256 otra vez, sin ejecutar PHP/JS.',
            'Controles negativos en memoria: desplazar una linea, cambiar un OID, asignar pin M a P, eliminar una dependencia al JS y marcar como verificado un callback excluido. Deben fallar o quedar fuera de alcance, nunca pasar silenciosamente.',
            'Control positivo: rangos reubicados de solicitudes (416-421->409-414 y510-521->505-516) conservan SHA256 y se aceptan solo como identidad acotada.',
            'Contrastar por separado el sidecar delegado de reportes contra sus OIDs HEAD, sin reabrir cuerpos ni navegacion; ausencia de resultado impide cerrar ese dominio.',
            'Registrar solo nuevas precisiones materiales o contradicciones con los IDs existentes; integrar cada novedad y reiniciar el conteo de pases sin delta que lleve el coordinador.',
        ],
        'acceptance': 'Todos los registros y citas integrados trazables; controles negativos detectados; procedencia M/P correcta; dependencias cambiadas o excluidas visibles; cero deltas materiales en este pase independiente. No prueba runtime, red, BD, politica empresarial ni cierre global automatico.',
    }
    return {'schema_version': '1.0', 'registry_type': 'peru_HEAD_carryforward_documentary_deltas',
            **POLICY, 'coverage': data['coverage'], 'items': items,
            'known_ids_considered': [x['id'] for x in audit.known['deltas']],
            'summary': {'documentary_precisions': len(items), 'new_independent_findings': 0,
                        'canonical_integrations': 0}, 'closure_test_proposal': closure}


def markdown(data, delta):
    cov = data['coverage']
    lines = ['# Matriz de revalidacion de conocimiento Peru HEAD', '',
             'Fecha cliente: **19-11-2026, Europe/Madrid**. Revision estatica lateral; no canonica.', '',
             '| Fuente | Commit |', '| --- | --- |']
    lines += [f'| {k} | `{v}` |' for k, v in POLICY['sourcepins'].items()]
    lines += ['', '## Cobertura y limite de las conclusiones', '',
              f"Arbol P95/HEAD: {cov['tree']['P95_entries']}/{cov['tree']['HEAD_entries']} entradas; "
              f"{cov['tree']['identical_entries_mode_type_oid']} identicas por modo/tipo/OID y tres paths cambiados. "
              '**Cero revisiones semanticas se atribuyen a esa igualdad global.**', '',
              f"Matriz: {cov['matrix_records']} registros; 81 glosario, nueve OPS, ocho mejoras operativas, cuatro BR y VAR-001. "
              f"{cov['P_citation_occurrences_from_md']} citas P en Markdown, {cov['P_citation_distinct_ranges_from_md']} rangos distintos. "
              f"{cov['md_documents_inventoried']} documentos inventariados. Las pruebas detalladas estan en el JSON de auditoria.", '',
              'Se preserva el significado y confianza del registro historico, sin repetir probes ni declarar aprobacion de negocio. '
              'Los rangos M se comparan separadamente; no acreditan por si solos conocimiento Peru. '
              'Citas de historia y prosa sin pin/rango no se promueven. Los 20 candidatos API raw siguen siendo candidatos.', '',
              f"Pruebas P95: {cov['range_statuses_by_origin']['P95']}. Comparacion historica M/HEAD: "
              f"{cov['range_statuses_by_origin']['M_historical']}. Los rangos M no coincidentes requieren otra revision "
              'si se pretende atribuirles comportamiento Peru; no son regresiones nuevas entre P95 y HEAD.', '',
              '## Paths cambiados', '', '| Path | Blob P95 | Blob HEAD | Tratamiento |', '| --- | --- | --- | --- |']
    lines += [f"| `{x['path']}` | `{x['P95']['blob']}` | `{x['HEAD']['blob']}` | {x['review']} |" for x in data['changed_paths']]
    lines += ['', '## Precisiones propuestas', '']
    for item in delta['items']:
        lines += [f"### {item['id']} — {item['title']}", '', item['statement'], '',
                  '**Deduplicacion:** ' + item['deduplication'], '']
    lines += ['## Solicitudes de negocio acotadas en datosEmbarques.js', '',
              '| ID | Metodo / destino | Rangos P95 → HEAD (pruebas) |', '| --- | --- | --- |']
    proofs = {p['id']: p for p in data['range_proofs']}
    for call in data['bounded_business_requests']:
        ranges = []
        for pid in call['evidence_proof_ids']:
            p = proofs[pid]
            ranges.append(f"{pid}: `{p['path']}` L{p['line_start']}-{p['line_end']} → L{p['head_line_start']}-{p['head_line_end']}")
        lines.append(f"| {call['id']} | {call['method']} `{call['endpoint']}` | " + '; '.join(ranges) + ' |')
    lines += ['', 'Los rangos anteriores contienen solo configuracion, parametros y solicitudes. '
              'No prueban respuesta, persistencia o servicio externo. No se analizan callbacks, salidas ni recarga. '
              'El catalogo documental API incluye filas de configuracion y atribuciones raw rechazadas: su numero no es un total de APIs validadas.', '',
              '## Matriz por registro', '',
              'C = evidencia P95 conservada por identidad; M = sin evidencia P original, sin promocion. '
              'D = referencia directa a path cambiado: requiere revision separada de esa frontera, sin invalidar automaticamente la cita local. '
              'Los IDs R apuntan a objetos Git, rangos inclusivos y SHA256 del JSON.', '',
              '| Grupo | ID / titulo | Estado | Pruebas P / M |', '| --- | --- | --- | --- |']
    for r in data['matrix']:
        state = 'C' if r['peru_proof_ids'] else 'M'
        if r['changed_reference_indexes']:
            state += '+D'
        lines.append(f"| {r['group']} | {r['id']} — {r['title']} | {state} | " + ', '.join(r['evidence_proof_ids']) + ' |')
    lines += ['', '## Citas P por documento', '', '| Documento | Ocurrencias |', '| --- | --- |']
    lines += [f'| `{p}` | {n} |' for p, n in cov['md_documents_with_P_citations'].items()]
    lines += ['', '## Dependencias directas y exclusiones', '',
              f"{cov['direct_dependency_edges']} aristas estaticas de un salto; {cov['changed_path_lexical_references']} referencias lexicales a paths cambiados. "
              'Los includes literales y scripts tienen identidad propia y del destino; las referencias lexicales no prueban ejecucion. '
              'Includes dinamicos quedan sin resolver; no hay cierre transitivo. Las dependencias del servicio externo y gitlinks siguen fuera de verificacion.', '']
    lines += ['- ' + s for s in POLICY['exclusions']]
    lines += ['', 'Master remoto a44 queda fuera de alcance. No se modifica fuente, documentos finales o manifest; no hay commit ni push.', '',
              '## Propuesta de cierre tras integrar novedades', '', delta['closure_test_proposal']['different_from_this_pass'], '',
              '**Precondicion:** ' + delta['closure_test_proposal']['precondition'], '']
    lines += [f'{i}. {s}' for i, s in enumerate(delta['closure_test_proposal']['steps'], 1)]
    lines += ['', '**Aceptacion:** ' + delta['closure_test_proposal']['acceptance'], '',
              '**Estado:** propuesta pendiente; este trabajo no declara cierre global ni pases posteriores a la integracion.', '',
              '## Reproduccion', '',
              '`python -B scripts/audit/peru_head_carryforward.py --check` compara en memoria los tres sidecars con los objetos fijados. '
              'Sin `--check`, solo escribe los tres sidecars autorizados. El script solo usa stdlib y comandos Git de lectura; no carga el auditor bloqueado.', '']
    return '\n'.join(lines).encode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('C:/repos/proveedores-peru-head-review-20261119'))
    parser.add_argument('--knowledge', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    audit = Audit(args.knowledge.resolve(), args.source.resolve())
    data = audit.build()
    delta = deltas(audit, data)
    payloads = (pack(data), pack(delta), markdown(data, delta))
    for name, content in zip(OUTPUTS, payloads):
        dest = audit.kb / name
        if args.check:
            if not dest.exists() or dest.read_bytes() != content:
                raise ValueError('Sidecar mismatch: ' + name)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
    print(json.dumps({'status': 'CHECK_PASS' if args.check else 'GENERATED',
                      'matrix_records': data['coverage']['matrix_records'],
                      'P_citations': data['coverage']['P_citation_occurrences_from_md'],
                      'range_statuses': data['coverage']['proof_statuses'],
                      'outputs': list(OUTPUTS)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
