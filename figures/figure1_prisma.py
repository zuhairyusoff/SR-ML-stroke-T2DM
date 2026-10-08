import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams['font.family']='DejaVu Sans'
fig,ax=plt.subplots(figsize=(10,12.5)); ax.set_xlim(0,100); ax.set_ylim(0,122); ax.axis('off')
def box(x,y,w,h,t,fs=10,ha='center',fc='white',bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='square,pad=0',fc=fc,ec='#222',lw=1.1))
    tx=x+w/2 if ha=='center' else x+2.2
    ax.text(tx,y+h/2,t,ha=ha,va='center',fontsize=fs,linespacing=1.45,fontweight='bold' if bold else None)
def arr(x1,y1,x2,y2): ax.annotate('',(x2,y2),(x1,y1),arrowprops=dict(arrowstyle='-|>',lw=1.2,color='#222',mutation_scale=14))
# header
box(10,114,88,6,'Identification of studies via databases',fs=11.5,fc='#F2C14E',bold=True)
def band(y,h,t):
    ax.add_patch(FancyBboxPatch((0,y),6.5,h,boxstyle='round,pad=0,rounding_size=1.2',fc='#A9CCE3',ec='#A9CCE3'))
    ax.text(3.25,y+h/2,t,rotation=90,ha='center',va='center',fontsize=11,fontweight='bold')
band(84,28,'Identification'); band(24,58,'Screening'); band(2,20,'Included')
L,W,R,RW=10,42,58,40
box(L,84,W,28,'Records identified from databases\n(n = 39,831)\n\nPubMed (n = 15,167)\nScopus (n = 17,468)\nWeb of Science (n = 6,581)\nIEEE Xplore (n = 576)\nACM Digital Library (n = 39)')
box(R,91,RW,14,'Records removed before screening:\nDuplicate records removed\n(n = 10,970)')
box(L,70,W,8,'Records screened\n(n = 28,861)'); box(R,70,RW,8,'Records excluded\n(n = 28,677)')
box(L,56,W,8,'Reports sought for retrieval\n(n = 184)'); box(R,56,RW,8,'Reports not retrieved\n(n = 16)')
box(L,42,W,8,'Reports assessed for eligibility\n(n = 168)')
box(R,22,RW,28,'Reports excluded (n = 146):\n  No stroke specific performance\n     (composite outcome only) (n = 102)\n  Trial population, R2 (n = 10)\n  Not T2D or type not specified, R1 (n = 10)\n  Wrong outcome or design (n = 9)\n  Prior stroke not excluded, R3 (n = 8)\n  No model performance reported (n = 4)\n  Preprint, retracted or duplicate (n = 3)',fs=9.3,ha='left')
box(L,4,W,16,'Studies included in review\n(n = 22)\n\nStudies included in meta-analysis\n(n = 19)')
cx=L+W/2
arr(L+W,98,R,98); arr(cx,84,cx,78); arr(L+W,74,R,74); arr(cx,70,cx,64)
arr(L+W,60,R,60); arr(cx,56,cx,50); arr(L+W,46,R,46); arr(cx,42,cx,20)
import os; os.chdir(os.path.dirname(os.path.abspath(__file__))); plt.savefig('Figure1_PRISMA_flow.png',dpi=300,bbox_inches='tight',facecolor='white'); plt.savefig('Figure1_PRISMA_flow.pdf',bbox_inches='tight')
