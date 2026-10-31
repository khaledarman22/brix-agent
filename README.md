# Brix — project-local UI/UX subagent

Invoke it with **“خلي brix يصمم…”** or ask the parent to delegate to `brix` from this project.

- [Agent instructions](agents/brix.md)
- [Project-scoped role](.codex/agents/brix.toml)
- [132 design skills](SKILLS-INVENTORY.md)
- [Provenance and checksums](sources.json)
- [Integration status](INTEGRATIONS.md)

The original 132 design skills remain available locally. Brix uses applicable skills for the requested design task. No dedicated reference-research or persistent-cache subsystem is installed.

The role covers UI/UX design rather than application coding. Native editable Figma output requires an actual connected Figma writer. This setup does not activate MCP services or paid accounts.

If the current host has not refreshed custom roles, a default subagent named brix can read `agents/brix.md`. No global installation is required.
