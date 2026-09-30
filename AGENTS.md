# HELM instructions

- Read README.md, docs/00-status.md and data/project-status.json before editing.
- First purchase is the old CSV left-side 29 rows. Second purchase is the new XLSX 2주차 rows 20-83. Do not force all second-purchase items into CAD or invent additional purchases.
- Current SER0063 CAD is REVIEW ONLY. Horn fit, existing camera hardware interference, strength, stock reconciliation and electrical integration remain unresolved.
- Supplied motor STEP excludes the horn and leads. Preserve source geometry and scale.
- Historical FINAL/PASS labels are limited to their recorded revision and test scope.
- Firmware/navigation/app source has not been supplied; plans are not implemented features.
- Do not rerun servo revision on an already modified baseline. Rebuild changed previews and necessary validation after geometry edits.
- Run python tools/check_repository.py for documentation changes; archive checks use tools/restore_archives.py --all --verify-only.
- Preserve LICENSE and source notices. Do not commit credentials or host authentication files.
