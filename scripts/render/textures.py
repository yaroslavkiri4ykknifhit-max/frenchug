"""Prepare licensed fonts and phone screens for Blender. Requires Pillow, fontTools, brotli."""
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
TMP = ROOT / '.render'
TMP.mkdir(exist_ok=True)
fonts = (
    ('archivo', 'node_modules/@fontsource-variable/archivo/files/archivo-latin-wght-italic.woff2', 850),
    ('dm', 'node_modules/@fontsource/dm-sans/files/dm-sans-latin-500-normal.woff', 500),
    ('inter', 'src/assets/inter-cyrillic.woff2', 500),
)
for name, source, weight in fonts:
    font = TTFont(ROOT / source)
    if 'fvar' in font:
        font = instantiateVariableFont(font, {'wght': weight})
    font.flavor = None
    font.save(TMP / (name + '.ttf'))

for screen in ('signal', 'result'):
    image = Image.new('RGB', (600, 1200), '#030303')
    draw = ImageDraw.Draw(image)

    def label(text, x, y, size, color='white', font='inter', anchor='lt'):
        typeface = ImageFont.truetype(str(TMP / (font + '.ttf')), size)
        draw.text((x, y), text, font=typeface, fill=color, anchor=anchor)

    def levels(rows, start):
        draw.rounded_rectangle((36, start, 564, start + len(rows) * 100), radius=28, fill='#17151a')
        for i, (name, value, color) in enumerate(rows):
            y = start + i * 100
            if i:
                draw.line((65, y, 535, y), fill='#343036', width=2)
            label(name, 70, y + 32, 33, '#e9e3e6')
            label(value, 530, y + 30, 41, color, 'archivo', 'rt')

    label('9:00', 30, 25, 22, font='dm')
    draw.rounded_rectangle((488, 27, 540, 42), radius=3, outline='white', width=2)
    draw.rectangle((493, 31, 534, 38), fill='white')
    draw.rectangle((541, 31, 545, 38), fill='white')
    label('FRENUGO', 300, 132, 50, font='archivo', anchor='mt')
    if screen == 'signal':
        draw.rounded_rectangle((92, 238, 508, 316), radius=39, fill='#fac5d0')
        label('СИГНАЛ ОТ БОТА', 300, 260, 33, '#191016', anchor='mt')
        label('BTC / USDT', 300, 385, 75, font='archivo', anchor='mt')
        label('ПОКУПКА', 300, 483, 34, '#fac5d0', anchor='mt')
        levels([('Вход', '90 000', 'white'), ('Стоп', '89 100', '#fac5d0'), ('Тейк', '91 800', '#f4ce62')], 575)
        label('Условный пример', 300, 990, 31, '#c4b7c0', anchor='mt')
    else:
        label('ПРИМЕР ИТОГА', 300, 246, 34, '#fac5d0', anchor='mt')
        label('+2R', 300, 332, 130, '#f4ce62', 'archivo', 'mt')
        label('При выходе по тейку', 300, 493, 33, '#e9e3e6', anchor='mt')
        for y in (602, 658, 714):
            draw.line((59, y, 541, y), fill='#342b1a', width=2)
        points = [(60, 723), (133, 696), (198, 710), (265, 653), (330, 675), (397, 609), (450, 626), (533, 575)]
        draw.polygon([*points, (533, 750), (60, 750)], fill='#2c2010')
        draw.line(points, fill='#f4ce62', width=9, joint='curve')
        draw.ellipse((522, 564, 544, 586), fill='#f4ce62')
        levels([('Вход', '90 000', 'white'), ('Выход', '91 800', '#f4ce62')], 808)
        label('До комиссий', 300, 1060, 31, '#c4b7c0', anchor='mt')
    image.save(TMP / ('phone-' + screen + '.png'))
