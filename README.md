# Brix — local design bundle

The source bundle is project-local. For an explicitly requested Claude Code installation, `python3 scripts/install_claude.py` copies the agent and all 15 skills into user-level Claude storage. It refuses to overwrite an existing Brix installation and never modifies MCP settings or Codex. Start by asking your host to read [agents/brix.md](agents/brix.md) and supplying the calling project folder, brand asset folder, brief and Figma destination. A host that supports the existing [project role](.codex/agents/brix.toml) can delegate to Brix; other hosts can execute the same instructions directly. Merely storing these files does not guarantee any host automatically discovers them.

The canonical [workflow](skills/brix-design-workflow/SKILL.md) runs:

1. Logo and color-reference intake into Figma.
2. Autonomous selection of **one reference for the entire website**.
3. Local Design DNA extraction and explicit brand adaptations.
4. DNA-derived variables, styles, named components and variants.
5. Instance-based screens in Auto Layout containers, Arabic/English by default.
6. Screenshot review, live-value comparisons and local anti-slop review.

[Configuration](brix.config.json) keeps anti-slop in `during` mode. Explicit user scope wins. Only the 15 linked skills remain: the workflow, six stages, Design DNA, five anti-slop skills, image prompt tracking and the optional impeccable helper. They must not mix visual references or override the effective DNA. [Inventory](SKILLS-INVENTORY.md) and [provenance](sources.json) describe local contents. Historical source paths in provenance are not runtime dependencies.

The calling project receives visible `reference-selection.json`, `reference-dna.json`, `design-dna.json`, `DESIGN.md`, `IMAGE-PROMPTS.md` and `anti-slop-report.json`. Evidence/specs/readbacks live in its `.brix/workflows/<task>/`. No design output belongs inside this tool bundle. Reuse the site-wide reference across tasks.

The helper enforces stage order, file hashes, one-reference identity, requested locale coverage, mapped DNA/spec/readback equality and review evidence. It validates recorded evidence; it is not an MCP hook and cannot prove that recorded responses are genuine. Brix must capture actual fresh Figma reads and visually inspect screenshots. See [DNA usage](skills/brix-design-workflow/references/dna-usage.md).

```sh
python3 -B scripts/validate_bundle.py
python3 -B scripts/test_workflow.py
python3 -B skills/antislop-human/contrast-check.py --selftest
npm test --prefix skills/design-dna/scripts
```

The optional Design DNA measurement scripts need local dependencies. If missing, install only into this bundle:

```sh
npm install --prefix skills/design-dna/scripts --cache "$PWD/.cache/npm" --ignore-scripts --no-fund --no-audit
```

[Integration status](INTEGRATIONS.md): Brix MCP is preserved separately. This bundle does not change its setup or global client configuration. Actual connection and Figma writes must be checked at task time.

Image-delivery follow-ups automatically route to the local image skill: Brix updates IMAGE-PROMPTS.md, matches supplied files, places approved images in the recorded Figma slots and verifies each placement. Disconnected or ambiguous slots remain explicitly unresolved. This is message-driven agent behavior, not background filesystem monitoring.

Claude installation: the callable agent is `~/.claude/agents/brix.md`, `/brix` is `~/.claude/skills/brix/SKILL.md`, and its independent copied bundle is `~/.claude/skill-bundles/brix/`. The original checkout can move without breaking that installation. Later source edits require an explicit installation update; they do not silently sync.
