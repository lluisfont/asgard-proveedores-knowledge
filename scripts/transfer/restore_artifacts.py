"""Restore compressed evidence or a historical checkpoint without trusting archive paths."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='Pack-relative .gz artifact')
    parser.add_argument('--checkpoint', help='Pack-relative historical checkpoint manifest')
    parser.add_argument('--destination', required=True)
    args = parser.parse_args()
    if bool(args.file) == bool(args.checkpoint):
        parser.error('Select exactly one of --file or --checkpoint')
    root = Path(__file__).resolve().parents[2]
    destination = Path(args.destination).resolve()
    source = (root / (args.file or args.checkpoint)).resolve()
    if not source.is_relative_to(root):
        raise ValueError('Artifact must be inside the Knowledge Pack')
    if args.file:
        if source.suffix != '.gz':
            raise ValueError('Expected a gzip artifact')
        output = destination / source.stem
        if output.exists():
            raise FileExistsError(output)
        data = gzip.decompress(source.read_bytes())
        inventory = json.loads((root / 'knowledge/transfer-artifacts.json').read_text(encoding='utf-8-sig'))
        matching = [e for e in inventory['entries'] if e['path'] == source.relative_to(root).as_posix()]
        current_index = root / 'knowledge/current-artifacts.json'
        if current_index.exists():
            current = json.loads(current_index.read_text(encoding='utf-8-sig'))
            matching += [e for e in current['entries'] if e['path'] == source.relative_to(root).as_posix()]
        if not matching or any(hashlib.sha256(data).hexdigest() != e['export_sha256'] for e in matching):
            raise ValueError('Artifact is not indexed or its integrity check failed')
        destination.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        print('Restored ' + str(output))
        return
    manifest = json.loads(source.read_text(encoding='utf-8-sig'))
    pending = []
    for entry in manifest['entries']:
        target = (destination / entry['path']).resolve()
        blob = (root / entry['object_path']).resolve()
        if not target.is_relative_to(destination) or not blob.is_relative_to(root):
            raise ValueError('Unsafe checkpoint path')
        if target.exists():
            raise FileExistsError(target)
        data = blob.read_bytes()
        if entry.get('compression') == 'gzip':
            data = gzip.decompress(data)
        if hashlib.sha256(data).hexdigest() != entry['export_sha256']:
            raise ValueError('Checkpoint integrity mismatch: ' + entry['path'])
        pending.append((target, data))
    for target, data in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    print('Restored ' + str(len(pending)) + ' checkpoint entries')


if __name__ == '__main__':
    main()
