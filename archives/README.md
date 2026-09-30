# 원본 아카이브

각 조각은 개별 ZIP이 아닙니다. 16 MiB 이하로 나눈 원본을 복원 도구로 합쳐야 합니다.

| 원본 | MB | 분할 수 | SHA-256 |
|---|---:|---:|---|
| v13-reissue-20260929 | 305.9 | 19 | `45da7ab9ee8f9bfcd0c07e39f022130386c571c70f52bd2d50c9376c73ad57bd` |
| ser0063-review-20260930 | 151.7 | 10 | `a51d47c2f159d4b2f9c46a0012ee79954463824e391c198d37cb8b8ac8ae1367` |
| purchase-inputs-20260930 | 40.5 | 3 | `af49b9360dca691791d69505f065f6217ac415ad678a566b464bdb9b1030478e` |

`python tools/restore_archives.py --all --extract`로 복원합니다. [자세한 안내](../docs/11-artifacts.md). 각 조각과 합친 원본의 SHA-256을 검사합니다.

일반 파일 크기 안내: https://docs.github.com/ko/repositories/working-with-files/managing-large-files/about-large-files-on-github

현재 Releases/LFS를 설정한 것은 아닙니다. 새 대용량 리비전을 계속 쌓을 때 보관 방식을 별도로 검토합니다.
