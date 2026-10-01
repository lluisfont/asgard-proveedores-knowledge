"""Transfer audited evidence with provenance, redaction and content hashes."""

import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import subprocess
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


TEXT = {'.md', '.txt', '.json', '.jsonl', '.csv', '.yaml', '.yml', '.html',
        '.mmd', '.bpmn', '.sha256', '.py', '.ps1', '.js'}
SENSITIVE_NAME = r'(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|tokenjwt|db[_-]?pass|key[_-]?jwt|jwt[_-]?key)'
LITERAL = re.compile(r'''(?ix)(?:[\$"']?[\w-]*''' + SENSITIVE_NAME + r'''[\w-]*["']?\s*(?:=>|[:=])\s*|define\s*\(\s*["'][\w-]*''' + SENSITIVE_NAME + r'''[\w-]*["']\s*,\s*)(["'])([^\r\n]{1,500}?)\1''')
TOKEN = re.compile(r'(?<![\w])(?:AIza[\w-]{30,}|gh[pousr]_[\w]{20,}|github_pat_[\w]{30,}|sk-(?:proj-)?[\w-]{20,}|AKIA[A-Z0-9]{16}|eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}|[ps]k\.eyJ[\w.-]{20,})(?![\w])')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


class Export:
    def __init__(self, args):
        self.args = args
        self.source = Path(args.source).resolve()
        self.audit = Path(args.audited_source).resolve()
        self.target = Path(args.target).resolve()
        self.stage = Path(args.stage).resolve()
        if self.stage in (self.source, self.audit, self.target):
            raise ValueError('Staging must be isolated from source and destination')
        self.entries = []
        self.exclusions = []
        self.secret_values = set()
        self.replacements = 0
        self.sanitized_large_payloads = {}
        self.now = datetime.now(timezone.utc).isoformat()
        for root in (self.source, self.audit):
            for path in root.rglob('*.php'):
                if any(part in {'.git', 'vendor', 'mcp129-venv', 'PHPExcel', 'MPDF57', 'PDFMerger'} for part in path.parts):
                    continue
                text = path.read_text(encoding='utf-8-sig', errors='replace')
                for match in LITERAL.finditer(text):
                    value = match.group(2)
                    if len(value) >= 8 and not any(t in value for t in ('$','[REDACTED', 'REPLACE', 'YOUR_', 'your_', 'example', 'TOKEN', 'password', 'secret', 'token')):
                        self.secret_values.add(value)
                self.secret_values.update(TOKEN.findall(text))
        self.secrets = sorted(self.secret_values, key=len, reverse=True)
        self.secret_pattern = re.compile('|'.join(re.escape(s) for s in self.secrets)) if self.secrets else None

    def redact(self, text):
        if self.secret_pattern is not None:
            text, count = self.secret_pattern.subn('[REDACTED]', text)
            self.replacements += count
        text, count = TOKEN.subn('[REDACTED]', text)
        self.replacements += count
        if not any(term in text.lower() for term in ('password', 'passwd', 'pwd', 'secret', 'key', 'token')):
            return text
        def literal(match):
            value = match.group(2)
            if len(value) < 8 or any(t in value for t in ('$', '[REDACTED', 'example', 'YOUR_', 'your_', 'password', 'secret', 'token')):
                return match.group(0)
            self.replacements += 1
            return match.group(0).replace(value, '[REDACTED]')
        return LITERAL.sub(literal, text)

    def sanitize(self, data, suffix):
        if len(data) > 50000:
            digest = sha(data)
            if digest in self.sanitized_large_payloads:
                return self.sanitized_large_payloads[digest]
            result = self.sanitize_payload(data, suffix)
            self.sanitized_large_payloads[digest] = result
            return result
        return self.sanitize_payload(data, suffix)

    def sanitize_payload(self, data, suffix):
        if suffix == '.xlsx':
            output = io.BytesIO()
            with zipfile.ZipFile(io.BytesIO(data)) as archive, zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as dest:
                for entry in archive.infolist():
                    blob = archive.read(entry.filename)
                    if entry.filename.endswith(('.xml', '.rels')):
                        blob = self.redact(blob.decode('utf-8')).encode('utf-8')
                    dest.writestr(entry, blob)
            return output.getvalue()
        if suffix not in TEXT and suffix != '':
            raise ValueError('Unsupported evidence type: ' + suffix)
        text = data.decode('utf-8-sig')
        if suffix == '.json':
            value = json.loads(text)
            def walk(obj):
                if isinstance(obj, dict):
                    return {k: walk(v) for k, v in obj.items()}
                if isinstance(obj, list):
                    return [walk(v) for v in obj]
                return self.redact(obj) if isinstance(obj, str) else obj
            return (json.dumps(walk(value), ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        if suffix == '.jsonl':
            rows = []
            for line in text.splitlines():
                if line.strip():
                    row = json.loads(line)
                    # The export keeps identifiers and locations even when observations contain secrets.
                    rows.append(self.sanitize(json.dumps(row).encode('utf-8'), '.json').decode('utf-8').strip())
            return ('\n'.join(json.dumps(json.loads(row), ensure_ascii=False) for row in rows) + '\n').encode('utf-8')
        if suffix == '.csv':
            rows = csv.reader(io.StringIO(text, newline=''))
            output = io.StringIO(newline='')
            writer = csv.writer(output, lineterminator='\n')
            for row in rows:
                writer.writerow([self.redact(cell) for cell in row])
            return output.getvalue().encode('utf-8')
        return self.redact(text).encode('utf-8')

    def copy(self, path, dest, origin):
        original = path.read_bytes()
        sanitized = self.sanitize(original, path.suffix.lower())
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(sanitized)
        self.entries.append({'origin': origin, 'source_path': path.relative_to(self.audit if origin == 'proveedores-master_peru' else self.source).as_posix(),
                             'stage_path': dest.relative_to(self.stage).as_posix(), 'source_sha256': sha(original),
                             'export_sha256': sha(sanitized), 'source_bytes': len(original), 'export_bytes': len(sanitized),
                             'transformed': original != sanitized})

    def tree(self, root, dest, origin):
        for path in sorted(root.rglob('*')):
            if not path.is_file():
                continue
            if '__pycache__' in path.parts or path.suffix == '.pyc':
                self.exclusions.append({'path': str(path), 'reason': 'runtime_cache'})
                continue
            self.copy(path, dest / path.relative_to(root), origin)

    def prepare(self):
        if self.stage.exists() and any(self.stage.iterdir()):
            raise ValueError('Staging directory must be new and empty')
        self.stage.mkdir(parents=True, exist_ok=True)
        print('Preparing Graphify artifacts', flush=True)
        self.tree(self.audit / 'graphify-out', self.stage / 'graphify-out', 'proveedores-master_peru')
        print('Preparing Brownfield evidence', flush=True)
        self.tree(self.audit / '.brownfield' / 'work', self.stage / 'audit' / 'reports', 'proveedores-master_peru')
        for name in ('config', 'schemas', 'prompts', 'custom_tools', 'baseline'):
            self.tree(self.audit / '.brownfield' / name, self.stage / 'audit' / 'verification' / name, 'proveedores-master_peru')
        for name in ('README.md', 'PIPELINE.md', 'ASGARD_ANALYSIS_FRAMEWORK.md', 'PROJECT_STATE.json'):
            self.copy(self.audit / '.brownfield' / name, self.stage / 'audit' / name, 'proveedores-master_peru')
        for path in sorted(self.audit.glob('AUDITORIA_*.md')):
            self.copy(path, self.stage / 'audit' / 'reports' / 'iterative' / path.name, 'proveedores-master_peru')
        custom = self.audit / '.brownfield' / 'work' / 'custom'
        for name in ('asgard-api-audit', 'asgard-api-audit-v2', 'asgard-api-audit-augmented', 'api-deep-iterative'):
            self.tree(custom / name, self.stage / 'audit' / 'api' / name, 'proveedores-master_peru')
        for path in sorted(custom.glob('asgard-api-*.json')):
            self.copy(path, self.stage / 'audit' / 'api' / path.name, 'proveedores-master_peru')
        write_json(self.stage / 'audit' / 'audit_summary.json', {
            'status': 'INCOMPLETE_BASELINE', 'commit': None,
            'baseline': read_json(self.audit / '.brownfield' / 'PROJECT_STATE.json')['baseline'],
            'inventory': read_json(self.audit / '.brownfield' / 'work' / 'inventory' / 'summary.json'),
            'evidence': read_json(self.audit / '.brownfield' / 'work' / 'evidence' / 'summary.json')})
        related = self.source / 'graphify-asgard-audit'
        print('Preparing related historical reports', flush=True)
        for path in sorted(related.rglob('*')):
            if not path.is_file():
                continue
            if any(p in {'mcp129-venv', '__pycache__', '.git'} for p in path.relative_to(related).parts):
                continue
            self.copy(path, self.stage / 'related-graphify-audits' / path.relative_to(related), 'proveedores-checkout')
        write_json(self.stage / 'transfer-preparation.json', {'entries': self.entries, 'excluded': self.exclusions,
            'generated_at': self.now, 'literal_secret_candidates': len(self.secrets), 'redactions': self.replacements})
        print(json.dumps({'prepared_files': len(self.entries), 'redactions': self.replacements, 'staging': str(self.stage)}))

    def archive_history(self):
        checkpoints = []
        objects = self.target / 'source-audits' / 'history' / 'objects'
        objects.mkdir(parents=True, exist_ok=True)
        for path in sorted((self.audit / '.brownfield' / 'releases').glob('*.zip')):
            print('Preserving checkpoint ' + path.name, flush=True)
            records = []
            with zipfile.ZipFile(path) as archive:
                for name in archive.namelist():
                    if name.endswith('/'):
                        continue
                    raw = archive.read(name)
                    data = self.sanitize(raw, Path(name).suffix.lower())
                    digest = sha(data)
                    object_path = objects / (digest + Path(name).suffix.lower() + ('.gz' if len(data) > 1000000 else ''))
                    if not object_path.exists():
                        object_path.write_bytes(gzip.compress(data, mtime=0) if object_path.suffix == '.gz' else data)
                    records.append({'path': name, 'source_sha256': sha(raw), 'export_sha256': digest,
                                    'object_path': object_path.relative_to(self.target).as_posix(),
                                    'compression': 'gzip' if object_path.suffix == '.gz' else None,
                                    'bytes': len(data), 'transformed': raw != data})
            checkpoint = {'name': path.name, 'original_sha256': sha(path.read_bytes()), 'entries': records,
                          'original_integrity_files_describe_original_archive': True,
                          'export_verification': 'Use export_sha256 for exported objects; original MANIFEST/SHA256SUMS are historical evidence.'}
            destination = self.target / 'source-audits' / 'history' / (path.stem + '.json')
            write_json(destination, checkpoint)
            checkpoints.append({'name': path.name, 'manifest': destination.relative_to(self.target).as_posix(), 'entries': len(records)})
        return checkpoints

    def coverage(self):
        baseline_path = self.audit / '.brownfield' / 'work' / 'inventory' / 'source_inventory.csv'
        rows = list(csv.DictReader(io.StringIO(baseline_path.read_text(encoding='utf-8-sig'))))
        result = []
        counts = Counter()
        for row in rows:
            path = self.source / row['path']
            current_sha = sha(path.read_bytes()) if path.is_file() else None
            status = 'same' if current_sha == row['sha256'] else 'missing' if current_sha is None else 'different'
            counts[status] += 1
            result.append({'path': row['path'], 'audited_sha256': row['sha256'], 'current_sha256': current_sha, 'status': status})
        write_json(self.target / 'knowledge' / 'snapshots' / 'current' / 'audited-source-comparison.json',
                   {'status': 'PARTIAL', 'source': str(self.source), 'audited_source': str(self.audit),
                    'counts': dict(counts), 'note': 'Checks the historical audited inventory only. Additional current files and runtime behavior are not covered.', 'files': result})
        return dict(counts)

    def finalize(self):
        import shutil
        preparation = read_json(self.stage / 'transfer-preparation.json')
        shutil.copytree(self.stage / 'audit' / 'api', self.target / 'source-audits' / 'api', dirs_exist_ok=True)
        shutil.copytree(self.stage / 'related-graphify-audits', self.target / 'source-audits' / 'related-graphify-audits', dirs_exist_ok=True)
        self.copy_target = {}
        for record in preparation['entries']:
            p = record['stage_path']
            if p.startswith('graphify-out/'):
                dest = 'source-audits/graphify/' + p[len('graphify-out/'):]
            elif p.startswith('audit/reports/'):
                dest = 'source-audits/brownfield/reports/' + p[len('audit/reports/'):]
            elif p.startswith('audit/verification/'):
                dest = 'source-audits/brownfield/verification/' + p[len('audit/verification/'):]
            elif p.startswith('audit/api/'):
                dest = 'source-audits/api/' + p[len('audit/api/'):]
            elif p.startswith('audit/'):
                dest = 'source-audits/brownfield/' + p[len('audit/'):]
            else:
                dest = 'source-audits/' + p
            # The upstream converter only copies selected Brownfield root documents.
            target = self.target / dest
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(self.stage / p, target)
            record['path'] = dest
            self.copy_target[p] = record
        checkpoints = self.archive_history()
        # Compress large text artifacts without discarding any content or path provenance.
        for path in sorted((self.target / 'source-audits').rglob('*')):
            if path.is_file() and path.stat().st_size > 1000000 and path.suffix in TEXT - {'.html'}:
                data = path.read_bytes()
                compressed = path.with_name(path.name + '.gz')
                compressed.write_bytes(gzip.compress(data, mtime=0))
                path.unlink()
                relative = path.relative_to(self.target).as_posix()
                for record in preparation['entries']:
                    if record['path'] == relative:
                        record['path'] = compressed.relative_to(self.target).as_posix()
                        record['compression'] = 'gzip'
        counts = self.coverage()
        tracked = subprocess.run(['git', '-C', str(self.source), 'ls-files', '-z'], capture_output=True, check=True).stdout
        current_files = []
        for relative in tracked.decode('utf-8').split('\0'):
            if not relative or relative == '.env.php':
                continue
            path = self.source / relative
            if path.is_file():
                current_files.append({'path': relative, 'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())})
        for path in self.source.glob('*.sql'):
            if path.name not in {entry['path'] for entry in current_files}:
                current_files.append({'path': path.name, 'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes()), 'untracked': True})
        write_json(self.target / 'knowledge' / 'snapshots' / 'current' / 'checkout-inventory.json', {
            'current_head': git(self.source, 'rev-parse', 'HEAD'), 'remote': git(self.source, 'remote', 'get-url', 'origin'),
            'status': git(self.source, 'status', '--porcelain'), 'files': current_files,
            'note': 'File metadata and hashes only. Application contents and environment credentials are not exported.'})
        manifest_path = self.target / 'knowledge' / 'manifest.json'
        manifest = read_json(manifest_path)
        state = read_json(self.audit / '.brownfield' / 'PROJECT_STATE.json')
        manifest['repository'].update({'name': 'asgard-proveedores',
            'url': 'https://gitlab.com/kpo-group/asgard-project/proveedores',
            'current_head': git(self.source, 'rev-parse', 'HEAD'), 'github_main': None,
            'audited_commit': None, 'current_checkout': str(self.source),
            'historical_audited_checkout': str(self.audit),
            'functional_paths': ['src', 'index_archivos', 'index.php', 'info.php', '.htaccess',
                                 '.env-example.php', 'asgard.sql', 'asgardpe Base de Datos Peru.sql', 'Dockerfile', 'package.json']})
        manifest['audits']['brownfield']['status'] = 'INCOMPLETE_BASELINE'
        manifest['audits']['brownfield']['canonical'] = False
        manifest['audits']['brownfield']['project_state'] = state
        manifest['audits']['api'].update({'status': 'partial_with_static_augmentation',
            'pinned_auditor_version': '0.8.0', 'documented_exposed_endpoints': None,
            'documented_consumed_endpoints': 2, 'native_exposed_endpoints_detected': 0,
            'exposed_endpoint_candidates': 246, 'consumed_call_candidates': 23,
            'note': 'Native zero is a detector limitation, not evidence of absence. Candidates require runtime and human verification.'})
        manifest['audits']['graphify']['status'] = 'imported_historical_graph_including_third_party'
        manifest['transfer'] = {'date': '2026-10-01', 'tool': 'lluisfont/convertidor-knowledge',
            'tool_commit': git(Path(self.args.converter), 'rev-parse', 'HEAD'),
            'coverage_status': 'PARTIAL', 'source_comparison': counts,
            'source_sha256': state['baseline']['source_hash'], 'database_sha256': state['baseline']['database_hash'],
            'artifact_manifest': 'knowledge/transfer-artifacts.json',
            'historical_checkpoints': checkpoints, 'related_audits_are_not_proveedores_findings': True}
        write_json(manifest_path, manifest)
        write_json(self.target / 'knowledge' / 'transfer-artifacts.json', {
            'schema_version': '1.0', 'generated_at': self.now, 'entries': preparation['entries'],
            'checkpoints': checkpoints, 'exclusions': preparation['excluded'],
            'redactions': preparation['redactions'] + self.replacements,
            'redaction_policy': 'Preserve source/evidence identifiers and hashes; remove detected literal credentials and token formats. Never copy application source or SQL dumps.'})
        graph = read_json(self.stage / 'graphify-out' / 'graph.json')
        write_json(self.target / 'knowledge' / 'graph-summary.json', {
            'nodes': len(graph['nodes']), 'edges': len(graph.get('links', graph.get('edges', []))),
            'includes_third_party': True, 'community_count': len({n.get('community') for n in graph['nodes']}),
            'full_graph': 'source-audits/graphify/graph.json.gz'})
        print(json.dumps({'exported_artifacts': len(preparation['entries']), 'checkpoints': len(checkpoints),
                          'source_comparison': counts, 'redactions': preparation['redactions'] + self.replacements}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prepare', 'finalize'])
    parser.add_argument('--source', required=True)
    parser.add_argument('--audited-source', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--stage', required=True)
    parser.add_argument('--converter', required=True)
    args = parser.parse_args()
    exporter = Export(args)
    getattr(exporter, args.mode)()


if __name__ == '__main__':
    main()
