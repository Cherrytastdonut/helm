# HELM 자율점검 로봇

**최신: MEASURED_LAYOUT_20261006 · 3,888개 노드 · 재단·통전 승인 전 검토본입니다.** 구매 93개 항목, 치수표 13개 기록, CAD 노드를 연결하고 26개 형상에 치수와 배치를 반영했습니다.

1. [현재 상태](docs/00-status.md)와 [부품번호·실측 적용표](data/measurements-20261006/HELM_부품번호_실측적용표.xlsx).
2. [실측 반영·제작 가이드 6쪽](drawings/measurements-20261006/HELM_MEASURED_BUILD_GUIDE_KO.pdf).
3. [A3 1:1 윤곽 검토도 20쪽](drawings/measurements-20261006/HELM_CURRENT_FLAT_PROFILES_REVIEW_A3.pdf)와 [섀시 기준 4홀 대조 양식](drawings/measurements-20261006/HELM_CHASSIS_4HOLE_CHECK_A3.pdf).
4. [전체 CAD 백업 복원](docs/11-artifacts.md)과 [필수 확인·현장 조정](docs/15-needed-measurements.md).

| 자료 | 바로가기 |
|---|---|
| 모든 구매 항목 | [93개 번호 CSV](data/measurements-20261006/parts-numbered.csv) · [치수 원문과 적용](data/measurements-20261006/measurement-register.csv) |
| 최신 CAD·설계 범위 | [이번 반영 내용](docs/16-measured-layout.md) · [재생성 코드](cad/measurements-20261006/source/) |
| 제작 준비 | [재단](docs/04-fabrication.md) · [조립](docs/05-assembly.md) · [전기](docs/06-electrical.md) |
| 검사와 미확정 사항 | [검증 범위](docs/08-validation.md) · [겹침 24쌍·회전 10쌍](docs/10-open-items.md) |
| 기존 근거 | [상품 사진 대조](docs/14-product-photo-review.md) · [1차 구매](docs/parts/first-purchase.md) · [2차 구매](docs/parts/second-purchase.md) |
| 이전 작업 | [아카이브](archives/README.md) · [이력](docs/09-history.md) · [FlutterFlow 초안](docs/13-flutterflow-ai.md) |

보유 판재는 **5T 포맥스 600×900 mm 2장**입니다. 작은 칩 개별 측정은 필요하지 않으며, 고정 부품의 홀·배선·스페이서는 현장에서 조정합니다. 혼·기준 홀·큰 장착 홀·범퍼 기능은 먼저 확인해야 합니다. 2차 구매품을 모두 설치할 필요는 없습니다.

`LIB_SER0063.zip`은 모터 몸체 CAD입니다. 혼은 별도입니다. 형상 생략은 체결 완료나 간섭 해결을 뜻하지 않습니다. 과거 FINAL/PASS 또는 디자인·검색 불필요는 당시 확인한 본체와 검사 범위에 한정하며 최신 [상태 JSON](data/project-status.json)을 우선합니다.
