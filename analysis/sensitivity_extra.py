import os
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','')
FIG=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','figures','forest','')
os.makedirs(FIG,exist_ok=True)
"""Additional sensitivity analyses: (1) stroke-only outcomes (CeVD outcomes removed);
(2) adding studies with unspecified diabetes type (rule R1 relaxed)."""
import pandas as pd, numpy as np
src=open(os.path.join(os.path.dirname(__file__),'meta_analysis.py')).read(); exec(src.split("D=pd.read_csv")[0])
D=pd.read_csv(DATA+'ma_data.csv'); D['se']=D.apply(se_logit,axis=1); D['y']=logit(D.c); D['v']=D.se**2
CEVD={144,397,11727,15304,4500,16555,4179}
groups=['UKPDS_RE','UKPDS_OM2','RECODe','NewReg','ML']
rows=[]
def add(name,sub):
    if len(sub)>=2: r=pool(sub.y.values,sub.v.values); r['analysis']=name; rows.append(r)
    else: rows.append(dict(analysis=name,k=len(sub)))
for g in groups:
    s=D[D.group==g]; add(f'{g} | main',s); add(f'{g} | stroke-only outcomes',s[~s.record.isin(CEVD)])
# unspecified diabetes type: 16828 omitted (overlapping cohort with 16065)
med=D[D.group=='ML'].se.median()
extra=pd.DataFrame([
 dict(group='ML',label='Longato 2021 Italy RNN (type NR)',record=16065,c=0.706,se=med,imputed='Median SE'),
 dict(group='ML',label='ACM 2024 XGBoost (type NR, CeVD)',record=13315,c=0.717,se=med,imputed='Median SE'),
 dict(group='ML',label='EHR ML CeVD (type NR)',record=14617,c=0.651,se=0.043/(0.651*0.349),imputed='No'),
 dict(group='ML',label='Mora 2023 Catalonia stacked ML (type NR)',record=4196,c=0.64,se=med,imputed='Median SE'),
 dict(group='NewReg',label='Manitoba logistic (type NR)',record=290,c=0.70,se=(logit(.72)-logit(.68))/3.92,imputed='No')])
extra['y']=logit(extra.c); extra['v']=extra.se**2
A=pd.concat([D,extra])
for g in ['NewReg','ML']: add(f'{g} | adding unspecified diabetes type',A[A.group==g])
R=pd.DataFrame(rows)[['analysis','k','C','lo','hi','pi_lo','pi_hi','I2','tau2']].round(3)
R.to_csv(DATA+'ma_sensitivity_extra.csv',index=False); print(R.to_string())
