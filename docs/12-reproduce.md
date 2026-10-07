# CAD·도면 도출과 재현

[기준본 + 델타](11-artifacts.md)를 복원한 뒤 현재 BREP를 사용합니다. 수정 스크립트를 이미 수정된 입력에 반복 적용하지 않습니다.

저장소 루트에서 CadQuery/OCP·ezdxf·ReportLab이 설치된 Python으로 실행합니다.

```bash
python cad/measurements-20261006/source/export_compact_snapshot.py --work downloads/measured/EDITABLE/HELM_WORK --step downloads/measured/CAD/HELM_MEASURED_COMPACT.step
python cad/measurements-20261006/source/export_current_parts.py --output downloads/measured
python cad/measurements-20261006/source/export_changed_parts.py --output downloads/measured
python cad/measurements-20261006/source/validate_full_step.py --output downloads/measured --step downloads/measured/CAD/HELM_MEASURED_COMPACT.step
python cad/measurements-20261006/source/validate_measurements.py --output downloads/measured
python cad/measurements-20261006/source/make_profiles.py --output downloads/measured --font /path/to/Korean-Regular.ttf
python cad/measurements-20261006/source/make_guide.py --output downloads/measured --font /path/to/Korean-Regular.ttf
python cad/measurements-20261006/source/make_chassis_check.py --output downloads/measured --font /path/to/Korean-Regular.ttf
```

폰트 경로는 실제 한국어 TTF로 바꾸고 전체 STEP은 빈 새 파일명으로 내보냅니다. compact 방식은 중복 2D 곡선 표현을 생략하며 3D 축척을 줄이지 않습니다.

BREP → 기준면·두께 확인 → 제작 STEP → 일정 두께 관통 윤곽 DXF → 보류 범위를 표시한 PDF → 재읽기·시각 검수 → 같은 리비전 ZIP 순서입니다. 깊이 형상을 평판으로 납작하게 만들지 않습니다.

`build_measured_cad.py`는 수정 전 PROCUREMENT_REVIEW 입력에서 변경을 처음 적용한 이력 코드입니다. 현재 재출력은 위 방식으로 충분합니다. 부품표 생성 소스는 `make_workbook.mjs`이며, 제공된 Excel을 그대로 사용하셔도 됩니다.
