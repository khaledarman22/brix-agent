---
name: brix-02-reference-selection
description: Brix ordered stage 02-reference-selection; execute when selected by the local workflow helper.
---

# 02-reference-selection

Read ../brix-design-workflow/references/reference-method.md. Reuse or autonomously select ONE reference for the entire site, save visible root reference-selection.json, and proceed directly. No mixing secondary sources. Import inspected reference captures to a named Figma reference board.

Save JSON completion evidence containing: selection_file, board_ids, selected_by (brix or user). Paths must identify real artifacts inside the calling project. Read BRIX_ROOT/scripts/workflow.py for the exact validation contract. Do not invent IDs, tool responses or review evidence. Complete this stage through the helper before proceeding.
