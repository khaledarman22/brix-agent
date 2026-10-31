---
name: brix-design-workflow
description: Design or refine native editable Figma interfaces using the Brix method—project inspection, section-specific visual references, reusable components, and screenshot-led iteration. Use when the user asks for Brix's design style or workflow, or reference-driven Figma design across projects. This transfers the process, not a previous project's visual identity.
---

# Brix design workflow

Apply this workflow to the user's selected project. Keep its audience, brand, language, content, device sizes, and existing decisions; never carry Snaabble names, assets, colors, dimensions, or layouts into another project by default. Speak the user's language (Egyptian Arabic when appropriate).

## 1. Orient before designing

- Discover the connected Figma tools. Prefer Brix when available or explicitly requested. Verify connection, file key, page, selection, and pause state before reading or writing. A skill is guidance, not an installed bridge.
- Read the saved brief, page structure, existing tokens/styles/components, and the target region. Inspect other relevant pages rather than assuming the file is empty. Read exact node properties before editing.
- Use the available provider's schemas and required host skills. For Brix operations, read [references/brix-tools.md](references/brix-tools.md). If the user explicitly requires Brix and it is unavailable, report the concrete connection issue; do not silently change providers.
- If the project uses `.ui-ux-magec/`, follow its project instructions and use that workspace as the source of truth. This skill supplies design method, not a replacement task/approval system.
- For status-only requests, inspect and report without starting design work or saving a new brief. Separate observed file contents from inferred history and unverified quality.

## 2. Understand and preserve the brief

For new work, establish the product, audience, user goal, requested screens/sections, key flows, language/direction, and target devices. Research relevant real products and market expectations where this affects the design; record actual sources and distinguish assumptions.

Reuse existing decisions. Ask only questions whose answers materially change the output; otherwise state a reasonable assumption and proceed. Do not turn a section request into a whole-product redesign.

During authorized design work, persist a compact brief in the file's supported brief storage or established project workspace:

- Product and audience; scope and screen/section inventory.
- Identity: color and type tokens, spacing, icon family, imagery, direction.
- Reference sources and selected regions with their intended use.
- Decisions and user feedback, including rejected directions.
- Progress: completed, unverified, remaining, and relevant node IDs.

Merge with the existing brief; preserve unrelated decisions. No saved brief means missing history, not proof that no design work happened.

## 3. Research by section and by reusable part

Read [references/reference-method.md](references/reference-method.md) for new screens, sections, or unfamiliar components.

Use real visual references for the actual problem: navigation, hero, service cards, project grids, forms, pricing, FAQ, footer, and relevant states. Search by function and visual structure, not only by industry. Cover the requested regions rather than researching only the hero.

Create focused reference boards and inspect the images. Choose a primary layout reference and borrow specific useful details from others; identify and crop those regions. Build from visible evidence, adapted to the current brand, rather than a prose recollection of a reference.

Select a direction autonomously unless the user asks to choose or the project's workflow requires approval. User-selected references and annotations take precedence. Do not impose fixed numbers of references or copy another project's large candidate boards.

Skip fresh research for a small copy/color/spacing correction, a pattern already established in the current design system, or an explicit request to design directly without references.

## 4. Build with reusable foundations

- Reuse existing components, tokens, and text styles first. Create missing foundations that the requested work needs; do not manufacture a full design system for a minor edit.
- Prefer components for reusable controls, cards, and sections, then instances in screens. Give genuinely reusable alternatives meaningful variants and states. Avoid duplicating near-identical main components.
- Use Auto Layout, deliberate fill/hug/fixed sizing, and project-appropriate screen dimensions. Text wrapping needs a real width. Handle RTL/LTR, long content, and responsive layouts relevant to the scope.
- Preserve existing page organization. For a new file, use purpose-specific pages such as App, Web, Dashboard, Components, References, and Trash, creating each only when needed. Do not rename an established Website page merely to match a convention.
- Keep one authoritative frame per screen/state/device. Update it rather than creating “new” copies after every revision. Place distinct breakpoints and states clearly beside their related screen.
- Build one meaningful section at a time, inspect it, and continue. Preserve manual changes outside the requested region.
- Use a coherent icon family and appropriate imagery. Record image provenance. Reference gallery screenshots belong on reference boards; they are not product assets. Generate imagery when available and suitable, or source permitted stock and inspect its crop. Label temporary stand-ins and pending image prompts honestly.

## 5. Look, fix, and verify

After each meaningful build/edit, export and inspect a screenshot. Check hierarchy, wrapping, clipping, overlaps, spacing, contrast, image fit, and direction. Fix visible problems before extending the same pattern elsewhere.

Use structural lint when available to check token/style bindings, layout, contrast, and component consistency. Apply automatic fixes only when their effect is understood and within scope. A successful write or lint is not visual verification.

After a timeout or disconnect, re-read the affected nodes before retrying: the change may already exist. Respect plugin Pause. Use recoverable trash for removals where supported, and obtain authorization before destructive replacement outside the user's requested scope.

## 6. Continue and hand off clearly

User feedback changes the named region or pattern. Keep accepted decisions, remember rejected directions, and research a new reference only where the change needs it. Avoid repeated approval gates for routine design choices already authorized.

At the end of design work, update the saved decisions/progress. Report the exact file/page/frames changed, the verification performed, and any remaining gaps. Never claim completion, responsive coverage, or visual quality that was not checked. Export implementation code only when requested.
