"""SER0063 mechanical integration review. Not a fabrication release.

Uses the supplied servo STEP unchanged under rigid transforms. Preserves the
baseline outside the camera integration changes. Horns are deliberately absent:
the upload contains only the servo body, so no spline/arm compatibility is faked.
"""
from pathlib import Path
import sys, json, hashlib, copy, time, math
import numpy as np
ROOT=Path(__file__).resolve().parent
W=ROOT/'work/HELM_V13_WORK'
sys.path.insert(0,str(W))
import core as c
from extras import change
from upgrade import remove
import cadquery as cq

OUT=ROOT/'output/HELM_SER0063_INTEGRATION_REVIEW'
OUT.mkdir(parents=True,exist_ok=True)
for d in ('CAD','PART_STEP','DXF_REVIEW_ONLY','DATA','PREVIEWS'):
    (OUT/d).mkdir(exist_ok=True)
CY=c.CY
DZ=24.38
PAN_TIP=(248,CY,320.38)
PAN_AXIS=(248,CY,322.38)
TILT_AXIS=(248,CY,374.38)
TILT_TIP=(248,CY+64,374.38)
source=ROOT/'motor/SER0063.stp'
raw=cq.importers.importStep(str(source)).val()
def pose(s,tip,normal):
    local=s.translate((9.86,-27.63,-10)).rotate((0,0,0),(1,0,0),90)
    return c.transform(local,tip,(1,0,0),normal)
def broad(a,b):
    return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-6 for i in range(3))
def common(a,b):
    try:return float(a.intersect(b).Volume())
    except Exception as ex:return {'error':str(ex)}
def meta(n):return next(p for p in c.P if p['name']==n)
def setmotion(n,group):meta(n)['moving']=group
def mark(n,note):meta(n)['note']+='; '+note
def plate(n,width,height,origin,holes,cuts=(),normal=(0,0,1),moving=''):
    remove([n]); c.plate(n,width,height,origin,holes=holes,cuts=cuts,n=normal,group='07_CAMERA_SYSTEM',moving=moving,note='SER0063 REVIEW ONLY; 5T PVC stock; drill and horn interfaces require physical check')
def stud(n,point,length,axis=(0,0,1),moving=''):
    c.add(n,c.cyl(*point,2,length,axis),'08_FASTENERS','metal','STANDARD_RECONSTRUCTION',moving=moving,note=f'M4 all-thread cut to {length:g} mm from second-order 1 m stock; no helical detail; REVIEW ONLY')
def washer(n,p,axis=(0,0,1),moving=''):
    c.washer(n,p,4,axis);setmotion(n,moving)
def nut(n,p,axis=(0,0,1),moving=''):
    c.nut(n,p,4,axis);setmotion(n,moving)
def lugnut(n,p,axis=(0,0,1),moving=''):
    nut(n,p,axis,moving)
    change(n,c.S[n].rotate(p,tuple(p[i]+axis[i] for i in range(3)),30))
    mark(n,'Flats parallel to servo case; plain nut bearing is a REVIEW proposal, verify supplied mounting hardware')

print('Loading baseline...',flush=True)
c.load()
original=copy.deepcopy(c.P)
original_by={p['name']:p for p in original}
(OUT/'DATA/BASELINE_MANIFEST.json').write_text(json.dumps(original,ensure_ascii=False))
print('Baseline loaded',len(c.P),flush=True)

# Verify why a drop-in swap at the old shaft positions is not valid.
dropin=[]
for role,tip,norm in [('PAN',(248,CY,296),(0,0,1)),('TILT',(248,CY+64,350),(0,-1,0))]:
    sh=pose(raw,tip,norm);bb=c.bounds(sh)
    hits=[]
    for p in c.P:
        if p['group'] in ('08_FASTENERS','09_WIRING') or 'MG90S' in p['name']:continue
        if broad(bb,p['bbox']):
            v=common(sh,c.S[p['name']])
            if isinstance(v,dict) or v>.5:hits.append({'part':p['name'],'volume_mm3':v})
    dropin.append({'role':role,'bounds':bb,'collisions':hits})
print('Drop-in collision counts',[len(x['collisions']) for x in dropin],flush=True)

remove_prefixes=('COMMUNITY_MG90S_','PHOTO_BASED_MG90S_','PAN_SUPPORT_',
                 'PAN_FLANGE_','TILT_FLANGE_','TILT_MOUNT_',
                 'TILT_COUPLER_FIX_','TILT_HORN_LINK_',
                 'STANDARD_PLUG_MG90S_')
remove_exact={'CUSTOM_TILT_HORN_COUPLER','CUSTOM_CABLE_PAN_PWM_POWER',
              'CUSTOM_CABLE_TILT_PWM_POWER','CUSTOM_CABLE_C920_USB'}
removed=[p['name'] for p in c.P if p['name'].startswith(remove_prefixes) or p['name'] in remove_exact]
remove(removed)

# Raise the preserved moving camera cradle. Fastener motion labels are repaired
# only where the parent linkage gives an unambiguous assignment.
shifted=[]
for p in list(c.P):
    n=p['name']
    if p['moving'] in ('PAN','TILT') or n=='TILT_AXIS_LEFT':
        change(n,c.S[n].translate((0,0,DZ)));shifted.append(n)
        if n=='TILT_AXIS_LEFT':p['moving']='PAN'
        for pl in c.PL:
            if pl['name']==n:pl['origin'][2]+=DZ
        mark(n,'Camera frame raised +24.38 mm for supplied SER0063 body; review revision')

# Exact body and flange geometry; no scaling and no invented motor hull.
for role,tip,norm,moving in [('PAN',PAN_TIP,(0,0,1),''),('TILT',TILT_TIP,(0,-1,0),'PAN')]:
    c.add('USER_SER0063_'+role,pose(raw,tip,norm),'07_CAMERA_SYSTEM','blue','USER_SUPPLIED_CAD',moving=moving,source='LIB_SER0063.zip / SER0063/3D/SER0063.stp',note='Exact uploaded STEP, rigid placement only. Shaft axis (-9.86, y, 10) in source. Horn and lead geometry not included.')

# Pan adapter: external 72 x 60 x 5; motor flange pitch 48 x 10 from STEP.
px0=218.;py0=CY-30
support_pan=[(234,CY-19),(274,CY-19),(227,CY+14),(274,CY+19)]
motor_xy=[(248+9.86+x,CY+10-z) for x in (-24,24) for z in (5,15)]
holes=[(x-px0,y-py0,4.5) for x,y in support_pan+motor_xy]
plate('CUSTOM_PAN_SERVO_MOUNT',72,60,(px0,py0,300),holes,
      cuts=[(257.86-20.5-px0,CY-10.75-py0,41,21.5)])
for n in ('CUSTOM_CAMERA_BASE','CUSTOM_ELECTRONICS_PLATE'):
    for x,y in support_pan:c.hole(n,(x,y,260),4.5)
    mark(n,'M4 support holes: (234,CY-19), (274,CY-19), (227,CY+14), (274,CY+19); left rear moved to clear ADC carrier')
for i,(x,y) in enumerate(support_pan):
    pre=f'SER0063_PAN_POST_{i}'
    stud(pre,(x,y,249),64)
    for j,z in enumerate((254.2,265,299.2,305)):washer(pre+f'_W{j}',(x,y,z))
    for j,z in enumerate((251,265.8,296,305.8)):nut(pre+f'_N{j}',(x,y,z))
for i,(x,y) in enumerate(motor_xy):
    pre=f'SER0063_PAN_LUG_{i}'
    stud(pre,(x,y,294),20)
    lugnut(pre+'_N0',(x,y,296.8));lugnut(pre+'_N1',(x,y,307.5))

# Tilt adapter and right cheek: stock rods replace unlisted custom spacers.
ty_inner=CY+79.38;ty_outer=ty_inner+5;tz=TILT_AXIS[2]
tilt_support=[(237,tz-18),(274,tz-18),(224,tz+18),(274,tz+18)]
tilt_lugs=[(248+9.86+x,tz+10-z) for x in (-24,24) for z in (5,15)]
holes=[(x-218,z-(tz-26),4.5) for x,z in tilt_support+tilt_lugs]
plate('CUSTOM_TILT_SERVO_MOUNT',72,49,(218,ty_outer,tz-26),holes,
      cuts=[(257.86-20.5-218,26-10.75,41,21.5)],normal=(0,-1,0),moving='PAN')
arm='CUSTOM_PAN_ARM_RIGHT'
extension=c.box(211,CY+59,362+DZ,74,5,11)
change(arm,c.S[arm].fuse(extension).clean())
for pl in c.PL:
    if pl['name']==arm:pl['height']=70
for x,z in tilt_support:c.hole(arm,(x,CY+64,z),4.5,(0,1,0))
mark(arm,'Upper edge extended 11 mm; four M4 support holes added; shortened above upper holes to clear LiDAR plate in sampled pan motion')
for i,(x,z) in enumerate(tilt_support):
    pre=f'SER0063_TILT_POST_{i}';y0=CY+55
    stud(pre,(x,y0,z),38,(0,1,0),'PAN')
    for j,y in enumerate((CY+58.2,CY+64,ty_inner-.8,ty_outer)):
        washer(pre+f'_W{j}',(x,y,z),(0,1,0),'PAN')
    for j,y in enumerate((CY+55,CY+64.8,ty_inner-4,ty_outer+.8)):
        nut(pre+f'_N{j}',(x,y,z),(0,1,0),'PAN')
for i,(x,z) in enumerate(tilt_lugs):
    pre=f'SER0063_TILT_LUG_{i}'
    stud(pre,(x,ty_inner-7,z),20,(0,1,0),'PAN')
    lugnut(pre+'_N0',(x,ty_inner-5.7,z),(0,1,0),'PAN')
    lugnut(pre+'_N1',(x,ty_outer,z),(0,1,0),'PAN')

# Preserve incomplete interfaces as explicit holds, not fictitious connectors.
for key in list(c.PORT):
    if 'MG90S' in key:del c.PORT[key]
c.PORT['C920_USB']['xyz'][2]+=DZ
c.PORT['C920_USB']['status']='RELOCATED_REFERENCE; cable route must be rebuilt'
route_holds=[]
for net in c.NET:
    if net['name'] in ('PAN_PWM_POWER','TILT_PWM_POWER','C920_USB'):
        route_holds.append(copy.deepcopy(net))
        net['route_status']='NOT_RELEASED_SER0063_REPLACEMENT'
        net['points']=[]
        net['note']='SER0063 5-8.4V per manufacturer; supply capacity/lead exit/horn motion and route must be verified. Old MG90S cable route removed.'
        net['length_mm']=None
for joint in c.JOINT:
    if joint.get('name')=='CAMERA_PAN':joint['origin']=list(PAN_AXIS)
    if joint.get('name')=='CAMERA_TILT':joint['origin']=list(TILT_AXIS)
    if joint.get('name','').startswith('CAMERA_'):
        joint['status']='REVIEW_ONLY; motor body fits, supplied horn interface unresolved'

old_hash={p['name']:hashlib.sha256((W/p['brep']).read_bytes()).hexdigest() for p in original if p['name'] not in shifted and p['name'] not in removed and p['name'] not in ('CUSTOM_PAN_SERVO_MOUNT','CUSTOM_TILT_SERVO_MOUNT','CUSTOM_PAN_ARM_RIGHT','CUSTOM_CAMERA_BASE','CUSTOM_ELECTRONICS_PLATE')}
changed=set(shifted)|{'CUSTOM_PAN_SERVO_MOUNT','CUSTOM_TILT_SERVO_MOUNT','CUSTOM_PAN_ARM_RIGHT','CUSTOM_CAMERA_BASE','CUSTOM_ELECTRONICS_PLATE'}
changed.update(p['name'] for p in c.P if p['name'].startswith(('SER0063_','USER_SER0063_')))
bad=[p['name'] for p in c.P if p['name'] in changed and not c.S[p['name']].isValid()]
assert not bad,bad
c.save()


# Restore preserved SER0063 metadata only after regenerated BREP names/bounds match.
saved=ROOT.parent/'recovery/unpacked/HELM_SER0063_INTEGRATION_REVIEW/DATA'
expected=json.loads((saved/'manifest.json').read_text())
assert {x['name'] for x in expected}==set(c.S)
errors=[]
for p in expected:
 err=max(abs(a-b) for a,b in zip(c.bounds(c.S[p['name']]),p['bbox']))
 if err>.00001:errors.append((p['name'],err))
assert not errors,errors
for n in ['manifest','plates','ports','wires','joints']:(W/(n+'.json')).write_bytes((saved/(n+'.json')).read_bytes())
print('Restored SER0063 snapshot',len(expected),hashlib.sha256((W/'manifest.json').read_bytes()).hexdigest(),flush=True)
