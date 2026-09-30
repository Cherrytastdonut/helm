# CAD·도면 도출 과정과 재현

원본을 [복원](11-artifacts.md)한 뒤 별도 작업본을 사용합니다. 수정 스크립트를 이미 수정한 작업본에 반복 실행하면 높이 이동이 중복될 수 있습니다.

## V13 재출력

원본 폴더에서 다음 순서입니다. 저장소 루트에서 곧바로 실행하는 명령이 아닙니다.

```bash
python HELM_V13_WORK/export_latest.py
python HELM_V13_WORK/validate_final_step.py
python HELM_V13_WORK/prepare_drawings.py
python HELM_V13_WORK/drawings.py
python finalize_generated_release.py
```

[원 실행 순서](../history/v13-reissue-20260929/BUILD_SEQUENCE_KO.md) · [환경 기록](../history/v13-reissue-20260929/GENERATION_RECORD.json)

사용 이력: Python 3.12.14, CadQuery 2.7.0, cadquery-ocp 7.8.1.1.post1, NumPy 2.3.5, ezdxf 1.4.4, ReportLab 4.4.9, PyMuPDF 1.26.6, Pillow 12.3.0, g++. 최신 권장 버전이라는 의미는 아닙니다.

## SER0063 검토 수정

[source](../cad/ser0063-review/source/)는 실행 당시 코드 보존본입니다. 자동 설치 패키지가 아니며 ROOT/W/OUT, 원본 V13 캐시, 구매 입력, 렌더러·한국어 폰트 경로를 맞춰야 합니다.

1. 매번 깨끗한 V13 HELM_V13_WORK를 복원합니다.
2. revise_servo.py: 모터/판/지지부 수정·내보내기.
3. validate_review.py: 새 체결부·9자세·17개 부품/카메라 재읽기·미리보기.
4. validate_full_step.py: 전체 제품 구조·교체 4개 형상 확인.
5. 검사 결과의 미해결 항목을 문서에 반영합니다.
6. make_review_guide.py: 구매 입력·폰트 준비 후 PDF 작성, 모든 페이지 렌더링 검수.
7. package_review.py: 해시와 ZIP·CRC 확인.

BREP/STEP → 제작 대상·기준면·외곽·두께·홀/홈 추출 → 개별 STEP → 일정 두께 관통 윤곽만 DXF → 배치·치수·연결 데이터로 PDF → 재읽기·시각 검수 → 동일 리비전 패키징 순서입니다.

형상 변경 후 오래된 메시/이미지를 그대로 사용하지 않습니다. 이번 검토는 변경 노드를 실제 BREP에서 새로 메시화하고 미변경 노드에만 과거 캐시를 사용했습니다. 과거 수정 스크립트를 전부 일괄 실행하지 않습니다.
