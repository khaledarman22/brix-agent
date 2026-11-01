#!/usr/bin/env python3
"""Ordered local evidence ledger; does not execute or verify remote Figma calls."""
import argparse
import hashlib
import json
import re
from dna_check import check as check_dna_usage
from datetime import datetime, timezone
from pathlib import Path

BUNDLE = Path(__file__).resolve().parents[1]
CONFIG = json.loads((BUNDLE / 'brix.config.json').read_text())
MANIFEST = json.loads((BUNDLE / 'workflow.json').read_text())
STAGES = [s['id'] for s in MANIFEST['stages']]
REQUIRED = {
 STAGES[0]: ['figma_file','asset_nodes','brand_file'],
 STAGES[1]: ['selection_file','board_ids','selected_by'],
 STAGES[2]: ['reference_dna','design_dna','adaptations'],
 STAGES[3]: ['variable_ids','component_ids','variant_sets','registry_file','spec_files','directions'],
 STAGES[4]: ['screen_ids','container_ids','screen_specs','locales','instance_map_file'],
 STAGES[5]: ['reviewed_screen_ids','screenshots','structural_checks','blocking_issues'],
}
FILE_FIELDS = {'brand_file','selection_file','reference_dna','design_dna','registry_file','spec_files','screen_specs','instance_map_file','screenshots'}

def read_json(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    temp.replace(path)

def in_project(project, raw):
    p=Path(raw)
    p=(p if p.is_absolute() else project/p).resolve()
    if not p.is_relative_to(project) or not p.is_file():
        raise ValueError(f'Artifact must be an existing file inside the project: {raw}')
    return p

def validate(stage, data, project, state):
    if not isinstance(data, dict):
        raise ValueError('Evidence must be a JSON object')
    for key in REQUIRED[stage]:
        if key not in data or (key != 'blocking_issues' and not data[key]):
            raise ValueError(f'Missing/empty evidence: {key}')
    files={}
    for key in FILE_FIELDS & data.keys():
        entries=data[key] if isinstance(data[key],list) else [data[key]]
        for raw in entries:
            p=in_project(project,raw)
            files[str(p)]=digest(p)
            if key != 'screenshots':
                payload=read_json(p)
                if key in {'reference_dna','design_dna'}:
                    prefix = key.replace('_', '-')
                    if p.parent != project or not (p.name == prefix + '.json' or (p.name.startswith(prefix + '.') and p.name.endswith('.json'))):
                        raise ValueError(f'{key}: save the authoritative DNA JSON directly in the visible project root')
                    for dimension in ('design_system','design_style','visual_effects'):
                        if not isinstance(payload.get(dimension),dict) or not payload[dimension]:
                            raise ValueError(f'{key}: missing dimension {dimension}')
    if stage==STAGES[0]:
        if not isinstance(data['asset_nodes'],dict) or not all(data['asset_nodes'].get(k) for k in ('logo','color_reference')):
            raise ValueError('Both logo and color_reference node IDs are required')
    if stage==STAGES[1]:
        if data['selected_by'] not in {'brix','user'}:
            raise ValueError('selected_by must accurately identify brix or user')
        selection_path=in_project(project,data['selection_file'])
        if selection_path != project/'reference-selection.json':
            raise ValueError('Use visible project-root reference-selection.json')
        selection=read_json(selection_path)
        primary=selection.get('primary')
        if not isinstance(primary,dict) or not primary.get('id') or not primary.get('source'):
            raise ValueError('One primary reference object with id and source is required')
        if selection.get('reference_policy')!='single-source' or selection.get('secondary'):
            raise ValueError('Single-source policy forbids mixing secondary references')
        if selection.get('applied_reference_ids') != [primary['id']]:
            raise ValueError('Apply exactly one design reference')
    if stage==STAGES[2]:
        selection_path=state['completed'][STAGES[1]]['evidence']['selection_file']
        selection=read_json(in_project(project,selection_path))
        reference_id=selection.get('primary',{}).get('id')
        if not reference_id or selection.get('reference_policy')!='single-source':
            raise ValueError('Reopen reference selection under the single-source policy first')
        for key in ('reference_dna','design_dna'):
            dna=read_json(in_project(project,data[key]))
            if dna.get('meta',{}).get('design_reference_id')!=reference_id:
                raise ValueError('DNA must use the one selected design_reference_id')
    if stage==STAGES[2]:
        if not data.get('design_direction_file'):
            raise ValueError('Missing design_direction_file: derive DESIGN.md from the selected DNA')
        direction=in_project(project,data['design_direction_file'])
        if direction != project/'DESIGN.md':
            raise ValueError('Design direction must be saved as visible project-root DESIGN.md')
        dna_hash=digest(in_project(project,data['design_dna']))
        if f'DNA-SHA256: {dna_hash}' not in direction.read_text():
            raise ValueError('DESIGN.md must identify the current DNA hash')
        files[str(direction)]=digest(direction)
    locales=set(state.get('locales', ['ar','en']))
    directions={'rtl' if locale=='ar' else 'ltr' for locale in locales}
    if stage==STAGES[3] and not directions <= set(data['directions']):
        raise ValueError('Both directions are required')
    if stage==STAGES[4] and not locales <= set(data['locales']):
        raise ValueError('Both locales are required')
    if stage==STAGES[5]:
        if data['blocking_issues'] != []:
            raise ValueError('Blocking issues remain')
        screens=state['completed'][STAGES[4]]['evidence']['screen_ids']
        if not set(screens) <= set(data['reviewed_screen_ids']):
            raise ValueError('Review must cover all assembled screens')
    if stage in STAGES[3:]:
        if not data.get('dna_usage_file'):
            raise ValueError('Missing DNA usage evidence: dna_usage_file')
        result=check_dna_usage(project,data['dna_usage_file'],mode='live',stage=stage, expected_dna=in_project(project,state['completed'][STAGES[2]]['evidence']['design_dna']), expected_file_key=state['completed'][STAGES[0]]['evidence']['figma_file'])
        files.update(result['files'])
        claimed = data.get('spec_files',[]) if stage==STAGES[3] else data.get('screen_specs',[])
        if not {str(in_project(project,p)) for p in claimed} <= set(result['spec_files']):
            raise ValueError('Every submitted spec needs a DNA usage mapping')
    if stage==STAGES[5]:
        if not data.get('antislop_report'):
            raise ValueError('Missing anti-slop delivery report')
        report_path=in_project(project,data['antislop_report'])
        report=read_json(report_path)
        dna_path=in_project(project,state['completed'][STAGES[2]]['evidence']['design_dna'])
        if report.get('mode') not in ('during','after') or report.get('scope')!='figma_design' or report.get('dna_sha256')!=digest(dna_path):
            raise ValueError('Anti-slop report must cover current DNA in a resolved mode and Figma scope')
        if report.get('runtime_verified') is not False:
            raise ValueError('Do not claim runtime verification from a Figma-only review')
        for block in ('hard_gate','purpose_gate','liveliness','craftsmanship'):
            items=report.get('blocks',{}).get(block)
            if not isinstance(items,list) or not items:
                raise ValueError('Missing anti-slop block: '+block)
            for item in items:
                if item.get('status') not in ('PASS','NOT_APPLICABLE') or not item.get('rule') or not item.get('evidence'):
                    raise ValueError('Unresolved or unsupported anti-slop finding in '+block)
                if item['status']=='NOT_APPLICABLE' and not item.get('reason'):
                    raise ValueError('Explain every not-applicable anti-slop item')
        if not any(item['status']=='PASS' for items in report['blocks'].values() for item in items):
            raise ValueError('Anti-slop report cannot mark the entire design not applicable')
        files[str(report_path)]=digest(report_path)
    return files

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['init','next','complete','reopen'])
    parser.add_argument('--project',required=True)
    parser.add_argument('--task',required=True)
    parser.add_argument('--stage',choices=STAGES)
    parser.add_argument('--evidence')
    parser.add_argument('--reason')
    parser.add_argument('--locales', nargs='+', choices=['ar','en'])
    a=parser.parse_args()
    project=Path(a.project).resolve()
    if not project.is_dir() or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}',a.task):
        raise ValueError('Use an existing project directory and a lowercase task slug')
    installation=Path(CONFIG['mcp_source']).resolve()
    if project.is_relative_to(installation) or project.is_relative_to(BUNDLE):
        raise ValueError('Task outputs belong in the calling project, not a tool or skill installation')
    state_file=project/'.brix'/'workflows'/a.task/'state.json'
    if state_file.exists():
        state=read_json(state_file)
        if state.get('version')!=1 or state.get('project')!=str(project):
            raise ValueError('State version or project mismatch; inspect before migrating')
    elif a.action=='init':
        state={'version':1,'project':str(project),'task':a.task,'locales':a.locales or CONFIG['defaults']['locales'],'completed':{},'history':[]}
        save(state_file,state)
    else:
        raise ValueError('Initialize this task first')
    if a.locales and set(a.locales)!=set(state.get('locales',['ar','en'])):
        raise ValueError('Existing locale scope differs; use a separate task for the new scope')
    if a.action=='reopen':
        if not a.stage or not a.reason:
            raise ValueError('Reopen requires --stage and --reason')
        removed={s:state['completed'].pop(s) for s in STAGES[STAGES.index(a.stage):] if s in state['completed']}
        state['history'].append({'reason':a.reason,'from':a.stage,'previous':removed,'at':datetime.now(timezone.utc).isoformat()})
        save(state_file,state)
    stale=[]
    for stage, record in state['completed'].items():
        if any(not Path(p).is_file() or digest(Path(p))!=h for p,h in record['files'].items()):
            stale.append(stage)
    next_stage=next((s for s in STAGES if s not in state['completed']),None)
    if a.action=='complete':
        if stale:
            raise ValueError(f'Completed artifacts changed; reopen from {stale[0]}')
        if not a.stage or a.stage!=next_stage:
            raise ValueError(f'Out of order: next stage is {next_stage}')
        if not a.evidence:
            raise ValueError('--evidence is required')
        evidence_path=in_project(project,a.evidence)
        evidence=read_json(evidence_path)
        files=validate(a.stage,evidence,project,state)
        files[str(evidence_path)]=digest(evidence_path)
        state['completed'][a.stage]={'evidence':evidence,'files':files,'at':datetime.now(timezone.utc).isoformat()}
        save(state_file,state)
        next_stage=next((s for s in STAGES if s not in state['completed']),None)
    index=STAGES.index(next_stage) if next_stage else None
    print(json.dumps({'state':str(state_file),'locales':state.get('locales',['ar','en']),'anti_slop_mode':CONFIG['anti_slop']['mode'],'next':next_stage,'skill':str(BUNDLE/MANIFEST['stages'][index]['skill']) if index is not None else None,'stale':stale,'complete':next_stage is None and not stale},indent=2))

if __name__=='__main__':
    try:
        main()
    except (ValueError,KeyError,TypeError,IndexError,OSError) as exc:
        raise SystemExit(f'Workflow error: {exc}')
