"""Compare mapped DNA values with implementation specs and captured Figma readbacks."""
import argparse
import hashlib
import json
from pathlib import Path

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pointer(data, value):
    if not isinstance(value,str) or not value.startswith('/'):
        raise ValueError('Use a JSON pointer starting with /')
    for segment in value[1:].split('/'):
        key=segment.replace('~1','/').replace('~0','~')
        data=data[int(key)] if isinstance(data,list) else data[key]
    return data

def normalize(value):
    if isinstance(value,str):
        text=value.strip()
        if text.startswith('#'): return text.lower()
        if text.endswith('px'):
            try: return float(text[:-2])
            except ValueError: pass
        return text
    return value

def check(project, usage_file, mode='live', stage=None, expected_dna=None, expected_file_key=None):
    project=Path(project).resolve()
    tracked={}
    def load(raw):
        path=Path(raw)
        path=(path if path.is_absolute() else project/path).resolve()
        if not path.is_relative_to(project) or not path.is_file():
            raise ValueError(f'Missing project artifact: {path}')
        tracked[str(path)]=sha(path)
        return json.loads(path.read_text()),path
    usage,usage_path=load(usage_file)
    dna,dna_path=load(usage['dna_file'])
    if dna_path.parent!=project or not dna_path.name.startswith('design-dna'):
        raise ValueError('Use the visible project-root effective design-dna JSON')
    if expected_dna is not None and dna_path != Path(expected_dna).resolve():
        raise ValueError('Usage must reference the effective DNA approved in stage 03')
    if usage.get('dna_sha256')!=sha(dna_path):
        raise ValueError('DNA changed: rebuild mappings/specs and read back Figma again')
    if stage is not None and usage.get('stage')!=stage:
        raise ValueError('DNA usage record belongs to another stage')
    mappings=usage.get('mappings',[])
    if not mappings: raise ValueError('Empty DNA usage mapping')
    categories=set()
    spec_paths=set()
    live_nodes=set()
    for entry in mappings:
        category=entry['category']
        source=entry['source_pointer']
        if not source.startswith('/design_system/'+category+'/'):
            raise ValueError(f'{category}: source pointer must address its DNA dimension')
        expected=normalize(pointer(dna,source))
        spec,spec_path=load(entry['spec_file'])
        actual=normalize(pointer(spec,entry['spec_pointer']))
        if expected!=actual:
            raise ValueError(f'Spec differs from DNA at {source}: {actual!r} != {expected!r}')
        categories.add(category)
        spec_paths.add(str(spec_path))
        if mode=='live':
            live,live_path=load(entry['live_file'])
            if live.get('provider')!='brix' or not live.get('file_key') or not live.get('captured_at'):
                raise ValueError('Live snapshot needs Brix provider, file key and capture time')
            if expected_file_key is not None and live.get('file_key') != expected_file_key:
                raise ValueError('Readback belongs to a different Figma file')
            if live.get('dna_sha256')!=sha(dna_path):
                raise ValueError('Live snapshot predates current DNA version')
            raw_path=Path(live['raw_response_file'])
            raw_path=(raw_path if raw_path.is_absolute() else project/raw_path).resolve()
            if not raw_path.is_relative_to(project) or not raw_path.is_file() or sha(raw_path)!=live.get('raw_response_sha256'):
                raise ValueError('Missing or changed original Brix readback')
            tracked[str(raw_path)]=sha(raw_path)
            if not entry.get('figma_id'): raise ValueError('Mapping must identify its actual Figma node/variable/style')
            observed=normalize(pointer(live,entry['live_pointer']))
            if expected!=observed:
                raise ValueError(f'Figma differs from DNA at {source}: {observed!r} != {expected!r}')
            live_nodes.add(entry['figma_id'])
    required={'color','typography','spacing','shape'}
    if (stage or usage.get('stage')) in {'05-screen-assembly','06-design-review'}:
        required.add('layout')
    if not required<=categories:
        raise ValueError('Missing DNA coverage: '+', '.join(sorted(required-categories)))
    return {'pass':True,'mode':mode,'mapped_values':len(mappings),'categories':sorted(categories),'files':tracked,'spec_files':sorted(spec_paths),'figma_ids':sorted(live_nodes)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',required=True)
    parser.add_argument('--usage',required=True)
    parser.add_argument('--mode',choices=['spec','live'],default='live')
    a=parser.parse_args()
    try:
        print(json.dumps(check(a.project,a.usage,a.mode),indent=2))
    except (ValueError,KeyError,TypeError,IndexError,OSError) as e:
        raise SystemExit('DNA check failed: '+str(e))
