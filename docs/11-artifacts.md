# 자료 다운로드·복원

[최신 PDF](../drawings/ser0063-review/HELM_SER0063_CHANGE_GUIDE_KO.pdf), [V13 PDF](../drawings/v13-baseline/HELM_FULL_FABRICATION_AND_ASSEMBLY_DRAWING.pdf), [현재 개별 부품](../cad/ser0063-review/), [과거 개별 부품](../cad/v13-baseline/)은 저장소에서 직접 열거나 다운로드합니다.

## 전체 CAD 받기

1. GitHub의 **Code → Download ZIP**으로 저장소 전체를 받거나 git clone합니다.
2. 받은 ZIP을 풉니다. README.md, tools, archives가 보이는 폴더가 루트입니다.
3. Python 3.9 이상이 설치된 터미널에서 그 폴더로 이동합니다.
4. 아래 명령을 실행합니다. 추가 Python 패키지는 필요하지 않습니다.

```bash
python tools/restore_archives.py --all --extract
```

Windows Python 런처는 `py tools/restore_archives.py --all --extract`를 사용합니다. 충분한 디스크 공간을 확보하고 기존 작업 폴더에 덮어쓰지 않습니다.

| 목적 | downloads 아래 위치 |
|---|---|
| 최신 전체 CAD | ser0063-review-20260930/HELM_SER0063_INTEGRATION_REVIEW/CAD/HELM_SER0063_FULL_REVIEW.step |
| 최신 카메라 CAD | 위 CAD 폴더의 HELM_SER0063_CAMERA_REVIEW.step |
| V13 전체 CAD | v13-reissue-20260929/HELM_V13_DELIVERY/HELM_V13_LATEST.step |
| V13 편집 캐시·코드 | v13-reissue-20260929/HELM_V13_WORK/ |
| V13 전체 도면·페이지 PNG | v13-reissue-20260929/HELM_V13_DRAWINGS/ |
| 구매 입력 원본 | purchase-inputs-20260930/original-inputs/ |

최신 ZIP만 받으려면 `--archive ser0063-review-20260930 --extract`, 원본 검사만 하려면 `--all --verify-only`를 사용합니다. 조각 하나만 압축 해제하거나 ZIP으로 이름을 바꾸지 않습니다.

전체 STEP은 약 740 MB로 여는 데 시간이 걸릴 수 있습니다. 파일을 받았다고 제작 승인이 된 것은 아닙니다. [현재 상태](00-status.md)를 먼저 확인합니다.

[아카이브 해시](../archives/manifest.json) · [직접 펼친 파일 목록](../data/repository-files.json)
