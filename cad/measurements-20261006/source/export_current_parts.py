#!/usr/bin/env python3
"""Export all installed fabrication candidates; never flatten unverified depth features."""
from pathlib import Path
import argparse,sys,json
import cadquery as cq
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();sys.path.insert(0,str(out/'EDITABLE/HELM_WORK'));import core as c;c.load();defs={p['name']:p for p in c.PL};rows=[]
for folder in ['FABRICATION_STEP','DXF_REVIEW_ONLY']:(out/folder).mkdir(exist_ok=True)
for p in c.P:
 if not p['fabricate']:continue
 n=p['name'];s=c.S[n];dest=out/'FABRICATION_STEP'/f'{n}.step';cq.exporters.export(s,str(dest));check=cq.importers.importStep(str(dest)).val();err=max(abs(x-y) for x,y in zip(c.bounds(s),c.bounds(check)));ve=abs(s.Volume()-check.Volume());rel=ve/max(abs(s.Volume()),1);assert check.isValid() and err<.002 and rel<1e-4,(n,err,ve,rel)
 row={'part':n,'step':'FABRICATION_STEP/'+dest.name,'bbox':c.bounds(s),'status':'REVIEW_ONLY','roundtrip_bbox_error_mm':err,'roundtrip_volume_error_mm3':ve,'roundtrip_relative_volume_error':rel,'note':p['note'],'dxf':None,'dxf_reason':'No verified constant-thickness plate definition; preserve depth/material detail in STEP'}
 if n in defs:
  d=defs[n];local=s.moved(cq.Location(cq.Plane(origin=d['origin'],xDir=d['u'],normal=d['normal'])).inverse);bb=local.BoundingBox();fs=[f for f in local.Faces() if f.geomType()=='PLANE' and abs(f.normalAt().z)>.999];row['plate_definition']=d
  if fs:
   face=max(fs,key=lambda f:f.Area());delta=abs(face.Area()*bb.zlen-local.Volume());row['extrusion_volume_error_mm3']=delta
   if len(s.Solids())==1 and delta<max(.01,abs(s.Volume())*1e-5):
    face=face.translate((-bb.xmin,-bb.ymin,-face.Center().z));path=out/'DXF_REVIEW_ONLY'/f'{n}.dxf';cq.exporters.exportDXF(face,str(path),approx='arc',tolerance=.01);row.update(dxf='DXF_REVIEW_ONLY/'+path.name,dxf_reason='Constant-thickness through profile verified by face area/solid volume; no kerf compensation; NOT fabrication released',local_bounds_mm=[bb.xlen,bb.ylen,bb.zlen])
   else:row['dxf_reason']='Depth features, multiple solids or non-through profile; no cutting DXF exported'
 rows.append(row)
 if len(rows)%20==0:print('Parts',len(rows),flush=True)
(out/'DATA/FABRICATION_INDEX.json').write_text(json.dumps({'revision':'MEASURED_LAYOUT_20261006','manufacturing_release':False,'roundtrip_criteria':{'bbox_mm':.002,'relative_volume':1e-4,'explanation':'Curved/healed geometry integration may vary slightly after STEP conversion; valid shape and bounds plus relative volume checked, all measured errors retained.'},'part_steps':len(rows),'flat_dxfs':sum(bool(x['dxf']) for x in rows),'parts':rows},ensure_ascii=False,indent=2)+'\n');print('Exported',len(rows),'STEP and',sum(bool(x['dxf']) for x in rows),'DXFs',flush=True)
