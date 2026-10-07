#!/usr/bin/env python3
"""Build a six-page Korean measured-layout guide from current records."""
from pathlib import Path
import argparse,json
from html import escape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--font',type=Path,required=True);a=ap.parse_args();out=a.output.resolve()
load=lambda n:json.loads((out/'DATA'/f'{n}.json').read_text())
measures=load('measurement-register');critical=load('critical-checks');field=load('field-adjustment');v=load('VALIDATION');fr=load('FABRICATION_INDEX')
pdfmetrics.registerFont(TTFont('KR',str(a.font)))
INK=HexColor('#173041');TEAL=HexColor('#087e83');GRAY=HexColor('#60788c');RED=HexColor('#983923')
body=ParagraphStyle('body',fontName='KR',fontSize=10,leading=16,textColor=INK,wordWrap='CJK')
small=ParagraphStyle('small',parent=body,fontSize=8.5,leading=12.2)
dest=out/'DRAWINGS';dest.mkdir(exist_ok=True);c=canvas.Canvas(str(dest/'HELM_MEASURED_BUILD_GUIDE_KO.pdf'),pagesize=A4);c.setTitle('HELM 실측 반영 CAD와 제작 가이드')
def text(x,y,s,size=11,color=INK):c.setFont('KR',size);c.setFillColor(color);c.drawString(x*mm,y*mm,s)
def para(y,s,sm=False,x=20,w=170):
 p=Paragraph(escape(s).replace('\n','<br/>'),small if sm else body);_,h=p.wrap(w*mm,240*mm);p.drawOn(c,x*mm,y*mm-h);return y-h/mm
def title(s,n):
 text(20,271,s,19);text(18,13,'MEASURED_LAYOUT_20261006 · 재단·통전 승인 전',8,GRAY);text(191,13,str(n),8,GRAY)
def section(y,t,s):text(20,y,t,12,TEAL);return para(y-5,s)-9
title('HELM / 실측 반영 CAD와 제작 가이드',1)
y=249
y=section(y,'현재 산출물','구매 93개 항목과 치수표 13개 기록을 연결했습니다. 이 중 10개에 실측 또는 근사 실측치가 있습니다. 전체 수정 조립체는 3,888개 노드이며 외곽 치수를 바꾼 형상은 26개입니다.')
y=section(y,'변경한 형상','로커: 몸통 Ø20 / 테두리 Ø27 / 전체 깊이 34.2와 위치 수정. C920: 본체 95W×28H×20D, 거치부 45W×18H×44D, 접힌 전체 깊이 57. 중형 꺽쇠 30×25×25와 소형 참고 20×24×24. 미구매 ADC 잔여 몸체 27개 제거.')
y=section(y,'실측과 맞아 유지한 형상','CP003 100×45×33, 배터리 케이스 151×65×94(공식 단자 포함 98), 승압기 75×75×31, 퓨즈박스 53×86×42. SER0063 원본 55×20.5×47.38은 반올림된 실측값에 맞춰 축소하지 않았습니다.')
y=section(y,'아직 확정되지 않은 형상','꺽쇠 두께·홀·보강 돌기, 혼 연결과 회전부 실제 체결품은 미확정입니다. 구형 꺽쇠 체결 형상 160개, 카메라 스트랩 2개, 이동한 스위치 배선 1개를 무효 처리했습니다. 형상 생략은 조립 완료나 간섭 해결을 뜻하지 않습니다.')
y=section(y,'파일 사용 순서','부품표의 전체번호 → 필수확인 → 현장조정 → 같은 리비전 CAD·도면 순서로 보시면 됩니다. 부스바와 MG995 프레임은 선택 재고 외곽 STEP으로 분리했으며 본체에 강제로 장착하지 않았습니다.')
para(y,'보유 판재는 5T 포맥스 600×900 mm 2장입니다. 128개 제작 후보가 모두 이 두 장에서 나오는 것은 아닙니다.');c.showPage()
title('실측 치수 기록과 적용',2)
rows=[[Paragraph(s,small) for s in ['번호 / 구매 ID','확인한 치수 mm','CAD 반영']]]
for m in measures:rows.append([Paragraph(escape(str(s)),small) for s in [f"{m['number']} / {m['purchase_id']}",m['normalized_mm'],m['cad_action']]])
t=Table(rows,colWidths=[39*mm,80*mm,55*mm]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#dcefeb')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,-1),.3,HexColor('#ccd8df'))]));_,h=t.wrap(174*mm,235*mm);assert h<214*mm;t.drawOn(c,18*mm,254*mm-h)
para(248-h/mm,'원본 번호 10은 없습니다. 웹캠 구매 행 22는 모델명으로 대조해 P1-003 / 1차 7행에 연결했습니다. 중형의 25m는 25mm 오기로 정규화했습니다. CP003의 A/B는 단자 크기이며 고정홀이 아닙니다.',True);c.showPage()
title('먼저 확인할 핵심 4가지',3);y=248
for p in critical[:4]:y=section(y,p['id']+' / '+p['item'],p['need']+'\n'+p['reason']+'\n완료 기준: '+p['accept'])
para(y,'모터 본체·작은 칩을 다시 전부 재는 작업은 필요하지 않습니다. 실제 혼의 스케치, 시험 끼움, 기준 4홀 종이 대조, 범퍼 기능 시험으로 필요한 범위를 확인합니다.',True);c.showPage()
title('현장에서 조정할 항목',4);y=249
for p in field[:5]:y=section(y,p['item'],p['method']+'\n'+p['limit'])
y=section(y,'선택 부품과 회전부의 조건','MG995 프레임은 회전축·하중부로 채택할 때만 내측 폭·홀·두께를 확인합니다. 소형 꺽쇠의 실물 보유는 불확실합니다. 중형으로 대체하려면 혼과 함께 회전부 배치를 다시 검사해야 합니다.')
para(y,'재고 미확인: 범퍼 스프링·가이드, LiDAR 40 mm 슬리브, 코너블록·부시, M2/M2.5 기계나사, 2T ESP 받침·소켓, 1.6T 5V 분배기판과 엔코더 레벨 회로. CAD에 있다는 이유만으로 보유 재료로 계산하지 않습니다.',True);c.showPage()
title('판재 재단과 조립 순서',5);y=249
for head,txt in [
 ('1 / 기준과 재료 확인','5T 실물 두께를 확인하고 섀시 기준 4홀에 1:1 종이를 대조합니다. 회전부 연결판과 큰 스위치 홀은 핵심 확인이 끝나기 전 최종 재단하지 않습니다.'),
 ('2 / 100% 출력과 시험 조각','A3 윤곽 도면은 실제 크기 100%, 페이지 맞춤 해제로 출력합니다. 100 mm 기준선을 자로 확인합니다. 로커는 아래 Ø20 시험 홀로 5T 끼움·걸림턱을 확인하며 Ø27로 뚫지 않습니다.'),
 ('3 / 외곽 재단과 홀 전사','판에 번호·기준 모서리를 표시하고 공구 여유·절삭 폭을 포함해 배치합니다. 판을 고정한 후 외곽을 가공하고 고정 꺽쇠·단자대 홀은 실물을 놓고 전사합니다. 기존 가정 홀을 먼저 전부 뚫지 않습니다.'),
 ('4 / 가조립과 길이 확정','전원을 분리한 상태에서 하판·기둥·상판을 가조립합니다. 너트·와셔를 포함한 적층 높이로 전산볼트를 최종 절단합니다. 카메라는 혼 확정과 간섭 수정 뒤 실제 체결품을 넣어 수동 회전 검사합니다.'),
 ('5 / 마감과 기능 검사','절단면 마감 후 배터리 인출·덮개 열림·공구 접근·배선 여유를 확인합니다. 보유 비트는 2/3/4/5/6/8 mm입니다. Ø4.5 홀을 임의로 Ø5로 넓히지 말고 가공법부터 결정합니다.')]:y=section(y,head,txt)
text(20,69,'로커 시험 조각 / 실제 크기 60×30 mm, 시작 홀 Ø20',9,TEAL)
c.setStrokeColor(INK);c.setLineWidth(.25*mm);c.rect(25*mm,32*mm,60*mm,30*mm);c.circle(55*mm,47*mm,10*mm);para(58,'5T 자투리에서 먼저 시험합니다.\n장착 몸통은 약 Ø20입니다.\n걸림턱과 후면 깊이도 확인합니다.',True,x=100,w=86);c.showPage()
title('검증 범위와 남은 설계 작업',6);y=249
y=section(y,'CAD 검증',f"전체 STEP의 구문·부품명을 확인하고 수정한 26개 형상을 다시 읽어 치수를 대조했습니다. 제작 후보 STEP {fr['part_steps']}개도 재읽기 검증했습니다. 전체 미변경 정지 부품의 모든 조합·강도·연속 회전·실물 동작을 검증한 결과는 아닙니다.")
y=section(y,'겹침과 회전부',f"변경부 후보 {v['changed_candidate_pairs']}쌍에서 0.5 mm³ 초과 겹침 {len(v['changed_unintended_hits'])}쌍을 기록했습니다. 이 중 C920 내부 참조 형상 4쌍은 별도로 표시했습니다. 9개 팬·틸트 자세 검사에는 고유 {v['unique_camera_pairs']}쌍이 남아 있습니다. 팬 ±45° / 틸트 ±20°는 검사 각도이며 승인 동작 범위가 아닙니다.")
y=section(y,'도면 사용 범위','DXF와 A3 윤곽 20개 중 19개는 5T, 1개는 1.6T 분배기판 참조입니다. 깊이가 다른 홈·다중 형상 판은 STEP으로 제공합니다. CUSTOM_LEFT_PANEL의 옛 꺽쇠 홀은 참고용이며 실물 전사 전 천공하지 않습니다. 측판의 새 로커 중심은 전체 좌표 X200 / Z239.389892 mm입니다.')
y=section(y,'외곽 모델의 한계','C920 힌지 상대 위치는 추정이며 실제 접힘 자세와 다를 수 있습니다. 로커 깊이의 내부 분할과 단자 블록도 여유 확인용입니다. MG995 프레임·부스바 별도 STEP은 외접 상자이며 상세 제조 CAD가 아닙니다.')
y=section(y,'앞선 문서와 충돌할 때','같은 리비전의 CAD·치수표·검증 기록을 우선합니다. 과거 FINAL/PASS 또는 디자인·추가 검색 불필요는 당시 확인한 본체와 검사 범위에 한정됩니다. 실제 부품과 다른 연결부는 수정해야 합니다. LIB_SER0063.zip은 모터 몸체 CAD이며 혼 자료가 아닙니다.')
para(y,'핵심 4가지와 채택한 회전부 부품을 확인한 뒤 연결판·실제 체결품·간섭을 마무리하고 최종 재단·조립 도면을 다시 도출합니다. 현재 파일은 실측 반영 전체 검토 조립체이며 제작 승인본은 아닙니다.',True)
c.save();print('Guide pages 6')
