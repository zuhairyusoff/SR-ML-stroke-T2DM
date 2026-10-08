"""Random-effects meta-analysis of stroke C statistics (logit scale).
REML tau^2, Hartung-Knapp-Sidik-Jonkman CI, prediction interval (t, k-2), per Debray et al. BMJ 2017.
SE: from reported 95% CI on logit scale; otherwise Hanley-McNeil from N and events (events imputed where flagged)."""
import os
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','')
FIG=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','figures','forest','')
os.makedirs(FIG,exist_ok=True)
import numpy as np, pandas as pd
from scipy import stats, optimize
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

def logit(p): return np.log(p/(1-p))
def expit(x): return 1/(1+np.exp(-x))
def hanley_se(c,n,e):
    q1=c/(2-c); q2=2*c*c/(1+c); ne=n-e
    v=(c*(1-c)+(e-1)*(q1-c*c)+(ne-1)*(q2-c*c))/(e*ne); return np.sqrt(v)

def se_logit(r):
    if pd.notna(r.lo) and pd.notna(r.hi): return (logit(r.hi)-logit(r.lo))/(2*1.96)
    return hanley_se(r.c,r.n,r.e)/(r.c*(1-r.c))

def reml(y,v):
    def nll(t2):
        w=1/(v+t2); mu=np.sum(w*y)/np.sum(w)
        return 0.5*(np.sum(np.log(v+t2))+np.log(np.sum(w))+np.sum(w*(y-mu)**2))
    res=optimize.minimize_scalar(nll,bounds=(0,10),method='bounded'); return max(res.x,0)

def pool(y,v):
    k=len(y); t2=reml(y,v) if k>1 else 0; w=1/(v+t2); mu=np.sum(w*y)/np.sum(w)
    q=np.sum(w*(y-mu)**2)/(k-1) if k>1 else 1
    se_h=np.sqrt(max(q,1)/np.sum(w)) if k>1 else np.sqrt(1/np.sum(w))
    tc=stats.t.ppf(.975,k-1) if k>1 else 1.96
    ci=(mu-tc*se_h,mu+tc*se_h)
    pi=(mu-stats.t.ppf(.975,k-2)*np.sqrt(t2+se_h**2),mu+stats.t.ppf(.975,k-2)*np.sqrt(t2+se_h**2)) if k>=3 else (np.nan,np.nan)
    wf=1/v; muf=np.sum(wf*y)/np.sum(wf); Q=np.sum(wf*(y-muf)**2)
    I2=max(0,(Q-(k-1))/Q)*100 if k>1 and Q>0 else 0
    return dict(k=k,C=expit(mu),lo=expit(ci[0]),hi=expit(ci[1]),pi_lo=expit(pi[0]),pi_hi=expit(pi[1]),tau2=t2,I2=I2)

D=pd.read_csv(DATA+'ma_data.csv')
D['se']=D.apply(se_logit,axis=1); D['y']=logit(D.c); D['v']=D.se**2
D['ci_lo']=expit(D.y-1.96*D.se); D['ci_hi']=expit(D.y+1.96*D.se)
out=[]; 
def run(name,sub,fname):
    r=pool(sub.y.values,sub.v.values); r['analysis']=name; out.append(r)
    fig,ax=plt.subplots(figsize=(8,0.45*len(sub)+2))
    ys=np.arange(len(sub))[::-1]+2
    ax.errorbar(sub.c,ys,xerr=[sub.c-sub.ci_lo,sub.ci_hi-sub.c],fmt='s',color='#1F4E78',ms=5,capsize=2)
    for yy,(_,s) in zip(ys,sub.iterrows()):
        ax.text(-0.02,yy,s.label,va='center',ha='right',fontsize=8,transform=ax.get_yaxis_transform()); ax.text(1.02,yy,f"{s.c:.2f} ({s.ci_lo:.2f}-{s.ci_hi:.2f}){' *' if s.imputed=='Yes' else ''}",va='center',fontsize=8,transform=ax.get_yaxis_transform())
    ax.fill([r['lo'],r['C'],r['hi'],r['C']],[0.6,0.9,0.6,0.3],color='#C00000')
    if r['k']>=3: ax.plot([r['pi_lo'],r['pi_hi']],[0.6,0.6],color='#C00000',lw=1,ls='--')
    ax.text(-0.02,0.6,f"Pooled (REML, HKSJ)  I²={r['I2']:.0f}%",va='center',ha='right',fontsize=8,weight='bold',transform=ax.get_yaxis_transform())
    ax.text(1.02,0.6,f"{r['C']:.2f} ({r['lo']:.2f}-{r['hi']:.2f})",va='center',fontsize=8,weight='bold',transform=ax.get_yaxis_transform())
    if r['k']>=3: ax.text(1.02,0.0,f"95% PI {r['pi_lo']:.2f}-{r['pi_hi']:.2f}",va='center',fontsize=7,transform=ax.get_yaxis_transform())
    ax.axvline(0.5,color='grey',lw=.6); ax.set_xlim(0.3,1.0); ax.set_ylim(-0.5,len(sub)+2.5); ax.set_yticks([])
    ax.set_xlabel('C statistic for stroke'); ax.set_title(name,fontsize=10,loc='center')
    ax.text(1.02,len(sub)+2,'C (95% CI)',fontsize=8,weight='bold',transform=ax.get_yaxis_transform())
    fig.text(0.01,0.005,'* SE approximated from N and estimated events (Hanley-McNeil). Dashed line: 95% prediction interval.',fontsize=6)
    for s in ['top','right','left']: ax.spines[s].set_visible(False)
    fig.savefig(FIG+fname,dpi=300,bbox_inches='tight'); plt.close(fig)

for grp,title in [('UKPDS_RE','A. UKPDS Risk Engine stroke equation (external validations)'),
                  ('UKPDS_OM2','B. UKPDS Outcomes Model 2 stroke equation (external validations)'),
                  ('RECODe','C. RECODe stroke equation (external validations)'),
                  ('NewReg','D. Newly developed regression models (best validation estimate per study)'),
                  ('ML','E. Machine learning models (best model per study)')]:
    sub=D[D.group==grp]; run(title,sub,f'forest_{grp}.png')
    if grp in ('NewReg','ML','UKPDS_RE'):
        s2=sub[sub.rob!='High']
        if len(s2)>=2: run(title+' | sensitivity: excluding high RoB',s2,f'forest_{grp}_lowRoB.png')
    s3=sub[sub.imputed!='Yes']
    if len(s3)>=2 and len(s3)<len(sub): run(title+' | sensitivity: excluding imputed SE',s3,f'forest_{grp}_noimpute.png')
R=pd.DataFrame(out)[['analysis','k','C','lo','hi','pi_lo','pi_hi','I2','tau2']].round(3)
R.to_csv(DATA+'ma_results.csv',index=False); D.round(4).to_csv(DATA+'ma_data_with_se.csv',index=False); print(R.to_string())
