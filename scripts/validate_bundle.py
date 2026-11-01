"""Validate local Brix routing without loading global agent configuration."""
from pathlib import Path
import json
import re
import tomllib

root=Path(__file__).resolve().parents[1]
config=json.loads((root/'brix.config.json').read_text())
assert config['reference_policy']=='single-source'
assert config['anti_slop']['mode'] in ('during','after')
assert set(config['defaults']['locales']) <= {'ar','en'}
manifest=json.loads((root/'workflow.json').read_text())
assert len(manifest['stages'])==6
owned=[root/'agents/brix.md',root/'skills/brix-design-workflow/SKILL.md']
owned.append(root/'skills/brix-image-prompts/SKILL.md')
owned+=list((root/'skills/brix-design-workflow/references').glob('*.md'))
for stage in manifest['stages']:
    p=root/stage['skill']; assert p.is_file(),p
    assert f'name: brix-{stage["id"]}' in p.read_text(),p
    owned.append(p)
for name in ['design-dna','antislop','antislop-ui','antislop-copywriting','antislop-human','antislop-layoutmobile']:
    assert (root/'skills'/name/'SKILL.md').is_file(),name
for p in owned:
    text=p.read_text()
    assert '/Users/khaled/.claude/' not in text,p
    assert '/Users/khaled/.codex/' not in text,p
    for link in re.findall(r'\]\(([^)]+\.md)\)',text):
        assert (p.parent/link).resolve().is_file(),(p,link)
role_file=root/'.codex/agents/brix.toml'
if role_file.is_file():
    role=tomllib.loads(role_file.read_text())
    assert str(root/'agents/brix.md') in role['developer_instructions']
    assert '/Users/khaled/.codex/' not in role['developer_instructions']
else:
    installed=json.loads((root/'installation.json').read_text())
    assert installed['host']=='claude' and installed['bundle_root']==str(root)
print('PASS: bundle routing, ordered stages, local dependencies and host registration metadata')
