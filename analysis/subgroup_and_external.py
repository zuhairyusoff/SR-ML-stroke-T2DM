"""(1) Test for subgroup difference between pooled ML and newly developed regression models
(random effects within groups, Wald test on the logit scale; groups are not fully independent,
so the test is exploratory). (2) Newly developed regression restricted to external validations."""
import os, numpy as np, pandas as pd
from scipy import stats
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'meta_analysis.py')).read().split("D=pd.read_csv")[0])
D=pd.read_csv(DATA+'ma_data.csv'); D['se']=D.apply(se_logit,axis=1); D['y']=logit(D.c); D['v']=D.se**2
def pool_logit(s):
    r=pool(s.y.values,s.v.values); mu=logit(r['C']); se=(logit(r['hi'])-logit(r['lo']))/(2*stats.t.ppf(.975,r['k']-1)); return r,mu,se
rows=[]
rm,mm,sm=pool_logit(D[D.group=='ML']); rr,mr,sr=pool_logit(D[D.group=='NewReg'])
z=(mm-mr)/np.sqrt(sm**2+sr**2); p=2*stats.norm.sf(abs(z))
rows.append(dict(analysis='ML vs NewReg difference in logit C',estimate=round(mm-mr,3),z=round(z,2),P=round(p,3)))
ext=D[(D.group=='NewReg')&D.label.str.contains('external')]
r=pool(ext.y.values,ext.v.values)
rows.append(dict(analysis='NewReg external validations only',estimate=f"{r['C']:.3f} ({r['lo']:.3f} to {r['hi']:.3f}), k={r['k']}, I2={r['I2']:.0f}"))
R=pd.DataFrame(rows); R.to_csv(DATA+'ma_subgroup_external.csv',index=False); print(R.to_string())
# (3) Same comparison restricted to stroke-only outcomes
CEVD={144,397,11727,15304,4500,16555,4179}
s=D[~D.record.isin(CEVD)]
ml=s[s.group=='ML']; mm2=ml.y.iloc[0]; sm2=ml.se.iloc[0]
rr2,mr2,sr2=pool_logit(s[s.group=='NewReg'])
z2=(mm2-mr2)/np.sqrt(sm2**2+sr2**2); p2=2*stats.norm.sf(abs(z2))
rows.append(dict(analysis='ML vs NewReg, stroke-only outcomes (ML k=1)',estimate=round(mm2-mr2,3),z=round(z2,2),P=round(p2,3)))
R=pd.DataFrame(rows); R.to_csv(DATA+'ma_subgroup_external.csv',index=False); print(R.to_string())
