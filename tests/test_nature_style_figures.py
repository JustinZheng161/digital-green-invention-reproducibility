"""Fail-closed checks for the released Nature-style figure delivery package."""
from pathlib import Path
from PIL import Image
import json, subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/nature_style_figures'
manifest=json.loads((OUT/'nature_style_figure_manifest.json').read_text(encoding='utf-8'))
expected=['Figure 1','Figure 2','Figure A1','Figure B1','Figure B2','Figure C1','Figure D1']
assert manifest['style']=='Nature-inspired graphical style (not a claim of journal acceptance)'
assert (ROOT/manifest['style_basis']).exists(),manifest['style_basis']
assert [x['figure'] for x in manifest['figures']]==expected
assert len(manifest['figures'])==7

for item in manifest['figures']:
    stem=item['semantic_stem']
    assert stem.startswith('figure_') and 'image' not in stem.lower(),stem
    assert item['raster_dpi']==600,item
    assert item['colour_space']=='RGB',item
    assert item['tiff_compression']=='LZW',item
    assert set(item['outputs'])=={'png','pdf','svg','tiff'},item
    for fmt,rel in item['outputs'].items():
        path=ROOT/rel
        assert path.exists() and path.stat().st_size>1000,(fmt,path)
    for fmt in ('png','tiff'):
        im=Image.open(ROOT/item['outputs'][fmt])
        assert im.mode=='RGB',(stem,fmt,im.mode)
        dpi=im.info.get('dpi')
        assert dpi and all(abs(x-600)<1 for x in dpi),(stem,fmt,dpi)
    tiff=Image.open(ROOT/item['outputs']['tiff'])
    assert tiff.tag_v2.get(259)==5,(stem,tiff.tag_v2.get(259)) # TIFF LZW
    svg=(ROOT/item['outputs']['svg']).read_text(encoding='utf-8')
    assert '<text' in svg and '<path' in svg,(stem,'SVG must retain text and vector paths')
    if item['figure']=='Figure B2': assert '<pattern' in svg,(stem,'matched-panel baseline must retain a grayscale-safe hatch pattern')
    fonts=subprocess.check_output(['pdffonts',str(ROOT/item['outputs']['pdf'])],text=True)
    assert 'TrueType' in fonts,(stem,'PDF lacks a TrueType/Type 42-compatible font embedding')

contact=OUT/'nature_style_figure_contact_sheet.png'
assert contact.exists() and contact.stat().st_size>1000
print('PASS: 7 semantic Nature-style figures each have 600 dpi RGB PNG/TIFF (LZW), editable SVG/PDF text, full manifest coverage, and a contact sheet.')
