# 구매품 사진·제조사 자료 대조

확인일 2026-10-01 / 적용 리비전 PROCUREMENT_REVIEW_20261001.

구매 링크, 제공된 XLSX의 구매측 판매 페이지 캡처, 제조사 치수·3D 파일을 함께 대조했습니다. 상품 사진·선택 옵션은 배송된 개체의 실측 기록과 구분합니다. 비교견적의 다른 판매자 제품을 추가 재고로 합산하지 않습니다.

| 구매 부품 | 확인한 근거 | CAD 처리 | 남은 범위 |
|---|---|---|---|
| C715, 2차 83행 | 512GB 선택·K512GM2SP0-C7T, 명목 80×22×2.5 mm | 2242 참조 6개·선택형 2230 SSD/나사 제거, 실제 2280 슬롯 배치 | PCB·키·칩은 명목 형상, 고정나사·실물 끼움 |
| CP003, 79행 | 녹색 몸체·투명 덮개, 100×45×33 mm, 입력 2/출력 8 | 실제 외곽 크기 공간 모델 적용, 전원판의 옛 홀·하단 간섭 수정 | 고정홀·덮개 개방·전선 출구·내부 연결 |
| 열화상 220565, 25행 | SEENGREAT MLX90640-D55, 제조사 STEP | 기존 215개 형상 경계·부피 대조 후 유지, PH2.0 정보 정정 | 결합 플러그 방향·케이블 |
| SER0063, 30행 | 첨부 모터 STEP, 25T/5.9 mm 축·혼 동봉 | 모터 2개 교체 유지, 축척 변경 없음 | 사용할 혼의 홀·두께·장착 높이 |
| MG995/MG996 브래킷, 78행 | 금속 프레임과 체결품·자 대조 사진 | 치수 없이 호환 브래킷을 만들어 넣지 않음 | 안쪽 폭·홀·두께·축 지지부 |
| NEXT-505UHP, 42행 | 흰 몸체·4포트·일체형 케이블, 101×41×25 mm | 기존 모델명·외형 유지 | USB/DC 포트·배선 치수 |
| 네이쳐툴 소형/중형, 54-55행 | 소형 각 면 2홀, 중형 각 면 3홀·보강 돌기 | 기존 가정을 실측 완료로 승격하지 않음 | 다리 길이·폭·두께·홀·돌기 |
| 혼합 볼트 세트, 53행 | M3/M4/M5 볼트·일반 너트·와셔 라벨 | 일반 M4 너트 존재 확인, 실제 길이별 수량은 별도 | 머리·너트·와셔 높이와 재고 |
| M4 나일론 너트, 75행 | M4 선택과 나일론 링 | 일반 너트 3.2 mm와 같은 높이로 가정하지 않음 | 높이·유효 체결 길이 |
| BNS-30, 39행 | 제조사 탭핑 나사·케이블 홀더 구성 | M2/M2.5 기계나사·너트 보유 증거로 쓰지 않음 | 실제 소형 기계나사 재고 |
| Bosch 2607010529, 60행 | 2/3/4/5/6/8 mm 구성 | D4.5 도면과 공구 차이를 보류 표시 | 설계·가공법 함께 확정 |

SSD는 원본 NVIDIA `OFFICIAL_JETSON_0564_Solid` 소켓과 `OFFICIAL_JETSON_0705_Solid` 끝단 지지부 기준입니다. 42 mm 카드를 예전 위치에서 80 mm로 늘리기만 하면 받침판과 겹칩니다. 카드 진입부·키는 명목 결합 형상이며 정확한 공급사 PCB 제조 도면은 아닙니다.

CP003의 고정홀·단자 좌표를 사진 비율로 추정해 가공 치수로 쓰지 않았습니다. 입력 2/출력 8에 이전 14개 논리 접속점을 임의 배정하지 않습니다. 기존 부스바 좌표와 관련 경로는 무효 처리했습니다.

열화상 제조사 STEP은 215개 형상 모두 경계 오차 0.001 mm 미만·부피 차이 0.01 mm³ 미만으로 일치했습니다. `HAT-V1.2` 파일명만으로 다른 구매품으로 판정하지 않습니다. 기존 보드 커넥터 접점 피치는 2 mm이며, 잘못된 2.54 mm 결합 플러그 프록시와 포트 표기를 정리했습니다. 표시 색은 실물 도장색을 보증하지 않습니다.

## 보존한 사진

[캡처 셀·원본 미디어·해시](../data/purchases/product-evidence-20261001.json)

| 부품 | 사진 |
|---|---|
| SSD·단자대·열화상 | [C715](../assets/purchase-evidence/c715-512gb.png) · [CP003](../assets/purchase-evidence/szh-cp003.png) · [220565](../assets/purchase-evidence/seengreat-220565.png) |
| 모터·브래킷 | [SER0063](../assets/purchase-evidence/ser0063.png) · [브래킷](../assets/purchase-evidence/mg995-bracket.png) · [자 대조 상세](../assets/purchase-evidence/mg995-detail.jpg) |
| 허브·꺽쇠 | [NEXT](../assets/purchase-evidence/next-505uhp.png) · [소형](../assets/purchase-evidence/naturetool-small.png) · [중형](../assets/purchase-evidence/naturetool-medium.png) |
| 체결품 | [혼합 세트](../assets/purchase-evidence/fastener-kit.png) · [M4 나일론](../assets/purchase-evidence/m4-nyloc.png) · [스페이서](../assets/purchase-evidence/m3-spacers.png) · [BNS-30](../assets/purchase-evidence/bns30.png) |
| 공구 | [Bosch](../assets/purchase-evidence/bosch-drills.png) |

## 제조사·판매자 출처

- [KLEVV C715](https://www.klevv.com/ken/products_details/ssd/Klevv_Cras_C715.php)
- [NVIDIA 2280 슬롯](https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/latest/hardware_layout.html)
- [CP003 규격표](https://www.devicemart.co.kr/goods/view_contents?no=12498800&setMode=pc&zoom=1)
- [SEENGREAT 220565](https://seengreat.com/product/209/thermal-camera) · [STEP·핀 기능](https://seengreat.com/wiki/88/thermal-camera-mlx90640-d55)
- [DFRobot SER0063](https://www.dfrobot.com/product-2787.html)
- [MG995 브래킷](https://m.intopion.com/goods/view?no=3831971)
- [NEXT 제조사](https://www.ez-net.co.kr/sub/sub01_01_view.php?idx=1818&offset=1440) · [판매 규격](https://www.ssg.com/item/itemView.ssg?itemId=1000034199687)
- [ROBOTIS BNS-30](https://en.robotis.com/shop_en/item.php?it_id=903-0212-000)
- [Bosch 비트 구성](https://www.bosch-professional.com/in/en/pro-metal-hss-g-twist-drill-bit-set-3089834-ocs-ac/)

일부 링크의 접근 제한 때문에 제공된 원본 캡처를 함께 사용했습니다. 유사 상품 치수를 해당 구매품의 확정 치수로 옮기지 않습니다.
