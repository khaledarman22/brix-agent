"""Copy the Brix bundle into Claude Code user storage; never change MCP settings."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]

def install(home):
    home=home.expanduser().resolve()
    bundle=home/'skill-bundles/brix'
    agent=home/'agents/brix.md'
    entry=home/'skills/brix'
    targets=[bundle,agent,entry]
    for target in targets:
        if target.exists() or target.is_symlink():
            raise ValueError(f'Refusing to overwrite an existing installation: {target}')
    for phase in json.loads((SOURCE/'workflow.json').read_text())['stages']:
        if not (SOURCE/phase['skill']).is_file(): raise ValueError('Missing stage '+phase['id'])
    ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store','.git')
    bundle.mkdir(parents=True)
    try:
        for name in ['skills','agents','scripts']:
            shutil.copytree(SOURCE/name,bundle/name,ignore=ignore)
        for name in ['workflow.json','brix.config.json','SKILLS-INVENTORY.md','sources.json']:
            shutil.copy2(SOURCE/name,bundle/name)
        # No project-only Codex role or global client config is copied.
        files={str(p.relative_to(bundle)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in bundle.rglob('*') if p.is_file()}
        (bundle/'installation.json').write_text(json.dumps({'host':'claude','bundle_root':str(bundle),'files':files},indent=2)+'\n')
        agent.parent.mkdir(parents=True,exist_ok=True)
        agent.write_text('''---
name: brix
description: Design and refine reference-driven Figma websites with Brix MCP, one reference, Design DNA, ordered components and image delivery tracking. Use for Brix design requests and image follow-ups.
model: inherit
---

You are Brix. Read and follow the installed agent instructions at '''+str(bundle/'agents/brix.md')+'''. Resolve all skill and helper paths inside that installed bundle, never from a development checkout. The calling project holds design output. Reuse its existing workflow state and IMAGE-PROMPTS.md on follow-ups. Honor explicit scope and report only verified Figma results.
''')
        entry.mkdir(parents=True)
        (entry/'SKILL.md').write_text('''---
name: brix
description: Delegate Brix Figma design and image-delivery follow-ups to the installed brix agent with the project brief, assets and destination.
---

# Invoke installed Brix

Delegate the user's request to the `brix` subagent and reuse that agent for follow-ups. Include the calling project's absolute path, brief, attachments or accessible image paths, Figma destination, selected reference and user feedback. The task is: $ARGUMENTS

Require reading '''+str(bundle/'agents/brix.md')+'''. If already acting as Brix, execute directly rather than delegating recursively. Missing task details should be recovered from the current project and conversation; ask only for essential unresolved inputs.

Image deliveries must automatically update project-root IMAGE-PROMPTS.md and place matched approved images in their recorded Figma slots with verification. Do not stop at changing the Markdown. Return confirmed output paths and links or concrete blockers.

All 15 design skills and helper scripts are copied into '''+str(bundle)+'''. Do not depend on the original source checkout. Do not change global MCP settings or install unrelated skills during design execution.
''')
        # Verify the complete copied tree before reporting success.
        assert all(hashlib.sha256((bundle/p).read_bytes()).hexdigest()==h for p,h in files.items())
        assert len(list((bundle/'skills').rglob('SKILL.md')))==15
        assert not any(p.is_symlink() for p in bundle.rglob('*'))
        print(json.dumps({'agent':str(agent),'command':str(entry/'SKILL.md'),'bundle':str(bundle),'skills':15,'verified_files':len(files)},indent=2))
    except Exception:
        # Preserve partial output for inspection; never delete unrelated directories.
        raise

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--claude-home',type=Path,default=Path.home()/'.claude')
    args=parser.parse_args()
    install(args.claude_home)
