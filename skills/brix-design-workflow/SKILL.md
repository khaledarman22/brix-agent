---
name: brix-design-workflow
description: Execute Brix reference-driven Figma design with one reference, project-root Design DNA, ordered evidence gates, reusable components and scoped bilingual review.
---

# Brix local workflow

BRIX_ROOT is two directories above this skill. Read BRIX_ROOT/brix.config.json. All dependencies are local to this bundle; never install or edit global Claude/Codex skills or settings. Explicit user choices prevail. Use the calling project's absolute folder for output, never the Brix installation.

For design tasks run the following stages in order using BRIX_ROOT/scripts/workflow.py. Read the skill returned by `next`, execute it, save genuine evidence, then `complete`. The helper validates saved artifacts; it does not intercept MCP calls or prove the authenticity of recorded responses.

1. [Brand intake](../brix-01-brand-intake/SKILL.md): inspect project and import logo/color reference.
2. [Reference selection](../brix-02-reference-selection/SKILL.md): select ONE reference for the entire website autonomously and proceed immediately.
3. [Design DNA](../brix-03-design-dna/SKILL.md): extract source DNA and effective brand-adapted DNA into visible project-root JSON.
4. [Components](../brix-04-components/SKILL.md): derive variables, styles, components and variants from effective DNA before screen assembly.
5. [Screen assembly](../brix-05-screen-assembly/SKILL.md): use instances in Auto Layout screen containers, Arabic/English by default; honor explicit locale narrowing.
6. [Review](../brix-06-design-review/SKILL.md): visual review plus actual live readback and DNA comparison.

```sh
python3 "$BRIX_ROOT/scripts/workflow.py" init --project /absolute/client-project --task home
python3 "$BRIX_ROOT/scripts/workflow.py" next --project /absolute/client-project --task home
python3 "$BRIX_ROOT/scripts/workflow.py" complete --project /absolute/client-project --task home --stage 01-brand-intake --evidence /absolute/client-project/.brix/workflows/home/intake.json
```

Use `init --locales ar` for an explicitly Arabic-only task; defaults are ar/en. Use a separate task scope when requested locales change. Resume existing state. After changes, `reopen --stage <earliest-affected-stage> --reason <reason>` invalidates dependent stages. Reuse valid existing foundations; never rebuild a whole website for a small edit. Inspect status-only requests without initializing work.

Keep `reference-selection.json`, `reference-dna.json`, `design-dna.json`, `DESIGN.md` and `anti-slop-report.json` visible in the calling project's root. Internal evidence/specs/readbacks belong in `.brix/workflows/<task>/`. The selected reference is site-wide: reuse it across tasks. Replacing it requires reconciliation of all affected screens, not mixing sources. Track adaptations to the user's logo, palette, content and locale in effective DNA.

Use [image prompts and tracking](../brix-image-prompts/SKILL.md) after DNA is established, during image delivery/placement, and at final review. Maintain visible project-root `IMAGE-PROMPTS.md` with prompts and evidence-backed per-image delivery/placement states. Reuse supplied assets; report missing required images explicitly. This supporting workflow runs within stages 03, 05 and 06, not as a new numbered stage. It is mandatory whenever those tasks involve imagery. An image-delivery follow-up automatically invokes it even after the original design task finished: update the Markdown and execute verified placement, without waiting for the user to name the skill. For an existing completed task reopen stage 05 (or the earliest affected stage if foundations change), update only affected slots, then refresh review evidence. Do not repeat reference selection or redesign unrelated screens.

Read [reference method](references/reference-method.md), [DNA usage](references/dna-usage.md), [anti-slop integration](references/anti-slop.md) and [Brix tools](references/brix-tools.md). Apply anti-slop during construction and final review using the resolved local mode. Do not ask for reference approval unless explicitly requested or required by the calling project's rules.

Discover the actual Brix MCP tool schemas and verify file/connection before writes. If Brix is unavailable, report the blocker. Use native editable Figma content, clear semantic layer/variant/variable names and reversible Trash moves. A Figma Page cannot have Auto Layout: create an Auto Layout root frame inside each design page and compose screen frames inside it. Reuse existing nodes and components. Inspect screenshots after meaningful changes; a successful write is not visual verification.

The only optional supporting skill retained is [impeccable](../impeccable/SKILL.md) for focused polish. Load it when relevant. Its palette/style recommendations must not replace the single reference or effective DNA. Keep code generation outside design scope unless requested. Host-required tool instructions still apply; for a ui-ux-magec workspace follow its authoritative task/approval rules.
