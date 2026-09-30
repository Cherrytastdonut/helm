# 자료 확인 도구

두 도구는 Python 3.9 이상과 표준 라이브러리만 사용합니다. 저장소 루트에서 실행합니다.

```bash
python tools/check_repository.py
python tools/restore_archives.py --all --verify-only
python tools/restore_archives.py --all --extract
```

첫 명령은 문서 링크·파일 수·상태 범위·파일 해시 목록을 검사합니다. 두 번째는 출력 파일을 만들지 않고 ZIP 조각과 전체 원본의 SHA-256을 검사합니다. 마지막은 검사가 끝난 ZIP을 downloads에 복원하고 각 원본별 빈 폴더에 풉니다.

의도한 문서 변경 후 `python tools/check_repository.py --write-catalog`로 파일 목록을 갱신하고 변경 내용을 검토하세요. 이 검사는 CAD 간섭 검증이나 실물 제작 승인이 아닙니다.

[원본 복원 안내](../docs/11-artifacts.md) · [CAD 생성 코드와 실행 이력](../docs/12-reproduce.md)
