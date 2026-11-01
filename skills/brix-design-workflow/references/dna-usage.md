# DNA usage: source → spec → live Figma

The authoritative project-root `design-dna.json` is an input to construction, not just a deliverable. Before a `variables`, `styles`, `create_component`, `build` or design-changing `edit`, re-read the relevant DNA fields and prepare the saved JSON payload from them. Do not independently invent values already defined by DNA. Preserve brand adaptations in the effective DNA. Legitimate layout adaptations need an explicit rule/decision in DNA before being mapped, not a silent bypass or a retroactive edit solely to force a pass.

Build a stage-specific `dna-usage-04.json`, `dna-usage-05.json` or `dna-usage-06.json` in the task folder. Each mapping links an actual DNA JSON pointer to a submitted spec JSON pointer and a normalized live readback pointer. Use real component/variable/style/node IDs. At least color, typography, spacing and shape must be represented; screens/review also require layout. Map every submitted spec and all materially used DNA properties, not a convenient sample. Raw rules that are prose must first be made explicit as machine-readable numeric/string fields in the effective DNA while retaining the original explanation.

Example mapping structure (replace all example values with current actual results):

```json
{
  "stage": "04-components",
  "dna_file": "design-dna.json",
  "dna_sha256": "<SHA-256 of current DNA bytes>",
  "mappings": [
    {
      "category": "color",
      "source_pointer": "/design_system/color/primary/hex",
      "spec_file": ".brix/workflows/website-home/specs/components/variables.json",
      "spec_pointer": "/collections/0/variables/2/value",
      "figma_id": "<actual variable ID>",
      "live_file": ".brix/workflows/website-home/readbacks/foundations.json",
      "live_pointer": "/values/primary"
    }
  ]
}
```

This single example is intentionally incomplete: the checker requires the other relevant categories too. Mapping category names are `color`, `typography`, `spacing`, `shape`, `layout`, matching `/design_system/<category>/…` pointers. JSON pointer escapes are `~1` for `/` and `~0` for `~`. Hex case and numeric `px` strings normalize; arbitrary approximation does not. Encode deliberate line-height rounding as an explicit effective DNA pixel value rather than an unexplained tolerance.

Before the corresponding Figma write:

```sh
python3 "$BRIX_ROOT/scripts/dna_check.py" --project /absolute/project --usage /absolute/project/.brix/workflows/website-home/dna-usage-04.json --mode spec
```

Write the exact validated specs through Brix. Then read actual results with `get_design_system`, `export_tokens`, `get_node` and screenshots as needed. Save original Brix response text unchanged. Normalize the relevant observed values into a separate JSON snapshot:

```json
{
  "provider": "brix",
  "file_key": "<actual file key>",
  "captured_at": "<actual ISO time>",
  "dna_sha256": "<current DNA hash>",
  "raw_response_file": ".brix/workflows/website-home/readbacks/foundations-raw.txt",
  "raw_response_sha256": "<original response hash>",
  "values": {"primary": "<observed resolved color>"}
}
```

Never populate observed values by copying the intended specs or DNA. Resolve aliases from actual Figma variable data, and inspect that the intended nodes/styles bind to the expected variables; matching unused tokens alone does not prove implementation. Snapshot node IDs and variable/style IDs must identify those real bindings. Keep `figma_id` traceability for every mapping.

Run the same command with `--mode live` after writes. Include `dna_usage_file` in completion evidence for stages 04, 05 and 06. The workflow helper reruns the comparison and hashes the DNA, specs, mappings, snapshots and original response files; it rejects mismatches, missing categories, missing spec coverage, or changed DNA. Changing DNA invalidates dependent completion until reconciled and reread.

This validator checks recorded data, not the truth of a tool response or whether every write went through the helper. It is not an MCP interception hook. Brix is responsible for capturing genuine fresh readbacks of the correct file after the latest writes and for mapping all material values. Figma can change after a snapshot: refresh readbacks on resume and before completion. Screenshots must still be visually compared for composition, imagery, hierarchy, style and effects that numeric mappings cannot establish. Record exact scope and limitations; do not turn a partial value check into a whole-design fidelity claim.
