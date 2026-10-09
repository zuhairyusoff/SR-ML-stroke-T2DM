"""Leave-one-out sensitivity analysis for each pooled model group (study-level: all estimates from one study removed together)."""
import os, pandas as pd, numpy as np
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'meta_analysis.py')).read().split("D=pd.read_csv")[0])
D=pd.read_csv(DATA+'ma_data.csv'); D['se']=D.apply(se_logit,axis=1); D['y']=logit(D.c); D['v']=D.se**2
rows=[]
for g in ['NewReg','ML','RECODe','UKPDS_RE','UKPDS_OM2']:
    s=D[D.group==g]; full=pool(s.y.values,s.v.values)
    rows.append(dict(group=g,omitted='None (all studies)',**{k:full[k] for k in ['k','C','lo','hi','I2']}))
    for rec in s.record.unique():
        t=s[s.record!=rec]
        if len(t)<2: continue
        r=pool(t.y.values,t.v.values)
        rows.append(dict(group=g,omitted=s[s.record==rec].label.iloc[0],**{k:r[k] for k in ['k','C','lo','hi','I2']}))
R=pd.DataFrame(rows).round(3); R.to_csv(DATA+'ma_leave_one_out.csv',index=False); print(R.to_string())
