# 변경 방법

1. README, docs/00-status.md, data/project-status.json을 먼저 확인합니다.
2. 구매 행·실측 사진·원본 파일을 근거로 변경 이유를 적습니다.
3. 확정/공칭/추정/미확정 값을 구분합니다.
4. CAD 변경 시 도면·BOM·메시·검증을 동일 리비전으로 갱신합니다.
5. 과거 원본 아카이브는 덮어쓰지 않고 새 리비전을 추가합니다.
6. `python tools/check_repository.py`로 링크·파일 목록을 확인합니다. 원본은 `python tools/restore_archives.py --all --verify-only`로 검사합니다.
7. 변경 결과·검사 범위·남은 항목을 커밋/PR에 적습니다.

보유하지 않은 부품, 없는 코드, 하지 않은 실물 시험을 완료로 표시하지 않습니다. 2차 전부 장착은 요구사항이 아닙니다. 실제 부품 불일치를 우선 수정합니다.
