from pathlib import Path
import json,hashlib,zipfile,shutil,collections
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output/HELM_SER0063_INTEGRATION_REVIEW';D=OUT/'DATA'
v=json.loads((D/'EXTENDED_VALIDATION.json').read_text());full=json.loads((D/'FULL_STEP_READBACK.json').read_text())
assert not v['new_hardware_hits']
assert hashlib.file_digest((OUT/'CAD/HELM_SER0063_FULL_REVIEW.step').open('rb'),'sha256').hexdigest()==full['sha256']
assert len(list((OUT/'PART_STEP').glob('*.step')))==17
assert len(list((OUT/'DXF_REVIEW_ONLY').glob('*.dxf')))==7
pairs={}
for pose in v['motion_samples']:
    for hit in pose['hits']:
        assert 'LIDAR' not in hit['a']+hit['b'],hit
        key=(hit['a'],hit['b']);pairs.setdefault(key,[]).append((pose['pan_deg'],pose['tilt_deg'],hit['volume_mm3']))
role={'CUSTOM_TILT_CHEEK_LEFT':'카메라 왼쪽 회전 측판','CUSTOM_PAN_ARM_RIGHT':'오른쪽 고정 지지판','CUSTOM_PAN_YOKE':'팬 회전 바닥판'}
def label(n):
    if n in role:return role[n]
    if n.startswith('CAM_L_LEFT_'):return '왼쪽 L브래킷 체결품'
    if n.startswith('CAM_L_RIGHT_'):return '오른쪽 L브래킷 체결품'
    if n.startswith('CUSTOM_TILT_CORNER_LEFT'):return '왼쪽 카메라 코너 체결품'
    if n.startswith('CUSTOM_TILT_CORNER_RIGHT'):return '오른쪽 카메라 코너 체결품'
    return n
lines=['# 재단 확정 전 남은 항목','',
'현재 모델은 조립 검토본입니다. SER0063 몸체·장착판·새 지지 체결부와 라이다 받침의 확인된 간섭은 수정했습니다. 아래 기존 카메라 체결부의 겹침이 남아 있으며, 0° 자세에서도 겹침이 있으므로 단순히 회전 각도만 줄여 해결됐다고 볼 수 없습니다.','',
'## 1. 실물 확인이 필요한 자료','',
'- SER0063 동봉 혼: 위·옆 사진, 구멍 중심 간격, 판 두께, 축에 끼운 상태의 높이.','- MG995/MG996 금속 브래킷: 위·옆 사진, 내측 폭, 구멍 중심 간격, 판 두께.','- 사용 가능한 M4 너트·와셔 실물과 치수. 현재 CAD는 일반 너트 높이 3.2 mm, 와셔 두께 0.8 mm 가정입니다. 보유 풀림방지 너트로 바로 대체하면 여유가 달라집니다.','- 촬영 시 자를 같은 평면에 놓아 주세요. 자 사진만으로 충분한 가공 공차를 확정할 수 없으면 구멍 간격과 두께의 실측값이 필요합니다.','',
'## 2. 남은 회전 간섭 위치','',
'CAD 트리에서 아래 이름을 검색해 해당 부품만 표시하면 위치를 찾을 수 있습니다. 표의 각도는 팬/틸트 순서이며, 검사한 각도일 뿐 허용 동작 범위가 아닙니다. 겹침 판정 기준은 0.5 mm³ 초과입니다.','',
'| 위치 | CAD 부품 A / B | 발견 각도 (도) | 최대 겹침 (mm³) |','|---|---|---|---:|']
for (a,b),hits in sorted(pairs.items()):
    angles=', '.join(f'{pa}/{ta}' for pa,ta,_ in hits)
    lines.append(f'| {label(a)} / {label(b)} | `{a}` / `{b}` | {angles} | {max(x[2] for x in hits):.3f} |')
lines+=['','볼트 돌출 길이·너트 위치·실제 브래킷을 먼저 확인한 뒤 짧게 가공하거나 배치를 수정해야 합니다. 실물 체결품이 확인되지 않은 상태에서 볼트 길이를 확정하지 않았습니다. 남은 혼 연결을 먼저 확정하면 측판 간격과 체결 위치가 함께 바뀔 수 있습니다.','',
'## 3. 판재와 가공','',
'5T 포맥스는 구매 목록에 있는 재료입니다. 모터 플랜지 옆의 좁은 구간과 너트가 직접 누르는 부분은 구조 검증이 끝나지 않았습니다. 보유 금속 브래킷의 호환성을 확인해 하중을 받는 연결에 사용할 수 있는지 판단해야 합니다. 현재 1:1 도면은 종이 대조용입니다. 모든 구멍은 도면 직경과 실제 보유 비트를 대조해야 합니다. 임의로 다른 구경의 구멍을 뚫거나 강제로 끼우는 지침이 아닙니다.','',
'## 4. 배선과 전원','',
'서보 2개와 C920의 움직이는 배선은 재설계 대기입니다. 새 서보의 제조사 전원 범위는 5-8.4 V입니다. 기존 5 V 변환기의 공유 부하와 두 서보 동시 동작 전류, 실제 단자 극성, 퓨즈를 대조한 뒤 통전해야 합니다. 기존 4.8 V 표기를 사용하지 않습니다. 제조사 출처: https://www.dfrobot.com/product-2787.html','',
'## 5. 전체 구매품 일치 여부','',
'구매 목록에 없는 ADS1115, 특수 길이 스페이서, 일부 소형 체결품·범퍼 스프링 등의 기존 CAD 가정이 남아 있습니다. SZH-CP003 단자대와 C715 SSD 등 다른 실제 구매품의 기구 반영도 후속 확인이 필요합니다. 전체 시스템의 구매품 일치 검증이나 최종 제작 승인을 완료했다는 의미가 아닙니다.']
(OUT/'OPEN_ISSUES_KO.md').write_text('\n'.join(lines)+'\n')
for n in ('validate_full_step.py','package_review.py'):shutil.copy2(ROOT/n,OUT/'SOURCE'/n)
files=[p for p in OUT.rglob('*') if p.is_file() and not any(x.startswith('.') for x in p.relative_to(OUT).parts) and p.name!='PACKAGE_CONTENTS.json']
manifest={'package_status':'REVIEW_ONLY_NOT_FOR_FABRICATION','files':[{'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()} for p in sorted(files)]}
(OUT/'PACKAGE_CONTENTS.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
files.append(OUT/'PACKAGE_CONTENTS.json')
dest=ROOT/'output/HELM_SER0063_CAD_REVIEW_20260930.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for p in sorted(files):z.write(p,OUT.name+'/'+str(p.relative_to(OUT)))
print('Zip written',dest.stat().st_size,flush=True)
with zipfile.ZipFile(dest) as z:
    bad=z.testzip();assert bad is None,bad
    assert len(z.infolist())==len(files)
print(json.dumps({'zip':str(dest.resolve()),'bytes':dest.stat().st_size,'files':len(files),'unique_unresolved_motion_pairs':len(pairs),'crc':'PASS','sha256':hashlib.file_digest(dest.open('rb'),'sha256').hexdigest()}),flush=True)
