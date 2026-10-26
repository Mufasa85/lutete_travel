# -*- coding: utf-8 -*-
"""Optimise le poids des images du catalogue.

Redimensionne a 1000 px de large max et recompresse en JPEG qualite 78 :
visuellement identique pour une vignette, mais ~3x plus leger.

Usage : python tools/optimize_images.py
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, 'assets', 'img')

MAX_W = 800
QUALITY = 72


def main():
    from PIL import Image
    if not os.path.isdir(IMG):
        print('pas de dossier images')
        return 0

    files = sorted(f for f in os.listdir(IMG) if f.lower().endswith('.jpg'))
    before = after = 0
    for f in files:
        p = os.path.join(IMG, f)
        before += os.path.getsize(p)
        try:
            im = Image.open(p)
            im = im.convert('RGB')
            if im.width > MAX_W:
                h = int(im.height * MAX_W / im.width)
                im = im.resize((MAX_W, h), Image.LANCZOS)
            im.save(p, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
            after += os.path.getsize(p)
        except Exception as e:
            print('  %s : %s' % (f, e))
    print('%d images : %.1f Mo -> %.1f Mo' % (len(files), before / 1048576.0,
                                              after / 1048576.0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
