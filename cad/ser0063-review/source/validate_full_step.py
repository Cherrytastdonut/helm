from pathlib import Path
import cadquery as cq,json,hashlib,time
from OCP.STEPControl import STEPControl_Reader
from OCP.StepBasic import StepBasic_ProductDefinition
from OCP.IFSelect import IFSelect_RetDone
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output/HELM_SER0063_INTEGRATION_REVIEW';path=OUT/'CAD/HELM_SER0063_FULL_REVIEW.step'
meta={p['name']:p for p in json.loads((OUT/'DATA/manifest.json').read_text())}
want={'USER_SER0063_PAN','USER_SER0063_TILT','CUSTOM_PAN_SERVO_MOUNT','CUSTOM_TILT_SERVO_MOUNT'}
r=STEPControl_Reader();start=time.monotonic();assert r.ReadFile(str(path))==IFSelect_RetDone
print('STEP parsed',flush=True)
model=r.StepModel();found={};products=[]
for i in range(1,model.NbEntities()+1):
    e=model.Value(i)
    if isinstance(e,StepBasic_ProductDefinition):
        n=e.Formation().OfProduct().Name().ToCString();products.append(n)
        if n in want:found[n]=i
assert set(found)==want,found
checks=[]
for n,i in found.items():
    assert r.TransferOne(i),n
    s=cq.Shape.cast(r.Shape(r.NbShapes()));b=s.BoundingBox();bb=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax]
    err=max(abs(a-b) for a,b in zip(bb,meta[n]['bbox']))
    assert s.isValid() and err<.001,n
    checks.append({'name':n,'valid':True,'solids':len(s.Solids()),'bbox_error_mm':err,'volume_mm3':s.Volume()})
    print('Readback',n,flush=True)
missing=set(meta)-set(products)
assert not missing,sorted(missing)
assert not any('MG90S' in n for n in products)
result={'scope':'Full STEP syntax/entity parse and all node names; roundtrip geometry transfer limited to the two new servos and two adapter plates. Not full-assembly shape or motion certification.',
        'bytes':path.stat().st_size,'sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest(),
        'entities':model.NbEntities(),'product_definitions':len(products),'expected_model_nodes':len(meta),
        'missing_model_nodes':sorted(missing),'replacement_roundtrips':checks,'seconds':time.monotonic()-start}
(OUT/'DATA/FULL_STEP_READBACK.json').write_text(json.dumps(result,indent=2))
print('Full STEP readback complete',flush=True)
