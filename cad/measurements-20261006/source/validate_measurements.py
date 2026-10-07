#!/usr/bin/env python3
"""Validate the current review: changed rigid parts, nine poses, changed STEP roundtrips."""
from pathlib import Path
import argparse,sys,json
import cadquery as cq
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();sys.path.insert(0,str(out/'EDITABLE/HELM_WORK'));import core as c;c.load();meta={p['name']:p for p in c.P};rev=json.loads((out/'DATA/REVISION.json').read_text());print('Loaded',len(meta),flush=True)
def broad(a,b):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-6 for i in range(3))
def contact(a,b):
 sols=a.intersect(b).Solids();return sum(s.Volume() for s in sols),[s.Volume() for s in sols]
pairs=set();shells=[]
for n in rev['changed_geometry']:
 for p in c.P:
  if n==p['name'] or p['group']=='09_WIRING' or not broad(meta[n]['bbox'],p['bbox']):continue
  if not p['solids']:shells.append([n,p['name']]);continue
  pairs.add(tuple(sorted([n,p['name']])))
hits=[];intended=[];errors=[]
for x,y in sorted(pairs):
 try:v,vs=contact(c.S[x],c.S[y])
 except Exception as e:errors.append({'a':x,'b':y,'error':str(e)});continue
 if v>.5:
  row={'a':x,'b':y,'volume_mm3':v,'largest_connected_intersection_mm3':max(vs,default=0)}
  if {x,y}=={'PURCHASE_C715_512GB_PCB','OFFICIAL_JETSON_0564_Solid'} and max(vs,default=0)<.1:
   row['classification']='Nominal card-edge contact with sprung connector terminals, each connected intersection below 0.1 mm3. Not a physical insertion/tolerance test.';intended.append(row)
  else:hits.append(row)
print('Changed exact pairs',len(pairs),'unintended',hits,'intended',intended,flush=True)
pan=(248,c.CY,322.38);tilt=(248,c.CY,374.38);moving=[p for p in c.P if p['moving'] in ('PAN','TILT') and p['group']!='09_WIRING' and p['solids']];fixed=[p for p in c.P if p['moving'] not in ('PAN','TILT') and p['group']!='09_WIRING' and p['solids']];samples=[]
for pa,ta in [(-45,-20),(-45,0),(-45,20),(0,-20),(0,0),(0,20),(45,-20),(45,0),(45,20)]:
 shapes={};bb={}
 for p in moving:
  s=c.S[p['name']]
  if p['moving']=='TILT' and ta:s=s.rotate(tilt,(tilt[0],tilt[1]+1,tilt[2]),ta)
  if pa:s=s.rotate(pan,(pan[0],pan[1],pan[2]+1),pa)
  shapes[p['name']]=s;bb[p['name']]=c.bounds(s)
 cand=[(p['name'],q['name']) for p in moving for q in fixed if broad(bb[p['name']],q['bbox'])]
 cand +=[(p['name'],q['name']) for p in moving if p['moving']=='TILT' for q in moving if q['moving']=='PAN' and broad(bb[p['name']],bb[q['name']])]
 mh=[]
 for x,y in cand:
  try:v,_=contact(shapes[x],shapes[y] if y in shapes else c.S[y])
  except Exception as e:errors.append({'pose':[pa,ta],'a':x,'b':y,'error':str(e)});continue
  if v>.5:mh.append({'a':x,'b':y,'volume_mm3':v})
 samples.append({'pan_deg':pa,'tilt_deg':ta,'candidate_pairs':len(cand),'hits':mh});print('Pose',pa,ta,'hits',len(mh),flush=True)
roundtrips=[]
for n in rev['part_exports']:
 s=cq.importers.importStep(str(out/'PART_STEP'/f'{n}.step')).val();error=max(abs(x-y) for x,y in zip(c.bounds(s),meta[n]['bbox']));assert s.isValid() and error<.002,(n,error)
 roundtrips.append({'name':n,'valid':True,'bbox_error_mm':error,'volume_error_mm3':abs(s.Volume()-c.S[n].Volume())})
report={'scope':'26 changed parts versus all current rigid solids at rest; nine camera sample poses versus fixed solids plus relative PAN/TILT motion; 26 changed STEP roundtrips. Unchanged stationary pairs, continuous sweep, stock tolerances, strength and cables are not certified.','intersection_threshold_mm3':.5,'changed_candidate_pairs':len(pairs),'changed_unintended_hits':hits,'intended_connector_contacts':intended,'shell_pairs_not_treated_as_material':shells,'errors':errors,'camera_samples':samples,'unique_camera_pairs':len({tuple(sorted([h['a'],h['b']])) for s in samples for h in s['hits']}),'part_roundtrips':roundtrips,'approved_pan_limits_deg':None,'approved_tilt_limits_deg':None}
report['suppressed_hardware_is_not_collision_resolution']=True
report['changed_geometry_count']=len(rev['changed_geometry'])
report['camera_internal_reference_pairs']=[h for h in hits if h['a'].startswith('COMMUNITY_C920') and h['b'].startswith('COMMUNITY_C920')]
(out/'DATA/VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert not errors,report
print('Validation complete, remaining camera pairs',report['unique_camera_pairs'],flush=True)
