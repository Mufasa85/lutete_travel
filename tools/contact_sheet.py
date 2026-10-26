# -*- coding: utf-8 -*-
"""Planche contact des images du catalogue (controle qualite visuel).

Genere des planches de 20 vignettes avec le nom du fichier, pour verifier
d'un coup d'oeil que chaque image correspond bien a son etablissement.

Usage : python tools/contact_sheet.py [dossier images] [sortie]
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

IMG = os.path.join(ROOT, 'assets', 'img')
OUT_DIR = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')),
                       'Temp', 'planches')
COLS, ROWS = 5, 4
THUMB = 260


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else IMG
    out = sys.argv[2] if len(sys.argv) > 2 else OUT_DIR
    os.makedirs(out, exist_ok=True)
    from PIL import Image, ImageDraw

    files = sorted(f for f in os.listdir(src) if f.lower().endswith('.jpg'))
    per = COLS * ROWS
    sheets = (len(files) + per - 1) // per
    print('images: %d -> %d planches' % (len(files), sheets))

    for s in range(sheets):
        chunk = files[s * per:(s + 1) * per]
        cw, ch = THUMB, THUMB + 26
        sheet = Image.new('RGB', (COLS * cw, ROWS * ch), 'white')
        d = ImageDraw.Draw(sheet)
        for i, f in enumerate(chunk):
            try:
                im = Image.open(os.path.join(src, f)).convert('RGB')
                im.thumbnail((cw - 8, ch - 34))
                x = (i % COLS) * cw + 4
                y = (i // COLS) * ch + 4
                sheet.paste(im, (x, y))
                label = f[:-4]
                # nom en deux lignes si trop long
                if len(label) > 30:
                    label = label[:29] + '.'
                d.text((x, y + ch - 30), label[:32], fill='black')
            except Exception as e:
                print('  %s : %s' % (f, e))
        p = os.path.join(out, 'planche_%02d.jpg' % (s + 1))
        sheet.save(p, 'JPEG', quality=85)
        print('  ', p)

    # index json slug -> fichier, pour retrouver vite
    idx = {f[:-4]: f for f in files}
    ip = os.path.join(out, 'index.json')
    with io.open(ip, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(idx, ensure_ascii=False, indent=1))
    print('index:', ip)


if __name__ == '__main__':
    main()
