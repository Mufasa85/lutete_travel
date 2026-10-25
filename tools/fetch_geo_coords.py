# -*- coding: utf-8 -*-
"""Geocode les hotels (visitrdc.org) et les sites touristiques (provinces).

Chaque requete Nominatim est mise en cache dans tools/geo_cache.json : le
script est reprenable et ne re-requete jamais deux fois le meme libelle.

Aucune coordonnee n'est inventee : un libelle non trouve reste sans position
et le site l'affiche comme « localisation sur demande ».
"""
import io, json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CACHE = os.path.join(HERE, 'geo_cache.json')

# ------------------------------------------------------- libelles a geocoder
def collect_targets():
    raw = io.open(os.path.join(ROOT, 'assets', 'provinces.js'), encoding='utf-8').read()
    prov = json.loads(raw[raw.index('['):raw.rindex(']') + 1])
    prov_by_name = {p['name']: p for p in prov}

    targets = []
    hot = os.path.join(HERE, 'hotels.json')
    if os.path.exists(hot):
        for h in json.load(io.open(hot, encoding='utf-8')):
            province = prov_by_name.get(h['province'])
            for it in h['items']:
                targets.append({
                    'kind': 'hotel',
                    'name': it['name'].strip(),
                    'place': it['place'].strip(),
                    'province': h['province'],
                    'city': it['place'].split(',')[0].strip(),
                    'country': 'Democratic Republic of the Congo',
                })
    for p in prov:
        for s in p['sites']:
            targets.append({
                'kind': 'site',
                'name': s['name'].strip(),
                'place': s['place'].strip(),
                'province': p['name'],
                'city': s['place'].strip(),
                'country': 'Democratic Republic of the Congo',
            })
    # dedoublonner par nom
    seen, out = set(), []
    for t in targets:
        k = t['name'].lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(t)
    return out


def nominatim(q, limit=5):
    url = ("https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote(q) +
           "&format=json&limit=%d&extratags=1&addressdetails=1&countrycodes=cd" % limit)
    req = urllib.request.Request(
        url, headers={'User-Agent': 'LuteteTravelMaquette/1.0 (static site mockup)'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception as e:
            print('   retry %d (%s)' % (attempt + 1, e), flush=True)
            time.sleep(8 * (attempt + 1))
    return []


def pick(res, target):
    """Choisit le resultat le plus plausible : meme ville/province si possible."""
    if not res:
        return None
    want = (target.get('city') or '').lower()

    def score(r):
        a = r.get('address', {})
        s = 0
        blob = ' '.join(str(v).lower() for v in a.values() if isinstance(v, str))
        if want and want in blob:
            s += 10
        if target['country'].lower() in blob:
            s += 5
        if r.get('name', '').lower() == target['name'].lower():
            s += 8
        if r.get('osm_type') in ('way', 'relation'):
            s += 2
        return s

    best = sorted(res, key=score, reverse=True)[0]
    return {'lat': float(best['lat']), 'lon': float(best['lon']),
            'display': best.get('display_name', '')[:160],
            'osm': best.get('osm_type', '') + '/' + str(best.get('osm_id', ''))}


def main():
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(io.open(CACHE, encoding='utf-8'))
    print('cache:', len(cache), flush=True)

    targets = collect_targets()
    print('cibles:', len(targets), flush=True)

    for i, t in enumerate(targets, 1):
        key = t['name'].lower()
        if key in cache:
            continue
        q = '%s, %s, Democratic Republic of the Congo' % (t['name'], t['place'])
        res = nominatim(q)
        hit = pick(res, t)
        cache[key] = hit
        if i % 5 == 0 or hit:
            json.dump(cache, io.open(CACHE, 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
        print('%3d/%d %-40s %s' % (i, len(targets), t['name'][:40],
                                   ('OK' if hit else '-')), flush=True)
        time.sleep(1.2)

    json.dump(cache, io.open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ok = sum(1 for v in cache.values() if v)
    print('geocodes: %d/%d' % (ok, len(cache)), flush=True)


if __name__ == '__main__':
    main()
