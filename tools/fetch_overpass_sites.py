# -*- coding: utf-8 -*-
"""Geocode les sites naturels via Overpass API (OpenStreetMap).

Nominatim est fait pour les adresses et sehongne sur les noms de sites
naturels. Overpass interroge directement les balises OSM (tourism=attraction,
leisure=park, natural=*, waterway=waterfall...) : c'est la bonne source.

Sortie : tools/overpass_sites.json, fusionne ensuite par build_activites.py.
"""
import io, json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

# Requete : tout le pays, balises touristiques et naturelles avec un nom.
# L'area ISO3166 n'est pas resolue par Overpass : on utilise la bounding box
# de la RDC (sud-ouest ~13.4E/-13.5S, nord-est ~31.5E/5.5N).
QUERY = """
[out:json][timeout:240];
(
  nwr["name"]["tourism"~"attraction|museum|viewpoint|artwork|gallery|theme_park|zoo|aquarium"](-13.5,12.0,6.0,31.5);
  nwr["name"]["leisure"~"park|nature_reserve"](-13.5,12.0,6.0,31.5);
  nwr["name"]["natural"~"waterfall|spring|crater|cave_entrance|peak|volcano|rock"](-13.5,12.0,6.0,31.5);
  nwr["name"]["historic"~"castle|monument|memorial|archaeological_site"](-13.5,12.0,6.0,31.5);
  nwr["name"]["waterway"="waterfall"](-13.5,12.0,6.0,31.5);
);
out center tags;
"""


def fetch():
    data = urllib.parse.urlencode({'data': QUERY}).encode()
    for ep in ENDPOINTS:
        for attempt in range(2):
            try:
                req = urllib.request.Request(
                    ep, data=data,
                    headers={'User-Agent': 'LuteteTravelMaquette/1.0 (static site mockup)'})
                print('query', ep, flush=True)
                with urllib.request.urlopen(req, timeout=240) as r:
                    return json.load(r)
            except Exception as e:
                print('  retry %d (%s)' % (attempt + 1, e), flush=True)
                time.sleep(10 * (attempt + 1))
    return None


def main():
    out = os.path.join(HERE, 'overpass_sites.json')
    res = fetch()
    if not res:
        print('ECHEC: aucune reponse Overpass', flush=True)
        return 1

    items = []
    for el in res.get('elements', []):
        t = el.get('tags', {})
        name = (t.get('name') or '').strip()
        if not name:
            continue
        lat = el.get('lat') or (el.get('center') or {}).get('lat')
        lon = el.get('lon') or (el.get('center') or {}).get('lon')
        if lat is None or lon is None:
            continue
        kind = (t.get('tourism') or t.get('leisure') or t.get('natural') or
                t.get('historic') or t.get('waterway') or t.get('amenity') or '')
        items.append({
            'name': name,
            'kind': kind,
            'lat': float(lat),
            'lon': float(lon),
            'city': t.get('addr:city') or t.get('addr:town') or t.get('addr:village') or '',
            'suburb': t.get('addr:suburb') or t.get('addr:neighbourhood') or '',
            'description': (t.get('description') or t.get('description:fr') or
                            t.get('tourism_description') or ''),
            'wikidata': t.get('wikidata', ''),
            'wikipedia': t.get('wikipedia', ''),
            'osm': t.get('type', el.get('type', '')) + '/' + str(el.get('id', '')),
        })

    with io.open(out, 'w', encoding='utf-8') as f:
        f.write(json.dumps(items, ensure_ascii=False, indent=1))
    print('sites Overpass:', len(items), '->', out, flush=True)
    for it in items[:20]:
        print('  %-45s %-18s %s %s' % (it['name'][:45], it['kind'],
                                        it['lat'], it['lon']), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
