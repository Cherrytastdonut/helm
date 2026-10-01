#!/usr/bin/env python3
from pathlib import Path
import cadquery as cq,json,hashlib,time,argparse
from OCP.STEPControl import STEPControl_Reader
from OCP.StepBasic import StepBasic_ProductDefinition
from OCP.IFSelect import IFSelect_RetDone
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--step',type=Path);a=ap.parse_args();out=a.output.resolve();path=a.step or out/'CAD/HELM_PROCUREMENT_FULL_REVIEW.step';meta={p['name']:p for p in json.loads((out/'DATA/manifest.json').read_text())};want=set(json.loads((out/'DATA/REVISION.json').read_text())['changed_geometry']);r=STEPControl_Reader();start=time.monotonic();assert r.ReadFile(str(path))==IFSelect_RetDone;print('STEP parsed',flush=True);model=r.StepModel();found={};products=[]
for i in range(1,model.NbEntities()+1):
 e=model.Value(i)
 if isinstance(e,StepBasic_ProductDefinition):
  n=e.Formation().OfProduct().Name().ToCString();products.append(n)
  if n in want:found[n]=i
assert set(found)==want;checks=[]
for n,i in found.items():
 assert r.TransferOne(i);s=cq.Shape.cast(r.Shape(r.NbShapes()));b=s.BoundingBox();bb=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax];err=max(abs(x-y) for x,y in zip(bb,meta[n]['bbox']));assert s.isValid() and err<.001,n;checks.append({'name':n,'valid':True,'solids':len(s.Solids()),'bbox_error_mm':err,'volume_mm3':s.Volume()});print('Readback',n,flush=True)
missing=set(meta)-set(products);assert not missing;assert not any(n.startswith(('DRAWING_BASED_SN530','PHOTO_BASED_SN530','APPROX_BUS_POS','APPROX_BUS_NEG','CUSTOM_ADC_','ADC_CARRIER_','ADC_M2_')) for n in products)
with path.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
(out/'DATA/FULL_STEP_READBACK.json').write_text(json.dumps({'scope':'Full STEP syntax/entity parse and all model names; shape transfers limited to four changed parts, not full-assembly geometry certification.','bytes':path.stat().st_size,'sha256':digest,'entities':model.NbEntities(),'product_definitions':len(products),'expected_model_nodes':len(meta),'missing_model_nodes':sorted(missing),'replacement_roundtrips':checks,'seconds':time.monotonic()-start},indent=2)+'\n');print('Full STEP check complete',flush=True)
