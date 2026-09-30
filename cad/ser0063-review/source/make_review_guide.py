from pathlib import Path
import csv,json,zipfile,xml.etree.ElementTree as ET,hashlib,shutil,collections
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output/HELM_SER0063_INTEGRATION_REVIEW';D=OUT/'DATA';P=OUT/'PREVIEWS'
report=json.loads((D/'REVISION_AND_VALIDATION.json').read_text())
extended=json.loads((D/'EXTENDED_VALIDATION.json').read_text())
plates={p['name']:p for p in json.loads((D/'plates.json').read_text())}
assert not extended['new_hardware_hits'],extended['new_hardware_hits']
upload=ROOT.parent/'upload'
csvp=next(upload.glob('*.csv'));xlsp=next(upload.glob('*.xlsx'))
with csvp.open(encoding='utf-8-sig') as f:rows=list(csv.reader(f))
first=[dict(source_row=i+1,item=r[0],model=r[1],quantity=r[2],purpose=r[4],url=r[5]) for i,r in enumerate(rows) if 4<=i<=32]
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(xlsp) as z:
    ss=[''.join(t.text or '' for t in a.findall('.//m:t',ns)) for a in ET.fromstring(z.read('xl/sharedStrings.xml'))]
    second=[]
    for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:sheetData/m:row',ns):
        ri=int(row.attrib['r'])
        if not 20<=ri<=83:continue
        cells={}
        for cell in row:
            v=cell.find('m:v',ns)
            if v is not None:cells[''.join(x for x in cell.attrib['r'] if x.isalpha())]=ss[int(v.text)] if cell.attrib.get('t')=='s' else v.text
        second.append(dict(sheet='2주차',source_row=ri,item=cells.get('A',''),model=cells.get('B','').strip(),quantity_cell=cells.get('C',''),url=cells.get('I','')))
assert len(first)==29 and len(second)==64
audit={'rule':'Previous CSV left-side first purchase columns plus current XLSX 2주차 rows 20-83. Do not force all second-purchase items into CAD. Do not treat comparison quotes as additional stock.',
       'first_purchase':first,'second_purchase':second,'sources':[{'file':p.name,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()} for p in (csvp,xlsp,ROOT/'motor/SER0063.stp')]}
(D/'PURCHASE_SOURCE_ROWS.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))

pdfmetrics.registerFont(TTFont('NotoKR',str(ROOT/'NotoSansKR-Regular.ttf')))
WW,HH=A4;M=38;CW=WW-2*M;mm=72/25.4
navy=colors.HexColor('#18374B');teal=colors.HexColor('#007F86');ink=colors.HexColor('#253743');muted=colors.HexColor('#536778');orange=colors.HexColor('#A45313');line=colors.HexColor('#D5E0E5')
st=ParagraphStyle('body',fontName='NotoKR',fontSize=9.3,leading=14,textColor=ink,wordWrap='CJK')
small=ParagraphStyle('small',parent=st,fontSize=8,leading=11)
pdf=OUT/'HELM_SER0063_CHANGE_GUIDE_KO.pdf';c=canvas.Canvas(str(pdf),pagesize=A4)
c.setTitle('HELM SER0063 교체 검토 및 재단 전 확인 안내');c.setAuthor('HELM CAD revision')
def para(text,x,y,w=CW,style=st):
    p=Paragraph(text,style);aw,ah=p.wrap(w,HH);p.drawOn(c,x,y-ah);return y-ah
def header(num,title,sub):
    c.setFillColor(navy);c.rect(0,HH-31,WW,31,fill=1,stroke=0)
    c.setFont('NotoKR',8);c.setFillColor(colors.white);c.drawString(M,HH-20,'HELM / SER0063 / REVIEW 2026-09-30')
    c.setFillColor(navy);c.setFont('NotoKR',21);c.drawString(M,HH-67,title)
    para(sub,M,HH-80,style=small)
    c.setStrokeColor(line);c.line(M,38,WW-M,38);c.setFont('NotoKR',8);c.setFillColor(orange)
    c.drawString(M,24,'조립 검토용 - 재단·통전 승인용 최종본 아님')
    c.setFillColor(muted);c.drawRightString(WW-M,24,f'{num} / 6')
def section(text,y):
    c.setFillColor(teal);c.setFont('NotoKR',12);c.drawString(M,y,text);return y-13
def table(data,widths,x,y,fs=8.5):
    s=ParagraphStyle('t',parent=st,fontSize=fs,leading=fs+4)
    t=Table([[Paragraph(str(v),s) for v in row] for row in data],colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8F2F3')),('LINEBELOW',(0,0),(-1,0),.8,teal),('LINEBELOW',(0,1),(-1,-1),.4,line),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    w,h=t.wrap(CW,HH);t.drawOn(c,x,y-h);return y-h
def image(path,x,y,w,h):
    c.drawImage(str(path),x,y,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
def notice(text,y):
    c.setFillColor(colors.HexColor('#FFF4E8'));c.roundRect(M,y-49,CW,49,6,fill=1,stroke=0)
    para(text,M+10,y-8,CW-20,small);return y-62

# Page 1
header(1,'모터 교체 CAD를 확인하세요','실제 첨부 STEP을 적용한 중간 검토본입니다. 기존 V13 전체 제작도는 이번 변경과 함께 다시 검토해야 합니다.')
y=notice('적용 기준: 1차는 이전 CSV의 왼쪽 구매 목록, 2차는 이번 XLSX입니다. 새 부품을 전부 넣지 않고, 기존 CAD와 실물 구성이 다른 항목을 교체 대상으로 정했습니다.',727)
image(P/'CAMERA_ISO.png',M,323,CW,337)
y=section('이번에 반영한 변경',304)
y=table([['구분','반영 내용'],['모터','MG90S 2개를 첨부 SER0063 STEP 2개로 교체. 모터 형상은 축척 변경 없이 배치했습니다.'],['장착 구조','팬·틸트 장착판, 지지봉 위치·길이, 오른쪽 지지판을 수정했습니다. 카메라 이동부를 위로 24.38 mm 이동했습니다.'],['미확정 연결','기존 MG90S 혼과 틸트 연결구를 제거했습니다. 새 혼 치수가 없어 구동축 연결은 아직 완성되지 않았습니다.'],['배선','기존 서보 2개 및 C920의 움직이는 케이블 경로를 제거하고 재배선 대기로 표시했습니다.']],[75,CW-75],M,y-4)
c.showPage()

# Page 2
header(2,'구매 목록을 CAD에 반영하는 기준','품목이 추가됐다는 이유만으로 장착하지 않습니다. 실물 교체·호환성·장착 목적을 나눠 판단합니다.')
data=[['구매품 / 출처','이번 처리','남은 확인'],['SER0063 ×2 / 2주차 30행','CAD 교체 완료','혼 실측, 하중과 배선'],['5T 포맥스 600 × 900 ×2 / 51행','장착판 재료 기준','합판으로 임의 대체하지 않음'],['M4 전산볼트 1 m ×5 / 52행','카메라 지지봉 검토안','실물 절단·끝단 정리·체결 여유'],['M3/M4/M5 혼합 세트 / 53행','M4 너트·와셔 후보','규격별 실제 개수, 1세트/2세트 표기 차이'],['M4 풀림방지 너트 / 75행','구매품으로 기록','CAD의 일반 너트와 높이가 다를 수 있음'],['MG995/MG996 브래킷 ×2 / 78행','호환 확인 전 미적용','실물 구멍 간격, 내측 폭, 두께'],['SZH-CP003 분배 단자대 / 79행','후속 교체 검토 대상','기존 배전부 대체 위치·단자 방향'],['KLEVV CRAS C715 / 83행','기존 SSD와 다른 품목으로 기록','보유 SSD 선택, 실제 규격·고정 위치'],['LED 패널·Edifier 스피커 / 81-82행','차체 장착을 강제하지 않음','전시용 사용 가능. 스피커 정확한 모델 필요'],['충전기 EO-1212 / 20행','새 구매 모델 기준으로 기록','기존 EO-1220 표기와 구분'],['공구·소모품 / 여러 행','가공·조립용으로 분류','차체 안에 모델을 억지로 넣지 않음']]
y=table(data,[148,142,CW-290],M,726,8.1)
y=section('자료 해석 주의',y-25)
y=para('이전 CSV는 1차 품목 29행을 사용했습니다. 이번 XLSX는 <b>2주차 A20:I83의 64개 구매 행</b>을 사용했습니다. 비교견적 시트의 예시·대체 견적을 추가 구매품으로 세지 않았습니다.',M,y-3)
y=para('기존 CAD의 ADS1115, 특수 길이 스페이서, 일부 체결품·범퍼 스프링은 실제 보유품과의 대조가 더 필요합니다. 전체 CAD가 구매품만으로 완성됐다는 뜻은 아닙니다.',M,y-12)
c.showPage()

# Page 3
header(3,'모터 기준 치수와 연결부','단위 mm. 치수 기준은 첨부 SER0063/3D/SER0063.stp이며, 제조사 규격은 보조 확인 자료입니다.')
image(ROOT/'motor/SER0063_views.png',M,403,CW,315)
y=table([['항목','확인값 / 의미'],['장착 홀','4개, 지름 4.5, 중심 간격 48 × 10'],['첨부 CAD 최대 외곽','55.00 × 47.38 × 20.50 (원본 X × Y × Z)'],['원본 출력축','축 방향 +Y, 축 끝 중심 (-9.86, 27.63, 10.00)'],['모델 구성','유효한 솔리드 1개. 혼·서보 리드선 형상은 포함되지 않음'],['제조사 표기','출력축 25T / 5.9 mm, 축 고정 나사 M3 × 6, 전원 5-8.4 V']],[130,CW-130],M,393)
y=section('혼 연결을 확정하려면',y-24)
y=para('동봉 금속 혼의 ① 위에서 본 구멍 위치 ② 옆에서 본 두께와 축에 끼운 높이 ③ 중앙 고정 나사를 확인해야 합니다. 자를 댄 앞·옆 사진과 브래킷의 앞·옆 사진을 준비해 주세요. 구멍 중심 간 거리는 실측값이 있으면 더 정확합니다.',M,y-3)
y=para('현재 팬 축 위의 2 mm 공간은 혼을 넣기 위한 임시 배치값입니다. 실제 혼 두께로 확정한 수치가 아닙니다. 기존 MG90S 혼을 재사용한다고 가정하지 않았습니다.',M,y-12)
para('제조사: https://www.dfrobot.com/product-2787.html<br/>첨부 STEP과 제품 치수도에서 장착 홀 간격을 대조했습니다. 확인일: 2026-09-30.',M,79,style=small)
c.showPage()

def profile_page(num,title,name,notes):
    pl=plates[name];w=pl['width'];h=pl['height']
    header(num,title,'종이 대조용 1:1 형상입니다. 인쇄 시 실제 크기 100%를 선택하고, 아래 100 mm 기준선을 먼저 재어 보세요.')
    y=notice('재단 보류: 이 평판은 모터 위치 검토용입니다. 혼 연결, 남은 간섭과 5T 포맥스 체결부 강도를 해결한 뒤 제작 치수를 확정해야 합니다.',725)
    x=M+28;by=430
    c.setStrokeColor(ink);c.setFillColor(colors.HexColor('#EDF3F5'));c.setLineWidth(.8);c.rect(x,by,w*mm,h*mm,fill=1,stroke=1)
    for cx,cy,cw,ch in pl['cuts']:
        c.setFillColor(colors.white);c.rect(x+cx*mm,by+cy*mm,cw*mm,ch*mm,fill=1,stroke=1)
    c.setFont('NotoKR',6.5)
    for i,(hx,hy,dd) in enumerate(pl['holes'],1):
        xx=x+hx*mm;yy=by+hy*mm;c.setFillColor(colors.white);c.circle(xx,yy,dd/2*mm,fill=1,stroke=1)
        c.setStrokeColor(muted);c.setLineWidth(.3);c.line(xx-9,yy,xx+9,yy);c.line(xx,yy-9,xx,yy+9)
        c.setFillColor(ink);c.drawString(xx+7,yy+6,str(i));c.setStrokeColor(ink);c.setLineWidth(.8)
    c.setFont('NotoKR',8);c.setFillColor(ink)
    c.drawCentredString(x+w*mm/2,by+h*mm+15,f'{w:g} mm');c.drawString(x-21,by+h*mm/2,f'{h:g}')
    c.drawString(x-3,by-17,'원점 (0, 0)');c.drawRightString(x+w*mm,by-17,'X → / Y ↑')
    para(f'외곽 {w:g} × {h:g}<br/>두께 5<br/>장착 홀 8개: D4.5<br/>중앙 창 41 × 21.5<br/><br/>1-4: 지지봉 홀<br/>5-8: 모터 플랜지 홀',330,616,WW-M-330,small)
    c.setStrokeColor(teal);c.setLineWidth(1);sy=391;c.line(M,sy,M+100*mm,sy)
    for tx in [M,M+100*mm]:c.line(tx,sy-4,tx,sy+4)
    c.setFillColor(teal);c.drawString(M,sy-15,'이 선을 자로 재면 100 mm여야 합니다.')
    hd=[['홀','X','Y','홀','X','Y']]
    for i in range(4):
        a=pl['holes'][i];b=pl['holes'][i+4];hd.append([i+1,f'{a[0]:.2f}',f'{a[1]:.2f}',i+5,f'{b[0]:.2f}',f'{b[1]:.2f}'])
    y=table(hd,[43,78,78,43,78,CW-320],M,356)
    cut=pl['cuts'][0]
    y=para(f'중앙 창의 왼쪽 아래: X {cut[0]:.2f}, Y {cut[1]:.2f}. 모서리 반경은 실제 가공 공구에 맞춰 다시 확인해야 합니다. CAD/DXF는 공구 경로와 절삭 폭 보정이 없는 윤곽입니다.',M,y-15)
    y=para(notes,M,y-12)
    para('대응 STEP과 DXF는 파일명 '+name+'로 찾으시면 됩니다. STEP은 조립 좌표이고, DXF는 평판의 왼쪽 아래가 원점인 mm 도면입니다.',M,84,style=small)
    c.showPage()

profile_page(4,'팬 모터 장착판 검토도','CUSTOM_PAN_SERVO_MOUNT','지지봉은 64 mm ×4 검토안입니다. 왼쪽 뒤 지지점을 기존 위치에서 옮겨 ADC 받침과의 간섭을 피했습니다. 본체 플랜지와 중앙 창 사이의 좁은 포맥스 구간은 하중 시험 없이 제작 확정하지 마세요.')
profile_page(5,'틸트 모터 장착판 검토도','CUSTOM_TILT_SERVO_MOUNT','지지봉은 38 mm ×4 검토안입니다. 아래쪽 왼쪽 지지점을 옮겼습니다. 오른쪽 팬 지지판 높이는 11 mm 늘렸고, 장착판 상단은 라이다 받침에 닿지 않도록 줄였습니다. 형상은 해당 PART_STEP 파일에서 확인하세요.')

# Page 6
header(6,'재단과 조립으로 이어가는 순서','지금 할 수 있는 종이 대조와, 실물 확인 뒤 진행할 재단·조립을 순서대로 정리했습니다.')
y=726
steps=[('1. 파일 열기','전체 배치는 CAD/HELM_SER0063_FULL_REVIEW.step, 카메라 집중 검토는 CAMERA_REVIEW.step을 여세요. 단위는 mm입니다. 파란 두 몸체가 첨부 SER0063입니다.'),('2. 종이로 먼저 맞추기','4-5쪽을 100%로 인쇄해 모터 플랜지와 대조합니다. 혼·브래킷 실측, 간섭 수정, 체결품 규격 확인 전에는 포맥스를 자르지 마세요.'),('3. 확정 뒤 판재 배치','600 × 900 판에 확정된 부품만 배치하고 번호·앞면·기준 모서리를 표시합니다. 현재 파일은 전체 판재 네스팅·수량 최적화 도면이 아닙니다.'),('4. 확정 뒤 절단·천공','시험 조각에서 절삭 폭과 구멍을 먼저 확인합니다. 판을 받침판에 고정하고, 보유 칼·톱으로 여러 번 나눠 가공한 뒤 줄·사포로 맞춥니다. 드릴 구경은 도면과 실제 비트를 대조하세요.'),('5. 전산볼트와 가조립','검토 길이: 64 ×4, 38 ×4, 20 ×8 = 합계 568 mm (절단 손실 제외). 너트를 먼저 끼우고 고정해 절단한 뒤 끝단을 정리합니다. 실물 너트 높이에 맞춰 길이를 확정하세요.'),('6. 혼·배선·동작 확인','혼과 중앙 나사를 먼저 맞춰 손으로 천천히 움직여 간섭을 확인합니다. 3개 케이블 경로와 전원 용량을 다시 설계한 뒤 통전해야 합니다. 기존 4.8 V 서보 배선 메모를 그대로 사용하지 마세요.')]
for title,body in steps:
    y=section(title,y);y=para(body,M,y-2)-17
hardware=len(extended['new_hardware_hits']);posecounts=[len(m['hits']) for m in extended['motion_samples']]
y=section('검증 결과와 제작 보류 이유',y-1)
y=para(f'새 모터·지지 체결부는 검사한 {extended["new_hardware_pairs"]}개 후보 쌍에서 0.5 mm³ 초과 겹침이 {hardware}건입니다. 부품 STEP 17개와 카메라 STEP 재불러오기에서 유효한 형상을 확인했습니다.',M,y-2)
y=para(f'팬 -45/0/+45°, 틸트 -20/0/+20°의 9개 조합을 검사했습니다. 기존 카메라 체결부 등에서 자세별 {min(posecounts)}-{max(posecounts)}건의 겹침이 남았습니다. 연속 회전·하중·케이블 검증을 통과했다는 뜻이 아닙니다. 위치 설명은 ZIP의 OPEN_ISSUES_KO.md에 있습니다.',M,y-10)
y=para('남은 핵심: 혼의 형상·장착 높이, 금속 브래킷 호환성, 기존 카메라 체결부 간섭, 포맥스 강도, 실물 체결품 규격, 전원과 배선. 이 사항을 반영한 뒤 최종 재단도를 확정해야 합니다.',M,y-10)
assert y>55,('page 6 overflow',y)
c.save()

# A concise Korean entry point, plus the exact source model and derivation code.
readme=f'''# HELM SER0063 교체 검토 패키지

**상태: 조립 검토용. 최종 재단·통전용으로 승인된 도면이 아닙니다.**

1차는 이전 CSV의 왼쪽 구매 목록 29품목, 2차는 이번 XLSX `2주차!A20:I83`의 64행을 기준으로 했습니다. 추가 구매품 전체를 CAD에 강제로 넣지 않았습니다. 비교견적의 예시·대안도 추가 재고로 세지 않았습니다.

## 먼저 열 파일

- `HELM_SER0063_CHANGE_GUIDE_KO.pdf`: 변경 내용, 종이 대조용 1:1 장착판 2종, 재단 전 확인 순서.
- `CAD/HELM_SER0063_FULL_REVIEW.step`: 전체 조립 검토 STEP. 단위 mm.
- `CAD/HELM_SER0063_CAMERA_REVIEW.step`: 변경 부품 중심의 카메라 검토 STEP. 전자부 데크도 포함합니다.
- `PART_STEP/`: 변경 또는 높이 이동된 제작 부품 17개. 모두 새로 잘라야 한다는 뜻이 아닙니다.
- `DXF_REVIEW_ONLY/`: 일정 두께 평판으로 추출 가능한 7개 윤곽. mm, 절삭 폭 보정 없음. 재단 확정 파일 아님.
- `DATA/`: 실제 구매 행, 변경 부품 목록, 간섭 검사와 재불러오기 결과.
- `OPEN_ISSUES_KO.md`: 남은 간섭의 한글 위치 설명, CAD 부품 이름, 필요한 실물 확인 목록.
- `SOURCE/`: 첨부 SER0063 원본 STEP과 수정·검증 스크립트.

## 실제 바뀐 내용

MG90S 2개를 사용자 제공 SER0063 STEP으로 교체했습니다. 모터 형상은 축척 변경 없이 강체 이동했습니다. 카메라 이동부를 24.38 mm 올리고 팬·틸트 장착판 및 오른쪽 지지판을 수정했습니다. M4 전산볼트 지지점과 길이는 새 모터와 기존 부품 간섭을 확인해 조정했습니다. 지지봉 검토 길이는 64 mm ×4, 38 mm ×4, 20 mm ×8입니다. 실제 체결품이 다르면 다시 확정해야 합니다.

이전 MG90S 혼·틸트 연결구와 서보 2개/C920의 기존 케이블 경로는 제거했습니다. 없는 혼을 임의로 만들어 체결 완료로 표시하지 않았습니다. 팬 축의 2 mm 혼 공간은 임시값입니다.

## 검증과 한계

- 새 모터 몸체 2개와 장착판 2개: 주변 강체와 정지 상태 교차 검사.
- 새 모터·체결부 후보 {extended['new_hardware_pairs']}쌍: 0.5 mm³ 초과 겹침 {hardware}건.
- 개별 부품 STEP 17개 및 카메라 STEP: 다시 읽어 형상 유효성 확인.
- 회전 9자세: 기존 카메라 체결부 등에서 자세별 {min(posecounts)}-{max(posecounts)}건의 겹침이 남음. 자세와 부품 이름은 `DATA/EXTENDED_VALIDATION.json`.
- 연속 운동, 없는 혼, 유연 케이블, 구조 강도, 전원 용량은 검증되지 않았습니다. 모델의 움직임 그룹과 임시 축을 이용한 검사입니다.
- 기존 CAD의 다른 가정부품·배선은 그대로 남아 있습니다. 전체 구매품만으로 조립 가능하다는 검증은 끝나지 않았습니다.

## 구매품 적용 판단

SER0063는 확정 교체했습니다. 포맥스 5T와 M4 전산볼트는 장착 검토에 사용했습니다. 보유 MG995/MG996 금속 브래킷은 실측 없이 호환을 단정하지 않았습니다. SZH-CP003 배전 단자대와 C715 SSD는 기존 모델과 다른 항목으로 후속 확인이 필요합니다. 전시 LED 패널과 데스크 스피커를 차체에 강제로 넣지 않았습니다. 혼합 체결 세트 등은 설명의 세트 수와 수량 열이 달라 실물 개수 확인이 필요합니다.

## 재단을 시작하기 전

동봉 혼의 위·옆 사진과 금속 브래킷의 위·옆 사진을 자와 함께 촬영하세요. 특히 혼의 구멍 중심 간격, 두께, 축에 끼운 높이, 브래킷의 내측 폭·구멍 간격이 필요합니다. 이를 반영하고 남은 간섭·강도를 해결한 뒤 재단 치수를 확정합니다. 현재 PDF의 1:1 판은 종이 맞춤용입니다. 구매 목록의 재료는 합판이 아니라 5T 포맥스입니다.

확정 뒤에는 판재에 부품 번호와 기준 모서리를 표시하고 시험 조각에서 절삭 폭·구멍을 확인합니다. 부재를 고정하고 보유 칼·톱·드릴로 가공하며, 절단면은 줄·사포로 마감합니다. 전체 판재 배치/수량 최적화는 이번 검토 범위에 포함되지 않았습니다.

## 출처와 재현

- 이전 CAD: `HELM_V13_CAD_DRAWINGS_FINAL_20260928.zip` (기존본은 유지).
- 1차 CSV: `{csvp.name}`.
- 2차 XLSX: `{xlsp.name}`, `2주차` 시트 구매 행.
- 모터: `LIB_SER0063.zip / SER0063/3D/SER0063.stp`.
- 제조사: https://www.dfrobot.com/product-2787.html (2026-09-30 확인).

수정 스크립트는 원래 V13의 `HELM_V13_WORK` 캐시와 cadquery/OCP 환경을 전제로 합니다. ZIP 안의 STEP은 별도 생성 스크립트 없이 CAD 프로그램에서 열 수 있습니다. `SOURCE` 스크립트의 경로 설정은 재현 시 작업 폴더에 맞춰야 합니다.
'''
(OUT/'README_KO.md').write_text(readme)
(OUT/'SOURCE').mkdir(exist_ok=True)
shutil.copy2(ROOT/'motor/SER0063.stp',OUT/'SOURCE/SER0063_USER_ORIGINAL.stp')
for f in ('revise_servo.py','validate_review.py','make_review_guide.py'):
    shutil.copy2(ROOT/f,OUT/'SOURCE'/f)
shutil.copy2(ROOT/'motor/SER0063_views.png',P/'SER0063_SOURCE_VIEWS.png')
print('Created',pdf,flush=True)
