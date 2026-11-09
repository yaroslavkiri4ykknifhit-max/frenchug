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
    ('inter-tight', 'src/assets/inter-tight-cyrillic-italic.woff2', 850),
)
for name, source, weight in fonts:
    font = TTFont(ROOT / source)
    if 'fvar' in font:
        font = instantiateVariableFont(font, {'wght': weight})
    font.flavor = None
    font.save(TMP / (name + '.ttf'))

for stats in (False, True):
    image = Image.new('RGB', (600, 1200), '#030303')
    draw = ImageDraw.Draw(image)

    def label(text, x, y, size, color='white', font='inter', anchor='lt'):
        typeface = ImageFont.truetype(str(TMP / (font + '.ttf')), size)
        draw.text((x, y), text, font=typeface, fill=color, anchor=anchor)

    label('9:00', 30, 25, 22, font='dm')
    draw.rounded_rectangle((488, 27, 540, 42), radius=3, outline='white', width=2)
    draw.rectangle((493, 31, 534, 38), fill='white')
    draw.rectangle((541, 31, 545, 38), fill='white')
    if stats:
        label('4 619', 300, 175, 96, font='archivo', anchor='mt')
        label('Итог прошлых сделок', 300, 280, 20, '#aaaaaa', anchor='mt')
        label('44%', 300, 425, 96, '#ffd54b', 'archivo', 'mt')
        label('ДОЛЯ ПРИБЫЛЬНЫХ СДЕЛОК', 300, 540, 20, '#aaaaaa', anchor='mt')
        label('РЕЗУЛЬТАТЫ', 35, 660, 20, '#999999')
        label('FRENUGO', 35, 720, 26, font='dm')
        label('Исторические данные автора', 35, 775, 19, '#888888')
        draw.line((35, 840, 565, 840), fill='#333333', width=2)
        draw.rounded_rectangle((35, 1015, 565, 1120), radius=20, fill='#dfbb43')
        label('Смотреть результаты', 300, 1050, 26, 'black', 'inter-tight', 'mt')
    else:
        label('FRENUGO', 300, 130, 52, font='archivo', anchor='mt')
        for text, y in (('Результаты', 300), ('Статистика', 380)):
            label(text, 300, y, 68, '#fac5d0', 'inter-tight', 'mt')
        label('Telegram', 300, 460, 68, '#fac5d0', 'archivo', 'mt')
        label('Загляни в канал', 300, 620, 27, anchor='mt')
        label('Обновления и данные', 300, 680, 22, '#999999', anchor='mt')
        draw.rounded_rectangle((35, 1015, 565, 1120), radius=20, fill='#fac5d0')
        label('Открыть канал', 300, 1050, 26, 'black', 'inter-tight', 'mt')
    image.save(TMP / ('phone-' + ('stats' if stats else 'welcome') + '.png'))
