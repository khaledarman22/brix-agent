# Local integration status

- Agent: `agents/brix.md`; canonical workflow: `skills/brix-design-workflow/SKILL.md`. The existing project-scoped `.codex/agents/brix.toml` points to this local agent, not a global skill.
- Six ordered stage skills are linked by `workflow.json` and checked by `scripts/workflow.py`.
- Design DNA: local `skills/design-dna`, upstream commit `593e39bc9e3652734653bd75544a333d7d43615e`.
- Anti-slop: five local skills (core, UI, copywriting, human/accessibility, mobile), upstream commit `3005235d030b4793146ad9afe8d01045efd90e1d`. Local adaptation explicitly overrides upstream global-install/preferences instructions. No code-comments skill or wizard. Mode is in `brix.config.json`.
- Only impeccable remains as an optional supporting resource. The 130 skills without specific workflow routing were moved to Trash at the user's request. There are 15 remaining SKILL.md entrypoints.
- Brix MCP source remains `/Users/khaled/Desktop/programming/tools/brix`. No bridge code, global client settings or service activation is changed here. Discover tools and verify the actual connection when designing; a filesystem path is not proof of connection.
- TypeUI, Lazyweb, Refero and Mobbin services are not connected by this bundle. No subscriptions/accounts were created.

All design artifacts belong to the calling project. Local tests exercise evidence validation with clearly labeled fixtures; they do not perform or certify a real Figma design.

- Image planning and status: `skills/brix-image-prompts/SKILL.md`, invoked within stages 03, 05 and 06. Saves project-root IMAGE-PROMPTS.md with prompts, actual delivered files, review state and confirmed Figma placement.

- The agent entrypoint also routes image-delivery follow-ups directly to image tracking and Figma placement, including after a completed design. Actual placement still requires the connected Brix MCP and verified target slots.

- Claude Code deployment is explicitly supported by `scripts/install_claude.py`: independent copied bundle in `~/.claude/skill-bundles/brix`, agent in `~/.claude/agents/brix.md`, and `/brix` entry in `~/.claude/skills/brix/SKILL.md`. No symlinks to the development checkout and no MCP settings modifications.
