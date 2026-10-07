#!/usr/bin/env python3
"""Re-export changed and optional reference STEP files from a restored snapshot."""
from pathlib import Path
import argparse,sys,json
import cadquery as cq
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();sys.path.insert(0,str(out/'EDITABLE/HELM_WORK'));import core as c;c.load()
rev=json.loads((out/'DATA/REVISION.json').read_text());dest=out/'PART_STEP';dest.mkdir(exist_ok=True)
for n in rev['part_exports']:
 p=dest/(n+'.step');cq.exporters.export(c.S[n],str(p));s=cq.importers.importStep(str(p)).val();assert s.isValid();assert max(abs(x-y) for x,y in zip(c.bounds(s),c.bounds(c.S[n])))<.002
optional=out/'OPTIONAL_INVENTORY_STEP';optional.mkdir(exist_ok=True)
for r in json.loads((out/'DATA/OPTIONAL_INVENTORY.json').read_text()):
 s=cq.Workplane('XY').box(*r['dimensions_mm'],centered=(False,False,False)).val();cq.exporters.export(s,str(optional/(r['name']+'.step')))
print('Changed STEP',len(rev['part_exports']),'and optional outer-only references exported')
