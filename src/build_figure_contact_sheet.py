from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
files=[
 ('Figure 1',ROOT/'results/nature_style_figures/figure_01_dt_and_green_invention_distributions.png'),
 ('Figure 2',ROOT/'results/nature_style_figures/figure_02_estimator_specific_associations.png'),
 ('Figure A1',ROOT/'results/nature_style_figures/figure_A1_count_ols_residual_diagnostic.png'),
 ('Figure B1',ROOT/'results/nature_style_figures/figure_B1_matching_selection_standardized_differences.png'),
 ('Figure B2',ROOT/'results/nature_style_figures/figure_B2_estimator_sample_retention.png'),
 ('Figure C1',ROOT/'results/nature_style_figures/figure_C1_ppml_residual_and_dispersion_diagnostics.png'),
 ('Figure D1',ROOT/'results/nature_style_figures/figure_D1_strict_timing_estimator_support.png'),
]
thumb_w,thumb_h=700,360
canvas=Image.new('RGB',(thumb_w*2+60,thumb_h*4+140),'white')
draw=ImageDraw.Draw(canvas)
try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24)
except: font=ImageFont.load_default()
for i,(name,p) in enumerate(files):
 im=Image.open(p).convert('RGB'); im.thumbnail((thumb_w,thumb_h-38),Image.Resampling.LANCZOS)
 x=20+(i%2)*(thumb_w+20); y=20+(i//2)*thumb_h
 draw.text((x,y),name,font=font,fill='black')
 canvas.paste(im,(x,y+35))
out=ROOT/'results/nature_style_figures/nature_style_figure_contact_sheet.png';out.parent.mkdir(parents=True,exist_ok=True);canvas.save(out,dpi=(150,150));print(out)
