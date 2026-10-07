# HELM instructions

- Read README.md, docs/00-status.md and data/project-status.json before editing.
- Current revision is MEASURED_LAYOUT_20261006, 3,888 nodes, REVIEW ONLY. 93 purchased rows; 13 measurement records including 10 physical/approximate measurements. Earlier revisions are history.
- First purchase is old CSV left 29 rows. Second is new XLSX 2주차 rows 20-83. Use owned parts only; do not require all second-purchase items or invent stock.
- Reuse docs/14-product-photo-review.md before requesting photos. docs/15-needed-measurements.md lists missing dimensions/interfaces. A verified body is not a blanket no-design-change instruction.
- C715 uses the 2280 slot with nominal card interface geometry. CP003 is an outline with unresolved mounting/terminals. Manufacturer thermal geometry is retained. Unpurchased ADC support and stale routes are removed; do not silently restore them.
- Required inputs: actual servo horn, E-stop mounting/5T fit, chassis 4-hole alignment/stack, bumper actuation/return. Camera bracket hardware and 10 sampled motion pairs, Fomex strength, stock and electrical integration remain unresolved. Fixed bracket/CP003 holes are field-transferred; tiny chips do not need individual measurements. CAD validity is not manufacturing approval.
- Preserve supplied SER0063 body geometry/scale. Horns/leads are not in the source. Retain confirmed manufacturer bodies unless new evidence warrants change.
- Historical FINAL/PASS and no-search-needed statements apply only to their recorded revision/component/scope. Explicit user instructions and actual part mismatches take precedence.
- Runtime firmware/navigation/app implementation was not supplied; plans are not working features.
- Do not reapply revision scripts to modified input. Use the current BREP snapshot and export_snapshot.py for re-export. Update meshes and necessary validation after geometry changes.
- GitHub backup uses the connected GitHub tools; do not stop for terminal git authentication. Preserve checkable checkpoints on the CAD branch until final main backup is verified.
- Run python tools/check_repository.py (regenerate catalog after intended changes); archive gate is python tools/restore_archives.py --all --verify-only.
- Preserve LICENSE and source notices. Never commit credentials/host authentication files.

- Restore current editable CAD using both the procurement baseline and measured delta (docs/11-artifacts.md). Delta-only output is incomplete. Keep byte checks and latest export reports distinct.
- 24 changed-rest overlaps include 4 C920 internal reference pairs. Suppressing 160 obsolete bracket fasteners is not collision resolution or fastening completion.
