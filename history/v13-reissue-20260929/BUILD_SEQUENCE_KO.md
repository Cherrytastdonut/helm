# CAD 및 설계도 재생성 순서

전체 폴더를 복사한 작업본에서 아래 명령을 순서대로 실행하세요. Python, CadQuery/OpenCascade, NumPy, ezdxf, ReportLab, PyMuPDF, Pillow와 g++가 필요합니다. 사용한 버전은 GENERATION_RECORD.json에 있습니다.

```bash
python HELM_V13_WORK/export_latest.py
python HELM_V13_WORK/validate_final_step.py
python HELM_V13_WORK/prepare_drawings.py
python HELM_V13_WORK/drawings.py
python finalize_generated_release.py
```

첫 단계는 후보 STEP을 생성하고 두 번째 단계가 통과하면 HELM_V13_LATEST.step으로 확정합니다. prepare_drawings.py는 제작 부품 STEP·DXF·치수 데이터를 출력합니다. 현재 형상을 유지하는 재출력에서는 기존 메시·뷰 캐시를 재사용합니다. 형상을 바꾼 작업본에서는 HELM_V13_DRAWINGS/DATA/mesh.npz와 VIEWS 폴더의 캐시를 지우고, manifest의 경계 좌표·면·솔리드 개수 및 INPUT_BREP_SHA256.json을 새 기준에 맞게 갱신한 뒤 필요한 형상·간섭·가동 검사를 수행해야 합니다.

drawings.py는 통합 PDF와 표를 생성합니다. finalize_generated_release.py는 가공 파일과 PDF를 검사하고 모든 페이지를 200 dpi PNG로 출력합니다. 시각 검토 완료를 DRAWING_VALIDATION.json의 visual_review에 기록한 다음 package_regenerated_release.py로 ZIP을 만듭니다.

HELM_V13_WORK에는 과거 수정 코드도 보존되어 있습니다. 위 목록 외의 수정 스크립트 전체를 일괄 실행하지 마세요. 현재 수정 없이 재출력하는 경우 기존 기준 파일과 검증 범위를 그대로 유지합니다.
