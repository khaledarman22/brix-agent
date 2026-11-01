import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
import unittest

HELPER=Path(__file__).with_name('workflow.py')
STAGES=json.loads((HELPER.parent.parent/'workflow.json').read_text())['stages']

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        work=HELPER.parent.parent/'.test-work'
        work.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(prefix='workflow-',dir=work)
        self.addCleanup(self.temp.cleanup)
        root=Path(self.temp.name)
        bundle=root/'package'
        (bundle/'scripts').mkdir(parents=True)
        for name in ['workflow.py','dna_check.py']: shutil.copy2(HELPER.parent/name,bundle/'scripts'/name)
        for name in ['workflow.json','brix.config.json']: shutil.copy2(HELPER.parent.parent/name,bundle/name)
        self.helper=bundle/'scripts/workflow.py'
        self.project=root/'project'
        self.project.mkdir()
        self.call('init')

    def call(self,action,*args,ok=True,task='home'):
        result=subprocess.run([sys.executable,str(self.helper),action,'--project',str(self.project),'--task',task,*args],capture_output=True,text=True)
        self.assertEqual(result.returncode==0,ok,result.stdout+result.stderr)
        return json.loads(result.stdout) if ok else result.stderr

    def write(self,name,data):
        p=self.project/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(data))
        return str(p)

    def evidence(self,index):
        datafile=self.write(f'artifacts/stage-{index}.json',{'name':'fixture'})
        if index==0:
            data={'figma_file':'fixture','asset_nodes':{'logo':'1:1','color_reference':'1:2'},'brand_file':datafile}
        elif index==1:
            datafile=self.write('reference-selection.json',{'reference_policy':'single-source','primary':{'id':'fixture-reference','source':'https://example.com/reference'},'secondary':[],'applied_reference_ids':['fixture-reference']})
            data={'selection_file':datafile,'board_ids':['2:1'],'selected_by':'brix'}
        elif index==2:
            dna={'meta':{'design_reference_id':'fixture-reference'},'design_system':{k:{'value':v} for k,v in {'color':'#000000','typography':'Example','spacing':8,'shape':12,'layout':1440}.items()},'design_style':{'mood':'calm'},'visual_effects':{'enabled':False}}
            data={'reference_dna':self.write('reference-dna.json',dna),'design_dna':self.write('design-dna.json',dna),'adaptations':{'palette':'source matches fixture brand'}}
            direction=self.project/'DESIGN.md'
            direction.write_text('DNA-SHA256: '+hashlib.sha256((self.project/'design-dna.json').read_bytes()).hexdigest()+'\nFixture direction')
            data['design_direction_file']=str(direction)
        elif index==3:
            data={'variable_ids':['v1'],'component_ids':['c1'],'variant_sets':{'c1':{'Dir':['RTL','LTR']}},'registry_file':datafile,'spec_files':[datafile],'directions':['rtl','ltr']}
        elif index==4:
            data={'screen_ids':['ar1','en1'],'container_ids':['root1'],'screen_specs':[datafile],'locales':['ar','en'],'instance_map_file':datafile}
        else:
            image=self.project/'fixture.png'
            image.write_bytes(b'fixture-only-no-visual-verification')
            data={'reviewed_screen_ids':['ar1','en1'],'screenshots':[str(image)],'structural_checks':{'fixture':True},'blocking_issues':[]}
        if index>=3:
            dna_path=self.project/'design-dna.json'
            dna=json.loads(dna_path.read_text())
            dna_hash=hashlib.sha256(dna_path.read_bytes()).hexdigest()
            values={k:v['value'] for k,v in dna['design_system'].items()}
            self.write(f'artifacts/stage-{index}.json',values)
            raw=self.project/f'raw-{index}.txt'
            raw.write_text('Fixture readback, not actual Figma evidence')
            live=self.write(f'live-{index}.json',{'provider':'brix','file_key':'fixture','captured_at':'fixture','dna_sha256':dna_hash,'raw_response_file':str(raw),'raw_response_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'values':values})
            usage={'stage':STAGES[index]['id'],'dna_file':str(dna_path),'dna_sha256':dna_hash,'mappings':[{'category':k,'source_pointer':f'/design_system/{k}/value','spec_file':datafile,'spec_pointer':f'/{k}','live_file':live,'live_pointer':f'/values/{k}','figma_id':'fixture-id'} for k in values]}
            data['dna_usage_file']=self.write(f'usage-{index}.json',usage)
        if index==5:
            report={'mode':'during','scope':'figma_design','dna_sha256':dna_hash,'runtime_verified':False,'blocks':{key:[{'rule':'fixture','status':'PASS','evidence':'Fixture only, not a live design review'}] for key in ['hard_gate','purpose_gate','liveliness','craftsmanship']}}
            data['antislop_report']=self.write('anti-slop-report.json',report)
        return data

    def complete(self,index,data=None,ok=True):
        path=self.write(f'evidence/{index}.json',data if data is not None else self.evidence(index))
        return self.call('complete','--stage',STAGES[index]['id'],'--evidence',path,ok=ok)

    def test_rejects_out_of_order_without_advancing(self):
        self.assertIn('Out of order',self.complete(4,{},ok=False))
        self.assertEqual(self.call('next')['next'],STAGES[0]['id'])

    def test_rejects_missing_brand_asset_and_missing_file(self):
        data=self.evidence(0)
        del data['asset_nodes']['color_reference']
        self.assertIn('Both logo',self.complete(0,data,ok=False))
        data=self.evidence(0)
        data['brand_file']='absent.json'
        self.assertIn('existing file',self.complete(0,data,ok=False))

    def test_ordered_run_resume_and_stale_artifact_detection(self):
        for i in range(6):
            result=self.complete(i)
            self.assertEqual(result['complete'],i==5)
        self.assertTrue(self.call('init')['complete'])
        self.write('design-dna.json',{'changed':True})
        self.assertEqual(self.call('next')['stale'],[s['id'] for s in STAGES[2:]])
        self.assertFalse(self.call('next')['complete'])

    def test_requires_dna_dimensions_and_both_locales(self):
        self.complete(0)
        self.complete(1)
        data=self.evidence(2)
        self.write('design-dna.json',{'design_system':{}})
        self.assertIn('missing dimension',self.complete(2,data,ok=False))
        self.complete(2)
        data=self.evidence(3)
        data['directions']=['ltr']
        self.assertIn('Both directions',self.complete(3,data,ok=False))
        self.complete(3)
        data=self.evidence(4)
        data['locales']=['en']
        self.assertIn('Both locales',self.complete(4,data,ok=False))

    def test_review_coverage_and_blocking_issues(self):
        for i in range(5): self.complete(i)
        data=self.evidence(5)
        data['reviewed_screen_ids']=['en1']
        self.assertIn('all assembled screens',self.complete(5,data,ok=False))
        data=self.evidence(5)
        data['blocking_issues']=['clipped text']
        self.assertIn('Blocking issues',self.complete(5,data,ok=False))

    def test_rejects_missing_mapping_and_live_mismatch(self):
        for i in range(3): self.complete(i)
        data=self.evidence(3)
        del data['dna_usage_file']
        self.assertIn('Missing DNA usage',self.complete(3,data,ok=False))
        data=self.evidence(3)
        live=json.loads((self.project/'live-3.json').read_text())
        live['values']['color']='#ffffff'
        self.write('live-3.json',live)
        self.assertIn('Figma differs',self.complete(3,data,ok=False))

    def test_rejects_spec_mismatch_and_old_dna_hash(self):
        for i in range(3): self.complete(i)
        data=self.evidence(3)
        spec=json.loads((self.project/'artifacts/stage-3.json').read_text())
        spec['spacing']=999
        self.write('artifacts/stage-3.json',spec)
        self.assertIn('Spec differs',self.complete(3,data,ok=False))
        data=self.evidence(3)
        usage=json.loads(Path(data['dna_usage_file']).read_text())
        usage['dna_sha256']='outdated'
        self.write('usage-3.json',usage)
        self.assertIn('DNA changed',self.complete(3,data,ok=False))

    def test_rejects_mixed_references_and_wrong_dna_source(self):
        self.complete(0)
        data=self.evidence(1)
        selection=json.loads(Path(data['selection_file']).read_text())
        selection['secondary']=[{'id':'other-reference'}]
        self.write('reference-selection.json',selection)
        self.assertIn('forbids mixing',self.complete(1,data,ok=False))
        self.complete(1)
        data=self.evidence(2)
        dna=json.loads(Path(data['design_dna']).read_text())
        dna['meta']['design_reference_id']='other-reference'
        self.write('design-dna.json',dna)
        self.assertIn('one selected',self.complete(2,data,ok=False))

    def test_requires_current_design_direction(self):
        self.complete(0); self.complete(1)
        data=self.evidence(2)
        del data['design_direction_file']
        self.assertIn('Missing design_direction',self.complete(2,data,ok=False))
        data=self.evidence(2)
        (self.project/'DESIGN.md').write_text('DNA-SHA256: stale')
        self.assertIn('current DNA hash',self.complete(2,data,ok=False))

    def test_requires_honest_complete_antislop_report(self):
        for i in range(5): self.complete(i)
        data=self.evidence(5)
        del data['antislop_report']
        self.assertIn('Missing anti-slop',self.complete(5,data,ok=False))
        data=self.evidence(5)
        report=json.loads(Path(data['antislop_report']).read_text())
        report['blocks']['hard_gate'][0]['status']='FAIL'
        self.write('anti-slop-report.json',report)
        self.assertIn('Unresolved',self.complete(5,data,ok=False))
        data=self.evidence(5)
        report=json.loads(Path(data['antislop_report']).read_text())
        report['runtime_verified']=True
        self.write('anti-slop-report.json',report)
        self.assertIn('runtime verification',self.complete(5,data,ok=False))

    def test_reopen_invalidates_descendants_and_preserves_other_tasks(self):
        for i in range(6): self.complete(i)
        self.call('init',task='contact')
        result=self.call('reopen','--stage',STAGES[2]['id'],'--reason','New reference')
        self.assertEqual(result['next'],STAGES[2]['id'])
        state=json.loads(Path(result['state']).read_text())
        self.assertEqual(len(state['completed']),2)
        self.assertEqual(len(state['history'][0]['previous']),4)
        self.assertEqual(self.call('next',task='contact')['next'],STAGES[0]['id'])

    def test_explicit_arabic_only_scope(self):
        self.call('init','--locales','ar',task='arabic')
        state_path=self.project/'.brix/workflows/home/state.json'
        state=json.loads(state_path.read_text()); state['locales']=['ar']
        state_path.write_text(json.dumps(state))
        for i in range(3): self.complete(i)
        data=self.evidence(3); data['directions']=['rtl']; self.complete(3,data)
        data=self.evidence(4); data['locales']=['ar']; self.complete(4,data)
        self.assertIn('scope differs',self.call('init','--locales','en',ok=False))

    def test_rejects_wrong_file_and_other_effective_dna(self):
        for i in range(3): self.complete(i)
        data=self.evidence(3)
        live=json.loads((self.project/'live-3.json').read_text()); live['file_key']='other'
        self.write('live-3.json',live)
        self.assertIn('different Figma file',self.complete(3,data,ok=False))
        data=self.evidence(3)
        usage=json.loads(Path(data['dna_usage_file']).read_text())
        alternate=self.project/'design-dna.other.json'
        alternate.write_bytes((self.project/'design-dna.json').read_bytes())
        usage['dna_file']=str(alternate); self.write('usage-3.json',usage)
        self.assertIn('effective DNA approved',self.complete(3,data,ok=False))

if __name__=='__main__': unittest.main()
