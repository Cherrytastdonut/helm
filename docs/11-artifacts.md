# 수정 CAD와 파일 복원

현재 검토본은 **MEASURED_LAYOUT_20261006**입니다. 전달한 전체 ZIP은 276,698,242바이트, SHA-256 `232775f755a6a90daa2d70e75ed116a9935b29ed06ccb87935e140dc86a2117a`입니다. 전체 STEP·편집 BREP·128개 제작 STEP·20개 DXF·부품표·도면·원본 치수표를 포함합니다.

GitHub에는 기존 전체 기준본과 변경 BREP·전체 편집 메타데이터를 담은 4.1MB 델타를 함께 보관합니다. **델타만으로 전체 CAD가 되지는 않습니다.** 다음 두 ZIP을 결합하면 편집 파일 3,897개의 해시를 모두 대조합니다.

```bash
python tools/restore_archives.py --archive procurement-review-20261001
python tools/restore_archives.py --archive measured-editable-delta-20261006
python cad/measurements-20261006/source/restore_measured.py --baseline downloads/HELM_PROCUREMENT_CAD_REVIEW_20261001.zip --delta downloads/HELM_MEASURED_EDITABLE_DELTA.zip --output downloads/measured
```

STEP 재생성은 [도출 과정](12-reproduce.md)을 따릅니다. STEP 헤더의 생성 시각 등은 재생성 때 달라질 수 있습니다. 편집 BREP 해시와 형상·치수 대조로 복원을 판단합니다. 델타 내부의 예전 내보내기 기록 대신 [최신 STEP 검사](../data/measurements-20261006/FULL_STEP_READBACK.json)를 참고합니다.

[부품번호·실측 적용표](../data/measurements-20261006/HELM_부품번호_실측적용표.xlsx) · [도면](../drawings/measurements-20261006/) · [재생성 소스](../cad/measurements-20261006/source/) · [백업 조각과 해시](../archives/manifest.json)

원본 LICENSE와 출처를 보존했습니다. GitHub Release/LFS 업로드나 재단·통전 승인을 의미하지 않습니다.
