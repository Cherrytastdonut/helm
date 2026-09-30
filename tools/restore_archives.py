#!/usr/bin/env python3
"""Restore the byte-identical HELM ZIPs from ordered, SHA-256 checked parts."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest_file(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def safe_path(root, relative):
    rel = PurePosixPath(relative)
    if not relative or '\\' in relative or rel.is_absolute() or '..' in rel.parts:
        raise ValueError(f'Unsafe path: {relative!r}')
    result = (root / relative).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes destination: {relative!r}')
    return result


def extract_checked(archive, destination):
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f'Extraction destination is not empty: {destination}')
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            safe_path(destination, item.filename)
            if stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError(f'Symbolic link in archive: {item.filename}')
        bad = z.testzip()
        if bad:
            raise ValueError(f'ZIP CRC failed: {bad}')
        destination.mkdir(parents=True, exist_ok=True)
        z.extractall(destination)
    print(f'Extracted: {destination}', flush=True)


def restore(entry, output_dir, verify_only=False, extract=False):
    name = entry['filename']
    if PurePosixPath(name).name != name or '\\' in name:
        raise ValueError(f'Invalid archive filename: {name!r}')
    output = output_dir / name
    partial = output.with_name(output.name + '.partial')
    writer = None
    own_partial = False
    try:
        if not verify_only:
            output_dir.mkdir(parents=True, exist_ok=True)
            if output.exists():
                if output.stat().st_size != entry['size_bytes'] or digest_file(output) != entry['sha256']:
                    raise ValueError(f'Refusing to replace a different file: {output}')
            else:
                writer = partial.open('xb')
                own_partial = True
        whole_hash = hashlib.sha256()
        whole_size = 0
        for part in entry['parts']:
            path = safe_path(ROOT, part['path'])
            part_hash = hashlib.sha256()
            part_size = 0
            with path.open('rb') as f:
                for block in iter(lambda: f.read(1024 * 1024), b''):
                    part_hash.update(block)
                    whole_hash.update(block)
                    part_size += len(block)
                    if writer:
                        writer.write(block)
            if part_size != part['size_bytes'] or part_hash.hexdigest() != part['sha256']:
                raise ValueError(f'Part checksum/size failed: {part["path"]}')
            whole_size += part_size
        if whole_size != entry['size_bytes'] or whole_hash.hexdigest() != entry['sha256']:
            raise ValueError(f'Archive checksum/size failed: {entry["id"]}')
        if writer:
            writer.close()
            writer = None
            # Never replace a file that appeared during verification.
            if output.exists():
                raise ValueError(f'Output appeared during restoration: {output}')
            partial.rename(output)
            own_partial = False
        print(f'PASS {entry["id"]}: {whole_size:,} bytes; SHA-256 matches', flush=True)
        if not verify_only:
            print(f'ZIP: {output}', flush=True)
        if extract:
            extract_checked(output, safe_path(output_dir, entry['id']))
    finally:
        if writer:
            writer.close()
        if own_partial:
            partial.unlink(missing_ok=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    select = p.add_mutually_exclusive_group()
    select.add_argument('--all', action='store_true', help='Restore all three archives')
    select.add_argument('--archive', default='ser0063-review-20260930', help='Archive id in manifest.json')
    p.add_argument('--output-dir', type=Path, default=ROOT / 'downloads')
    p.add_argument('--verify-only', action='store_true', help='Check all parts without creating output')
    p.add_argument('--extract', action='store_true', help='Also extract into an empty per-archive directory')
    args = p.parse_args()
    if args.verify_only and args.extract:
        p.error('--verify-only cannot be combined with --extract')
    manifest = json.loads((ROOT / 'archives/manifest.json').read_text(encoding='utf-8'))
    if manifest.get('format_version') != 1 or manifest.get('hash_algorithm') != 'sha256':
        raise ValueError('Unsupported manifest format')
    entries = [e for e in manifest['archives'] if args.all or e['id'] == args.archive]
    if not entries:
        p.error(f'Unknown archive id: {args.archive}')
    for entry in entries:
        restore(entry, args.output_dir.resolve(), args.verify_only, args.extract)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, zipfile.BadZipFile) as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)
