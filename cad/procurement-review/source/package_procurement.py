#!/usr/bin/env python3
"""Package a verified current review, preserving old archives and per-file hashes."""
from pathlib import Path
import argparse,json,hashlib,zipfile,shutil,re,posixpath
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();repo=a.repo.resolve();base=Path(__file__).resolve().parent

def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for n in ['restore_servo_geometry.py','revise_procurement.py','validate_procurement.py','export_current_parts.py','validate_procurement_step.py','render_procurement.py','make_procurement_guide.py','export_snapshot.py','package_procurement.py']:
 shutil.copy2(base/n,out/'SOURCE'/n)
(out/'SOURCE/NOTICES.md').write_text('''# Source provenance\n\nThe original HELM repository LICENSE is preserved. Third-party manufacturer CAD and product photos retain their original ownership/notices; no new license grant is asserted.\n\nSEENGREAT manufacturer model: https://seengreat.com/wiki/88/thermal-camera-mlx90640-d55\nDownloaded archive: https://seengreat.com/upload/file/88/Thermal%20Camera%20HAT-V1.2.zip\nStored STEP SHA-256: 5623f4aba40f299465756719ec73b9ef6cf0a6151bb10656da6c709e14155c59\n\nSER0063 derives from the user-supplied motor CAD, preserved under rigid transforms with no scaling. Earlier native chassis, NVIDIA and other manufacturer parts retain their source metadata in DATA/manifest.json. Evidence captures come from the supplied purchase workbook and identified seller. See DOCS/14-product-photo-review.md and EVIDENCE/PROVENANCE.json.\n\nThe PDFs embed a subset of Noto Sans KR. The standalone font is not included; regeneration accepts a Korean TTF path.\n''')
for src,dst in [('DATA','data/procurement-review'),('SOURCE','cad/procurement-review/source'),('DRAWINGS','drawings/procurement-review'),('PREVIEWS','assets/procurement-review')]:
 target=repo/dst;target.mkdir(parents=True,exist_ok=True)
 for p in (out/src).iterdir():
  if p.is_file():shutil.copy2(p,target/p.name)
(out/'DOCS').mkdir(exist_ok=True)
for n in ['00-status.md','02-parts.md','03-cad.md','04-fabrication.md','05-assembly.md','06-electrical.md','08-validation.md','10-open-items.md','11-artifacts.md','12-reproduce.md','14-product-photo-review.md','15-needed-measurements.md']:
 s=(repo/'docs'/n).read_text()
 def link(m):
  t=m.group(1)
  if re.match(r'^[a-z]+:|^#',t):return m.group(0)
  return '](https://github.com/Cherrytastdonut/helm/blob/main/'+posixpath.normpath('docs/'+t)+')'
 (out/'DOCS'/n).write_text(re.sub(r'\]\(([^)]+)\)',link,s))
shutil.copytree(repo/'assets/purchase-evidence',out/'EVIDENCE',dirs_exist_ok=True);shutil.copy2(repo/'data/purchases/product-evidence-20261001.json',out/'EVIDENCE/PROVENANCE.json');shutil.copy2(repo/'LICENSE',out/'LICENSE')
(out/'README_KO.md').write_text('''# HELM 구매품 반영 CAD 검토 패키지\n\nPROCUREMENT_REVIEW_20261001 / 제작 승인 전.\n\n- DRAWINGS/HELM_PROCUREMENT_CHANGE_GUIDE_KO.pdf: 변경 내용·자료 요청·제작 순서 6쪽.\n- CAD/HELM_PROCUREMENT_FULL_REVIEW.step: 4,078개 노드 전체 모델.\n- EDITABLE/HELM_WORK: 같은 BREP 4,078개와 메타데이터. 제조사 네이티브 피처 이력은 아님.\n- FABRICATION_STEP: 현재 제작 대상 128개 입체 형상. 모두 포맥스 가공품이라는 뜻은 아님.\n- PART_STEP: 변경 4개. 전원판 1개는 위 폴더와 중복.\n- DXF_REVIEW_ONLY 및 DRAWINGS/HELM_CURRENT_FLAT_PROFILES_REVIEW_A3.pdf: 일정 두께 20개 윤곽. A3 1:1, 100 mm 기준선 확인. 재단 승인 전.\n- DATA: 변경·검증·출력·가정 목록. SOURCE: 실행 코드와 제조사 열화상 STEP. DOCS: 설명. EVIDENCE: 상품 사진.\n\nC715 512GB는 실제 2280 위치의 명목 결합 모델입니다. CP003는 100×45×33 mm 공간 외곽으로 적용했으며 상세 고정홀·단자는 아직 없습니다. 전원판 구형 홀과 하단 겹침을 수정했습니다. 열화상 제조사 본체 유지·PH2.0 정보 정정, 미구매 ADC 받침·체결품·잘못된 배선 제외를 반영했습니다.\n\n변경부 후보 29쌍에서 의도하지 않은 0.5 mm³ 초과 겹침 0건. 기존 카메라 9자세에서는 고유 15쌍이 남습니다. 혼·MG995 브래킷·꺽쇠·CP003 치수가 우선 필요합니다. DOCS/15-needed-measurements.md를 확인하세요. 전체 움직임·강도·회로·실물 작동을 승인한 파일이 아닙니다.\n\n보유 판재는 5T 포맥스 600×900 mm 2장입니다. 1.6 mm 분배기판이나 특수 입체 부품을 모두 이 판재에서 만들 수 있다는 뜻은 아닙니다. 깊이 형상은 STEP으로 확인합니다. 재고·공구·절삭 폭·강도·네스팅 확정 후 최종 도면을 다시 도출합니다.\n\nSOURCE/export_snapshot.py로 현재 BREP 스냅샷을 다시 내보낼 수 있습니다. 과거 revision 스크립트를 현재 작업본에 반복 적용하지 마세요. DOCS/12-reproduce.md에 실행 순서가 있습니다.\n\nPACKAGE_CONTENTS.json은 목록 자체를 제외한 모든 파일의 SHA-256을 기록합니다. 임시 공간 정리 후 입력 해시를 맞춰 재생성했으므로 현재 검증과 현재 패키지 해시를 사용합니다. 과거 FINAL/PASS는 당시 범위에만 해당합니다.\n\n저장소: https://github.com/Cherrytastdonut/helm\n''')
paths=sorted(p for p in out.rglob('*') if p.is_file() and p.name!='PACKAGE_CONTENTS.json' and '__pycache__' not in p.parts and p.suffix!='.pyc');inventory=out/'PACKAGE_CONTENTS.json';inventory.write_text(json.dumps({'revision':'PROCUREMENT_REVIEW_20261001','manufacturing_release':False,'hash_algorithm':'sha256','scope':'Every ZIP file except this inventory itself','files':[{'path':p.relative_to(out).as_posix(),'size_bytes':p.stat().st_size,'sha256':sha(p)} for p in paths]},ensure_ascii=False,indent=2)+'\n')
zp=out.parent/'HELM_PROCUREMENT_CAD_REVIEW_20261001.zip';assert not zp.exists(),'Refuse silent replacement of existing archive';print('Packaging',len(paths)+1,'files',flush=True)
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for i,p in enumerate(paths+[inventory],1):
  z.write(p,out.name+'/'+p.relative_to(out).as_posix())
  if i%500==0:print('Zipped',i,flush=True)
with zipfile.ZipFile(zp) as z:assert z.testzip() is None
size=zp.stat().st_size;digest=sha(zp);mp=repo/'archives/manifest.json';manifest=json.loads(mp.read_text());id='procurement-review-20261001';assert id not in {x['id'] for x in manifest['archives']};target=repo/'archives'/id;target.mkdir(exist_ok=False);parts=[]
with zp.open('rb') as f:
 i=0
 while True:
  b=f.read(manifest['part_size_bytes'])
  if not b:break
  i+=1;p=target/f'{zp.name}.part-{i:03d}';p.write_bytes(b);parts.append({'path':p.relative_to(repo).as_posix(),'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest['archives'].append({'id':id,'filename':zp.name,'size_bytes':size,'sha256':digest,'parts':parts});mp.write_text(json.dumps(manifest,indent=2)+'\n');report={'revision':'PROCUREMENT_REVIEW_20261001','zip_filename':zp.name,'zip_bytes':size,'zip_sha256':digest,'zip_crc':'PASS','zip_file_count':len(paths)+1,'split_parts':len(parts),'manufacturing_release':False};(repo/'data/procurement-review/PACKAGE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# CAD와 입력 자료 아카이브','','각 조각은 개별 ZIP이 아닙니다. 16 MiB 이하의 조각을 복원 도구로 합칩니다. 최신 기본값은 **procurement-review-20261001**입니다.','','| 원본 | MB | 분할 수 | SHA-256 |','|---|---:|---:|---|']
for e in manifest['archives']:lines.append(f"| {e['id']} | {e['size_bytes']/1e6:.1f} | {len(e['parts'])} | `{e['sha256']}` |")
lines+=['','최신본: `python tools/restore_archives.py --extract`','','과거 원본까지: `python tools/restore_archives.py --all --extract`','','검사만: `python tools/restore_archives.py --all --verify-only`','','[다운로드·내부 파일](../docs/11-artifacts.md). 최신 ZIP은 전체 수정 STEP·현재 BREP·128개 제작 STEP·20개 DXF·6쪽 안내·20쪽 A3 윤곽·근거·미확정 목록을 포함합니다. 재단·통전 승인본이 아닙니다.','','기존 아카이브와 해시는 그대로 보존합니다. GitHub Releases/LFS를 설정한 것은 아닙니다.'];(repo/'archives/README.md').write_text('\n'.join(lines)+'\n');print('ZIP CRC and split completed',json.dumps(report),flush=True)
