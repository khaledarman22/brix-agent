---
name: brix-05-screen-assembly
description: Brix ordered stage 05-screen-assembly; execute when selected by the local workflow helper.
---

# 05-screen-assembly

Read ../brix-design-workflow/references/dna-usage.md. Use component instances, bound variables, clear names and Auto Layout. Inside each page create an Auto Layout root frame containing screen frames. Support ar/en by default or the explicit scoped locales. Respect RTL layout, icon direction and Arabic typography. Validate DNA-derived specs before writes and capture genuine live readbacks afterwards. Export and inspect screenshots. Move removed owned nodes to Trash, never hard-delete by default.

Use [image prompts and tracking](../brix-image-prompts/SKILL.md) to keep IMAGE-PROMPTS.md current as images arrive or are generated. Inspect delivered images and record actual files and versions; mark placement only after confirmed Figma write/readback. Keep missing images pending and identify placeholders. Record the exact file key and target node ID for every intended image slot, including each shared or locale-specific placement. On image-delivery follow-ups place approved matches immediately through Brix MCP and update per-slot verification; do not stop after updating Markdown.

Save JSON completion evidence containing: screen_ids, container_ids, screen_specs, locales, instance_map_file, dna_usage_file. Paths must identify real artifacts inside the calling project. Read BRIX_ROOT/scripts/workflow.py for the exact validation contract. Do not invent IDs, tool responses or review evidence. Complete this stage through the helper before proceeding.
