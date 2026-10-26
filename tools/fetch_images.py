# -*- coding: utf-8 -*-
"""Recupere de vraies photos pour le catalogue d'activites.

Ordre de recherche pour chaque etablissement / site :
  1. pageimages Wikipedia (fr puis en) sur le titre exact  -> image la plus fiable
  2. recherche Wikimedia Commons (namespace File) sur le nom
     - le titre du fichier doit partager un mot significatif avec l'item
  3. rien -> pas d'image : le site affiche un visuel genere (jamais une photo
     generique qui ferait croire a une photo de l'etablissement).

Les images sont telechargees dans assets/img/ et redimensionnees (Pillow),
pour que le site n depende pas d'un CDN externe et reste rapide.

Cache : tools/image_cache.json (reprise possible).
"""
import io, json, os, re, sys, time, unicodedata, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG_DIR = os.path.join(ROOT, 'assets', 'img')
CACHE = os.path.join(HERE, 'image_cache.json')
META = os.path.join(HERE, 'image_meta.json')

# Wikimedia exige un User-Agent identifiant (URL + contact) : un UA generique
# est renvoye en 403.
UA = ('LuteteTravelDemo/1.0 (https://github.com/Mufasa85/lutete_travel; '
      '16paysayocesar@gmail.com) python-urllib/3.11')
WIKI = 'https://%s.wikipedia.org/w/api.php'
COMMONS = 'https://commons.wikimedia.org/w/api.php'
MAX_W = 1200

STOP = {'hotel', 'hôtel', 'hotel', 'la', 'le', 'les', 'de', 'des', 'du', 'the',
        'et', 'a', 'au', 'aux', 'en', 'restaurant', 'cafe', 'bar', 'guest', 'house',
        'national', 'parc', 'palace', 'centre', 'ville', 'city', 'lac', 'lake',
        'mont', 'monts', 'chutes', 'parc', 'national', 'residence', 'sur', 'avec',
        'grand', 'maison', 'plage', 'fleuve', 'riviere', 'rivière', 'cathedrale',
        'bas', 'haut', 'moyen', 'sud', 'nord', 'est', 'ouest', 'du', 'de', 'la'}

# indice de presence de la RDC dans les metadonnees Wikimedia
RDC_RE = re.compile(
    r'(kinshasa|lubumbashi|goma|bukavu|matadi|kisangani|mbandaka|kananga|'
    r'kolwezi|likasi|kindu|bunia|mbuji.?mayi|kalemie|uvira|tshikapa|'
    r'bandundu|kabinda|gbadolite|gemena|isiro|buta|mbanza|kamina|lusambo|'
    r'boende|beni|kailo|inaongo|moba|kasaï|kasai|lomami|sankuru|tanganyika|'
    r'maniema|tshuapa|tshopo|ituri|ubangi|mayi.?ndombe|democratic republic of '
    r'the congo|republique democratique|kinshasa|congo|katanga|kivu|kasai|'
    r'sankuru|lualaba|tshapo|nord.?kivu|sud.?kivu|haut.?katanga|tanganyika)',
    re.I)

OTHER_COUNTRY_RE = re.compile(
    r'\b(nebraska|california|texas|florida|new york|ontario|quebec|paris|'
    r'london|barcelona|madrid|rome|italy|france|spain|belgium|portugal|'
    r'japan|china|india|brazil|kenya|tanzania|uganda|zambia|angola|'
    r'ireland|scotland|wales|australia|germany|netherlands|switzerland|'
    r'austria|poland|greece|turkey|egypt|morocco|south africa|argentina|'
    r'mexico|brazil|nepal|sri lanka|philippines|indonesia|vietnam)\b', re.I)


def api(url, params, tries=3):
    params = dict(params)
    params['format'] = 'json'
    params['formatversion'] = 2
    full = url + '?' + urllib.parse.urlencode(params)
    for attempt in range(tries):
        try:
            req = urllib.request.Request(full, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:
            print('   retry %d (%s)' % (attempt + 1, e), flush=True)
            time.sleep(4 * (attempt + 1))
    return {}


def words(name):
    s = unicodedata.normalize('NFKD', name or '')
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    ws = re.split(r'[^a-z0-9]+', s)
    return [w for w in ws if len(w) > 2 and w not in STOP]


def page_image(title, lang):
    """Image principale de l'article Wikipedia (titre exact)."""
    d = api(WIKI % lang, {'action': 'query', 'titles': title,
                          'prop': 'pageimages', 'piprop': 'thumbnail',
                          'pithumbsize': str(MAX_W), 'redirects': 1})
    for p in d.get('query', {}).get('pages', []):
        th = p.get('thumbnail')
        if th and th.get('source'):
            return th['source']
    return None


def commons_search(name, limit=8, place=None):
    """Fichiers Commons dont le titre ET le lieu concordent avec l'item.

    Regle stricte : le lieu (ville RDC ou le mot "Congo") doit apparaitre dans
    le titre, la description ou les categories, et aucun autre pays ne doit
    etre mentionne. Sinon l'image est rejetee : mieux vaut pas de photo
    qu'une photo qui montre un autre pays.

    Retourne [(url, title, blob)] ou blob = description + categories.
    """
    q = name
    d = api(COMMONS, {'action': 'query', 'generator': 'search',
                      'gsrsearch': q, 'gsrnamespace': 6, 'gsrlimit': str(limit),
                      'prop': 'imageinfo', 'iiprop': 'url|mime|size|extmetadata',
                      'iiurlwidth': str(MAX_W)})
    want = set(words(name))
    hits = []
    for p in d.get('query', {}).get('pages', []):
        info = (p.get('imageinfo') or [{}])[0]
        mime = info.get('mime', '')
        if mime not in ('image/jpeg', 'image/png'):
            continue
        w, h = info.get('width', 0), info.get('height', 0)
        if w and h and (w < 400 or h < 300):
            continue
        title = p.get('title', '')
        tw = set(words(title))
        if want and not (want & tw):
            continue
        em = info.get('extmetadata', {})
        blob = ' '.join([
            title,
            em.get('ImageDescription', {}).get('value', '') or '',
            em.get('Categories', {}).get('value', '') or '',
            em.get('ObjectName', {}).get('value', '') or '',
        ])
        blob_clean = re.sub(r'<[^>]+>', ' ', blob)
        low = blob_clean.lower()
        # le lieu RDC doit etre identifiable
        if not (RDC_RE.search(low) or place and place.lower() in low):
            continue
        # un autre pays dominant = rejet
        if OTHER_COUNTRY_RE.search(low) and not RDC_RE.search(low):
            continue
        url = info.get('thumburl') or info.get('url')
        if url:
            hits.append((url, title, blob_clean[:600]))
    return hits


def download(url, dest_base):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'image/*'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except Exception as e:
        print('   dl erreur:', e, flush=True)
        return None
    if len(data) < 6000:
        return None
    try:
        from PIL import Image
        import io as _io
        im = Image.open(_io.BytesIO(data))
        im = im.convert('RGB')
        if im.width > MAX_W:
            h = int(im.height * MAX_W / im.width)
            im = im.resize((MAX_W, h), Image.LANCZOS)
        im.save(dest_base, 'JPEG', quality=82, optimize=True)
    except Exception as e:
        print('   PIL erreur:', e, flush=True)
        return None
    return os.path.basename(dest_base)


def slugify(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace('&', ' et ')
    out = []
    for c in s:
        if c.isalnum():
            out.append(c)
        elif out and out[-1] != '-':
            out.append('-')
    return ''.join(out).strip('-')


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    raw = io.open(os.path.join(ROOT, 'assets', 'activites.js'), encoding='utf-8').read()
    items = json.loads(raw[raw.index('{'):raw.rindex('}') + 1])['items']

    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(io.open(CACHE, encoding='utf-8'))
    meta = {}
    if os.path.exists(META):
        meta = json.load(io.open(META, encoding='utf-8'))

    ok = 0
    for i, it in enumerate(items, 1):
        slug = it['slug']
        if slug in cache:
            ok += 1 if cache[slug] else 0
            continue
        dest = os.path.join(IMG_DIR, slug + '.jpg')
        got = None
        src_title = ''
        src_url = ''
        try:
            if os.path.exists(dest):
                got = slug + '.jpg'
            else:
                # 1. Wikipedia exact
                for lang in ('fr', 'en'):
                    src = page_image(it['name'], lang)
                    if src:
                        src_url = src
                        src_title = it['name'] + ' (' + lang + ' wikipedia)'
                        got = download(src, dest)
                        if got:
                            print('%3d %-42s wiki-%s' % (i, it['name'][:42], lang), flush=True)
                            break
                    time.sleep(0.4)
                # 2. Commons
                if not got:
                    for url, title, blob in commons_search(it['name'], place=it.get('place')):
                        src_url = url
                        src_title = title
                        got = download(url, dest)
                        if got:
                            print('%3d %-42s commons' % (i, it['name'][:42]), flush=True)
                            break
                        time.sleep(0.5)
        except Exception as e:
            print('%3d %-42s ERREUR %s' % (i, it['name'][:42], e), flush=True)
            got = None
        cache[slug] = got
        meta[slug] = {'file': got, 'title': src_title, 'url': src_url}
        if got:
            ok += 1
        else:
            print('%3d %-42s --' % (i, it['name'][:42]), flush=True)
        if i % 10 == 0:
            json.dump(cache, io.open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            json.dump(meta, io.open(META, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        time.sleep(0.35)

    json.dump(cache, io.open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(meta, io.open(META, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('images: %d/%d' % (ok, len(items)), flush=True)


if __name__ == '__main__':
    main()
