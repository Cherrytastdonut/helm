# 전체 CAD·ZIP 다운로드와 복원

[현재 안내 PDF](../drawings/procurement-review/HELM_PROCUREMENT_CHANGE_GUIDE_KO.pdf), [A3 윤곽 PDF](../drawings/procurement-review/HELM_CURRENT_FLAT_PROFILES_REVIEW_A3.pdf), [개별 STEP/DXF](../cad/procurement-review/)는 저장소에서 직접 받습니다.

1. GitHub의 Code → Download ZIP 또는 git clone으로 저장소 전체를 받습니다.
2. 압축을 풀고 README.md·tools·archives가 있는 폴더로 이동합니다.
3. Python 3.9 이상에서 다음 명령을 실행합니다. 복원에는 추가 패키지가 필요하지 않습니다.

```bash
python tools/restore_archives.py --archive procurement-review-20261001 --extract
```

Windows에서는 `python` 대신 `py`를 사용할 수 있습니다. 기본 archive도 최신 구매품 반영본입니다. 과거 원본까지 복원하려면 `--all --extract`를 사용합니다.

복원 폴더: `downloads/procurement-review-20261001/HELM_PROCUREMENT_REVIEW_20261001/`

| ZIP 내부 | 내용 |
|---|---|
| CAD/HELM_PROCUREMENT_FULL_REVIEW.step | 4,078개 노드 전체 모델, 약 737 MB |
| EDITABLE/HELM_WORK/ | 현재 BREP 4,078개·코어·manifest/plates/ports/wires/joints |
| FABRICATION_STEP/ | 제작 대상 128개 STEP |
| PART_STEP/ | 변경 4개; 전원판은 위 폴더와 중복 |
| DXF_REVIEW_ONLY/ | 확인된 일정 두께 윤곽 20개 |
| DRAWINGS/ | 안내 6쪽·A3 윤곽 20쪽 |
| DATA/ | 변경·검증·출력·가정 목록 |
| SOURCE/ | 생성·검사 코드와 제조사 열화상 STEP |
| DOCS/·EVIDENCE/ | 설명·자료 요청·보존한 사진 |

합친 전달용 ZIP은 `downloads/HELM_PROCUREMENT_CAD_REVIEW_20261001.zip`입니다. 각 조각은 개별 ZIP이 아니며 하나만 압축 해제하거나 확장자를 바꾸지 않습니다. 파일별 SHA-256은 ZIP의 PACKAGE_CONTENTS.json에 있습니다.

충분한 디스크 공간을 확보하고 기존 작업본에 덮어쓰지 않습니다. 전체 STEP은 여는 데 시간이 걸립니다. 편집 캐시는 원래 네이티브 피처 이력과 다릅니다. [현재 제작 보류](00-status.md)를 먼저 확인합니다.

과거 원본 id: `v13-reissue-20260929`, `ser0063-review-20260930`, `purchase-inputs-20260930`. [아카이브 해시](../archives/manifest.json).
