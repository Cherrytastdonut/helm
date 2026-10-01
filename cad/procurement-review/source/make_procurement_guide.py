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
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--font',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();dest=out/'DRAWINGS';dest.mkdir(exist_ok=True);pdfmetrics.registerFont(TTFont('KR',str(a.font)));REV='PROCUREMENT_REVIEW_20261001';INK=HexColor('#173041');TEAL=HexColor('#087e83');GRAY=HexColor('#5b6873');RED=HexColor('#983923');style=ParagraphStyle('body',fontName='KR',fontSize=10.2,leading=16.2,textColor=INK,wordWrap='CJK');small=ParagraphStyle('small',parent=style,fontSize=8.4,leading=12)
def txt(c,x,y,s,size=10,color=INK):c.setFillColor(color);c.setFont('KR',size);c.drawString(x*mm,y*mm,s)
def para(c,x,y,w,s,sm=False):
 p=Paragraph(s,small if sm else style);_,h=p.wrap(w*mm,600*mm);p.drawOn(c,x*mm,y*mm-h);return y-h/mm

def base(c,title,n):
 c.setFillColor(TEAL);c.rect(0,287*mm,210*mm,10*mm,stroke=0,fill=1);txt(c,18,273,'HELM / 구매품 반영 CAD 검토',10,TEAL);txt(c,18,259,title,20);c.setStrokeColor(HexColor('#d4dfe3'));c.line(18*mm,21*mm,192*mm,21*mm);txt(c,18,15,REV+' | 재단·통전 승인 전',8,GRAY);c.drawRightString(192*mm,15*mm,f'{n} / 6')
def section(c,y,title,body):txt(c,18,y,title,12,TEAL);return para(c,18,y-5,174,body)-8
def image(c,name,y,h):c.drawImage(str(out/'PREVIEWS'/name),19*mm,y*mm,172*mm,h*mm,preserveAspectRatio=True,anchor='c',mask='auto')
v=json.loads((out/'DATA/VALIDATION.json').read_text());fr=json.loads((out/'DATA/FABRICATION_INDEX.json').read_text());c=canvas.Canvas(str(dest/'HELM_PROCUREMENT_CHANGE_GUIDE_KO.pdf'),pagesize=A4);c.setTitle('HELM 구매품 반영 CAD 변경 안내 - 검토본')
base(c,'확인한 부품을 전체 모델에 적용',1);para(c,18,247,174,'최신 조립체는 4,078개 노드입니다. SER0063 수정 위에 SSD·배전 외곽·전원 받침판을 반영하고, 구매하지 않은 ADC 받침과 잘못된 연결 형상을 제외했습니다.');image(c,'FULL_REVIEW.png',104,117)
y=section(c,97,'이번 수정','C715 512GB를 실제 Jetson 2280 위치에 배치 / CP003 100×45×33 mm 공간 모델 / 전원판의 구형 홀 정리와 하단 간섭 홈 / 열화상 제조사 본체 유지 및 PH2.0 정정')
para(c,18,63,174,f'현재 제작 대상 STEP {fr["part_steps"]}개와 일정 두께가 확인된 DXF {fr["flat_dxfs"]}개를 다시 도출했습니다. 카메라 간섭 {v["unique_camera_pairs"]}쌍과 혼·브래킷 실측이 남아 있어 최종 재단본으로 승인하지 않았습니다.');c.showPage()
base(c,'SSD: 실제 2280 슬롯으로 교체',2);image(c,'SSD_2280.png',112,132);y=105
y=section(c,y,'C715 512GB, 2차 83행','제조사 명목 외형 80×22×2.5 mm입니다. 기존 WD 2242 참조와 선택형 2230 SSD를 제거하고 실제 2280 소켓·끝단 지지부 기준으로 배치했습니다.')
y=section(c,y,'정확한 범위','PCB 카드 끝·키·칩은 결합 공간을 확인하는 명목 모델입니다. 복원 시 카드 진입부의 미세 여유를 다시 구성했습니다. 공급사의 정확한 기판·칩 제조 CAD는 아니며, 실제 끼움·고정나사·장착 여유는 확인이 필요합니다.')
para(c,18,y,174,'소켓 OFFICIAL_JETSON_0564_Solid / 끝단 지지 OFFICIAL_JETSON_0705_Solid. 끝단 기준 중심 XYZ = (102.795, 64.377, 273.324) mm. 단순히 이전 42 mm 카드를 80 mm로 늘린 위치가 아닙니다.',True);c.showPage()
base(c,'배전: 외곽과 전원판 수정',3);image(c,'POWER_DISTRIBUTION.png',125,120);y=119
y=section(c,y,'CP003 외곽 적용, 상세 고정부 보류','2차 79행의 100(L)×45(W)×33(H) mm를 녹색 공간 모델에 반영했습니다. 덮개 포함 외곽이며 단자·고정홀의 상세 CAD는 아닙니다. 고정홀과 덮개 개방 공간·전선 입구·내부 연결을 확인해야 합니다.')
y=section(c,y,'전원 백플레이트','불필요한 닫힌 홀 3개를 메웠고 기존 개구부 안의 1개 위치는 유지했습니다. 하단 폭 7×높이 8 mm 홈 2개로 범퍼 발 체결품과의 겹침을 해소했습니다. 홈 중심의 전체 좌표 X는 125.970 / 153.970 mm입니다.')
para(c,18,y,174,'이 판은 다른 깊이 형상이 있어 STEP으로 제공합니다. CP003 입력 2/출력 8에 예전 14개 논리 접속점을 임의 배정하지 않았으며 관련 15개 배선 경로를 무효 처리했습니다.',True);c.showPage()
base(c,'열화상: 제조사 본체 유지',4);image(c,'THERMAL_VERIFIED.png',138,108);y=131
y=section(c,y,'SEENGREAT 220565 대조','제조사 HAT-V1.2 STEP을 확보해 기존 215개 형상의 경계·부피를 대조했습니다. 경계 오차 0.001 mm, 부피 차이 0.01 mm³ 미만 기준을 통과하여 기존 본체와 배치를 유지했습니다. 렌더링 색은 식별용입니다.')
y=section(c,y,'PH2.0 4핀과 배선','포트 정보를 PH2.0 4핀으로 바로잡고 구형 2.54 mm 플러그 프록시를 제거했습니다. GND/VCC/SDA/SCL 기능은 확인했지만, 결합 방향과 실제 리드선 출구·길이는 미확정입니다.')
y=section(c,y,'구매하지 않은 ADC 제외','ADS1115 받침·스페이서·체결품과 가짜 연결을 제거했습니다. 추가 구매를 전제하지 않으며 보유품으로 전압을 읽는 회로는 후속 확정 대상입니다. 배전·열화상·ADC를 합쳐 이번에 총 18개 경로를 무효 처리했습니다.')
para(c,18,y,174,'“본체 자료 불필요”는 확보한 본체 자료에만 해당합니다. 체결·강도·배선 또는 다른 부품의 설계 변경을 중단한다는 뜻이 아닙니다.',True);c.showPage()
base(c,'사용자께서 찾아 주실 자료',5);y=244
for title,body in [('1. SER0063 동봉 혼','사용할 혼의 형상, 홀 중심 간격·지름, 두께, 축에 끼웠을 때의 상면 높이. 모터 몸체 CAD는 이미 확보했습니다.'),('2. MG995/MG996 브래킷','프레임별 안쪽 폭·높이·두께, 홀 좌표·지름, 원형 축 지지부 내경·외경·두께. 판매자 자 대조 사진만으로 정밀 가공을 확정하지 않습니다.'),('3. 네이쳐툴 소형·중형 꺽쇠','두 다리 길이·폭·두께, 홀 중심·지름, 굽힘부 보강 돌기 높이. 제품 사진은 확보했습니다.'),('4. SZH-CP003 고정부·단자','고정홀 중심 간격·지름, 덮개 개방 방향과 여유, 전선 입구 위치, 단자 내부 연결 그림. 외형 크기는 이미 적용했습니다.'),('추가 보유 규격','휴대형 스피커와 리미트 스위치의 정확한 치수, 전압센서, 너트·와셔·스페이서, 소형 기계나사, 범퍼 스프링·LiDAR 슬리브와 1.6 mm 분배기판 재료·회로의 보유 여부를 확인해야 합니다.')]:y=section(c,y,title,body)
para(c,18,y,174,'정확한 치수도 또는 STEP이 있으면 실측 대신 보내 주세요. 이미 확보한 정면 사진을 다시 모을 필요는 없습니다. 자세한 범위는 docs/15-needed-measurements.md에 정리했습니다.',True);c.showPage()
base(c,'도면에서 제작으로 넘어가는 순서',6);y=244
for title,body in [('01 / 최신 파일 확인','전체 모델은 CAD/HELM_PROCUREMENT_FULL_REVIEW.step입니다. EDITABLE/HELM_WORK에는 같은 BREP 4,078개와 메타데이터가 있습니다. 과거 FINAL/PASS는 당시 검사 범위에만 해당합니다.'),('02 / 치수·간섭·강도 확정','혼과 실제 브래킷·체결품을 적용하고 남은 카메라 간섭 15쌍을 해결합니다. 포맥스 강도·공구 접근·배터리 인출·움직이는 케이블을 확인합니다.'),('03 / 재료와 판재 배치','보유 판재는 5T 포맥스 600×900 mm 2장입니다. 128개 형상이 모두 이 두 장에서 나오지는 않습니다. 1.6 mm 분배기판은 포맥스 가공 대상이 아닙니다. 재료·수량 대조 뒤 공구 여유와 절삭 폭을 넣어 배치합니다.'),('04 / 출력 대조와 시험 조각','별도 A3 윤곽 20쪽은 1:1 검토용입니다. 실제 크기 100%로 인쇄하고 100 mm 선을 먼저 재세요. Bosch 비트는 2/3/4/5/6/8 mm이므로 D4.5 홀의 가공법을 먼저 확정해야 합니다. 임의로 5 mm로 넓히지 않습니다.'),('05 / 가공·가조립·단계 시험','번호·기준 모서리 표시 → 시험 조각 → 고정 후 절단·천공 → 마감 → 전원 분리 상태 가조립 → 전압·극성·보호 동작 확인 순서로 기록합니다. 최종 재단·결선도는 미확정 항목 해소 후 다시 도출합니다.')]:y=section(c,y,title,body)
para(c,18,y,174,f'검사 범위: 이번 변경부 후보 {v["changed_candidate_pairs"]}쌍에서 의도하지 않은 0.5 mm³ 초과 겹침 {len(v["changed_unintended_hits"])}건. 제작 STEP 128개 재읽기. 전체 STEP은 이름·구문과 변경 4개 형상 확인. 전체 연속 회전·강도·실물 동작 승인은 포함하지 않습니다.',True);c.save()
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
c.save();(out/'DATA/DRAWING_INDEX.json').write_text(json.dumps({'revision':REV,'guide':'DRAWINGS/HELM_PROCUREMENT_CHANGE_GUIDE_KO.pdf','guide_pages':6,'profiles':'DRAWINGS/HELM_CURRENT_FLAT_PROFILES_REVIEW_A3.pdf','profile_pages':len(rows),'scope':'Verified constant-thickness outlines, not a complete system manufacturing drawing set','sheets':sheets},ensure_ascii=False,indent=2)+'\n');print('Created 6 guide pages and',len(rows),'outline sheets')
