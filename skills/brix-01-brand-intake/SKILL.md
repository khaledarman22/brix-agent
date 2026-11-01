---
name: brix-01-brand-intake
description: Brix ordered stage 01-brand-intake; execute when selected by the local workflow helper.
---

# 01-brand-intake

Inspect the calling project, assets, existing Figma nodes and brief. Import both the user logo and color-reference asset into Figma and record actual node IDs. Preserve brand identity. Ask only for essential missing inputs. Read ../brix-design-workflow/references/brix-tools.md.

Save JSON completion evidence containing: figma_file (the actual Figma file-key string), asset_nodes (logo and color_reference), brand_file. Paths must identify real artifacts inside the calling project. Read BRIX_ROOT/scripts/workflow.py for the exact validation contract. Do not invent IDs, tool responses or review evidence. Complete this stage through the helper before proceeding.
