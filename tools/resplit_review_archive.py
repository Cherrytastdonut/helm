#!/usr/bin/env python3
"""Re-split the current review ZIP for connector transfer without changing ZIP bytes."""
import argparse
import hashlib
import json
from pathlib import Path
from restore_archives import ROOT, digest_file, safe_path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--zip', type=Path, required=True)
p.add_argument('--part-mib', type=int, default=4)
a = p.parse_args()
if not 1 <= a.part_mib <= 16:
    p.error('--part-mib must be between 1 and 16')
mp = ROOT / 'archives/manifest.json'
m = json.loads(mp.read_text())
entry = next(e for e in m['archives'] if e['id'] == 'procurement-review-20261001')
if a.zip.stat().st_size != entry['size_bytes'] or digest_file(a.zip) != entry['sha256']:
    raise ValueError('Input ZIP does not match the registered review archive')
old_paths = {x['path'] for x in entry['parts']}
target = ROOT / 'archives' / entry['id']
target.mkdir(exist_ok=True)
parts = []
with a.zip.open('rb') as source:
    while block := source.read(a.part_mib * 1024 * 1024):
        path = target / f"{entry['filename']}.part-{len(parts)+1:03d}"
        path.write_bytes(block)
        parts.append({'path': path.relative_to(ROOT).as_posix(), 'size_bytes': len(block),
                      'sha256': hashlib.sha256(block).hexdigest()})
for old in old_paths - {x['path'] for x in parts}:
    safe_path(ROOT, old).unlink()
entry['parts'] = parts
entry['part_size_bytes'] = a.part_mib * 1024 * 1024
mp.write_text(json.dumps(m, indent=2) + '\n')
vp = ROOT / 'data/procurement-review/PACKAGE_VALIDATION.json'
v = json.loads(vp.read_text())
v.update(split_parts=len(parts), split_max_bytes=entry['part_size_bytes'])
vp.write_text(json.dumps(v, indent=2) + '\n')
rp = ROOT / 'archives/README.md'
lines = rp.read_text().splitlines()
for i, line in enumerate(lines):
    if line.startswith('| procurement-review-20261001 |'):
        lines[i] = f"| {entry['id']} | {entry['size_bytes']/1e6:.1f} | {len(parts)} | `{entry['sha256']}` |"
rp.write_text('\n'.join(lines) + '\n')
print(f"Re-split into {len(parts)} parts; ZIP SHA-256 unchanged: {entry['sha256']}")
