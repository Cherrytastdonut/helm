# CAD·도면 도출과 재현

[현재 ZIP](11-artifacts.md)은 전체 STEP과 같은 리비전 BREP 편집 상태를 보존합니다. 이전 수정 스크립트를 현재 스냅샷에 반복 적용하지 않습니다.

최신 ZIP을 복원한 `HELM_PROCUREMENT_REVIEW_20261001` 폴더에서:

```bash
python SOURCE/export_snapshot.py --work EDITABLE/HELM_WORK --step CAD/HELM_REEXPORTED.step
python SOURCE/export_current_parts.py --output .
python SOURCE/validate_procurement_step.py --output .
python SOURCE/make_procurement_guide.py --output . --font /path/to/NotoSansKR-Regular.ttf
```

첫 명령은 현재 BREP를 새 이름으로 내보내며 원본을 덮어쓰지 않습니다. STEP 검사의 기본 파일은 `CAD/HELM_PROCUREMENT_FULL_REVIEW.step`이고 `--step`으로 변경할 수 있습니다. PDF는 PREVIEWS·DATA와 한국어 TTF가 필요합니다.

## 변경을 처음부터 재현

1. V13 원본 HELM_V13_WORK를 별도 복원합니다.
2. 보존한 SER0063 source/revise_servo.py의 경로를 맞춰 한 번 적용하고 검증 단계의 메타데이터 수정을 반영합니다. 현재 복원 보조 스크립트는 보존된 SER0063 manifest와 모든 이름·경계를 대조한 뒤 해당 메타데이터를 복구합니다.
3. 원래 4,152개 입력 manifest의 SHA-256이 `0b7b8cb640d072559c6d5957bcc3574d5be0e502dfbf6f83cc1efa5b37bced69`인지 확인합니다.
4. `revise_procurement.py --input-work ... --thermal-step ... --output ...`를 빈 출력 폴더에 실행합니다.
5. `validate_procurement.py --output ... --servo-report ...`로 변경부와 9자세를 검사합니다.
6. 제작 부품과 전체 STEP을 재읽기하고 변경 노드는 새로 메시화합니다. `render_procurement.py --help`의 원본 메시·manifest·렌더러·SER0063 기록 경로가 필요합니다.
7. PDF 전 페이지를 렌더링해 확인하고 보류 목록·문서를 동기화합니다. 파일 해시·ZIP CRC·분할 해시 검사 후 백업합니다.

BREP/STEP → 제작 대상·기준면·두께 확인 → 3D STEP → 일정 두께 관통 윤곽만 DXF → 배치·치수·보류 상태 PDF → 재읽기·시각 검수 → 동일 리비전 ZIP 순서입니다. 깊이 형상을 평판으로 납작하게 만들지 않습니다.

[현재 소스](../cad/procurement-review/source/) · [과거 V13 순서](../history/v13-reissue-20260929/BUILD_SEQUENCE_KO.md). 현재 스냅샷 재출력에는 과거 변경 스크립트의 재실행이 필요하지 않습니다. 일부 복원 보조 코드는 당시 작업 폴더 경로가 있으므로 경로를 맞춰야 합니다.

사용 환경: Python 3.12.14, CadQuery 2.7.0, cadquery-ocp 7.8.1.1.post1, NumPy 2.3.5, ezdxf 1.4.4, ReportLab 4.4.9, PyMuPDF 1.26.6, Pillow 12.3.0, g++. 권장 최신 버전이라는 의미는 아닙니다.
