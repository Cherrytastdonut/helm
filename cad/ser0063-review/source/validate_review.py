from pathlib import Path
import json,sys,hashlib,collections
import numpy as np
import cadquery as cq
ROOT=Path(__file__).resolve().parent
W=ROOT/'work/HELM_V13_WORK';sys.path.insert(0,str(W))
import core as c
OUT=ROOT/'output/HELM_SER0063_INTEGRATION_REVIEW';D=OUT/'DATA'
r=json.loads((D/'REVISION_AND_VALIDATION.json').read_text())
c.load();meta={p['name']:p for p in c.P};changed=set(r['changed'])
base={p['name']:p for p in json.loads((D/'BASELINE_MANIFEST.json').read_text())}
print('Loaded',len(meta),flush=True)
# Repair metadata to match the moved BREP, and invalidate all stale routing
# results. A logical servo endpoint is not a measured lead-exit position.
for pl in c.PL:
    if pl['name'] in changed and pl['name'] in base and base[pl['name']]['moving'] in ('PAN','TILT'):
        if not pl.get('ser0063_world_drill_shifted'):
            for drill in pl.get('world_drill',[]):
                if drill['point'][2] in (356.38,392.38):continue
                drill['point'][2]+=24.38
            pl['ser0063_world_drill_shifted']=True
for role in ('PAN','TILT'):
    c.PORT['SER0063_'+role+'_CABLE']={'xyz':None,'owner':'USER_SER0063_'+role,'connector':'Servo 3-wire, verify supplied pinout','status':'UNMEASURED_LEAD_EXIT','direction':None}
for net in c.NET:
    if net['name'] not in ('PAN_PWM_POWER','TILT_PWM_POWER','C920_USB'):continue
    net.update(status='NOT_RELEASED_SER0063_REPLACEMENT',geometry_valid=False,endpoint_error_mm=None,reserve_mm=None,min_bend_radius_mm=None)
    net.pop('motion_point_groups',None)
    if net['name']!='C920_USB':
        role=net['name'].split('_')[0];net['to_port']='SER0063_'+role+'_CABLE'
        net['to_status']='UNMEASURED_LEAD_EXIT'
        net['stock_length_mm']=None
        net['signal']='SER0063 power 5-8.4 V per manufacturer; shared ground; PWM pinout and supply current unverified'
    else:
        net['from_status']='RELOCATED_REFERENCE';net['note']='C920 flexible USB route removed after camera frame elevation; reroute with pan/tilt motion and strain relief.'
c.save()
for joint in c.JOINT:
    if joint.get('name','').startswith('CAMERA_'):
        if 'limits' in joint:joint['requested_limits_deg']=joint.pop('limits')
        joint['approved_limits_deg']=None
        joint['status']='UNRELEASED: horn fit, existing camera hardware contacts, cable routing and loads unresolved; sampled angles are not approved limits'
c.save()
for name,data in [('manifest',c.P),('plates',c.PL),('ports',c.PORT),('wires',c.NET),('joints',c.JOINT)]:
    (D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2))

def broad(a,b):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-6 for i in range(3))
def volume(a,b):
    try:return float(a.intersect(b).Volume())
    except Exception as e:return {'error':str(e)}

# New hardware against every rigid node. Existing contacts between unchanged
# baseline components are not recertified by this local review.
new=[p for p in c.P if p['name'].startswith(('SER0063_','USER_SER0063_'))]
pairs=set()
for p in new:
    for q in c.P:
        if p['name']==q['name'] or q['group']=='09_WIRING':continue
        if broad(p['bbox'],q['bbox']):pairs.add(tuple(sorted((p['name'],q['name']))))
hits=[]
for a,b in sorted(pairs):
    v=volume(c.S[a],c.S[b])
    if isinstance(v,dict) or v>.5:hits.append({'a':a,'b':b,'volume_mm3':v})
print('Hardware pairs',len(pairs),'hits',hits,flush=True)

# Sample motion, with the reserved (unmeasured) horn joint axes. The test is
# deliberately discrete and excludes flexible wires, missing horns and loads.
moving=[p for p in c.P if p['moving'] in ('PAN','TILT') and p['group']!='09_WIRING']
fixed=[p for p in c.P if p['moving'] not in ('PAN','TILT') and p['group']!='09_WIRING']
pan=tuple(r['pan_joint']);tilt=tuple(r['tilt_joint'])
motion=[]
for pa,ta in [(-45,-20),(-45,0),(-45,20),(0,-20),(0,0),(0,20),(45,-20),(45,0),(45,20)]:
    shapes={};bounds={}
    for p in moving:
        s=c.S[p['name']]
        if p['moving']=='TILT' and ta:s=s.rotate(tilt,(tilt[0],tilt[1]+1,tilt[2]),ta)
        if pa:s=s.rotate(pan,(pan[0],pan[1],pan[2]+1),pa)
        shapes[p['name']]=s;bounds[p['name']]=c.bounds(s)
    candidates=[]
    for p in moving:
        for q in fixed:
            if broad(bounds[p['name']],q['bbox']):candidates.append((p['name'],q['name']))
    # Internal relative tilt motion: PAN and TILT groups only.
    for p in moving:
        if p['moving']!='TILT':continue
        for q in moving:
            if q['moving']=='PAN' and broad(bounds[p['name']],bounds[q['name']]):candidates.append((p['name'],q['name']))
    mh=[]
    for a,b in candidates:
        v=volume(shapes[a],shapes[b] if b in shapes else c.S[b])
        if isinstance(v,dict) or v>.5:mh.append({'a':a,'b':b,'volume_mm3':v})
    motion.append({'pan_deg':pa,'tilt_deg':ta,'pairs':len(candidates),'hits':mh})
    print('Motion',pa,ta,'pairs',len(candidates),'hits',len(mh),flush=True)

# Reimport every exported fabrication part, plus the camera STEP as a whole.
roundtrip=[]
for file in sorted((OUT/'PART_STEP').glob('*.step')):
    s=cq.importers.importStep(str(file)).val();src=c.S[file.stem]
    e=max(abs(a-b) for a,b in zip(c.bounds(s),c.bounds(src)))
    ve=abs(s.Volume()-src.Volume())
    assert s.isValid() and e<.001 and ve<.01,(file,e,ve)
    roundtrip.append({'part':file.stem,'valid':True,'bbox_max_error_mm':e,'volume_error_mm3':ve})
camera=cq.importers.importStep(str(OUT/'CAD/HELM_SER0063_CAMERA_REVIEW.step')).val()
camera_check={'valid':camera.isValid(),'solids':len(camera.Solids()),'bounds':c.bounds(camera)}
assert camera_check['valid']
vreport={'scope':'New servo bodies and new hardware versus rigid model; nine discrete camera poses; 17 exported part roundtrips and camera STEP roundtrip. No continuous sweep, strength, horn fit or flexible routing validation.',
         'intersection_threshold_mm3':.5,'new_hardware_pairs':len(pairs),'new_hardware_hits':hits,
         'motion_samples':motion,'part_step_roundtrips':roundtrip,'camera_step_roundtrip':camera_check}
(D/'EXTENDED_VALIDATION.json').write_text(json.dumps(vreport,indent=2))
print('Validation done',flush=True)

# Use old mesh only for unchanged nodes; all revised nodes are tessellated from
# the actual revised BREP. Preserve identities rather than relying on new IDs.
import render_fast as rf
from PIL import Image,ImageDraw,ImageFont
old_list=json.loads((D/'BASELINE_MANIFEST.json').read_text())
mesh=np.load(ROOT/'work/HELM_V13_DRAWINGS/DATA/mesh.npz')
old_ids=[i for i,p in enumerate(old_list) if p['name'] in meta and p['name'] not in changed]
mask=np.isin(mesh['part_ids'],old_ids)
tri=[mesh['tri'][mask]];colors=[mesh['colors'][mask]]
new_tri=[];new_color=[];fail=[]
for n in sorted(changed):
    if n not in c.S:continue
    v,f=c.S[n].tessellate(.35,.3)
    if not f:fail.append(n);continue
    a=np.array([v.toTuple() for v in v],dtype=np.float32)[np.array(f)]
    co=np.tile(meta[n]['color'],(len(a),1))
    tri.append(a);colors.append(co)
    if n!='CUSTOM_ELECTRONICS_PLATE':new_tri.append(a);new_color.append(co)
fulltri=np.concatenate(tri);fullco=np.concatenate(colors)
ctri=np.concatenate(new_tri);cco=np.concatenate(new_color)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
for name,tr,co,view in [('FULL_REVIEW',fulltri,fullco,(1,-1,.8)),('CAMERA_ISO',ctri,cco,(1,1,.65)),('CAMERA_FRONT',ctri,cco,(1,0,0)),('CAMERA_SIDE',ctri,cco,(0,1,0))]:
    path=OUT/'PREVIEWS'/(name+'.png')
    rf.render(tr,co,path,view,'Exact supplied SER0063 geometry | Horns and cable routes unresolved | NOT FOR FABRICATION')
    im=Image.open(path);draw=ImageDraw.Draw(im);draw.rectangle((0,0,1400,65),fill=(248,248,248))
    draw.text((45,25),'HELM | SER0063 INTEGRATION REVIEW',fill='#173046',font=font);im.save(path)
    print('Rendered',name,flush=True)
(D/'PREVIEW_PROVENANCE.json').write_text(json.dumps({'new_triangle_count':len(ctri),'full_triangle_count':len(fulltri),'tessellation_failures':fail,'unchanged_mesh_source':'HELM V13 baseline; changed node mesh regenerated'},indent=2))
