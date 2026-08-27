"""Rebuild the manuscript's seven figures in a Nature-inspired editorial style.

This script preserves each figure's original data mapping, samples, estimators and
reference values. It emits only figures and a public provenance manifest: no row-level
records, firm identifiers or private input data are written to the public repository.

Nature-inspired technical choices: sans-serif editable text; RGB, colour-blind-safe
palette; lower-left axes and outward ticks; no background grids; bold lowercase panel
labels for multi-panel figures; vector PDF/SVG plus native 600 dpi PNG/LZW TIFF.
"""
from __future__ import annotations
from pathlib import Path
import json, os, warnings
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import pyfixest as pf
import statsmodels.formula.api as smf
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path(os.environ.get('DGI_PRIVATE_DATA_ROOT', ROOT / 'data' / 'private'))
OUT = ROOT / 'results' / 'nature_style_figures'
OUT.mkdir(parents=True, exist_ok=True)
PANEL = PRIVATE / 'derived' / 'matched_panel_private.csv'
CONTROLS = ['leverage','cash_flow','firm_size','book_to_market','roa','growth','fixed_asset_ratio','equity_balance','independent_directors','board_size','largest_holder','employee_scale','ceo_duality','soe']

# Nature Figure Guide-inspired theme: editable TrueType fonts and sparse visual hierarchy.
COLORS = {'blue':'#0072B2', 'orange':'#D55E00', 'teal':'#009E73', 'violet':'#CC79A7', 'grey':'#7A7A7A', 'light_grey':'#D9D9D9', 'black':'#222222'}
mpl.rcParams.update({
    'font.family':['Liberation Sans','DejaVu Sans'], 'font.size':7,
    'axes.labelsize':7, 'axes.titlesize':7, 'xtick.labelsize':6.5, 'ytick.labelsize':6.5,
    'legend.fontsize':6.5, 'axes.linewidth':0.6, 'axes.edgecolor':COLORS['black'],
    'axes.labelcolor':COLORS['black'], 'xtick.color':COLORS['black'], 'ytick.color':COLORS['black'],
    'xtick.direction':'out', 'ytick.direction':'out', 'xtick.major.size':3, 'ytick.major.size':3,
    'xtick.major.width':0.6, 'ytick.major.width':0.6, 'figure.dpi':600, 'savefig.dpi':600,
    'savefig.facecolor':'white', 'figure.facecolor':'white', 'pdf.fonttype':42, 'ps.fonttype':42,
    'svg.fonttype':'none', 'axes.grid':False,
})

figure_records=[]
def style_axes(ax):
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.6); ax.spines['bottom'].set_linewidth(0.6)
    ax.tick_params(which='both', top=False, right=False)

def panel_label(ax, letter):
    ax.text(-0.17, 1.08, letter, transform=ax.transAxes, fontsize=8, fontweight='bold',
            va='top', ha='left', color=COLORS['black'], clip_on=False)

def save_figure(fig, stem, label, source, description):
    paths={}
    for suffix in ['png','pdf','svg']:
        p=OUT/f'{stem}.{suffix}'; fig.savefig(p, bbox_inches='tight', dpi=600, transparent=False); paths[suffix]=p
    # Matplotlib writes harmless spaces at the end of some SVG path lines; normalize the text
    # so a reproducible generated artifact also passes repository whitespace checks.
    svg=paths['svg']
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    # Matplotlib PNGs may carry an unnecessary alpha channel; publish strict RGB rasters.
    rgb=Image.open(paths['png']).convert('RGB')
    rgb.save(paths['png'], dpi=(600,600))
    tif=OUT/f'{stem}.tiff'; rgb.save(tif, compression='tiff_lzw', dpi=(600,600)); paths['tiff']=tif
    figure_records.append({'figure':label,'semantic_stem':stem,'data_source':source,'description':description,
                           'outputs':{k:str(v.relative_to(ROOT)) for k,v in paths.items()},
                           'raster_dpi':600,'colour_space':'RGB','tiff_compression':'LZW','vector_text':'editable SVG/PDF with Type 42 PDF fonts'})
    plt.close(fig)

# Figure 1: identical complete-case panel mapping, with symlog axis to expose the long tail.
panel=pd.read_csv(PANEL)
dt=panel['dt_raw'].dropna(); count=panel['green_invention_count'].dropna()
fig,axs=plt.subplots(1,2,figsize=(7.09,2.85), constrained_layout=True)
ax=axs[0]; ax.hist(dt,bins=70,color=COLORS['blue'],edgecolor='white',linewidth=.25); ax.axvline(dt.median(),color=COLORS['orange'],lw=1,ls='--')
ax.set_xscale('symlog',linthresh=1); ax.set_xlabel('DT_raw_count (symlog scale)'); ax.set_ylabel('Firm-year observations'); ax.set_title('Raw digital-transformation score',loc='left',fontweight='bold'); style_axes(ax); panel_label(ax,'a')
ax.text(.98,.96,f'Mean {dt.mean():.3f}\nMedian {dt.median():.3f}\nSkewness {dt.skew():.3f}',transform=ax.transAxes,ha='right',va='top',fontsize=6.5,color=COLORS['black'])
ax=axs[1]; ax.hist(count,bins=np.arange(-.5,min(int(count.max()),15)+1.5,1),color=COLORS['teal'],edgecolor='white',linewidth=.3)
ax.set_xlabel('Collaborative green invention count (0–15)'); ax.set_ylabel('Firm-year observations'); ax.set_title('Outcome distribution',loc='left',fontweight='bold'); style_axes(ax); panel_label(ax,'b')
ax.text(.98,.96,f'Zero share {count.eq(0).mean():.1%}\nMean {count.mean():.3f}\nMedian {count.median():.3f}',transform=ax.transAxes,ha='right',va='top',fontsize=6.5,color=COLORS['black'])
save_figure(fig,'figure_01_dt_and_green_invention_distributions','Figure 1','Private matched complete-case panel','Distribution of DT_raw_count and collaborative-green-invention count; the DT axis is symlog to show the observed right tail and the count display is truncated at 15.')

# Figure 2: uses released aggregate coefficient table only.
coef=pd.read_csv(ROOT/'results/reviewer_r3/tables/r3_proxy_sensitivity_models.csv').set_index('Model')
left=[('Locked log-outcome reference','Main log outcome'),('Lagged released R&D-expenditure field: log outcome','+ lagged released R&D field'),('Lagged invention-patent activity: log outcome','+ lagged invention-patent activity'),('Both lagged proxy fields: log outcome','+ both lagged proxies')]
right=[('Locked conditional count reference','Main conditional count'),('Lagged released R&D-expenditure field: conditional count','+ lagged released R&D field'),('Lagged invention-patent activity: conditional count','+ lagged invention-patent activity'),('Both lagged proxy fields: conditional count','+ both lagged proxies')]
fig,axs=plt.subplots(1,2,figsize=(7.09,3.25),constrained_layout=True)
for ax,rows,title,xlabel,letter in [(axs[0],left,'Log-outcome models','Coefficient on DT_log', 'a'),(axs[1],right,'Conditional PPML models','Coefficient on DT_log','b')]:
    sub=coef.loc[[x[0] for x in rows]].reset_index(); y=np.arange(len(rows))[::-1]; x=sub['Coefficient on DT_log'].to_numpy(); lo=sub['95% CI lower'].to_numpy(); hi=sub['95% CI upper'].to_numpy()
    ax.errorbar(x,y,xerr=[x-lo,hi-x],fmt='o',color=COLORS['blue'],ecolor=COLORS['blue'],markersize=3.8,lw=.8,capsize=2,capthick=.8,zorder=3)
    ax.axvline(0,color=COLORS['grey'],lw=.7,ls='--',zorder=1); ax.set_yticks(y,[x[1] for x in rows]); ax.set_xlabel(xlabel); ax.set_title(title,loc='left',fontweight='bold'); style_axes(ax); panel_label(ax,letter)
axs[0].set_xlim(-.01,.06); axs[1].set_xlim(-.06,.21)
save_figure(fig,'figure_02_estimator_specific_associations','Figure 2','Released aggregate R3 coefficient table','Estimator-specific DT_log associations with 95% confidence intervals; panels retain their original estimator-specific scales and samples.')

# Figure A1: same deterministic 3,000-point OLS residual diagnostic.
counts=panel.groupby('firm_id')['firm_id'].transform('size'); ols_sample=panel.loc[counts>1].copy(); assert len(ols_sample)==6443
formula='green_invention_count ~ log_dt + '+' + '.join(CONTROLS)+' + C(firm_id) + C(year)'
with warnings.catch_warnings():
    warnings.simplefilter('ignore'); fit=smf.ols(formula,data=ols_sample).fit()
rng=np.random.default_rng(20260827); idx=rng.choice(np.arange(len(fit.resid)),size=min(3000,len(fit.resid)),replace=False)
fig,ax=plt.subplots(figsize=(3.54,2.85),constrained_layout=True); ax.scatter(np.asarray(fit.fittedvalues)[idx],np.asarray(fit.resid)[idx],s=3,alpha=.28,color=COLORS['blue'],linewidths=0); ax.axhline(0,color=COLORS['black'],lw=.7)
ax.set_xlabel('Fitted count (OLS)'); ax.set_ylabel('OLS residual'); style_axes(ax); ax.text(.02,.96,'3,000 fixed-seed observations shown\nfrom N = 6,443 retained observations',transform=ax.transAxes,ha='left',va='top',fontsize=6.5,color=COLORS['black'])
save_figure(fig,'figure_A1_count_ols_residual_diagnostic','Figure A1','Private matched complete-case panel; locked count-OLS diagnostic','Residual-versus-fitted view of the same deterministic 3,000-observation subset used in the locked count-OLS diagnostic.')

# Figure B1: uses released aggregate standardized differences only.
smd=pd.read_csv(ROOT/'results/reviewer_r1/tables/selection_standardized_mean_differences.csv').sort_values('Absolute SMD')
labels={'green_output_log':'Log green-patent output','roa':'Return on assets','firm_size':'Firm size','green_quality_log':'ln(1 + collaborative green invention count)','green_invention_count':'Collaborative green invention count','growth':'Growth','leverage':'Leverage','cash_flow':'Cash flow','book_to_market':'Book-to-market'}
y=np.arange(len(smd)); fig,ax=plt.subplots(figsize=(3.54,3.4),constrained_layout=True); ax.hlines(y,0,smd['Absolute SMD'],color=COLORS['light_grey'],lw=1.2,zorder=1);ax.scatter(smd['Absolute SMD'],y,s=14,color=COLORS['blue'],zorder=3);ax.axvline(.10,color=COLORS['orange'],lw=.8,ls='--',zorder=2)
ax.set_yticks(y,[labels.get(v,v) for v in smd['Variable']]); ax.set_xlabel('Absolute standardized mean difference'); ax.text(.102,len(y)-.25,'0.10 reference',fontsize=6.3,va='top',ha='left',color=COLORS['black']); style_axes(ax)
save_figure(fig,'figure_B1_matching_selection_standardized_differences','Figure B1','Released aggregate selection standardized-difference table','Absolute standardized mean differences between D1 source observations and the matched panel.')

# Figure B2: uses released aggregate retention profiles only.
profiles=pd.read_csv(ROOT/'results/reviewer_r2/tables/r2_sample_flow_and_estimator_profiles.csv'); keep=profiles.loc[profiles['Sample'].ne('D1 green-source file'),['Sample','Share of matched complete-case observations']].iloc[::-1].copy()
short={'Matched complete-case panel':'Matched complete-case panel','TWFE log-outcome retained sample':'TWFE log-outcome sample','Conditional PPML retained sample':'Conditional PPML sample','Strict t−1 PPML retained sample':'Strict t−1 PPML sample','Strict t+1 PPML retained sample':'Strict t+1 PPML sample'}
fig,ax=plt.subplots(figsize=(3.54,3.25),constrained_layout=True); colors=[COLORS['blue'] if v<.999 else COLORS['grey'] for v in keep['Share of matched complete-case observations']]; bars=ax.barh(np.arange(len(keep)),keep['Share of matched complete-case observations'],color=colors,height=.68)
for i,v in enumerate(keep['Share of matched complete-case observations']):ax.text(v+.018,i,f'{v:.1%}',va='center',fontsize=6.5,color=COLORS['black'])
ax.set_yticks(np.arange(len(keep)),[short.get(s,s) for s in keep['Sample']]); ax.set_xlim(0,1.14); ax.set_xlabel('Share of matched complete-case observations');style_axes(ax)
save_figure(fig,'figure_B2_estimator_sample_retention','Figure B2','Released aggregate R2 sample-flow table','Estimator-specific retained-observation shares relative to the matched complete-case panel.')

# Figure C1: same conditional PPML retained sample, residual definition and 20 quantile bins.
FULL=' + '.join(CONTROLS); ppml=pf.fepois(f'green_invention_count ~ log_dt + {FULL} | firm_id + year',data=panel,vcov={'CRV1':'firm_id'}); retained=ppml._data.copy().reset_index(drop=True); mu=np.asarray(ppml.predict(type='response'),float).reshape(-1); resid=np.asarray(ppml.resid(type='response'),float).reshape(-1); pearson=resid/np.sqrt(mu); threshold=3.0
q=pd.qcut(pd.Series(mu),q=20,duplicates='drop'); binned=pd.DataFrame({'mu':mu,'pearson':pearson,'bin':q}).groupby('bin',observed=False).agg(fitted_mean=('mu','mean'),mean_sq_pearson=('pearson',lambda z:float(np.mean(np.square(z))))).reset_index(drop=True)
fig,axs=plt.subplots(1,2,figsize=(7.09,2.85),constrained_layout=True); ax=axs[0]; ax.hist(pearson,bins=55,color=COLORS['blue'],edgecolor='white',linewidth=.25);ax.axvline(-threshold,color=COLORS['orange'],ls='--',lw=.8);ax.axvline(threshold,color=COLORS['orange'],ls='--',lw=.8);ax.set_xlabel('Pearson residual');ax.set_ylabel('Retained observations');ax.set_title('Conditional PPML residual screen',loc='left',fontweight='bold');style_axes(ax);panel_label(ax,'a')
ax=axs[1];ax.plot(binned['fitted_mean'],binned['mean_sq_pearson'],color=COLORS['teal'],lw=1,marker='o',markersize=2.8);ax.axhline(1,color=COLORS['grey'],ls='--',lw=.8);ax.set_xlabel('Mean fitted conditional count');ax.set_ylabel('Mean squared Pearson residual');ax.set_title('Binned dispersion pattern',loc='left',fontweight='bold');style_axes(ax);panel_label(ax,'b')
save_figure(fig,'figure_C1_ppml_residual_and_dispersion_diagnostics','Figure C1','Private matched complete-case panel; locked conditional PPML diagnostic','Pearson-residual screen and 20-bin mean-squared-Pearson-residual pattern for the estimator-retained conditional-PPML sample.')

# Figure D1: uses released aggregate timing support only.
year=pd.read_csv(ROOT/'results/reviewer_r2/tables/r2_timing_estimates_with_sample_composition.csv')
# Detail by year is not in the timing-estimate table; it is a released aggregate file written by the R2 script.
support_path=ROOT/'results/reviewer_r2/tables/r2_timing_year_support.csv'
if not support_path.exists():
    raise FileNotFoundError(f'Missing released aggregate timing support: {support_path}')
support=pd.read_csv(support_path)
fig,ax=plt.subplots(figsize=(3.54,2.85),constrained_layout=True)
styles=[(COLORS['blue'],'o','Strict t−1 PPML'),(COLORS['orange'],'s','Strict t+1 PPML placebo')]
for (name,sub),(color,marker,label) in zip(support.groupby('Test',sort=True),styles):
    ax.plot(sub['Outcome year'],sub['Retained PPML observations'],color=color,marker=marker,markersize=3,lw=1,label=label)
ax.set_xticks(range(2014,2021));ax.set_xlabel('Outcome year');ax.set_ylabel('Retained PPML observations');style_axes(ax);ax.legend(frameon=False,loc='lower left',handlelength=1.4)
save_figure(fig,'figure_D1_strict_timing_estimator_support','Figure D1','Released aggregate R2 calendar-year support table','Calendar-year retained-observation support for strict lag and strict lead conditional-PPML timing estimators.')

manifest={'style':'Nature-inspired graphical style (not a claim of journal acceptance)','style_basis':'docs/NATURE_STYLE_FIGURE_GUIDE.md','figures':figure_records,'privacy':'Only figures, public aggregate inputs and source code are written under results/nature_style_figures.'}
(OUT/'nature_style_figure_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
