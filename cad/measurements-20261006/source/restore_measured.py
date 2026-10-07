"""Restore byte-verified editable measured CAD from baseline ZIP and delta ZIP."""
from pathlib import Path,PurePosixPath
import argparse,zipfile,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--delta',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists() and any(a.output.iterdir()):raise SystemExit('Output must be empty')
assert hashlib.file_digest(a.baseline.open('rb'),'sha256').hexdigest()=='12390393ead32219a6b898b747dd1469170536a5e1e0bfa7ac7cbfdf60cd4690'
with zipfile.ZipFile(a.delta) as dz:
 expected=json.loads(dz.read('DATA/EDITABLE_SHA256.json'))
 with zipfile.ZipFile(a.baseline) as bz:
  for n in bz.namelist():
   rel=n.split('/',1)[-1]
   if rel in expected and rel not in dz.namelist():
    dest=a.output/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(bz.read(n))
 for n in dz.namelist():
  r=PurePosixPath(n)
  if r.is_absolute() or '..' in r.parts:raise ValueError('Unsafe archive path')
  if not n.endswith('/'):
   dest=a.output/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(dz.read(n))
for n,digest in expected.items():
 assert hashlib.file_digest((a.output/n).open('rb'),'sha256').hexdigest()==digest,n
print('PASS: restored',len(expected),'editable files; SHA-256 all match')
