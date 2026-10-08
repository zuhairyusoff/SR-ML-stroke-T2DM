"""PROBAST+AI traffic light (Figure 3) and summary bar chart (Figure 4) from data/probast_ratings.csv."""
import os, csv, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Patch
HERE=os.path.dirname(os.path.abspath(__file__))
rows=list(csv.DictReader(open(os.path.join(HERE,'..','data','probast_ratings.csv'))))
ov=lambda v:'High' if 'High' in v else 'Unclear' if 'Unclear' in v else 'Low'
R=[]
for r in rows:
    d=[r['rob_participants'],r['rob_predictors'],r['rob_outcome'],r['rob_analysis']]; a=[r['app_participants'],r['app_predictors'],r['app_outcome']]
    R.append((r['study'],d+[ov(d)]+a+[ov(a)]))
col={'Low':'#4caf50','Unclear':'#f2c037','High':'#d9534f'}; sym={'Low':'+','Unclear':'?','High':'−'}
cols=['Participants','Predictors','Outcome','Analysis','Overall','Participants','Predictors','Outcome','Overall']
fig,ax=plt.subplots(figsize=(10,0.42*len(R)+2.2))
for i,(n,v) in enumerate(R):
    y=len(R)-i; ax.text(-0.3,y,n,ha='right',va='center',fontsize=9)
    for j,s in enumerate(v):
        x=j+(0.6 if j>4 else 0); ax.add_patch(plt.Circle((x,y),0.33,color=col[s])); ax.text(x,y,sym[s],ha='center',va='center',color='white',fontweight='bold')
for j,c in enumerate(cols): ax.text(j+(0.6 if j>4 else 0),len(R)+0.9,c,rotation=45,ha='left',va='bottom',fontsize=9)
ax.text(2,len(R)+3.6,'Risk of bias',ha='center',fontweight='bold'); ax.text(7.1,len(R)+3.6,'Applicability concerns',ha='center',fontweight='bold')
ax.set_xlim(-6,9.2); ax.set_ylim(0,len(R)+4.2); ax.set_aspect('equal'); ax.axis('off')
ax.legend(handles=[Patch(color=col[k],label=k) for k in col],loc='lower center',bbox_to_anchor=(0.5,-0.06),ncol=3,frameon=False)
plt.savefig(os.path.join(HERE,'Figure3_PROBAST_traffic_light.png'),dpi=300,bbox_inches='tight')
fig,ax=plt.subplots(figsize=(9,4.2))
for j,c in enumerate(cols):
    left=0
    for k in col:
        w=sum(1 for _,v in R if v[j]==k)/len(R)*100
        ax.barh(-j,w,left=left,color=col[k],edgecolor='white')
        if w>6: ax.text(left+w/2,-j,str(round(w*len(R)/100)),ha='center',va='center',color='white',fontsize=9)
        left+=w
ax.set_yticks([-j for j in range(9)]); ax.set_yticklabels([('RoB: ' if j<5 else 'Applicability: ')+c for j,c in enumerate(cols)])
ax.set_xlabel('Studies (%)'); ax.legend(handles=[Patch(color=col[k],label=k) for k in col],ncol=3,loc='upper center',bbox_to_anchor=(0.5,1.15),frameon=False)
plt.savefig(os.path.join(HERE,'Figure4_PROBAST_summary.png'),dpi=300,bbox_inches='tight')
