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

# Monochrome notification icon (white scales on transparent), Android status bar sizes
from PIL import ImageDraw
for folder, px in {'drawable-mdpi': 24, 'drawable-hdpi': 36, 'drawable-xhdpi': 48, 'drawable-xxhdpi': 72, 'drawable-xxxhdpi': 96}.items():
    S = px * 4
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def P(x, y): return (x * S, y * S)
    w = max(4, int(S * 0.075)); W = (255, 255, 255, 255)
    d.line([P(0.5, 0.12), P(0.5, 0.84)], fill=W, width=w)
    d.line([P(0.10, 0.28), P(0.90, 0.28)], fill=W, width=w)
    d.line([P(0.30, 0.88), P(0.70, 0.88)], fill=W, width=w)
    for cx in (0.22, 0.78):
        d.line([P(cx, 0.28), P(cx - 0.14, 0.58)], fill=W, width=int(w * 0.6))
        d.line([P(cx, 0.28), P(cx + 0.14, 0.58)], fill=W, width=int(w * 0.6))
        d.chord([*P(cx - 0.18, 0.46), *P(cx + 0.18, 0.72)], 0, 180, fill=W)
    os.makedirs(f'{res}/{folder}', exist_ok=True)
    im.resize((px, px), Image.LANCZOS).save(f'{res}/{folder}/ic_stat_icon.png')
print('notification icon added')
