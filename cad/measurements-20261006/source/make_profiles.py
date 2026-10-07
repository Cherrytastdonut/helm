#!/usr/bin/env python3
"""Create a Korean change guide and true-scale A3 outline review sheets."""
from pathlib import Path
import argparse,json
import ezdxf
from ezdxf.path import make_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor,black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--font',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();dest=out/'DRAWINGS';dest.mkdir(exist_ok=True);pdfmetrics.registerFont(TTFont('KR',str(a.font)));REV='MEASURED_LAYOUT_20261006';INK=HexColor('#173041');TEAL=HexColor('#087e83');GRAY=HexColor('#5b6873');RED=HexColor('#983923');style=ParagraphStyle('body',fontName='KR',fontSize=10.2,leading=16.2,textColor=INK,wordWrap='CJK');small=ParagraphStyle('small',parent=style,fontSize=8.4,leading=12)
def txt(c,x,y,s,size=10,color=INK):c.setFillColor(color);c.setFont('KR',size);c.drawString(x*mm,y*mm,s)
def para(c,x,y,w,s,sm=False):
 p=Paragraph(s,small if sm else style);_,h=p.wrap(w*mm,600*mm);p.drawOn(c,x*mm,y*mm-h);return y-h/mm

def base(c,title,n):
 c.setFillColor(TEAL);c.rect(0,287*mm,210*mm,10*mm,stroke=0,fill=1);txt(c,18,273,'HELM / 구매품 반영 CAD 검토',10,TEAL);txt(c,18,259,title,20);c.setStrokeColor(HexColor('#d4dfe3'));c.line(18*mm,21*mm,192*mm,21*mm);txt(c,18,15,REV+' | 재단·통전 승인 전',8,GRAY);c.drawRightString(192*mm,15*mm,f'{n} / 6')
def section(c,y,title,body):txt(c,18,y,title,12,TEAL);return para(c,18,y-5,174,body)-8
def image(c,name,y,h):c.drawImage(str(out/'PREVIEWS'/name),19*mm,y*mm,172*mm,h*mm,preserveAspectRatio=True,anchor='c',mask='auto')
fr=json.loads((out/'DATA/FABRICATION_INDEX.json').read_text());
rows=[r for r in fr['parts'] if r['dxf']];c=canvas.Canvas(str(dest/'HELM_CURRENT_FLAT_PROFILES_REVIEW_A3.pdf'),pagesize=landscape(A3));c.setTitle('HELM 현재 평면 윤곽 - A3 1:1 검토용');sheets=[]
for number,row in enumerate(rows,1):
 name=row['part'];dw,dh,t=row['local_bounds_mm'];rotate=dh>172 and dw<=172;polys=[]
 for e in ezdxf.readfile(out/row['dxf']).modelspace():
  pts=[(v.x,v.y) for v in make_path(e).flattening(.015)]
  if pts:polys.append(pts)
 raw=[v for p in polys for v in p];xmin=min(x for x,y in raw);ymin=min(y for x,y in raw);xmax=max(x for x,y in raw);ymax=max(y for x,y in raw);assert abs(xmax-xmin-dw)<.05 and abs(ymax-ymin-dh)<.05
 if rotate:polys=[[(y-ymin,xmax-x) for x,y in p] for p in polys];ww,hh=dh,dw
 else:polys=[[(x-xmin,y-ymin) for x,y in p] for p in polys];ww,hh=dw,dh
 assert ww<=345 and hh<=172;ox=(420-ww)/2;oy=68+(172-hh)/2;c.setFillColor(TEAL);c.rect(0,287*mm,420*mm,10*mm,fill=1,stroke=0);txt(c,20,273,'HELM / 현재 형상에서 추출한 평면 윤곽',12,TEAL);txt(c,20,259,name,17);txt(c,20,249,f'외곽 {dw:.3f} × {dh:.3f} mm | 두께 {t:.3f} mm | 축척 1:1 | '+('지면상 90도 회전' if rotate else 'DXF 로컬 좌표 방향'),10);c.setStrokeColor(black);c.setLineWidth(.22*mm)
 for poly in polys:
  p=c.beginPath();p.moveTo((ox+poly[0][0])*mm,(oy+poly[0][1])*mm)
  for x,y in poly[1:]:p.lineTo((ox+x)*mm,(oy+y)*mm)
  c.drawPath(p)
 c.setStrokeColor(GRAY);c.setLineWidth(.15*mm);dimy=oy-8;dimx=ox-8
 for x in (ox,ox+ww):c.line(x*mm,(oy-1)*mm,x*mm,(dimy-2)*mm);c.line((x-1)*mm,(dimy-1)*mm,(x+1)*mm,(dimy+1)*mm)
 c.line(ox*mm,dimy*mm,(ox+ww)*mm,dimy*mm);c.setFillColor(INK);c.setFont('KR',8);c.drawCentredString((ox+ww/2)*mm,(dimy-4)*mm,f'{ww:.3f} mm')
 for y in (oy,oy+hh):c.line((ox-1)*mm,y*mm,(dimx-2)*mm,y*mm)
 c.line(dimx*mm,oy*mm,dimx*mm,(oy+hh)*mm);c.saveState();c.translate((dimx-3)*mm,(oy+hh/2)*mm);c.rotate(90);c.drawCentredString(0,0,f'{hh:.3f} mm');c.restoreState();txt(c,20,43,'도면 대조용 / 재단 승인 전 / mm / 절삭 폭·끼워맞춤 공차 미반영',11,RED);txt(c,20,35,'원본: '+row['dxf']+' | STEP으로 입체 형상·조립 위치를 확인',8,GRAY)
 txt(c,20,27,'주의: 1.6 mm 분배기판 형상 참조이며 포맥스 재단·회로 제작 승인 도면이 아닙니다.' if abs(t-5)>.01 else 'A3 용지 · 실제 크기 100% · 페이지 맞춤 해제 · 아래 기준선 실측 후 사용',9,RED if abs(t-5)>.01 else GRAY);c.setStrokeColor(INK);c.setLineWidth(.4*mm);c.line(20*mm,17*mm,120*mm,17*mm)
 for x in (20,120):c.line(x*mm,15*mm,x*mm,19*mm)
 txt(c,57,10,'100 mm',8);c.drawRightString(400*mm,14*mm,f'{REV} | {number:02d} / {len(rows)}');sheets.append({'part':name,'page':number,'scale':1,'paper':'A3_LANDSCAPE','rotated_on_paper':rotate,'dxf':row['dxf'],'thickness_mm':t,'vector_flattening_tolerance_mm':.015,'manufacturing_release':False});c.showPage()
c.save();(out/'DATA/DRAWING_INDEX.json').write_text(json.dumps({'revision':REV,'guide':'DRAWINGS/HELM_MEASURED_BUILD_GUIDE_KO.pdf','guide_pages':6,'profiles':'DRAWINGS/HELM_CURRENT_FLAT_PROFILES_REVIEW_A3.pdf','profile_pages':len(rows),'scope':'Verified constant-thickness outlines, not a complete system manufacturing drawing set','sheets':sheets},ensure_ascii=False,indent=2)+'\n');print('Created 6 guide pages and',len(rows),'outline sheets')
