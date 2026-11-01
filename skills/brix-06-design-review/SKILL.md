---
name: brix-06-design-review
description: Brix ordered stage 06-design-review; execute when selected by the local workflow helper.
---

# 06-design-review

Read local DNA usage and anti-slop integration guides. Refresh live readbacks and inspect screenshots of every assembled screen. Check reference fidelity, identity, composition, wrapping, spacing, contrast, instances, variable bindings, variants and task locales/directions. Fix blockers. Save root anti-slop-report.json with evidence and truthful Figma limitations. Never report browser behavior verified from Figma.

Reconcile project-root IMAGE-PROMPTS.md using [image prompts and tracking](../brix-image-prompts/SKILL.md). Verify delivered files and current Figma placements. Include missing required images in blocking_issues; report pending, revision-needed and unplaced images explicitly.

Save JSON completion evidence containing: reviewed_screen_ids, screenshots, structural_checks, blocking_issues (empty only after fixes), dna_usage_file, antislop_report. Paths must identify real artifacts inside the calling project. Read BRIX_ROOT/scripts/workflow.py for the exact validation contract. Do not invent IDs, tool responses or review evidence. Complete this stage through the helper before proceeding.
