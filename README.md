# HELM 자율점검 로봇

구매 부품, 기구 CAD, 도면, 제작·조립 준비와 검증 기록을 정리한 저장소입니다.

> **최신: PROCUREMENT_REVIEW_20261001. 구매품 반영 검토본이며 재단·통전 승인 전입니다.** SSD·CP003 외곽·전원판 수정과 미구매 ADC 가정 제거를 전체 모델에 반영했습니다. 혼·브래킷 실측과 카메라 간섭 15쌍이 남아 있습니다.

![HELM 최신 검토 CAD](assets/procurement-review/FULL_REVIEW.png)

1. [현재 상태](docs/00-status.md)와 [확인한 상품 사진·근거](docs/14-product-photo-review.md).
2. [변경 안내 PDF 6쪽](drawings/procurement-review/HELM_PROCUREMENT_CHANGE_GUIDE_KO.pdf).
3. [A3 1:1 윤곽 검토도 20쪽](drawings/procurement-review/HELM_CURRENT_FLAT_PROFILES_REVIEW_A3.pdf).
4. [수정 전체 CAD·ZIP 다운로드](docs/11-artifacts.md).
5. [사용자께서 찾아 주실 치수·자료](docs/15-needed-measurements.md).

| 찾는 자료 | 바로가기 |
|---|---|
| 최신 부품 CAD | [제작 STEP 128개](cad/procurement-review/part-step/) · [변경 4개](cad/procurement-review/purchased-step/) · [DXF 20개](cad/procurement-review/dxf-review-only/) |
| 보유 부품 | [1차 29품목](docs/parts/first-purchase.md) · [2차 64행](docs/parts/second-purchase.md) · [적용 기준](docs/02-parts.md) |
| 설계·제작 | [CAD 해석](docs/03-cad.md) · [재단](docs/04-fabrication.md) · [조립](docs/05-assembly.md) · [배선](docs/06-electrical.md) |
| 검사·미해결 사항 | [검증 범위](docs/08-validation.md) · [간섭 위치](docs/10-open-items.md) |
| 원본·생성 과정 | [아카이브](archives/README.md) · [재현 방법](docs/12-reproduce.md) · [이력](docs/09-history.md) |
| 앱 입력 초안 | [FlutterFlow AI](docs/13-flutterflow-ai.md) · [실제 소프트웨어 현황](docs/07-software.md) |

보유 판재는 **5T 포맥스 600×900 mm 2장**입니다. 128개 형상이 모두 이 두 장에서 가공되는 것은 아닙니다. 1차는 이전 CSV, 2차는 새 XLSX이며 새 품목 전부를 장착할 필요는 없습니다.

`LIB_SER0063.zip`은 모터 몸체 CAD입니다. 혼·리드선은 별도 확인 대상입니다. 원본 CAD나 부품 이름이 있어도 구매·실측·실물 검증 완료를 뜻하지 않습니다.

[현재 상태 JSON](data/project-status.json)과 같은 리비전의 CAD·검증을 우선합니다. 과거 FINAL/PASS 또는 “수정·추가 검색 불필요”는 확인한 리비전·본체·범위에 한정합니다. 실제 부품과 차이가 확인되면 설계를 수정합니다.
