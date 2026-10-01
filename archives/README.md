# CAD와 입력 자료 아카이브

각 조각은 개별 ZIP이 아닙니다. 16 MiB 이하의 조각을 복원 도구로 합칩니다. 최신 기본값은 **procurement-review-20261001**입니다.

| 원본 | MB | 분할 수 | SHA-256 |
|---|---:|---:|---|
| v13-reissue-20260929 | 305.9 | 19 | `45da7ab9ee8f9bfcd0c07e39f022130386c571c70f52bd2d50c9376c73ad57bd` |
| ser0063-review-20260930 | 151.7 | 10 | `a51d47c2f159d4b2f9c46a0012ee79954463824e391c198d37cb8b8ac8ae1367` |
| purchase-inputs-20260930 | 40.5 | 3 | `af49b9360dca691791d69505f065f6217ac415ad678a566b464bdb9b1030478e` |
| procurement-review-20261001 | 233.3 | 56 | `12390393ead32219a6b898b747dd1469170536a5e1e0bfa7ac7cbfdf60cd4690` |

최신본: `python tools/restore_archives.py --extract`

과거 원본까지: `python tools/restore_archives.py --all --extract`

검사만: `python tools/restore_archives.py --all --verify-only`

[다운로드·내부 파일](../docs/11-artifacts.md). 최신 ZIP은 전체 수정 STEP·현재 BREP·128개 제작 STEP·20개 DXF·6쪽 안내·20쪽 A3 윤곽·근거·미확정 목록을 포함합니다. 재단·통전 승인본이 아닙니다.

기존 아카이브와 해시는 그대로 보존합니다. GitHub Releases/LFS를 설정한 것은 아닙니다.

최신본은 연결 전송에 맞춰 4 MiB 이하 56개 조각으로 보관합니다. 원본 ZIP은 바뀌지 않습니다. `tools/resplit_review_archive.py --zip <검증된_ZIP> --part-mib 4`로 같은 분할을 재현할 수 있습니다. 복원 명령은 그대로입니다.
