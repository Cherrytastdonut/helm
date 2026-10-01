#!/usr/bin/env python3
"""Apply owned-part procurement changes to a clean SER0063 snapshot. REVIEW ONLY."""
from pathlib import Path
import argparse,sys,json,hashlib,shutil,copy
import cadquery as cq
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input-work',type=Path,required=True);ap.add_argument('--thermal-step',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();src=a.input_work.resolve();out=a.output.resolve();w=out/'EDITABLE/HELM_WORK'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
assert sha(src/'manifest.json')=='0b7b8cb640d072559c6d5957bcc3574d5be0e502dfbf6f83cc1efa5b37bced69','Requires original 4152-node SER0063 metadata, not a revised snapshot'
assert not out.exists(),'Use a fresh output directory'
for d in ['CAD','DATA','PART_STEP','DXF_REVIEW_ONLY','FABRICATION_STEP','SOURCE','PREVIEWS','EDITABLE/HELM_WORK/cache']:(out/d).mkdir(parents=True,exist_ok=True)
base=json.loads((src/'manifest.json').read_text());assert len(base)==4152
for n in ['core.py','manifest.json','plates.json','ports.json','wires.json','joints.json']:shutil.copy2(src/n,w/n)
for p in base:shutil.copy2(src/p['brep'],w/p['brep'])
sys.path.insert(0,str(w));import core as c;c.load();meta={p['name']:p for p in c.P};before={p['name']:sha(src/p['brep']) for p in base};removed=[];removed_wires=[];changes=[];changed=[]
def remove(names,reason):
 names=set(names)
 for p in list(c.P):
  if p['name'] in names:
   removed.append(dict(p,removal_reason=reason));c.P.remove(p);c.S.pop(p['name']);meta.pop(p['name']);(w/p['brep']).unlink()
 c.PL[:]=[x for x in c.PL if x['name'] not in names]
def add(n,s,group,color,note,status='PROCUREMENT_REVIEW'):
 assert s.isValid(),n;c.add(n,s,group,color,status,note=note,source='Purchased-part evidence; see DOCS/14-product-photo-review.md');meta[n]=c.P[-1];changed.append(n)
def replace(n,s,note):
 assert s.isValid(),n;c.S[n]=s;s.exportBrep(str(w/meta[n]['brep']));meta[n].update(bbox=c.bounds(s),faces=len(s.Faces()),solids=len(s.Solids()),valid=True,note=meta[n]['note']+'; '+note);changed.append(n)
def hold_wire(net,reason):
 if net['name'] in {x['name'] for x in removed_wires}:return
 removed_wires.append(dict(copy.deepcopy(net),superseded_reason=reason));remove(['CUSTOM_CABLE_'+net['name']],reason)
 net.update(geometry_valid=False,points=[],length_mm=None,endpoint_error_mm=None,reserve_mm=None,min_bend_radius_mm=None,stock_length_mm=None,status='NOT_RELEASED_PROCUREMENT_REPLACEMENT',route_status='NOT_RELEASED_PROCUREMENT_REPLACEMENT',note=reason)
 net.pop('motion_point_groups',None)
# C715 512GB: native NVIDIA 2280 socket and end support, not the old 2242 proxy.
remove([p['name'] for p in c.P if p['name'].startswith(('DRAWING_BASED_SN530','PHOTO_BASED_SN530'))] + ['OFFICIAL_JETSON_1897_Solid','OFFICIAL_JETSON_1898_Solid'],'Replaced by one purchased C715 512GB 2280 card; optional 2230 SSD and its screw are not installed')
x=22.7950001;y=53.376875;zt=273.323821523386
# Nominal M-key edge: 1 mm side relief and 1.5 mm key slot. Mating verification is still a hold.
outline=[(0,1),(5,1),(5,0),(80,0),(80,22),(5,22),(5,21),(0,21),(0,5.6),(4,5.6),(4,4.1),(0,4.1)]
pcb=cq.Workplane('XY').polyline(outline).close().extrude(.8).val().translate((x,y,zt-.8))
pcb=pcb.cut(c.cyl(x+80,y+11,zt-1,1.75,1.2))
# Remove the nominal card-edge bevel volume where it meets the socket lip. This is interface geometry, not vendor PCB fabrication CAD.
# Exact native connector lip projects only 0.005 mm onto the zero-thickness entry plane.
entry=c.box(x-.01,y-1,zt-.9,.04,24,1.0);pcb=pcb.cut(entry)
add('PURCHASE_C715_512GB_PCB',pcb,'04_COMPUTE','green','P2-R83 C715 512GB, manufacturer nominal 80x22x2.5 mm; 0.8 mm nominal PCB and M-key/semicircular fixing notch reconstructed for existing 2280 interface. Entry relief 0.03 mm is nominal. Not exact PCB fabrication CAD or verified insertion.')
add('PURCHASE_C715_COMPONENT_ENVELOPE',c.box(x+5.7,y+2,zt-2.5,69,18,1.7),'04_COMPUTE','dark','P2-R83 simplified component envelope; actual chip map not modeled, total nominal thickness 2.5 mm')
changes.append({'purchase':'P2-R83','action':'Replace 2242 reference and optional 2230 envelope with one nominal C715 512GB in actual 2280 slot','overall_nominal_mm':[80,22,2.5],'pcb_top_z_mm':zt,'end_mount_center_world_mm':[x+80,y+11,zt],'card_entry_relief_mm':.03,'mounting_state':'Existing 2280 interface; nominal card geometry. Retention screw stock and physical engagement pending.'})
# CP003 external envelope. No unverified holes or terminal cavities are invented.
remove([p['name'] for p in c.P if p['name'].startswith(('APPROX_BUS_POS','APPROX_BUS_NEG','BUS_FIX'))],'Old thin busbar approximation and mounting superseded by purchased CP003 envelope')
add('PURCHASE_SZH_CP003_OUTLINE',c.box(65,10,155,100,33,45),'03_POWER_SYSTEM','green','P2-R79 seller 100(L)x45(W)x33(H) mm including cover; clearance outline only. Fixing holes, cover motion and terminals unmeasured.','DIMENSIONED_CLEARANCE_OUTLINE')
bp='CUSTOM_POWER_BACKPLANE';s=c.S[bp];old_drills={(74,152),(164,152),(74,181),(164,181)};filled=[(74,181),(164,152),(164,181)]
for hx,hz in filled:s=s.fuse(c.cyl(hx,5,hz,1.7,5,(0,1,0)))
reliefs=[]
for hx in [125.969558604152,153.969558604152]:
 s=s.cut(c.box(hx-3.5,4.9,134.3898922198363-.1,7,5.2,8.1));reliefs.append({'center_x_world_mm':hx,'width_mm':7,'height_from_lower_edge_mm':8,'reason':'0.5 mm lateral/1 mm upper nominal clearance around existing M3 bumper-foot bolt head'})
s=s.clean();replace(bp,s,'CP003 review: obsolete busbar bores filled except location already within a clearance opening; two 7x8 mm lower-edge reliefs. New CP003 holes pending measured data.')
pl=next(p for p in c.PL if p['name']==bp);pl['world_drill']=[d for d in pl.get('world_drill',[]) if (d['point'][0],d['point'][2]) not in old_drills];pl.setdefault('review_changes',[]).append({'filled_old_bores_world_xz_mm':filled,'unchanged_clearance_location_xz_mm':[74,152],'lower_reliefs':reliefs,'new_cp003_holes':'PENDING_MEASUREMENTS'})
for key,p in c.PORT.items():
 if key.startswith('BUS_'):
  p['legacy_xyz']=p.get('xyz');p.update(xyz=None,owner='PURCHASE_SZH_CP003_OUTLINE',status='LOGICAL_NET_ONLY_TERMINAL_ASSIGNMENT_PENDING')
  for field in ['connection_xyz','wire_xyz']:p.pop(field,None)
for net in c.NET:
 if net['from_port'].startswith('BUS_') or net['to_port'].startswith('BUS_'):hold_wire(net,'Old busbar endpoint removed. CP003 internal grouping and input 2/output 8 capacity must be resolved before assigning the old logical branches.')
changes.append({'purchase':'P2-R79','action':'CP003 clearance envelope and revised backplane','overall_mm':[100,45,33],'world_bbox_mm':[65,10,155,165,43,200],'filled_old_bores_world_xz_mm':filled,'old_hole_locations_already_inside_clearance_opening_xz_mm':[[74,152]],'backplane_lower_reliefs':reliefs,'mounting_state':'HOLD: fixing holes, cover opening and terminal assignments unknown'})
# Native thermal board, connector and 2 mm contact pitch are preserved.
raw=cq.importers.importStep(str(a.thermal_step)).val();origin=(309.91148,81.69212767985001,245.08437090946);placed=c.transform(raw,origin,(0,1,0),(1,0,0));thermal=[]
for i,s in enumerate(placed.Solids()):
 n=f'OFFICIAL_THERMAL_{i:04d}_Solid';old=c.S[n];err=max(abs(q-r) for q,r in zip(c.bounds(s),c.bounds(old)));ve=abs(s.Volume()-old.Volume());assert err<.001 and ve<.01,(n,err,ve)
 thermal.append({'name':n,'bbox_max_error_mm':err,'volume_error_mm3':ve});meta[n]['procurement_evidence']='P2-R25 SEENGREAT 220565; matched manufacturer STEP; original healed BREP retained';meta[n]['source']='https://seengreat.com/wiki/88/thermal-camera-mlx90640-d55 -> Thermal Camera HAT-V1.2_step.stp'
assert len(thermal)==215
p=c.PORT['THERMAL_I2C'];p['legacy_xyz']=p.get('xyz');p.update(xyz=None,connector='PH2.0 4-pin',pin='GND/VCC/SDA/SCL; functions verified, mating orientation pending',status='MANUFACTURER_INTERFACE_ROUTING_PENDING',owner='SEENGREAT 220565 MLX90640-D55')
for field in ['connection_xyz','wire_xyz']:p.pop(field,None)
remove([p['name'] for p in c.P if p['name'].startswith('STANDARD_PLUG_THERMAL_')],'Old 2.54 mm mating plug proxy mismatches the manufacturer PH2.0 interface')
for net in c.NET:
 if net['name']=='THERMAL_I2C':hold_wire(net,'Manufacturer interface is PH2.0 4-pin. Mating plug orientation and actual lead exit/length are unresolved.')
adc=[p['name'] for p in c.P if p['name'].startswith(('CUSTOM_ADC_','ADC_CARRIER_','ADC_M2_','STANDARD_PLUG_ADC_'))];remove(adc,'ADS1115 module is absent from the authoritative purchases; remove carrier, mounting and phantom connector parts')
for key,p in c.PORT.items():
 if key.startswith('ADC_'):
  p['legacy_xyz']=p.get('xyz');p.update(xyz=None,status='NOT_INSTALLED_UNPURCHASED_MODULE',owner='UNRESOLVED_VOLTAGE_ACQUISITION')
  for field in ['connection_xyz','wire_xyz']:p.pop(field,None)
for net in c.NET:
 if net['name'] in ('ADC_I2C','VOLTAGE_SENSE'):hold_wire(net,'Unpurchased ADS1115 support omitted. Voltage acquisition using owned parts remains unresolved; no new module is assumed.')
changes.append({'action':'Remove unpurchased ADC support and phantom interfaces','removed_nodes':len(adc),'function':'Voltage acquisition remains unresolved'})
for p in c.P:
 if p['status'] in ('ASSUMED','PHOTO_ESTIMATE','COMMUNITY_CAD','ADAPTED_COMMUNITY_CAD','MODIFIED_STOCK_BRACKET'):p['procurement_state']='DETAIL_OR_STOCK_CONFIRMATION_PENDING'
 if p['name']=='PHOTO_BASED_NEXT505UHP':p['procurement_evidence']='P2-R42 model and 101x41x25 mm body confirmed; port positions remain estimates'
c.save()
for n,data in [('manifest',c.P),('plates',c.PL),('ports',c.PORT),('wires',c.NET),('joints',c.JOINT)]:dump(out/'DATA'/f'{n}.json',data)
dump(out/'DATA/REMOVED_NODES.json',removed);dump(out/'DATA/SUPERSEDED_ROUTES.json',removed_wires)
dump(out/'DATA/THERMAL_SOURCE_COMPARISON.json',{'manufacturer_step_sha256':sha(a.thermal_step),'source_url':'https://seengreat.com/upload/file/88/Thermal%20Camera%20HAT-V1.2.zip','rigid_origin':origin,'x_direction':[0,1,0],'normal':[1,0,0],'nodes':thermal,'result':'All 215 bounds within 0.001 mm; volume errors below 0.01 mm3; existing healed geometry retained'})
for n in changed:cq.exporters.export(c.S[n],str(out/'PART_STEP'/f'{n}.step'))
unchanged=[p['name'] for p in c.P if p['name'] in before and sha(w/p['brep'])==before[p['name']]]
assert len(c.P)==4078 and len(removed)==77 and len(unchanged)==4074,(len(c.P),len(removed),len(unchanged))
report={'revision':'PROCUREMENT_REVIEW_20261001','release_status':'NOT_FOR_FABRICATION','input_manifest_sha256':sha(src/'manifest.json'),'baseline_nodes':len(base),'nodes':len(c.P),'changed_geometry':changed,'removed_count':len(removed),'removed_names':[p['name'] for p in removed],'unchanged_brep_count':len(unchanged),'changes':changes,'part_exports':changed,'dxf_exports':[],'dxf_hold_reason':'Backplane depth features are preserved in STEP; do not flatten into an unverified cutting profile.','wire_routes_invalidated':[p['name'] for p in removed_wires],'holds':['SER0063 horn, MG995 bracket and NatureTool bracket dimensions','15 remaining camera hardware pairs pending actual dimensions','CP003 fixing holes, cover motion and terminal groups','Nominal C715 edge and retained screw physical fit','Small fasteners, special spacers, springs and 1.6 mm distributor stock','Fomex strength, nesting and drill sizes','Voltage acquisition, power protection and moving cables'],'recovery_note':'Regenerated from verified input after temporary-workspace cleanup. Nominal C715 key/entry geometry rebuilt; use this run validation and hashes, not previous unpublished output hashes.'}
dump(out/'DATA/REVISION.json',report)
shutil.copy2(a.thermal_step,out/'SOURCE/SEENGREAT_220565_manufacturer.stp');shutil.copy2(Path(__file__),out/'SOURCE/revise_procurement.py')
print('Revised',len(c.P),'removed',len(removed),'unchanged BREP',len(unchanged),'routes held',len(removed_wires),flush=True)
assy=cq.Assembly(name=report['revision']);groups={}
for p in c.P:
 g=p['group'];groups.setdefault(g,cq.Assembly(name=g));groups[g].add(c.S[p['name']],name=p['name'],color=cq.Color(*[q/255 for q in p['color']]))
for g,group in sorted(groups.items()):assy.add(group)
print('Full STEP export started',flush=True);assy.save(str(out/'CAD/HELM_PROCUREMENT_FULL_REVIEW.step'),exportType='STEP',mode='default',write_pcurves=True);print('Full STEP exported',flush=True)
