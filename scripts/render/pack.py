"""Pack physically rendered frames and assets for the production page."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'public/visuals'
for name in ('coin-front', 'coin-angled'):
    with Image.open(ROOT/'.render'/(name+'.png')) as image:
        image.save(ROOT/'src/assets'/(name+'.webp'), quality=93, method=6)
for p in out.glob('*.png'):
 im=Image.open(p)
 if p.stem=='green':
  b=im.getbbox();im=im.crop((max(0,b[0]-12),max(0,b[1]-12),min(im.width,b[2]+12),min(im.height,b[3]+12)))
 im.save(p.with_suffix('.webp'),quality=95 if p.stem=='green' else 93,method=6)
