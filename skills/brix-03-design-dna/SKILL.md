---
name: brix-03-design-dna
description: Brix ordered stage 03-design-dna; execute when selected by the local workflow helper.
---

# 03-design-dna

Read ../design-dna/SKILL.md and ../brix-design-workflow/references/anti-slop.md. The local package already owns its dependencies: do not follow upstream installation commands that use a global cache; if dependencies are missing, use the project-local command in BRIX_ROOT/README.md. Apply the extraction schema to native Figma output, not an unsolicited HTML implementation. Analyze the selected source into root reference-dna.json. Adapt it to supplied brand assets and requested scope in root design-dna.json. Both must have nonempty design_system, design_style and visual_effects objects, plus meta.design_reference_id matching the selection. Include machine-readable color, typography, spacing, shape and layout fields. Record honest unavailable effects, not invented observations. Derive root DESIGN.md with current DNA-SHA256. Never merely save DNA and ignore it in construction.

Read [image prompts and tracking](../brix-image-prompts/SKILL.md) after saving effective DNA. Plan required image slots and write project-root IMAGE-PROMPTS.md, preserving existing deliveries. If no images are required, record that scoped finding.

Save JSON completion evidence containing: reference_dna, design_dna, adaptations, design_direction_file. Paths must identify real artifacts inside the calling project. Read BRIX_ROOT/scripts/workflow.py for the exact validation contract. Do not invent IDs, tool responses or review evidence. Complete this stage through the helper before proceeding.
