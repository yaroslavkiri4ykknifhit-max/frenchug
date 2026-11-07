"""Pack physically rendered frames and assets for the production page."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'public/visuals'
frames = []
for i in range(120):
    with Image.open(ROOT/'.render'/f'coin-turn-{i:03}.png') as image:
        frames.append(image.convert('RGBA'))
assets = ROOT/'src/assets'
frames[0].save(assets/'coin-front.webp', quality=94, method=6)
# Millisecond timestamps alternate between 16 and 17 ms to retain 60 fps.
durations = [round((i+1)*1000/60) - round(i*1000/60) for i in range(len(frames))]
frames[0].save(
    assets/'coin-spin.webp', save_all=True, append_images=frames[1:],
    duration=durations, loop=0, quality=74, method=3,
)
for p in out.glob('*.png'):
 im=Image.open(p)
 if p.stem=='green':
  b=im.getbbox();im=im.crop((max(0,b[0]-12),max(0,b[1]-12),min(im.width,b[2]+12),min(im.height,b[3]+12)))
 im.save(p.with_suffix('.webp'),quality=95 if p.stem=='green' else 93,method=6)
