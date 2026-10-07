"""Number every purchase row; preserve source measurements and map CAD ownership.
No network. Run from an immutable baseline or the resulting snapshot.
"""
import json,csv,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'DATA'; D.mkdir(exist_ok=True)
def dump(n,x): (D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
source=json.loads((D/'purchase-source-rows.json').read_text())
measure=json.loads((D/'source-measurements.json').read_text())
spec={
1:('P2-R79','실측','100 × 45 × 33; 입력 나사 ≈7.5; 출력 개구 ≈5.5–6','외곽 유지; A/B는 고정홀이 아닙니다.','현장 조정','고정 위치는 실물 전사. 덮개 열림·절연 간격·단자 그룹은 결선 전에 확인'),
2:('P1-009','실측','151 × 65 × 94 (케이스); 공식 단자 포함 98','기존 케이스와 단자 형상 유지','현장 조정','단자에 연결한 케이블 여유를 남기고 벨크로 길이는 가조립 후 결정'),
3:('P2-R30','근사 실측','≈55 × ≈20 × ≈47–48; 원본 CAD 55 × 20.5 × 47.38','원본 모터 2개 유지; 반올림한 20으로 축소하지 않음','필수 확인','모터 본체 재측정 불필요. 사용할 혼의 홀 간격·지름·두께·끼운 높이만 필요'),
4:('P2-R21','상품명','길이 300; 피치 2.0; 6핀','실측으로 집계하지 않음; 케이블 길이 정보 기록','현장 조정','핀 순서·같은면 여부를 실물 확인하고 당기지 않는 경로로 정리'),
5:('P2-R56','미실측','설치할 길이만 선택','세트의 모든 스페이서를 측정할 필요 없음','현장 조정','부품을 올린 뒤 필요한 몸통 길이·나사 체결 길이·절연 간격 선택'),
6:('P2-R54','사용자 전사 규격','20 × 24 × 24; 소형 실물 보유 불확실','외곽만 참고 CAD에 반영; 두께·홀·돌기 미확정','조건부 확인','고정부는 보유 중형으로 재배치 가능. 회전부에 쓸 때만 두께·돌기·체결 여유 확인'),
7:('P2-R55','실측','30 × 25 × 25','기존 30 × 40 × 40 외곽 수정; 두께 2는 가정','현장 조정','고정된 판의 홀은 실물 꺽쇠 전사. 카메라 회전부에 채택하면 회전 간격 확인'),
8:('P2-R22','실측','75 × 75 × 31','기존 형상 유지','현장 조정','방열·배선 여유를 남기고 고정홀만 실물 전사'),
9:('P1-016','실측','53 × 86 × 42','기존 받침+덮개 전체 외곽 유지','현장 조정','덮개 탈착·퓨즈 교체 공간을 실물로 확인'),
11:('P1-018','근사 실측','≈165 × 15 × 18, 2개','선택 재고 외곽 STEP; 본체에 강제 장착하지 않음','현장 조정','채택할 때 고정홀 전사. 단자 수·내부 연결·극 배정은 별도 확인'),
12:('P1-029','근사 실측','몸통 Ø≈20; 테두리 Ø≈27; 전체 34.2','외곽·뒤쪽 여유 수정. 구멍은 테두리 27로 뚫지 않음','조건부 확인','5T 자투리에 Ø20 시험 구멍을 만들어 걸림턱·끼움 확인 후 본판에 전사'),
13:('P2-R78','사진 근사 실측','ㄷ자 64 × 55 × 25; 다른 프레임 58 × 37 × 25','선택 재고 외곽 STEP; 정밀 홀·회전축 미생성','조건부 확인','회전 지지부로 채택할 때만 안쪽 폭·두께·축홀/베어링 치수 필요'),
14:('P1-003','사진 근사 실측','본체 95 × 20 × 28; 클립 44 × 45 × 18; 접힌 측면 전체 57','본체/클립 따로 보정. 상대 힌지 자세는 추정','현장 조정','구매 행 22 오기를 모델명으로 원본 7행에 연결. 스트랩·EVA는 실물에 맞춤')}
measurement_rows=[]
for r in measure['records']:
 pid,kind,dims,apply,risk,action=spec[r['number']]
 measurement_rows.append({**r,'purchase_id':pid,'evidence_type':kind,'normalized_mm':dims,'cad_action':apply,'decision':risk,'required_action':action,'source':'부품 치수.xlsx / 시트1 / '+str(r['row'])+'행'})
dump('measurement-register.json',measurement_rows)
checks=[
 {'id':'G1','purchase_id':'P2-R30','item':'SER0063 출력 혼','decision':'필수 확인','need':'실제 사용할 혼의 홀 중심 간격·지름·두께·축에 끼운 체결면 높이','reason':'회전축과 연결판의 위치가 바뀌어 재단 후 현장 보정이 어렵습니다.','accept':'치수 스케치 또는 혼 STEP, 팬/틸트에 사용할 혼을 지정. 모터 몸체는 다시 잴 필요 없음'},
 {'id':'G2','purchase_id':'P1-012','item':'비상정지 스위치 장착부','decision':'필수 확인','need':'실물 장착 지름·5T 판을 잡는 길이·뒤쪽 돌출','reason':'구매 22mm 표기와 기존 CAD 참조품의 일치가 확인되지 않았습니다. 큰 홀은 복구하기 어렵습니다.','accept':'5T 자투리 끼움+너트 체결 시험과 후면 여유 확인. 맞으면 세부 외형 재측정 불필요'},
 {'id':'G3','purchase_id':'P1-006 / P2-R51','item':'섀시 기준 홀과 판 두께','decision':'필수 확인','need':'실물 섀시 상부 기준 4홀에 1:1 종이를 대조; 실제 판 두께와 가조립 높이','reason':'기준이 어긋나면 상하판·전산볼트 전체가 맞지 않습니다.','accept':'네 점 모두 맞으면 새로 전부 측정할 필요 없음. 다르면 해당 홀 중심 좌표만 측정'},
 {'id':'G4','purchase_id':'P1-014','item':'범퍼 스위치와 복귀 기구','decision':'필수 확인','need':'작동점·여유 이동·복귀 확인; 실제 스프링/가이드 보유 여부','reason':'기존 4mm 스트로크·2mm 작동점은 가정이며 멈춤과 복귀 기능에 영향을 줍니다.','accept':'간이 지그에서 네 방향을 눌러 작동과 복귀를 확인. 미보유 스프링 등을 가상 재고로 취급하지 않음'},
 {'id':'C1','purchase_id':'P1-029','item':'원형 로커 스위치','decision':'조건부 확인','need':'5T 자투리 Ø20 끼움·걸림턱·후면 34.2 깊이','reason':'테두리 Ø27은 가공 구멍 지름이 아닙니다.','accept':'자투리 합격 후 본판. 정밀 전 치수 측정 대신 끼움 시험 가능'},
 {'id':'C2','purchase_id':'P2-R78','item':'MG995 금속 프레임','decision':'채택 시 필수','need':'안쪽 폭·판 두께·축홀 피치와 지름·원형 지지부 치수','reason':'외곽 치수만으로 SER0063와 회전축 호환을 판정할 수 없습니다.','accept':'사용하지 않으면 측정 불필요. 사용 시 혼과 함께 대조'},
 {'id':'C3','purchase_id':'P2-R54 / P2-R55 / P2-R53 / P2-R75','item':'카메라 회전부 꺽쇠·체결품','decision':'채택 시 필수','need':'소형 보유 확인 또는 중형 재배치; 회전 안쪽 돌출 높이·볼트/너트 실제 간격','reason':'기존 회전 체결부 간섭이 남아 있고, 형상 생략은 간섭 해결이 아닙니다.','accept':'혼 확정 후 배치 수정과 회전 검사. 고정된 판의 일반 꺽쇠는 현장 전사 가능'}]
dump('critical-checks.json',checks)
field=[
 ('고정 ㄱ자 꺽쇠·CP003·퓨즈박스','실물 놓기 → 덮개/공구 여유 확인 → 홀 중심 전사 → 가조립','기존 CAD의 가정 홀을 먼저 모두 뚫지 않습니다.'),
 ('PCB·허브·USB 스피커','보드 모서리와 커넥터 여유를 맞춘 뒤 스페이서/벨크로 위치 선택','작은 칩 개별 측정 불필요. PCB 자체 홀을 임의로 넓히지 않습니다.'),
 ('M3 스페이서·M4 전산볼트','실물 적층 높이와 너트·와셔에 맞춰 필요한 길이만 선택/최종 절단','회전부에서는 돌출 나사 끝과 공구 접근을 확인합니다.'),
 ('EVA·벨크로·케이블','실제 압축 두께와 여유 길이로 현장 조정','방열구·배터리 단자·가동부를 덮거나 케이블을 팽팽하게 당기지 않습니다.'),
 ('미사용 재고·공구·개별 칩','전체 구매 목록에는 유지하되 로봇 CAD에 강제로 장착하지 않음','부스바와 MG995 프레임은 별도 선택 재고 형상입니다.'),
 ('배선·전원 통합','보유 배선·단자·퓨즈 규격으로 회로와 극성 대조 후 결선','CP003 단자 크기를 고정홀로 오해하지 않습니다. CAD 배선 경로는 전기 검증이 아닙니다.')]
dump('field-adjustment.json',[dict(item=a,method=b,limit=c) for a,b,c in field])
manifest_path=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'EDITABLE/HELM_WORK/manifest.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else []
# Ownership is separate from hardware kit candidates and custom-material attribution.
def owner(p):
 n=p['name']
 rules=[('OFFICIAL_JETSON','P1-001'),('OFFICIAL_CHASSIS','P1-006'),('OFFICIAL_MDD10A','P1-007'),('OFFICIAL_BNO085','P1-008'),('OFFICIAL_THERMAL','P2-R25'),('OFFICIAL_ESTOP','P1-012'),('COMMUNITY_C920','P1-003'),('USER_SER0063','P2-R30'),('PURCHASE_C715','P2-R83'),('PURCHASE_SZH_CP003','P2-R79'),('ADAPTED_ESP32','P1-005'),('STANDARD_ESP32','P1-005'),('STANDARD_USB_C_CONTACT','P1-005'),('DRAWING_BASED_A2M12','P1-004'),('PHOTO_BASED_A2M12','P1-004'),('DRAWING_BASED_ES7_12','P1-009'),('PHOTO_BASED_ES7_12','P1-009'),('DRAWING_BASED_BATTERY_F2','P1-009'),('PHOTO_BASED_SZH_EK366','P1-011'),('PHOTO_BASED_BUCK_CAP','P1-011'),('PHOTO_BASED_EK366','P1-011'),('STANDARD_EK366','P1-011'),('PHOTO_BASED_BOOST','P2-R22'),('PHOTO_BASED_NEXT505','P2-R42'),('APPROX_HUB','P2-R42'),('PHOTO_BASED_SZH_JA020','P1-016'),('PHOTO_BASED_FUSEBLOCK','P1-016'),('DRAWING_BASED_ATO_FUSE','P1-017'),('PHOTO_BASED_RELAY','P1-013'),('DRAWING_BASED_1N4007','P2-R31'),('PHOTO_BASED_MAIN_ROCKER','P1-029'),('DRAWING_BASED_760K','P2-R23'),('PHOTO_BASED_760K','P2-R23'),('DRAWING_BASED_FHAC','P2-R26'),('STANDARD_FHAC','P2-R26'),('PHOTO_BASED_FHAC','P2-R26'),('PHOTO_BASED_USB_SPEAKER','P1-025'),('PHOTO_BASED_SPEAKER_CONE','P1-025'),('STANDARD_SPEAKER','P1-025'),('OFFICIAL_TE187','P2-R24'),('DRAWING_BASED_MOTOR_PH6','P2-R21')]
 for prefix,pid in rules:
  if n.startswith(prefix):return pid,'구매품 본체/구성 형상','개별 칩·단자는 상위 구매품에 귀속; 정밀도는 원래 상태 열 참조'
 if 'V_J166' in n or re.search(r'DRAWING_BASED_(FRONT|REAR|LEFT|RIGHT)_SWITCH_TAB',n):return 'P1-014','구매품 참조','범퍼 작동/복귀는 G4 확인'
 if n.startswith('APPROX_MEDIUM_L_'):return 'P2-R55','외곽 실측/체결 미확정','두께·홀·보강 돌기는 미확정'
 if n.startswith(('APPROX_SMALL_L_','APPROX_BACKPLANE_L_','APPROX_CAM_L_')) and p['group']!='08_FASTENERS':return 'P2-R54','소형 규격 참고/재고 미확인','사용자 전사20×24×24. 실물 미보유일 수 있음'
 if n.startswith('DRAWING_BASED_M4_ROD') or re.match(r'SER0063_(PAN|TILT)_POST_\d+$',n):return 'P2-R52','재료 후보','가조립 적층 후 절단 길이 결정'
 if n.startswith(('CUSTOM_BATTERY_STRAP','PHOTO_BASED_STRAP_BUCKLE')):return 'P2-R57','재료 후보','실제 보유 스트랩으로 길이 조정'
 if n=='CUSTOM_C920_PAD' or 'GROMMET' in n or 'RUBBER' in n or 'EVA' in n:return 'P2-R76','재료 후보','압축 두께는 현장 조정값; 실제 재고 두께와 같다는 뜻 아님'
 if n.startswith('OFFICIAL_ADS1115'):return 'UNPURCHASED','미구매 제거 대상','현재 조립체에 포함하면 안 됨'
 if any(s in n for s in ['ENCODER_LEVEL','ENC_LEVEL','ENCODER_DIVIDER','CUSTOM_5V_DISTRIBUTOR','CUSTOM_ESP32_CARRIER','CUSTOM_ESP32_SOCKET','RETURN_SPRING','GUIDE_ROD','GUIDE_BUSH','TILT_CORNER','TILT_BUSH','LIDAR_SP','TILT_AXIS']) or n.startswith('D5_'):
  return 'UNVERIFIED-STOCK','보유·설계 미확정','구매품으로 확정하지 않음. 재고/동봉품 대조 또는 보유품 설계 변경 필요'
 if p['group']=='09_WIRING':
  if 'ESP32_USB' in n:return 'P1-023 | P2-R43','배선 후보','현장 케이블 선택; 핀맵·길이·경로 미확정'
  return 'P1-019 | P1-020 | P2-R21 | P2-R50 | P2-R80','배선 후보','여러 보유 케이블 중 기능에 맞게 선택. 각 선의 구매확정 매핑 아님'
 if p['group']=='08_FASTENERS':return 'P2-R53 | P1-024 | P2-R56 | P2-R75','체결 키트 후보','M2/M2.5·특수 길이·나일론너트 치수는 보유 미확인; 수량 확정 아님'
 if p.get('fabricate'):
  if '2T' in p.get('note','') or '1.6' in p.get('note',''):return 'UNVERIFIED-STOCK','다른 재료 필요','5T 포맥스 판에 포함하지 않음'
  return 'P2-R51','사용자 제작 형상','5T 판 해당 여부는 판재 인덱스로 확인; 곡면/특수 부품까지 5T 재단 승인 아님'
 return 'UNVERIFIED-STOCK','보유·설계 미확정','형상 존재만으로 실제 부품 보유를 뜻하지 않음'
node_rows=[]
for p in manifest:
 pid,kind,note=owner(p)
 node_rows.append(dict(node=p['name'],purchase_id=pid,relation=kind,note=note,group=p['group'],geometry_status=p['status'],moving=p.get('moving',''),fabricate=p.get('fabricate',False)))
dump('cad-node-map.json',node_rows)
rows=[]
for key in ('first_purchase','second_purchase'):
 for i,r in enumerate(source[key]):
  pid=f'P1-{i+1:03d}' if key=='first_purchase' else f"P2-R{r['source_row']}"
  mapped=[n for n in node_rows if pid in n['purchase_id'].split(' | ')]
  m=next((m for m in measurement_rows if m['purchase_id']==pid),None)
  risk='현장 조정' if mapped else '측정 불필요'
  action='현장 상황에 따라 위치·고정·길이를 유연하게 조정. 강제 끼움/기판 홀 확대는 하지 않음' if mapped else '도구·소모품·예비/외부 사용품은 CAD에 강제 장착하지 않음'
  evidence='이전 CAD/상품 자료 (실측 기록 없음)' if mapped else '구매 기록'
  dims='';use='CAD 적용/재료 후보' if mapped else '미장착·외부 사용·소모품'
  if pid in {'P1-006','P1-012','P1-014','P2-R51'}:
   risk='필수 확인';action=next(c['accept'] for c in checks if pid in c['purchase_id'])
  if pid=='P1-002':action='P2-R83 C715 2280으로 교체됨. 예비 2242를 현재 슬롯에 강제 장착하지 않음';use='교체된 예비품'
  if pid=='P1-027':action='P2-R22 190W 승압기를 현재 배치에 사용. MT3608 전부 장착할 필요 없음';use='미사용 예비'
  if pid=='P1-015':action='현재 FHAC0002LXN(P2-R26) 형상 사용. 동일 기능의 예비 홀더';use='대체/예비'
  if pid=='P2-R39':action='BNS-30 탭핑 나사와 M2/M2.5 기계나사를 구분. 키트라는 이유로 모든 CAD 체결품을 보유했다고 보지 않음';risk='현장 조정'
  if m:risk=m['decision'];action=m['required_action'];evidence=m['evidence_type'];dims=m['normalized_mm']
  if pid in {'P1-018','P2-R78'}:use='선택 재고 외곽 STEP / 본체 미장착'
  if pid=='P2-R54':use='규격 참고 / 소형 실물 미확인'
  if pid=='P2-R42':dims='101 × 41 × 25 (이전 상품 근거)'
  if pid=='P2-R83':dims='80 × 22 × 2.5 (공식 명목 카드 외곽)'
  rows.append(dict(number=len(rows)+1,purchase_id=pid,round='1차' if key=='first_purchase' else '2차',source_row=r['source_row'],item=r['item'],model=r['model'],quantity_source=r.get('quantity',r.get('quantity_cell')),measurement_number=m['number'] if m else None,evidence_type=evidence,dimensions_mm=dims,decision=risk,action=action,cad_usage=use,cad_nodes=len(mapped),node_examples='; '.join(n['node'] for n in mapped[:4]),source_url=r['url'],quantity_caution='수량 셀과 상품명 묶음 수량을 임의 곱셈하지 않음'))
assert len(rows)==93 and len({r['purchase_id'] for r in rows})==93
assert len(measurement_rows)==13 and sum('실측' in m['evidence_type'] and m['evidence_type']!='미실측' for m in measurement_rows)==10
dump('parts-numbered.json',rows)
for fn,records in [('parts-numbered.csv',rows),('measurement-register.csv',measurement_rows),('cad-node-map.csv',node_rows)]:
 if records:
  with (D/fn).open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
dump('mapping-check.json',dict(purchase_rows=len(rows),first_purchase=29,second_purchase=64,measurement_records=13,physical_measurement_records=10,source_measurement_number_10='원본에 없음',webcam_source_correction='치수표 1차22행 → 원본 1차7행 P1-003; 모델명으로 대조',medium_typo_normalization='25m → 25mm (문맥에 따른 단위 오기 정정)',cad_nodes=len(node_rows),unmapped_nodes=0 if len(node_rows)==len(manifest) else None))
print('Mapped:',len(rows),'purchases;',len(measurement_rows),'measurements;',len(node_rows),'CAD nodes')

