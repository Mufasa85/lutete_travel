# -*- coding: utf-8 -*-
"""Controle qualite des images du catalogue (rapide, en batch).

Recupere les metadonnees Wikimedia de tous les fichiers images en 3 requetes
(titles multiples, 50 par requete), puis filtre localement :

  - le TITRE du fichier doit contenir le nom de l'etablissement (complet ou
    au moins 2 mots significatifs) ;
  - la description / les categories doivent mentionner la RDC ou la ville ;
  - aucun autre pays / autre etat ne doit apparaitre.

Les images qui ne passent pas sont retirees du cache ET du disque : le site
retombe sur l'icone de repli, ce qui vaut mieux qu'une photo trompeuse.

Usage : python tools/check_images.py [--fix]
"""
import io, json, os, re, sys, time, unicodedata, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

UA = ('LuteteTravelDemo/1.0 (https://github.com/Mufasa85/lutete_travel; '
      '16paysayocesar@gmail.com) python-urllib/3.11')
COMMONS = 'https://commons.wikimedia.org/w/api.php'
CACHE = os.path.join(HERE, 'image_cache.json')
IMG_DIR = os.path.join(ROOT, 'assets', 'img')

STOP = {'hotel', 'hôtel', 'la', 'le', 'les', 'de', 'des', 'du', 'the', 'et',
        'a', 'au', 'aux', 'en', 'restaurant', 'cafe', 'bar', 'guest', 'house',
        'national', 'parc', 'palace', 'centre', 'ville', 'city', 'lac', 'lake',
        'mont', 'monts', 'chutes', 'residence', 'du', 'sur', 'avec', 'grand',
        'maison', 'plage', 'fleuve', 'riviere', 'rivière', 'cathedrale',
        'bas', 'haut', 'moyen', 'sud', 'nord', 'est', 'ouest'}

AUTRE_PAYS = re.compile(
    r'\b(nebraska|california|texas|florida|new york|ontario|quebec|paris|'
    r'london|barcelona|madrid|rome|italy|france|spain|belgium|portugal|'
    r'japan|china|india|brazil|kenya|tanzania|uganda|zambia|angola|'
    r'congo brazzaville|ireland|scotland|wales|australia|germany|netherlands|'
    r'switzerland|austria|poland|greece|turkey|egypt|morocco|south africa)\b')

VILLES = ['kinshasa', 'lubumbashi', 'goma', 'bukavu', 'matadi', 'kisangani',
          'mbandaka', 'kananga', 'kolwezi', 'likasi', 'kindu', 'bunia',
          'mbuji-mayi', 'kalemie', 'uvira', 'tshikapa', 'bandundu', 'kabinda',
          'gbadolite', 'gemena', 'isiro', 'buta', 'mbanza', 'kamina',
          'lusambo', 'boende', 'beni', 'kailo', 'inaongo', 'moba', 'kalemie',
          'tangi', 'ipline', 'kasaï', 'kasai', 'lomami', 'sankuru', 'tanganyika',
          'maniema', 'tshuapa', 'tshopo', 'ituri', 'ubangi', 'mayi', 'ndombe']


def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return ' ' + re.sub(r'\s+', ' ', s).strip() + ' '


def sig_words(s):
    return [w for w in norm(s).split() if len(w) > 2 and w not in STOP]


def api_batch(titles):
    """Metadonnees extmetadata pour une liste de titres Commons."""
    out = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        p = {'action': 'query', 'titles': '|'.join(chunk),
             'prop': 'imageinfo', 'iiprop': 'url|mime|extmetadata'}
        url = COMMONS + '?' + urllib.parse.urlencode(
            dict(p, format='json', formatversion=2))
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    d = json.load(r)
                break
            except Exception as e:
                print('  retry %d (%s)' % (attempt + 1, e), flush=True)
                time.sleep(4 * (attempt + 1))
        else:
            continue
        for pg in d.get('query', {}).get('pages', []):
            ii = (pg.get('imageinfo') or [{}])[0]
            em = ii.get('extmetadata', {})
            blob = ' '.join([
                pg.get('title', ''),
                em.get('ImageDescription', {}).get('value', '') or '',
                em.get('Categories', {}).get('value', '') or '',
                em.get('ObjectName', {}).get('value', '') or '',
            ])
            blob = re.sub(r'<[^>]+>', ' ', blob)
            out[pg.get('title', '')] = blob
        time.sleep(0.4)
    return out


def main():
    fix = '--fix' in sys.argv
    raw = io.open(os.path.join(ROOT, 'assets', 'activites.js'), encoding='utf-8').read()
    items = {it['slug']: it for it in
             json.loads(raw[raw.index('{'):raw.rindex('}') + 1])['items']}
    cache = json.load(io.open(CACHE, encoding='utf-8'))

    # 1. retrouver le titre Commons de chaque image (par le nom de l'item)
    to_check = [(s, f) for s, f in cache.items() if f and s in items]
    print('images en cache :', len(to_check), flush=True)

    titles = []
    slug_by_title = {}
    for s, f in to_check:
        it = items[s]
        p = {'action': 'query', 'generator': 'search',
             'gsrsearch': it['name'], 'gsrnamespace': 6, 'gsrlimit': 5,
             'prop': 'imageinfo', 'iiprop': 'url'}
        url = COMMONS + '?' + urllib.parse.urlencode(
            dict(p, format='json', formatversion=2))
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                d = json.load(r)
            for pg in d.get('query', {}).get('pages', []):
                t = pg.get('title', '')
                titles.append(t)
                slug_by_title.setdefault(t, s)
            time.sleep(0.35)
        except Exception as e:
            print('  %s : %s' % (it['name'], e), flush=True)

    titles = sorted(set(titles))
    print('fichiers Commons a verifier :', len(titles), flush=True)
    blobs = api_batch(titles)

    ok, bad, unknown = [], [], []
    for t, blob in blobs.items():
        slug = slug_by_title.get(t)
        if not slug:
            continue
        it = items[slug]
        b = blob.lower()
        name_words = sig_words(it['name'])
        title_norm = norm(t)
        in_title = sum(1 for w in name_words if w in title_norm)
        place_ok = any(v in b for v in VILLES) or 'congo' in b or 'kin' in b
        if AUTRE_PAYS.search(b):
            bad.append((slug, it['name'], 'autre pays'))
        elif in_title < min(2, len(name_words)):
            bad.append((slug, it['name'], 'titre non concordant'))
        elif not place_ok:
            bad.append((slug, it['name'], 'lieu non confirme'))
        else:
            ok.append((slug, it['name']))

    # images sans metadonnees : a verifier manuellement
    for s, f in to_check:
        if not any(sl == s for sl, _ in ok) and not any(sl == s for sl, _, _ in bad):
            unknown.append((s, items[s]['name']))

    print('\nvalides   :', len(ok))
    print('rejetes   :', len(bad))
    for s, n, why in bad:
        print('   X %-38s %s' % (n[:38], why))
    print('non verifiables :', len(unknown))
    for s, n in unknown:
        print('   ?', n)

    if fix:
        n = 0
        for slug, name, why in bad:
            cache[slug] = None
            p = os.path.join(IMG_DIR, slug + '.jpg')
            if os.path.exists(p):
                os.remove(p)
                n += 1
        json.dump(cache, io.open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('\n%d images retirees du cache et du disque' % n)


if __name__ == '__main__':
    main()
