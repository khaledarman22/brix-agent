# Local anti-slop integration

Read `../../antislop/SKILL.md`, then the relevant local siblings antislop-ui, antislop-copywriting, antislop-human and antislop-layoutmobile. Paths are relative to this reference directory. The user's local-only configuration overrides upstream global installation/preferences instructions: do not run an install wizard, read/write ~/.config/antislop, register hooks, install skills globally, or load antislop-code.

Read BRIX_ROOT/brix.config.json: anti_slop.mode defaults to `during`. Honor an explicit session override; do not ask again when resolved. Apply during construction and final review. The one reference and effective project-root design-dna.json remain the visual direction: preserve intentional reference details rather than replacing them with another aesthetic.

Derive visible root DESIGN.md from current effective DNA with reference identity, brand adaptations, typography, palette, spacing, layout and effect rules. Include `DNA-SHA256: <sha256 of effective DNA bytes>` and preserve unrelated user notes when updating.

Save root anti-slop-report.json with mode (`during` or explicit `after`), scope `figma_design`, dna_sha256, runtime_verified false, and blocks hard_gate, purpose_gate, liveliness and craftsmanship. Each block is a list of findings with rule, status PASS/NOT_APPLICABLE and concrete evidence (node IDs, screenshots, measured values). NOT_APPLICABLE needs reason. Fix FAIL findings before completion; do not fabricate PASS or mark everything inapplicable.

Browser behavior, DOM semantics, keyboard operation and runtime performance cannot be verified from static Figma: mark them NOT_APPLICABLE with that reason. Contrast checks use actual resolved colors. WCAG large text is at least 24 CSS px regular or approximately 18.67 px bold, not all text at 18 px. Visual review and live structural checks remain required.
