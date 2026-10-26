"""Recalculate recorded scalar policy summaries; Python standard library only."""
import itertools, json, sys
from decimal import Decimal
from pathlib import Path
P=Path(__file__).resolve().parent
D=Decimal

def run(path):
    cells=json.loads(path.read_text(encoding='utf8'),parse_float=D)['cells']
    cases=sorted({c['case_id'] for c in cells}); budgets=['low','high']; setups=[425,475]; delays=[D(2),D(6)]
    if len(cases)!=2 or len(cells)!=16: raise ValueError('expected two cases and 16 cells')
    keys={}
    for c in cells:
        k=(c['budget'],c['case_id'],D(str(c['delay_s'])),c['setup'])
        if k in keys or k[0] not in budgets or k[1] not in cases or k[2] not in delays or k[3] not in setups: raise ValueError('duplicate or invalid cell key')
        for field in ('original_success','task_contact_success','strict_success','external_pass','planning_qualified'):
            if type(c[field]) is not int or not 0<=c[field]<=2: raise ValueError('invalid count')
        for field in ('physical_gap_m','planning_gap_m'):
            if not D(str(c[field])).is_finite(): raise ValueError('nonfinite gap')
        keys[k]=c
    if len(keys)!=16: raise ValueError('incomplete cells')
    def metrics(rows):
        return {'O':sum(r['original_success'] for r in rows),'T':sum(r['task_contact_success'] for r in rows),'S':sum(r['strict_success'] for r in rows),'E':sum(r['external_pass'] for r in rows),'Q':sum(r['planning_qualified'] for r in rows),'M_mm':sum(D(str(r['physical_gap_m'])) for r in rows)*250,'planning_M_mm':sum(D(str(r['planning_gap_m'])) for r in rows)*250}
    result={}
    for b in budgets:
        def rows(mapping): return [keys[b,c,t,mapping[c,t]] for c in cases for t in delays]
        def make(kind, choices):
            if kind=='F00': return {(c,t):choices[0] for c in cases for t in delays}
            if kind=='F01': return {(c,t):choices[delays.index(t)] for c in cases for t in delays}
            if kind=='F10': return {(c,t):choices[cases.index(c)] for c in cases for t in delays}
            return {(c,t):choices[2*cases.index(c)+delays.index(t)] for c in cases for t in delays}
        def entry(mapping): return {'mapping':[[c,str(t),mapping[c,t]] for c in cases for t in delays],**metrics(rows(mapping))}
        classes={}
        for name,n in [('F00',1),('F01',2),('F10',2),('F11',4)]:
            entries=[entry(make(name,ch)) for ch in itertools.product(setups,repeat=n)]
            classes[name]=max(entries,key=lambda x:(x['O'],x['M_mm']))
        delay=[entry(make('F01',ch)) for ch in itertools.product(setups,repeat=2)]
        planning_delay=max(delay,key=lambda x:(x['Q'],x['planning_M_mm']))
        joint=[entry(make('F11',ch)) for ch in itertools.product(setups,repeat=4)]
        planning_joint=max(joint,key=lambda x:(x['Q'],x['planning_M_mm']))
        fixed=[x for x in delay if x['mapping'][0][2]==x['mapping'][1][2]]
        planning_fixed=max(fixed,key=lambda x:(x['Q'],x['planning_M_mm']))
        f0=next(x for x in delay if x['mapping'][0][2]==425 and x['mapping'][1][2]==475)
        f={k:v['M_mm'] for k,v in classes.items()}
        result[b]={'primary':{'fixed_425':fixed[0],'fixed_475':fixed[1],'f0':f0,'planning_best_fixed':planning_fixed,'executed_best_fixed':classes['F00'],'f0_minus_planning_fixed_mm':f0['planning_M_mm']-planning_fixed['planning_M_mm'],'f0_minus_executed_fixed_mm':f0['M_mm']-f['F00']},'delay_only_all':delay,'planning_derived':{'delay_only':planning_delay,'case_and_delay':planning_joint},'hindsight_class_maxima':classes,'nesting_mm':{'delay_then_case':[f['F01']-f['F00'],f['F11']-f['F01']],'case_then_delay':[f['F10']-f['F00'],f['F11']-f['F10']],'interaction':f['F11']-f['F10']-f['F01']+f['F00']}}
    return result

def check(r):
    # Printed paper values: inclusive half-unit in last printed place.
    expected={'low':{'p':[D('11.190'),D('12.984'),D('10.990'),D('-1.995')],'e':[D('11.275'),D('12.788'),D('10.904'),D('-1.884')],'s':[D('11.274786'),D('10.903830'),D('13.159000'),D('12.788044')]},'high':{'p':[D('19.474'),D('16.420'),D('19.632'),D('0.157')],'e':[D('19.554'),D('16.327'),D('19.540'),D('-0.015')],'s':[D('19.554096'),D('19.539504'),D('16.341668'),D('16.327076')]}}
    for b in expected:
        p=r[b]['primary']; a=[p['fixed_425'],p['fixed_475'],p['f0']]
        groups={'p':[x['planning_M_mm'] for x in a]+[p['f0_minus_planning_fixed_mm']],'e':[x['M_mm'] for x in a]+[p['f0_minus_executed_fixed_mm']],'s':[x['M_mm'] for x in r[b]['delay_only_all']]}
        for g,vals in groups.items():
            tol=D('0.0000005') if g=='s' else D('0.0005')
            for x,y in zip(vals,expected[b][g]):
                if abs(x-y)>tol: raise ValueError('paper mismatch: '+b+' '+g+' '+str(x)+' vs '+str(y))
        expected_counts={'low':[(6,6),(6,6),(5,5)],'high':[(7,7),(7,7),(7,7)]}
        if [(x['Q'],x['E']) for x in a]!=expected_counts[b] or any((x['O'],x['T'],x['S'])!=(8,8,0) for x in r[b]['delay_only_all']): raise ValueError('paper count mismatch')
        for name,expected_m in ({'F10':D('14.126180'),'F11':D('14.126180')} if b=='low' else {'F10':D('19.554096'),'F11':D('19.671708')}).items():
            if abs(r[b]['hindsight_class_maxima'][name]['M_mm']-expected_m)>D('0.0000005'): raise ValueError('S31 mismatch')
    return True

if __name__=='__main__':
    try:
        r=run(Path(sys.argv[1]) if len(sys.argv)>1 else P/'cells.json'); check(r)
        print(json.dumps({'paper_rounding_checks':'passed','results':r},indent=2,default=str))
    except (ValueError,KeyError,TypeError,json.JSONDecodeError) as e:
        print('INVALID OR MISMATCH: '+str(e),file=sys.stderr); sys.exit(1)
