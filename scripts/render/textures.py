"""Prepare licensed fonts and original phone screens for Blender. Requires Pillow, fontTools, brotli."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'.render';TMP.mkdir(exist_ok=True)
for name,src in [('archivo','node_modules/@fontsource-variable/archivo/files/archivo-latin-wght-italic.woff2'),('dm','node_modules/@fontsource/dm-sans/files/dm-sans-latin-500-normal.woff')]:
 f=TTFont(ROOT/src)
 if 'fvar' in f:f=instantiateVariableFont(f,{'wght':850})
 f.flavor=None;f.save(TMP/(name+'.ttf'))
for stats in [False,True]:
 im=Image.new('RGB',(600,1200),'#030303');d=ImageDraw.Draw(im)
 def txt(text,y,size,color='white',bold=False):
  font=ImageFont.truetype(str(TMP/('archivo.ttf' if bold else 'dm.ttf')),size);d.text((300,y),text,font=font,fill=color,anchor='mt')
 d.text((30,25),'9:00',font=ImageFont.truetype(str(TMP/'dm.ttf'),22),fill='white');d.text((470,25),'▰ ▰',font=ImageFont.truetype(str(TMP/'dm.ttf'),20),fill='white')
 if stats:
  txt('4,619',175,96,bold=True);txt('Historical PnL · USD',280,20,'#aaaaaa');txt('44%',425,96,'#ffd54b',True);txt('WIN RATE',540,20,'#aaaaaa')
  d.text((35,660),'RESULTS',font=ImageFont.truetype(str(TMP/'dm.ttf'),20),fill='#999999');d.text((35,720),'FRENUGO',font=ImageFont.truetype(str(TMP/'dm.ttf'),26),fill='white');d.text((35,775),'Historical author-reported figures',font=ImageFont.truetype(str(TMP/'dm.ttf'),19),fill='#888888');d.line((35,840,565,840),fill='#333333',width=2)
  d.rounded_rectangle((35,1015,565,1120),radius=20,fill='#dfbb43');txt('View Results    →',1050,26,'black',True)
 else:
  txt('FRENUGO',130,52,bold=True)
  for t,y in [('Results.',300),('Statistics.',380),('Telegram.',460)]:txt(t,y,68,'#fac5d0',True)
  txt('Take a closer look.',620,27);txt('Explore the channel',680,22,'#999999');d.rounded_rectangle((35,1015,565,1120),radius=20,fill='#fac5d0');txt('Open Telegram    →',1050,26,'black',True)
 im.save(TMP/('phone-'+('stats' if stats else 'welcome')+'.png'))
