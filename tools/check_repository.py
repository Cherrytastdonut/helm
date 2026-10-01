#!/usr/bin/env python3
"""Validate HELM navigation, declared scope, file counts, and content hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG = 'data/repository-files.json'
SKIP = {'.git', '__pycache__', '.venv', 'downloads', 'build', 'tmp'}


def repository_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not set(p.relative_to(ROOT).parts) & SKIP
                  and p.relative_to(ROOT).as_posix() != CATALOG)


def hash_file(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


def check(write_catalog=False):
    files = repository_files()
    entries = [{'path': p.relative_to(ROOT).as_posix(), 'size_bytes': p.stat().st_size,
                'sha256': hash_file(p)} for p in files]
    if write_catalog:
        (ROOT / CATALOG).write_text(json.dumps({
            'format_version': 1, 'created_on': '2026-10-01',
            'scope': 'All tracked deliverables except this catalog itself; SHA-256 of file bytes',
            'files': entries,
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    errors = []
    for path in files:
        if path.suffix.lower() != '.md':
            continue
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', text):
            target = target.strip().split(' "', 1)[0].strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            linked = (path.parent / unquote(parsed.path)).resolve()
            if not linked.exists():
                errors.append(f'Broken local link: {path.relative_to(ROOT)} -> {target}')
    status = read_json('data/project-status.json')
    revision = read_json('data/procurement-review/REVISION.json')
    validation = read_json('data/procurement-review/VALIDATION.json')
    fabrication = read_json('data/procurement-review/FABRICATION_INDEX.json')
    drawings = read_json('data/procurement-review/DRAWING_INDEX.json')
    model = read_json('data/procurement-review/manifest.json')
    full_step = read_json('data/procurement-review/FULL_STEP_READBACK.json')
    required = {'manufacturing_release': False, 'current_revision': revision['revision'],
                'review_nodes': len(model), 'review_part_steps': fabrication['part_steps'],
                'changed_part_steps': len(revision['part_exports']), 'review_dxfs': fabrication['flat_dxfs'],
                'review_guide_pages': drawings['guide_pages'], 'review_profile_pages': drawings['profile_pages'],
                'changed_candidate_pairs': validation['changed_candidate_pairs'],
                'changed_unintended_overlap_count': len(validation['changed_unintended_hits']),
                'unique_remaining_motion_pairs': validation['unique_camera_pairs'],
                'sample_motion_hit_counts': [len(x['hits']) for x in validation['camera_samples']],
                'invalidated_wire_routes': revision['wire_routes_invalidated']}
    for key, value in required.items():
        if status.get(key) != value:
            errors.append(f'Status disagrees with current evidence: {key}')
    if revision['nodes'] != len(model) or full_step['expected_model_nodes'] != len(model):
        errors.append('Current node counts disagree')
    if validation['errors'] or full_step['missing_model_nodes']:
        errors.append('Unresolved CAD validation/export error')
    if {x['name'] for x in model}.intersection(revision['removed_names']):
        errors.append('Removed node still present')
    wires = {x['name']: x for x in read_json('data/procurement-review/wires.json')}
    for n in revision['wire_routes_invalidated']:
        if wires[n].get('geometry_valid') is not False or wires[n].get('points'):
            errors.append(f'Stale wire geometry: {n}')
    if status['archive_id'] not in {x['id'] for x in read_json('archives/manifest.json')['archives']}:
        errors.append('Current archive not registered')
    purchases = read_json('data/purchases/source-rows.json')
    for key, count in [('first_purchase', 29), ('second_purchase', 64)]:
        if len(purchases[key]) != count:
            errors.append(f'Unexpected purchase count: {key}')
    for directory, extension, count in [
        ('cad/v13-baseline/part-step', '*.step', 130),
        ('cad/v13-baseline/dxf', '*.dxf', 54),
        ('cad/ser0063-review/part-step', '*.step', 17),
        ('cad/ser0063-review/dxf-review-only', '*.dxf', 7),
        ('cad/procurement-review/part-step', '*.step', fabrication['part_steps']),
        ('cad/procurement-review/purchased-step', '*.step', len(revision['part_exports'])),
        ('cad/procurement-review/dxf-review-only', '*.dxf', fabrication['flat_dxfs']),
    ]:
        actual = len(list((ROOT / directory).glob(extension)))
        if actual != count:
            errors.append(f'Unexpected file count: {directory}: {actual} vs {count}')
    if read_json(CATALOG)['files'] != entries:
        errors.append('File catalog differs: review changes, then run --write-catalog')
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'PASS: {len(files) + 1} files; local links, scope, counts and SHA-256 catalog verified.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write-catalog', action='store_true', help='Regenerate catalog after intentional changes')
    args = p.parse_args()
    try:
        check(args.write_catalog)
    except (OSError, ValueError, KeyError) as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)
