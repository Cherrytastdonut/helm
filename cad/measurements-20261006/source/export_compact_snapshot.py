#!/usr/bin/env python3
"""Re-export a current BREP snapshot without applying any historical revision."""
from pathlib import Path
import argparse,importlib.util,json
import cadquery as cq
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--step',type=Path,required=True);p.add_argument('--check-only',action='store_true');a=p.parse_args();w=a.work.resolve();dest=a.step.resolve()
if dest.exists() and not a.check_only:p.error('Choose a new STEP output path; existing files are not overwritten')
spec=importlib.util.spec_from_file_location('helm_snapshot_core',w/'core.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);c.load();names=[x['name'] for x in c.P];assert len(names)==len(set(names))==len(c.S)
for m in c.P:assert max(abs(x-y) for x,y in zip(c.bounds(c.S[m['name']]),m['bbox']))<.002,m['name']
print('Loaded and checked',len(names),'BREP shapes',flush=True)
if not a.check_only:
 revision=json.loads((w.parent.parent/'DATA/REVISION.json').read_text())['revision'];assy=cq.Assembly(name=revision);groups={}
 for m in c.P:
  g=m['group'];groups.setdefault(g,cq.Assembly(name=g));groups[g].add(c.S[m['name']],name=m['name'],color=cq.Color(*[q/255 for q in m['color']]))
 for g,group in sorted(groups.items()):assy.add(group)
 dest.parent.mkdir(parents=True,exist_ok=True);assy.save(str(dest),exportType='STEP',mode='default',write_pcurves=False);print('Exported',dest,flush=True)
