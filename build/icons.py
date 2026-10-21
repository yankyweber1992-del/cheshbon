# Replace Capacitor's default launcher icons and splash images with the app's own.
import glob, os, shutil
from PIL import Image
res = 'app/android/app/src/main/res'
icon = Image.open('icons/icon-512.png').convert('RGBA')
mask = Image.open('icons/icon-maskable-512.png').convert('RGBA')
shutil.rmtree(f'{res}/mipmap-anydpi-v26', ignore_errors=True)  # use plain PNG icons
for f in glob.glob(f'{res}/mipmap-*/ic_launcher*.png'):
    w, h = Image.open(f).size
    src = mask if 'foreground' in f else icon
    src.resize((w, h), Image.LANCZOS).save(f)
for f in glob.glob(f'{res}/drawable*/splash.png'):
    w, h = Image.open(f).size
    bg = Image.new('RGBA', (w, h), (15, 23, 42, 255))
    s = int(min(w, h) * 0.35)
    bg.alpha_composite(icon.resize((s, s), Image.LANCZOS), ((w - s) // 2, (h - s) // 2))
    bg.convert('RGB').save(f)
print('icons replaced')
