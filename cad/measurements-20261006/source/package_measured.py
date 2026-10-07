#!/usr/bin/env python3
"""Package the verified current CAD; exclude stale and intermediate artifacts."""
from pathlib import Path
import argparse,json,hashlib,zipfile
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve()
load=lambda n:json.loads((out/'DATA'/f'{n}.json').read_text())
hashfile=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
readback=load('FULL_STEP_READBACK');step=out/'CAD/HELM_MEASURED_COMPACT.step'
assert step.stat().st_size==readback['bytes'] and hashfile(step)==readback['sha256']
assert not readback['missing_model_nodes'] and len(readback['replacement_roundtrips'])==26
assert len(load('parts-numbered'))==93 and len(load('manifest'))==3888
for rel,digest in load('EDITABLE_SHA256').items():assert hashfile(out/rel)==digest,rel
docs=out/'DOCS';docs.mkdir(exist_ok=True)
header='# HELM 실측 반영 CAD\n\n**MEASURED_LAYOUT_20261006 · 3,888개 노드 · 재단·통전 승인 전 검토 조립체**\n\n'
(out/'README.md').write_text(header+'''실측 기록을 전체 CAD에 반영한 파일입니다. 구매 93개 행과 CAD 노드, 실측 기록 13개를 연결했습니다. 정확한 치수가 필요한 연결부와 회전부가 남아 있어 최종 제조 승인본은 아닙니다.

## 파일 열기

- `CAD/HELM_MEASURED_COMPACT.step`: 전체 조립체. STEP 지원 CAD에서 mm 단위로 여세요.
- `EDITABLE/HELM_WORK`: 전체 3,888개 BREP와 그룹·포트·배선·조인트 정보.
- `HELM_부품번호_실측적용표.xlsx`: 전체번호 93개, 실측기록 13개, 필수확인, 현장조정, CAD노드, 출처.
- `DRAWINGS/HELM_MEASURED_BUILD_GUIDE_KO.pdf`: 실측 적용·재단·조립 가이드 6쪽.
- `DRAWINGS/HELM_CURRENT_FLAT_PROFILES_REVIEW_A3.pdf`: 1:1 윤곽 검토도 20쪽.
- `DRAWINGS/HELM_CHASSIS_4HOLE_CHECK_A3.pdf`: 섀시 기준 4홀 1:1 종이 대조 양식.
- `FABRICATION_STEP`: 제작 후보 128개. 전부 포맥스 재단품은 아닙니다.
- `DXF_REVIEW_ONLY`: 일정 두께 윤곽 20개. 19개는 5T, 1개는 1.6T 분배기판 참조입니다.
- `PART_STEP`: 변경 형상 26개. `OPTIONAL_INVENTORY_STEP`의 3개는 선택 재고 외접 상자입니다.
- `EVIDENCE`: 받은 치수표 원본과 삽입 사진. `DATA`: 매핑·치수·검증 원자료.

## 재단 전에 확인할 내용

1. SER0063에 사용할 실제 혼의 홀·두께·장착 높이. 몸체는 재측정하지 않으셔도 됩니다.
2. 비상정지 스위치 장착 지름·5T 체결 길이·후면 돌출. 시험 끼움으로 확인 가능합니다.
3. 섀시 기준 4홀과 실제 판 두께·적층 높이. 1:1 종이와 실물이 맞으면 전체 재측정은 불필요합니다.
4. 범퍼 스위치 작동점·복귀 기능과 실제 스프링·가이드 보유 여부.

로커는 5T 자투리에 Ø20부터 시험하고, Ø27 테두리 치수로 본판을 뚫지 않습니다. MG995 프레임은 회전축·하중 부품으로 채택할 때만 내측·홀·두께를 확인합니다. 카메라 꺽쇠·체결품은 실제 혼을 정한 뒤 간섭 수정이 필요합니다.

고정 꺽쇠·CP003 홀은 실물 전사, 스페이서·전산볼트는 가조립 높이, 벨크로·EVA·배선은 현장 여유에 맞춰 조정합니다. 작은 칩은 개별 측정하지 않습니다. PCB 홀을 넓히거나 강제로 끼우지 않습니다.

## 남은 설계 범위

변경부 후보 80쌍 중 0.5 mm³ 초과 겹침 24쌍을 기록했으며 C920 내부 참조 4쌍을 포함합니다. 카메라 9개 자세 검사에는 고유 10쌍이 남아 있습니다. 상세 목록은 `DOCS/collision-register.md`입니다. 가정 체결품을 제거한 것은 간섭 해결이나 체결 완료가 아닙니다.

보유 판재는 **5T 포맥스 600×900 mm 2장**입니다. 최종 네스팅·강도·케이블 동작·결선은 아직 승인되지 않았습니다. 소형 꺽쇠·스프링·가이드·소형 나사·일부 받침과 분배기판의 실제 보유 여부도 구분되어 있습니다.

## 이전 자료와 적용 순서

같은 리비전의 CAD·치수표·검증을 우선합니다. 과거 FINAL/PASS와 “디자인 변경·검색 불필요”는 당시 확인한 본체와 범위에 한정합니다. 실제 부품과 다르면 해당 연결부를 수정합니다. `LIB_SER0063.zip`은 모터 몸체 CAD이며 혼은 포함하지 않습니다.

재생성은 현재 BREP에 `SOURCE/export_compact_snapshot.py`를 사용합니다. `build_measured_cad.py`는 변경 전 PROCUREMENT_REVIEW_20261001 입력에만 적용하며 현재 형상에 반복 적용하지 않습니다. compact STEP은 중복된 2D 곡선 표현을 생략한 3D STEP으로, 형상 축척을 줄인 파일이 아닙니다.

라이선스와 출처는 `LICENSE`, `SOURCE/NOTICES.md`에 보존했습니다. 전체 파일 SHA-256은 `PACKAGE_SHA256.json`에 있습니다.
''',encoding='utf8')
critical=load('critical-checks');field=load('field-adjustment')
s='# 필요한 확인과 현장 조정\n\n## 필수·조건부 확인\n\n| ID | 구매 ID | 부품 | 필요한 확인 | 완료 기준 |\n|---|---|---|---|---|\n'
for p in critical:s+='| '+' | '.join(str(p[k]).replace('|','/') for k in ['id','purchase_id','item','need','accept'])+' |\n'
s+='\n## 현장 조정\n\n| 대상 | 방법 | 제한 |\n|---|---|---|\n'
for p in field:s+='| '+' | '.join(p[k].replace('|','/') for k in ['item','method','limit'])+' |\n'
(docs/'required-checks.md').write_text(s,encoding='utf8')
v=load('VALIDATION');s='# 겹침과 미확정 체결부\n\nMEASURED_LAYOUT_20261006. 0.5 mm³ 초과 교집합을 기록했습니다. C920 내부 참조 형상·홀 없는 외곽 모델을 포함하므로 전부 실물 충돌로 단정하지 않습니다. 실제 고정부 재구성과 회전 검사가 필요합니다.\n\n## 변경부 정지 상태 24쌍\n\n| 형상 A | 형상 B | 부피 mm³ | 분류 |\n|---|---|---:|---|\n'
for h in v['changed_unintended_hits']:
 cl='C920 내부 참조 형상' if h['a'].startswith('COMMUNITY_C920') and h['b'].startswith('COMMUNITY_C920') else '실물 체결·홀·배치 확인 필요'
 s+=f"| {h['a']} | {h['b']} | {h['volume_mm3']:.3f} | {cl} |\n"
s+='\n## 카메라 자세 검사 고유 10쌍\n\n| 형상 A | 형상 B | 검사 자세 팬/틸트 ° | 최대 부피 mm³ |\n|---|---|---|---:|\n';pairs={}
for sample in v['camera_samples']:
 for h in sample['hits']:
  pair=tuple(sorted([h['a'],h['b']]));row=pairs.setdefault(pair,{'poses':[],'vol':0});row['poses'].append(f"{sample['pan_deg']}/{sample['tilt_deg']}");row['vol']=max(row['vol'],h['volume_mm3'])
for (x,y),r in sorted(pairs.items()):s+=f"| {x} | {y} | {', '.join(r['poses'])} | {r['vol']:.3f} |\n"
s+='\n팬 ±45°·틸트 ±20°는 검사한 자세일 뿐 승인 범위가 아닙니다. 연속 회전·공차·강도·가동 배선을 보증하지 않습니다.\n';(docs/'collision-register.md').write_text(s,encoding='utf8')
skip={'HELM_MEASURED_FULL_REVIEW.step','HELM_MEASURED_COMPACT.step.zip','PACKAGE_SHA256.json'}
files=[p for p in sorted(out.rglob('*')) if p.is_file() and not p.is_symlink() and p.name not in skip and not any(x in {'__pycache__','node_modules'} for x in p.parts) and not p.name.endswith('.inspect.ndjson')]
manifest={p.relative_to(out).as_posix():{'bytes':p.stat().st_size,'sha256':hashfile(p)} for p in files}
mp=out/'PACKAGE_SHA256.json';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');files.append(mp)
dest=out.parent/(out.name+'.zip')
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as z:
 for p in files:z.write(p,out.name+'/'+p.relative_to(out).as_posix())
with zipfile.ZipFile(dest) as z:assert z.testzip() is None;assert len(z.namelist())==len(files)
report={'filename':dest.name,'files':len(files),'bytes':dest.stat().st_size,'sha256':hashfile(dest),'full_step':readback,'manufacturing_release':False}
(out.parent/'HELM_MEASURED_PACKAGE_CHECK.json').write_text(json.dumps(report,indent=2)+'\n');print('PACKAGE VERIFIED',len(files),dest.stat().st_size,report['sha256'],flush=True)
