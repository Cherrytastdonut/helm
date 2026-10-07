# CAD와 입력 자료 아카이브

최신 편집 모델은 **기준본 procurement-review-20261001 + measured-editable-delta-20261006**을 결합해 복원합니다. [전체 복원 명령](../docs/11-artifacts.md)을 따르세요. 각 part 파일은 개별 ZIP이 아닙니다.

측정 델타 ZIP: 4,059,445바이트 / 17조각 / SHA-256 `28bc90890de76f5c3b2eefee8ada1eb0d5a57adcde6a709c5c8b1a4753e478d0`. 변경 BREP 26개와 전체 편집 메타데이터·치수 근거를 포함합니다. 원본 기준본과 결합하여 편집 파일 3,897개를 바이트 단위로 대조합니다.

이전 네 아카이브와 해시는 [manifest.json](manifest.json)에 그대로 보존합니다. `restore_archives.py`의 인자 없는 기본값은 의존 기준본 procurement-review-20261001입니다. 최신 모델 전체로 오해하지 마세요.

```bash
python tools/restore_archives.py --all --verify-only
```

이 백업은 파일 복원용이며 제조 승인이나 GitHub Releases/LFS 설정을 의미하지 않습니다.
