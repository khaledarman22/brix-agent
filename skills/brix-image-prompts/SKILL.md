---
name: brix-image-prompts
description: Plan image assets for a Brix design, write generation prompts in a project-root Markdown file, and track which images have been supplied, generated, reviewed and placed in Figma. Automatically use when planning imagery or when the user sends requested images, attachments or image paths, including follow-ups after design completion.
---

# Image prompts and delivery tracking

Maintain one visible `IMAGE-PROMPTS.md` in the calling design project's root. This is the authoritative image request/status list, not a file in the Brix installation. Read and merge existing entries on resume; preserve user edits, delivered files and other screens' requests. Use stable IDs such as `IMG-001` and semantic filenames such as `home-hero-workspace.webp`.

## Plan from the actual design

After effective `design-dna.json` is available, inventory image slots in the requested screens. Reuse suitable supplied assets first. Record the selected reference ID and relevant DNA image/style rules. Use the single chosen reference's art direction with the project's own identity; do not introduce another style source.

Write one entry per unique asset, listing every placement that reuses it. Specify page/section, purpose, intended frame size and aspect ratio, crop/focal point, subject, composition, lighting, materials, palette and background/transparency when relevant. Leave suitable negative space for adjacent or overlaid UI text; specify RTL/LTR crop variants only when actually required. Keep headings, buttons and most text as editable Figma content, not baked into imagery. Do not regenerate the user's logo or fabricate product screenshots when supplied originals are needed.

Give each needed generated image a complete, ready-to-copy prompt in a fenced text block. Use a consistent prompt language suitable for the generation tool and the user's preference; labels and explanations follow the user's language. Include an `Avoid` line for relevant unwanted content. A reference to “same style” alone is not a complete prompt. Supplied reusable assets need a source/path, not an unnecessary generation prompt.

Prompt writing alone does not generate an image. If generation is part of the authorized design work and a generation tool is available, use its required host workflow. Otherwise leave the request pending and hand over the Markdown file; do not simulate completion. Do not create missing assets merely to demonstrate this skill.

## Record evidence, not assumed progress

Track two independent fields so “made” never implies “placed”:

| Asset status | Meaning |
|---|---|
| `pending` | Image still needed; no usable delivered/generated file confirmed. |
| `generated` | Generation returned an actual image artifact; visual review still pending. |
| `supplied` | User/source delivered an actual image artifact; visual review still pending. |
| `approved` | Image was visually inspected and fits the brief, DNA, dimensions and crop. |
| `needs-revision` | Delivered image exists but needs changes; record the reason. |
| `cancelled` | Slot is no longer needed; retain the entry and reason. |

Track each intended placement separately as `not-placed`, `awaiting-verification`, or `placed`. The asset overview is `placed` only when all intended slots contain the current approved version; use `partial` for a mixture of completed and outstanding slots. Mark `placed` only after a successful Figma write and readback; record file key and node ID. A generated image can remain `not-placed`. A placeholder is never a completed asset.

For every delivered image record the actual accessible local path or returned artifact URL, source (`generated`, `user`, or named provider), version and delivery time when known. Do not invent timestamps, links or IDs. Never mark `generated`, `supplied`, or `approved` from a filename mentioned in chat alone: locate/open the artifact. Inspect the image before approval. Record external-source attribution/license where applicable.

When the user sends images, match them by ID, filename and visible content. Ask only when placement is materially ambiguous; keep unmatched requests pending. When a prompt changes, increment its version, preserve prior versions/artifacts, and reset approval for the affected image. If an old version remains in Figma, explicitly record that placed version as outdated until replaced and verified. Never relabel old placement as the new image.

## Automatic delivery and Figma placement

Image delivery in an active Brix design task authorizes completing that image's already defined placement; do not re-ask permission for each matched image. Honor explicit review-only, hold, or alternative destination instructions. A delivery-only follow-up must execute this workflow even if stages 03–06 previously completed.

1. Resolve the calling project and read IMAGE-PROMPTS.md, effective DNA and the existing Figma destination. Open the actual attachments/files. Preserve supplied originals; if local copies are needed use the calling project's `assets/images/` with semantic names and version suffixes. Never overwrite an older delivered version silently. Record actual delivery immediately as `supplied`, even if Figma is disconnected.
2. Match by explicit IMG ID or user mapping first, then filename and visible content. Confirm dimensions/crop suitability visually. Mark suitable images `approved` without requiring user approval again. For ambiguous matches or unsuitable images record the exact unresolved issue and ask only the necessary question; continue clear matches. If there is no ledger, reconstruct confirmed image slots from the existing project/Figma before creating records. Never guess between different projects or files.
3. Discover actual Brix MCP schemas and check connection/file key. Resolve every target by recorded node ID and inspect its current role, parent, image fill and component/instance relationships. If a recorded node disappeared, locate its intended replacement from the named screen/section; ask only if still ambiguous. Record target mappings as soon as slots are created, so delivery has an exact destination.
4. Use supported Brix image placement/edit operations to replace the intended placeholder/image fill in place. Preserve dimensions, Auto Layout, clipping, corner radii, overlays, semantic names and component structure. Apply the specified fit/crop/focal point; inspect RTL/LTR variants where required. Prefer an instance image override for a one-screen replacement. Edit a main component only when the image is intended to change all its uses. Never duplicate whole screens or replace unrelated images. Move truly obsolete owned nodes to Trash when needed.
5. Read back the affected nodes and export/inspect their screenshots. Check the actual image assignment and visual crop, not merely the existence of the target node. Record file key, actual node IDs, delivered version and readback/screenshot evidence for each slot. Only then set that slot to `placed` in the Markdown. If a write times out or its result is uncertain, mark `awaiting-verification`, inspect current Figma state before retrying, and never create duplicate placements blindly.
6. Update the summary table, per-image details, per-slot mapping and outstanding lists after each batch. Already verified identical image versions in the correct slots need no new write; changed or missing placements need repair. On resume verify live state before relying on old completion. If blocked, retain delivery/approval evidence and report what remains unplaced and why. Finish with placed image IDs and Figma links plus any pending/revision-needed IDs.

This is automatic agent routing when Brix receives a message, not a background folder watcher. Do not claim automatic filesystem monitoring or a successful placement without connected-tool evidence.

## Markdown shape

Start with project name, selected reference ID, task/screen scope and last update. Include an overview table:

| ID | Image / placement | Prompt version | Asset status | Placement | Delivered file | Figma node |
|---|---|---|---|---|---|---|

Follow it with a section per asset using this structure (replace template markers with actual values; use `—` for unknown fields):

````markdown
## IMG-001 — <semantic image name>
- Used in: <page / section / slots>
- Required: yes
- Source: <generated / user / provider>
- Size / ratio: <actual intended size and ratio>
- Crop / direction: <focal point, negative space, applicable locales>
- DNA direction: <reference ID and applicable imagery rules>
- Current prompt version: v1
- Asset status: pending
- Placement: not-placed
- Delivered file / version: —
- Intended slots: <page / section / file key / node IDs where known>
- Per-slot placement: <slot, status, file key, node ID, placed version, evidence>
- Figma file / node / placed version: —
- Review or blocker: —

### Prompt v1
```text
<Complete prompt: subject, action, setting, composition, art direction,
lighting, palette, crop, background and text restrictions.>
Avoid: <relevant exclusions>
```

### History
- <Actual delivery, review, revision or placement event and evidence.>
````

Keep the overview and details consistent. End with explicit lists of **still needed**, **delivered but awaiting review/revision**, and **approved but not placed** image IDs. Count unique active IDs, not repeated placements; exclude cancelled entries from outstanding totals.

If no images are needed, write a short scoped “No image assets required” note and rationale instead of inventing prompts. Before final design handoff, reconcile every required image with actual files and Figma placements. Missing required images remain visible blockers; report partial delivery honestly rather than claiming the screen is finished. Updating a small scope must not erase requests for other screens.
