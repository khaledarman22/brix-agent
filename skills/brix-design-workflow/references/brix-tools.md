# Brix tool routing

This is a capability map, not a frozen API schema. Discover the tools exposed in the current session and read their actual arguments. Do not assume a tool prefix, filesystem installation path, or file selection from a previous project.

| Purpose | Brix tools |
| --- | --- |
| Connection, active file, pages and selection | `status` |
| Read hierarchy and precise properties | `get_metadata`, `get_node` |
| Saved decisions and product requirements | `brief`, `product_analysis` |
| Existing foundations | `get_design_system`, `search` |
| Visual reference boards and crops | `references`, `reference_crops` |
| Variables, text styles, reusable components | `variables`, `styles`, `create_component` |
| Build and modify native layers | `build`, `edit` |
| Fonts and icons | `fonts`, `icons` |
| Stock, pending prompts and image placement | `stock_photos`, `image_prompts`, `place_images` |
| Visual and structural verification | `screenshot`, `lint` |
| Requested interactions | `prototype` |
| Requested export or implementation handoff | `export`, `export_tokens`, `get_design_context` |

Start with `status`; match the file key from the user's link and explicitly target the file when multiple are connected. Read metadata with a shallow depth, then drill into the requested region. Read the brief and existing design system before building.

For a disconnected Brix plugin, instruct the user to open the intended file in Figma Desktop and run **Plugins → Development → brix**, leaving the panel open. Verify the installation's actual manifest path if first-time import is needed. Do not run setup/restart commands merely to inspect status: they may change integrations for other clients.

Use the installed tool's supported interface. If Brix tools are not exposed, inspect local documentation before using a supported fallback; explain the limitation. Never treat connection metadata alone as proof of a successful file read or write, and never work around Pause or access controls.

Keep exported assets, prompts and other output in the user's project, not inside the Brix installation. Avoid modifying the bridge code or global MCP settings as a side effect of a design task.

If Brix is unavailable and the user has not required it, a connected native Figma provider can implement the same design method using its own instructions. This does not imply identical APIs or automatic availability of Brix's brief/trash/reference features.
