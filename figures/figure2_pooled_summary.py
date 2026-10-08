import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
rows=[('Newly developed regression',7,.70,.69,.72,.67,.73,'#1F4E78'),('Machine learning (best per study)',4,.78,.67,.86,.42,.95,'#C55A11'),('RECODe (external)',5,.68,.61,.75,.49,.83,'#7F7F7F'),('UKPDS Risk Engine (external)',7,.66,.53,.77,.32,.89,'#7F7F7F'),('UKPDS OM2 (external)',6,.62,.59,.65,.56,.69,'#7F7F7F'),(None,)*8,('Sensitivity: regression, stroke only',5,.71,.68,.75,.63,.78,'#1F4E78'),('Sensitivity: ML, stroke only (1 study)',1,.72,.70,.74,None,None,'#C55A11'),('Sensitivity: ML, adding unspecified type',8,.73,.67,.79,.52,.88,'#C55A11')]
fig,ax=plt.subplots(figsize=(10,5.2));n=len(rows)
for i,r in enumerate(rows):
    y=n-i
    if r[0] is None: ax.axhline(y,color='#ccc',lw=.6);continue
    lab,k,c,lo,hi,pl,ph,col=r
    if pl: ax.plot([pl,ph],[y,y],color=col,lw=1,ls=':')
    ax.plot([lo,hi],[y,y],color=col,lw=2.2);ax.plot(c,y,'D' if k>1 else 's',color=col,ms=8)
    ax.text(-0.01,y,lab,transform=ax.get_yaxis_transform(),ha='right',va='center',fontsize=9.5)
    ax.text(1.01,y,f'{k}',transform=ax.get_yaxis_transform(),va='center',fontsize=9.5)
    ax.text(1.06,y,f'{c:.2f} ({lo:.2f} to {hi:.2f})',transform=ax.get_yaxis_transform(),va='center',fontsize=9.5)
ax.text(1.01,n+.9,'k',transform=ax.get_yaxis_transform(),fontweight='bold');ax.text(1.06,n+.9,'C-statistic (95% CI)',transform=ax.get_yaxis_transform(),fontweight='bold')
ax.axvline(.5,color='grey',lw=.6);ax.axvline(.70,color='#1F4E78',lw=.6,ls='--',alpha=.5)
ax.set_xlim(.3,1);ax.set_ylim(.3,n+1.4);ax.set_yticks([]);ax.set_xlabel('Pooled C-statistic for stroke (random effects, HKSJ 95% CI; dotted line 95% prediction interval)')
for s in ['top','right','left']: ax.spines[s].set_visible(False)
import os; plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),'Figure2_pooled_C_summary.png'),dpi=300,bbox_inches='tight')
