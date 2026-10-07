#!/usr/bin/env python3
"""True-scale paper comparison of the four existing chassis attachment centres."""
from pathlib import Path
import argparse,json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--font',type=Path,required=True);a=ap.parse_args();out=a.output.resolve()
fr=json.loads((out/'DATA/FABRICATION_INDEX.json').read_text());p=next(x for x in fr['parts'] if x['part']=='CUSTOM_BOTTOM_PLATE')['plate_definition'];holes=p['holes'][6:10];assert len(holes)==4
assert [(round(x-10,4),round(y-15,4)) for x,y,d in holes]==[(41.6247,62.6484),(41.6247,130.9651),(228.4383,65.433),(228.4383,128.1804)]
pdfmetrics.registerFont(TTFont('KR',str(a.font)));dest=out/'DRAWINGS/HELM_CHASSIS_4HOLE_CHECK_A3.pdf';c=canvas.Canvas(str(dest),pagesize=landscape(A3));c.setTitle('HELM 섀시 기준 4홀 종이 대조 - 재단용 아님')
def txt(x,y,t,size=10):c.setFont('KR',size);c.drawString(x*mm,y*mm,t)
c.setFillColorRGB(.09,.19,.25);txt(18,281,'HELM / 섀시 기준 4홀 대조',17);txt(18,270,'A3 실제 크기 100% · 위에서 본 +X 오른쪽 / +Y 위쪽 · 좌우 반전 금지 · 종이 대조용, 재단 도면 아님',10)
ox,oy=60,35;c.setStrokeColorRGB(.58,.67,.7);c.setDash(2*mm,2*mm);c.rect(ox*mm,oy*mm,p['width']*mm,p['height']*mm);c.setDash();txt(63,248,'점선: 하판 기준 사각형 300×223 mm (실제 홈·가공 형상 생략)',8)
records=[]
for i,(x,y,d) in enumerate(holes,1):
 xx,yy=(ox+x)*mm,(oy+y)*mm;c.setStrokeColorRGB(0,0,0);c.setLineWidth(.2*mm);c.circle(xx,yy,d/2*mm);c.line(xx-5*mm,yy,xx+5*mm,yy);c.line(xx,yy-5*mm,xx,yy+5*mm)
 txt(ox+x+7,oy+y+3,f'H{i}  X{x-10:.4f} / Y{y-15:.4f}',8);txt(ox+x+7,oy+y-3,f'하판 로컬 {x:.4f}, {y:.4f} / CAD 홀 Ø{d}',8)
 records.append({'id':f'H{i}','world_xy_mm':[x-10,y-15],'bottom_local_xy_mm':[x,y],'cad_hole_mm':d,'source':'CUSTOM_BOTTOM_PLATE plate_definition.holes[6:10] and CUSTOM_CHASSIS_PAD centres','physical_match_verified':False})
txt(67,52,'종이를 실물 섀시 위에 놓아 4개 중심이 동시에 맞는지 확인해 주세요.',10)
txt(67,43,'맞으면 다시 전부 재지 않으셔도 됩니다. 다르면 해당 중심 위치만 기록해 주세요.',9)
c.setLineWidth(.4*mm);c.line(20*mm,18*mm,120*mm,18*mm)
for x in [20,120]:c.line(x*mm,16*mm,x*mm,20*mm)
txt(49,9,'기준선 100 mm',8);txt(145,16,'프린터 배율 확인 후 사용 · 5T 실물 두께·적층 높이는 별도 확인',9);txt(320,7,'MEASURED_LAYOUT_20261006',7);c.save()
(out/'DATA/CHASSIS_4HOLE_CHECK.json').write_text(json.dumps({'revision':'MEASURED_LAYOUT_20261006','manufacturing_release':False,'scale':1,'paper':'A3_LANDSCAPE','holes':records},ensure_ascii=False,indent=2)+'\n')
q=out/'DATA/DRAWING_INDEX.json';d=json.loads(q.read_text());d['reference_template']='DRAWINGS/HELM_CHASSIS_4HOLE_CHECK_A3.pdf';d['reference_template_pages']=1;q.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Chassis template complete')
