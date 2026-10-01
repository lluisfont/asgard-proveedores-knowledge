"""Validate transferred evidence, structured formats and checkpoint integrity."""

import csv
import gzip
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


def main():
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / 'knowledge/transfer-artifacts.json').read_text(encoding='utf-8-sig'))
    seen = set()
    files = 0
    checkpoint_entries = 0
    text_count = 0
    token = re.compile(r'(?<![\w])(?:AIza[\w-]{30,}|gh[pousr]_[\w]{20,}|github_pat_[\w]{30,}|sk-(?:proj-)?[\w-]{20,}|AKIA[A-Z0-9]{16}|eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}|[ps]k\.eyJ[\w.-]{20,})(?![\w])')
    def check(record):
        nonlocal files, text_count
        path = (root / record.get('object_path', record.get('path', ''))).resolve()
        if not path.is_relative_to(root):
            raise ValueError('Unsafe evidence path')
        data = path.read_bytes()
        if record.get('compression') == 'gzip':
            data = gzip.decompress(data)
        if hashlib.sha256(data).hexdigest() != record['export_sha256']:
            raise ValueError('Hash mismatch: ' + str(path.relative_to(root)))
        if path in seen:
            return
        seen.add(path)
        suffix = Path(path.stem).suffix if path.suffix == '.gz' else path.suffix
        if suffix == '.xlsx':
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                if archive.testzip():
                    raise ValueError('Invalid workbook')
                for name in archive.namelist():
                    if name.endswith(('.xml', '.rels')):
                        xml = archive.read(name)
                        ElementTree.fromstring(xml)
                        if token.search(xml.decode('utf-8')):
                            raise ValueError('Unredacted token in workbook: ' + str(path.relative_to(root)))
        else:
            text = data.decode('utf-8-sig')
            text_count += 1
            if token.search(text):
                raise ValueError('Unredacted token: ' + str(path.relative_to(root)))
            if suffix == '.json':
                json.loads(text)
            elif suffix == '.jsonl':
                for line in text.splitlines():
                    if line.strip():
                        json.loads(line)
            elif suffix == '.csv':
                rows = csv.reader(io.StringIO(text, newline=''), strict=True)
                header = next(rows, [])
                for line, row in enumerate(rows, start=2):
                    if row and len(row) != len(header):
                        raise ValueError('CSV column mismatch: ' + str(path.relative_to(root)) + ':' + str(line))
        files += 1
    for entry in manifest['entries']:
        check(entry)
    for checkpoint in manifest['checkpoints']:
        records = json.loads((root / checkpoint['manifest']).read_text(encoding='utf-8-sig'))['entries']
        for entry in records:
            check(entry)
            checkpoint_entries += 1
    leaked = [p.relative_to(root).as_posix() for p in (root / 'source-audits').rglob('*')
              if p.is_file() and (p.name == '.env.php' or p.suffix in {'.sql', '.php', '.exe', '.dll'})]
    if leaked:
        raise ValueError('Unexpected application/runtime files: ' + ', '.join(leaked))
    graph = json.loads((root / 'knowledge/graph-summary.json').read_text(encoding='utf-8'))
    graph_data = json.loads(gzip.decompress((root / graph['full_graph']).read_bytes()))
    if len(graph_data['nodes']) != graph['nodes'] or len(graph_data['links']) != graph['edges']:
        raise ValueError('Graph count mismatch')
    report = {'status': 'PASS', 'transferred_artifact_entries': len(manifest['entries']),
              'historical_checkpoints': len(manifest['checkpoints']), 'historical_checkpoint_entries': checkpoint_entries,
              'distinct_verified_payloads': files, 'text_artifacts_checked': text_count,
              'nodes': graph['nodes'], 'edges': graph['edges'],
              'coverage_status': 'PARTIAL',
              'note': 'PASS confirms export integrity and format validity, not application correctness or audit completeness.'}
    print(json.dumps(report, indent=2))
    (root / 'knowledge/snapshots/current/transfer-validation.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('Transfer validation FAIL: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
