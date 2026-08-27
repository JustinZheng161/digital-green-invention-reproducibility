"""Render the Figure 2 estimator-panel chart from released aggregate data only."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 8, 'axes.labelsize': 9, 'axes.titlesize': 11, 'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8})
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results/reviewer_r3/tables/r3_proxy_sensitivity_models.csv'
OUT=ROOT/'results/reviewer_r3/figures'
OUT.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(SRC)
rows=[
 ('Locked log-outcome reference','Main log outcome\nN=6,443; firms=1,337'),
 ('Lagged released R&D-expenditure field: log outcome','+ lagged released R&D field\nN=4,222; firms=1,035'),
 ('Lagged invention-patent activity: log outcome','+ lagged invention-patent activity\nN=4,222; firms=1,035'),
 ('Both lagged proxy fields: log outcome','+ both lagged proxy fields\nN=4,222; firms=1,035'),
]
rows2=[
 ('Locked conditional count reference','Main conditional count\nN=2,774; firms=505'),
 ('Lagged released R&D-expenditure field: conditional count','+ lagged released R&D field\nN=1,891; firms=418'),
 ('Lagged invention-patent activity: conditional count','+ lagged invention-patent activity\nN=1,891; firms=418'),
 ('Both lagged proxy fields: conditional count','+ both lagged proxy fields\nN=1,891; firms=418'),
]
plt.style.use('seaborn-v0_8-whitegrid')
fig,axes=plt.subplots(1,2,figsize=(10.2,4.3),dpi=600)
for ax, spec, title, xlabel in [
 (axes[0],rows,'Log-outcome models','Coefficient on DT_log; outcome ln(1 + count)'),
 (axes[1],rows2,'Conditional PPML models','Coefficient on DT_log; conditional count mean scale'),
]:
 sub=df.set_index('Model').loc[[r[0] for r in spec]].reset_index()
 y=list(range(len(sub)))[::-1]
 x=sub['Coefficient on DT_log'].to_numpy()
 lo=sub['95% CI lower'].to_numpy(); hi=sub['95% CI upper'].to_numpy()
 ax.errorbar(x,y,xerr=[x-lo,hi-x],fmt='o',color='#1f4e79',ecolor='#1f4e79',capsize=3,markersize=6,lw=1.5)
 ax.axvline(0,color='#333333',ls='--',lw=1)
 ax.set_yticks(y,[r[1] for r in spec],fontsize=8)
 ax.set_title(title,fontsize=11)
 ax.set_xlabel(xlabel,fontsize=9)
 ax.tick_params(axis='both',labelsize=8)
 ax.grid(axis='x',alpha=.35)
fig.suptitle('Estimator-specific DT_log association estimates with 95% confidence intervals',fontsize=12,y=1.02)
fig.tight_layout()
png=OUT/'r3_estimator_specific_coefficient_panels.png'
fig.savefig(png,bbox_inches='tight',dpi=600)
fig.savefig(OUT/'r3_estimator_specific_coefficient_panels.pdf',bbox_inches='tight')
plt.close(fig)
im=Image.open(png)
im.save(OUT/'r3_estimator_specific_coefficient_panels.tiff',compression='tiff_lzw',dpi=(600,600))
print(png)
