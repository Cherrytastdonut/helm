"""Rebuild measured review from immutable PROCUREMENT_REVIEW_20261001.
Outer dimensions are evidenced; unmeasured joints are not manufactured geometry.
"""
from pathlib import Path
import json,shutil,sys,argparse,hashlib
import cadquery as cq
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--baseline',type=Path,required=True);a=ap.parse_args()
out=Path(__file__).resolve().parents[1];base=a.baseline.resolve();w=out/'EDITABLE/HELM_WORK'
if w.exists():raise SystemExit('Refusing to reapply revision; use immutable input and fresh output')
shutil.copytree(base/'EDITABLE/HELM_WORK',w);sys.path.insert(0,str(w));import core as c
for f,t in [('manifest',c.P),('plates',c.PL),('ports',c.PORT),('wires',c.NET),('joints',c.JOINT)]:
 d=json.loads((w/(f+'.json')).read_text());t.update(d) if isinstance(t,dict) else t.extend(d)
meta={p['name']:p for p in c.P};changed=[];removed=[];holds=[]
def get(n):
 if n not in c.S:c.S[n]=cq.Shape.importBrep(str(w/meta[n]['brep']))
 return c.S[n]
def put(n,s,note,status):
 assert s.isValid(),n;p=meta[n];c.S[n]=s;s.exportBrep(str(w/p['brep']));p.update(bbox=c.bounds(s),valid=True,solids=len(s.Solids()),faces=len(s.Faces()),note=note,status=status,source='EVIDENCE/source-measurements.xlsx / DATA/measurement-register.json');changed.append(n)
def remove(n,reason):
 p=meta[n];removed.append({**p,'removal_reason':reason});c.P.remove(p);c.S.pop(n,None);(w/p['brep']).unlink(missing_ok=True)
for p in list(c.P):
 if p['name'].startswith('OFFICIAL_ADS1115_ADDED_'):remove(p['name'],'Unpurchased ADS1115 body remaining after prior support deletion')
for n,no in [('PURCHASE_SZH_CP003_OUTLINE',1),('DRAWING_BASED_ES7_12_BATTERY',2),('PHOTO_BASED_ES7_12_LID',2),('USER_SER0063_PAN',3),('USER_SER0063_TILT',3),('PHOTO_BASED_BOOST_190W',8),('PHOTO_BASED_SZH_JA020_BASE',9),('PHOTO_BASED_FUSEBLOCK_COVER',9)]:
 meta[n].update(measurement_number=no,measurement_evidence='Outer dimensions agree; original geometry preserved. Rounded measurements do not rescale supplied motor CAD.')
shifts={'APPROX_MEDIUM_L_2':12,'APPROX_MEDIUM_L_3':-24,'APPROX_SMALL_L_0_245_LEFT':-3,'APPROX_SMALL_L_1_23_RIGHT':3}
for p in list(c.P):
 n=p['name']
 if not n.startswith(('APPROX_MEDIUM_L_','APPROX_SMALL_L_','APPROX_BACKPLANE_L_','APPROX_CAM_L_')) or p['group']=='08_FASTENERS':continue
 b=p['bbox'];s=get(n);medium=n.startswith('APPROX_MEDIUM');width,leg,t=(30,25,2) if medium else (20,24,1.5);dx,dy,dz=[b[i+3]-b[i] for i in range(3)]
 y0=s.intersect(c.box(b[0]-.1,b[1]+.01,b[2]-.1,dx+.2,.3,dz+.2)).Volume();y1=s.intersect(c.box(b[0]-.1,b[4]-.31,b[2]-.1,dx+.2,.3,dz+.2)).Volume()
 z0=s.intersect(c.box(b[0]-.1,b[1]-.1,b[2]+.01,dx+.2,dy+.2,.3)).Volume();z1=s.intersect(c.box(b[0]-.1,b[1]-.1,b[5]-.31,dx+.2,dy+.2,.3)).Volume()
 yl=y0>=y1;zl=z0>=z1;x=(b[0]+b[3]-width)/2+shifts.get(n,0);y=b[1] if yl else b[4]-leg;z=b[2] if zl else b[5]-leg
 shape=c.box(x,y,z if zl else z+leg-t,width,leg,t).fuse(c.box(x,y if yl else y+leg-t,z,width,t,leg)).clean()
 put(n,shape,f'Outer {width}x{leg}x{leg} mm. Thickness {t} PROVISIONAL; holes/ribs not inferred. '+('Measured medium.' if medium else 'User-transcribed catalog size; small stock unconfirmed.')+f' X placement adjustment {shifts.get(n,0)} mm; actual fixed holes transfer onsite.','MEASURED_L_OUTER_NO_HOLES' if medium else 'CATALOG_L_OUTER_STOCK_UNCONFIRMED')
 p['measurement_number']=7 if medium else 6;holds.append({'node':n,'old_bbox':b,'new_bbox':c.bounds(shape),'thickness_assumed_mm':t,'reason':'Outer-only profile; actual holes/ribs/fasteners and stock still required'})
for p in list(c.P):
 n=p['name']
 if n.startswith(('MEDIUM_','BP_FLOOR','BP_WALL','CAM_L_')) or (n.startswith('APPROX_SMALL_L_') and p['group']=='08_FASTENERS'):remove(n,'Old bracket hole-pitch hardware suppressed; joint NOT completed or certified')
CY=c.CY
for indexes,dst in [(range(5),[228,CY-22.5,343.38,272,CY+22.5,361.38]),(range(5,7),[265,CY-47.5,361.38,285,CY+47.5,389.38])]:
 names=[f'COMMUNITY_C920_{i}' for i in indexes];bs=np.array([meta[n]['bbox'] for n in names]);lo=bs[:,:3].min(0);hi=bs[:,3:].max(0);k=(np.array(dst[3:])-dst[:3])/(hi-lo);o=np.array(dst[:3])-k*lo
 mat=cq.Matrix([[k[0],0,0,o[0]],[0,k[1],0,o[1]],[0,0,k[2],o[2]],[0,0,0,1]])
 for n in names:put(n,get(n).transformGeometry(mat),'Measurement14: body95W x20D x28H; stand45W x44D x18H; folded depth57. Hinge registration inferred. Internal reference surfaces are not manufacturing geometry.','MEASURED_APPROX_C920')
put('CUSTOM_C920_PAD',c.box(228,CY-22.5,339.38,44,45,4),'Measured clip footprint44x45. Compressed EVA4mm is a field target, not measured stock thickness.','FIELD_FIT_EVA')
for n in ['CUSTOM_C920_STRAP_0','CUSTOM_C920_STRAP_1']:remove(n,'Strap route invalid after measured camera update; fit actual owned strap onsite')
pl=next(p for p in c.PL if p['name']=='CUSTOM_LEFT_PANEL')
def makewall(drills):
 s=c.box(0,0,0,pl['width'],pl['height'],pl['thickness'])
 for x,y,d in pl['holes']:s=s.cut(c.cyl(x,y,-.1,d/2,5.2))
 for x,y,l,d,angle in pl['slots']:s=s.cut(cq.Workplane('XY').center(x,y).slot2D(l,d,angle).extrude(5.2).val().translate((0,0,-.1)))
 for x,y,dx,dy in pl['cuts']:s=s.cut(c.box(x,y,-.1,dx,dy,5.2))
 s=c.transform(s,pl['origin'],pl['u'],pl['normal'])
 for d in drills:s=s.cut(c.cyl(*(np.array(d['point'])-np.array(d['axis'])*60),d['d']/2,120,d['axis']))
 return s
reliefs=makewall(pl['world_drill']).cut(get('CUSTOM_LEFT_PANEL'));newdr=[d for d in pl['world_drill'] if not(d['d']==20.4 and abs(d['point'][0]-265)<.01)]
newdr.append({'point':[200,-12,239.3898922198363],'d':20,'axis':[0,1,0],'status':'COUPON_FIRST_NOT_RELEASED'})
wall=makewall(newdr)
for relief in reliefs.Solids():wall=wall.cut(relief,tol=1e-5)
# OCC coplanar cleanup invalidates wires here; preserve valid split faces.
put('CUSTOM_LEFT_PANEL',wall.fix(),'5T Fomex; rocker centre X200/Z239.389892; initial coupon Ø20. Existing reliefs retained. Bracket holes are old reference only, not a drilling release.','CUSTOM_REVIEW_ONLY');pl['world_drill']=newdr;pl['note']='Rocker revised; coupon first. Transfer actual bracket holes onsite; old pattern NOT RELEASED.'
z=239.3898922198363;rocker=c.cyl(200,-19,z,13.5,4,(0,1,0)).fuse(c.cyl(200,-15,z,10,20,(0,1,0))).fuse(c.box(193,5,z-2.4,14,10.2,4.8)).clean()
put('PHOTO_BASED_MAIN_ROCKER',rocker,'Measurement12: bezelØ27, bodyØ20, total34.2. Axial subdivisions4+20+10.2 and terminal block are clearance assumptions, not pin CAD. X200/Z239.389892. 5T coupon required.','MEASURED_ROCKER_CLEARANCE')
invalid=[]
for n,p in c.PORT.items():
 if n.startswith('ROCKER') or p.get('owner')=='PHOTO_BASED_MAIN_ROCKER':p.update(xyz=None,status='ACTUAL_TERMINAL_POSITION_PENDING')
for wire in c.NET:
 if any(str(wire.get(k,'')).startswith('ROCKER') for k in ['from_port','to_port']):
  wire.update(points=[],geometry_valid=False,length_mm=None,endpoint_error_mm=None,status='NOT_RELEASED_MEASURED_ROCKER_MOVE',route_status='NOT_RELEASED_MEASURED_ROCKER_MOVE');invalid.append(wire['name']);n='CUSTOM_CABLE_'+wire['name']
  if any(p['name']==n for p in c.P):remove(n,'Rocker moved; actual terminals and route pending')
c.save()
for folder in ['DATA','PART_STEP','OPTIONAL_INVENTORY_STEP','CAD','PREVIEWS','DOCS','DRAWINGS']:(out/folder).mkdir(exist_ok=True)
roundtrips=[]
for n in changed:
 s=get(n);dest=out/'PART_STEP'/f'{n}.step';cq.exporters.export(s,str(dest));r=cq.importers.importStep(str(dest)).val();err=max(abs(x-y) for x,y in zip(c.bounds(s),c.bounds(r)));assert r.isValid() and err<.002,(n,err)
 roundtrips.append({'name':n,'valid':True,'bbox_error_mm':err,'volume_difference_mm3':abs(s.Volume()-r.Volume())})
inventory=[]
for n,d,pid in [('BUSBAR_OUTER_ONLY',[165,15,18],'P1-018'),('MG995_U_FRAME_OUTER_ONLY',[64,55,25],'P2-R78'),('MG995_OTHER_FRAME_OUTER_ONLY',[58,37,25],'P2-R78')]:
 cq.exporters.export(c.box(0,0,0,*d),str(out/'OPTIONAL_INVENTORY_STEP'/f'{n}.step'));inventory.append({'name':n,'dimensions_mm':d,'purchase_id':pid,'installed':False,'representation':'Bounding solid only; inner geometry, thickness and holes unknown'})
def dump(n,d):(out/'DATA'/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for f in ['manifest','plates','ports','wires','joints']:shutil.copyfile(w/(f+'.json'),out/'DATA'/(f+'.json'))
dump('REVISION.json',dict(revision='MEASURED_LAYOUT_20261006',manufacturing_release=False,release_status='NOT_FOR_FABRICATION',baseline='PROCUREMENT_REVIEW_20261001',baseline_nodes=len(meta),nodes=len(c.P),changed_geometry=changed,part_exports=changed,removed_names=[p['name'] for p in removed],removed_count=len(removed),wire_routes_invalidated=invalid,interface_holds=holds,rocker_centre_world_mm=[200,-15,z],part_roundtrips=roundtrips,measurement_source_sha256=hashlib.file_digest((out/'EVIDENCE/source-measurements.xlsx').open('rb'),'sha256').hexdigest()))
dump('REMOVED_NODES.json',removed);dump('OPTIONAL_INVENTORY.json',inventory)
for n in ['export_snapshot.py','NOTICES.md']:shutil.copyfile(base/'SOURCE'/n,out/'SOURCE'/n)
shutil.copyfile(base/'LICENSE',out/'LICENSE')
print('CAD',len(c.P),'nodes;',len(changed),'changed;',len(removed),'suppressed',flush=True)
