# -*- coding: utf-8 -*-
"""Verifie la syntaxe des scripts inline de chaque page HTML du site.

Piège classique : une apostrophe dans une chaine JS concatenee casse tout le
script silencieusement (la page reste vide). Ce controle le detecte.

Usage : python tools/check_js.py
"""
import io, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html', 'province.html', 'activite.html']

TMP = os.path.join(tempfile.gettempdir(), 'hermes_js_check')
os.makedirs(TMP, exist_ok=True)

ok = True
for page in PAGES:
    path = os.path.join(ROOT, page)
    if not os.path.exists(path):
        continue
    html = io.open(path, encoding='utf-8').read()
    # scripts inline (sans attribut src)
    blocks = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.S)
    for i, js in enumerate(blocks):
        if not js.strip():
            continue
        f = os.path.join(TMP, '%s_%d.js' % (page.replace('.html', ''), i))
        io.open(f, 'w', encoding='utf-8').write(js)
        r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
        if r.returncode != 0:
            ok = False
            print('ERREUR %s bloc %d :' % (page, i))
            print(r.stderr[:900])
        else:
            print('OK %-16s bloc %d (%d car.)' % (page, i, len(js)))

# verification des <script src=...> pointant vers un fichier existant
for page in PAGES:
    path = os.path.join(ROOT, page)
    if not os.path.exists(path):
        continue
    html = io.open(path, encoding='utf-8').read()
    for src in re.findall(r'<script[^>]*\bsrc="([^"]+)"', html):
        if src.startswith('http'):
            continue
        target = os.path.join(ROOT, src)
        if not os.path.exists(target):
            ok = False
            print('MANQUANT %s -> %s' % (page, src))

print('\n%s' % ('TOUT EST VALIDE' if ok else 'PROBLEMES DETECTES'))
sys.exit(0 if ok else 1)
