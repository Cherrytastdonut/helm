#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json,hashlib,subprocess
import cadquery as cq,numpy as np
from PIL import Image,ImageDraw,ImageFont
ap=argparse.ArgumentParser()
for n in ['output','legacy-work','legacy-mesh','legacy-manifest','servo-report']:ap.add_argument('--'+n,type=Path,required=True)
a=ap.parse_args();out=a.output.resolve();sys.path.insert(0,str(out/'EDITABLE/HELM_WORK'));import core as c;c.load();meta={p['name']:p for p in c.P};rev=json.loads((out/'DATA/REVISION.json').read_text());servo=json.loads(a.servo_report.read_text());sys.path.insert(0,str(a.legacy_work.resolve()));import render_fast as rf;rf.W=a.legacy_work.resolve()
if not (rf.W/'raster.so').exists():
 (rf.W/'raster.cpp').write_text(rf.CPP);subprocess.run(['g++','-O3','-shared','-fPIC',str(rf.W/'raster.cpp'),'-o',str(rf.W/'raster.so')],check=True)
old=json.loads(a.legacy_manifest.read_text());mesh=np.load(a.legacy_mesh);changed=set(servo['changed'])|set(rev['changed_geometry']);ids=[i for i,p in enumerate(old) if p['name'] in meta and p['name'] not in changed];mask=np.isin(mesh['part_ids'],ids);tri=[mesh['tri'][mask]];colors=[mesh['colors'][mask]];names=[old[i]['name'] for i in mesh['part_ids'][mask]];fresh=set(meta)-{old[i]['name'] for i in ids};failed=[]
for n in sorted(fresh):
 v,f=c.S[n].tessellate(.35,.3)
 if not f:failed.append(n);continue
 t=np.array([x.toTuple() for x in v],dtype=np.float32)[np.array(f)];tri.append(t);colors.append(np.tile(meta[n]['color'],(len(t),1)));names.extend([n]*len(t))
tri=np.concatenate(tri);colors=np.concatenate(colors);names=np.array(names)
def render(n,nodes,view,subtitle):
 mask=np.ones(len(tri),bool) if nodes is None else np.isin(names,nodes);p=out/'PREVIEWS'/f'{n}.png';rf.render(tri[mask],colors[mask],p,view,subtitle);im=Image.open(p);d=ImageDraw.Draw(im);d.rectangle((0,0,1400,65),fill=(248,248,248));d.text((45,25),'HELM | PURCHASE INTEGRATION REVIEW',fill='#173046',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28));im.save(p);print('Rendered',n,flush=True)
render('FULL_REVIEW',None,(1,-1,.8),'2026-10-01 | Updated purchased parts | Manufacturing holds remain')
render('SSD_2280',[n for n in meta if n.startswith('PURCHASE_C715') or n in ['OFFICIAL_JETSON_0564_Solid','OFFICIAL_JETSON_0705_Solid']],(1,-1,-.6),'C715 512GB | Nominal 2280 card interface | Check actual retention screw')
render('POWER_DISTRIBUTION',[n for n in meta if n.startswith(('PURCHASE_SZH','CUSTOM_POWER_BACKPLANE','APPROX_BACKPLANE_L','DRAWING_BASED_FHAC_BODY','CUSTOM_FUSE_SHELF'))],(1,1,.7),'CP003 100 x 45 x 33 mm clearance outline | Fixing holes/terminals pending')
render('THERMAL_VERIFIED',[n for n in meta if n.startswith('OFFICIAL_THERMAL_')],(1,-1,.5),'SEENGREAT 220565 | 215 nodes checked against manufacturer STEP')
(out/'DATA/PREVIEW_PROVENANCE.json').write_text(json.dumps({'total_triangles':len(tri),'tessellated_names':sorted(fresh),'failures':failed,'unchanged_mesh_sha256':hashlib.sha256(a.legacy_mesh.read_bytes()).hexdigest(),'unchanged_mesh_policy':'Original nodes excluding all servo/purchase changes; changed geometry retessellated'},indent=2)+'\n')
