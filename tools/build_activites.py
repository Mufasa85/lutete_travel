# -*- coding: utf-8 -*-
"""Catalogue des activites lutete-travel : preparation des donnees POI.

Sources :
  - hotels.json      : hotels de la RDC par province (visitrdc.org/hotels)
  - osm_poi.json     : POI OpenStreetMap (restaurants, cafes, hotels) avec GPS
  - geo_cache.json   : geocodage Nominatim des hotels et sites (OSM / ODbL 1.0)
  - circuits         : circuits de l'index.html (experiences)

Sortie : assets/activites.json consomme par activite.html.
Aucune coordonnee n'est inventee : sans geocode verifie, l'item est marque
« localisation sur demande ».
"""
import io, json, os, re, sys, unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ACT_JS = os.path.join(ROOT, 'assets', 'activites.js')
PROV_JS = os.path.join(ROOT, 'assets', 'provinces.js')
OSM_JSON = os.path.join(HERE, 'osm_poi.json')
GEO_JSON = os.path.join(HERE, 'geo_cache.json')
HOTELS_JSON = os.path.join(HERE, 'hotels.json')

# ---------------------------------------------------------------- provinces
raw = io.open(PROV_JS, encoding='utf-8').read()
PROV = json.loads(raw[raw.index('['):raw.rindex(']') + 1])
PROV_BY_NAME = {p['name']: p for p in PROV}
PROV_BY_SLUG = {p['slug']: p for p in PROV}

CAPITAL_TO_PROV = {}
for p in PROV:
    CAPITAL_TO_PROV[p['capital'].lower()] = p

# ------------------------------------------------------------------- sources
osm = json.load(io.open(OSM_JSON, encoding='utf-8')) if os.path.exists(OSM_JSON) else {}
geo = json.load(io.open(GEO_JSON, encoding='utf-8')) if os.path.exists(GEO_JSON) else {}
hotels_by_prov = {}
if os.path.exists(HOTELS_JSON):
    for h in json.load(io.open(HOTELS_JSON, encoding='utf-8')):
        hotels_by_prov[h['province']] = h

CAT_LABEL = {
    'restaurant': 'Restaurant', 'cafe': 'Café', 'bar': 'Bar', 'pub': 'Pub',
    'fast_food': 'Restauration rapide', 'ice_cream': 'Glacier',
    'beverages': 'Boissons', 'nightclub': 'Boîte de nuit',
    'internet_cafe': 'Cybercafé',
    'hotel': 'Hôtel', 'guest_house': "Maison d'hôtes", 'hostel': 'Auberge de jeunesse',
    'motel': 'Motel', 'lodging': 'Hébergement', 'apartments': 'Appartements',
    'house': 'Résidence', 'apartment': 'Appartement', 'camp_site': 'Camping',
    'museum': 'Musée', 'attraction': 'Site', 'artwork': 'Œuvre',
    'viewpoint': 'Point de vue', 'park': 'Parc', 'experience': 'Expérience',
}

OSM_DESC = {
    'restaurant': 'Table locale et internationale, sur place ou en terrasse.',
    'cafe': 'Café pour une pause, un café et un croissant.',
    'bar': 'Bar et lounge, cocktails et ambiance du soir.',
    'pub': 'Pub et bar à ambiance conviviale.',
    'fast_food': 'Restauration rapide, sandwichs et menus à emporter.',
    'ice_cream': 'Glacier et desserts artisanaux.',
    'beverages': 'Détaillant de boissons, liqueurs et jus locaux.',
    'nightclub': 'Club et discothèque.',
    'internet_cafe': 'Cybercafé et espace de travail.',
    'hotel': 'Hôtel avec services et restauration.',
    'guest_house': "Maison d'hôtes, hébergement simple et convivial.",
    'hostel': 'Auberge de jeunesse, chambres partagées.',
    'motel': 'Motel, idéal pour un passage sur la route.',
    'lodging': 'Hébergement de passage.',
    'apartments': 'Appartements meublés.',
    'house': 'Résidence privée.',
    'apartment': 'Appartement en location.',
    'camp_site': 'Camping, emplacement de tente au calme.',
    'museum': 'Musée et collections.',
    'attraction': 'Site touristique à découvrir.',
    'artwork': 'Œuvre, monument ou sculpture notable.',
    'viewpoint': 'Point de vue panoramique.',
    'park': 'Parc et espace vert.',
}

RESTAURANT_TYPES = {'restaurant', 'cafe', 'bar', 'pub', 'fast_food', 'ice_cream',
                     'beverages', 'nightclub', 'internet_cafe'}
HOTEL_TYPES = {'hotel', 'guest_house', 'hostel', 'motel', 'lodging', 'apartments',
               'house', 'apartment', 'camp_site'}


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


def prov_for(ville):
    v = (ville or '').strip().lower()
    if v in CAPITAL_TO_PROV:
        return CAPITAL_TO_PROV[v]
    for name, p in PROV_BY_NAME.items():
        if name.lower() == v:
            return p
    for p in PROV:
        if p['capital'].lower() in v or v in p['capital'].lower():
            return p
    return None


items = []
seen = set()


def add(name, cat, place, province, desc, source, lat=None, lon=None, osm_ref=''):
    key = slugify(name)
    if not key or key in seen:
        return None
    seen.add(key)
    it = {
        'slug': key,
        'name': name,
        'cat': cat,
        'catLabel': CAT_LABEL.get(cat, cat.title()),
        'place': place,
        'province': province['slug'] if province else '',
        'provinceName': province['name'] if province else '',
        'desc': desc,
        'source': source,
        'lat': lat,
        'lon': lon,
        'osm': osm_ref,
        'hasCoords': lat is not None and lon is not None,
        'image': '',
    }
    items.append(it)
    return it


def geocode(name):
    """Retourne (lat, lon, display, osm_ref) depuis le cache Nominatim."""
    g = geo.get(name.strip().lower())
    if not g:
        return (None, None, '', '')
    return (g['lat'], g['lon'], g.get('display', ''), g.get('osm', ''))


# ---------------------------------------------- 1. hotels (visitrdc.org + OSM)
for prov_name, h in hotels_by_prov.items():
    province = PROV_BY_NAME.get(prov_name)
    if not province:
        continue
    for it in h['items']:
        name = it['name'].strip()
        place = it['place'].strip()
        desc = it['desc'].strip()
        if desc.startswith('Hébergement à'):
            desc = ('Hébergement %s — réservation confirmée par notre équipe '
                    'Lutete Travel.' % place.split(',')[0].strip())

        lat, lon, display, osm_ref = geocode(name)
        if lat is None:
            # recoupement par nom exact dans le cache OSM brut
            for k, o in osm.items():
                if o['name'].lower() == name.lower() and o.get('type') in HOTEL_TYPES:
                    lat, lon = o['lat'], o['lon']
                    osm_ref = o.get('osm', '')
                    break
        add(name, 'hotel', place, province, desc, 'visitrdc.org', lat, lon, osm_ref)

# ------------------------------- 2. hebergements OSM non couverts par visitrdc
for k, o in osm.items():
    if o.get('type') not in HOTEL_TYPES:
        continue
    if slugify(o['name']) in seen:
        continue
    province = prov_for(o.get('ville'))
    if not province:
        continue
    ville = (o.get('ville') or '').strip()
    quartier = (o.get('quartier') or '').strip()
    place = ', '.join([x for x in (quartier, ville) if x]) or province['capital']
    add(o['name'].strip(), o.get('type'), place, province,
        OSM_DESC.get(o.get('type'), 'Hébergement.'), 'OpenStreetMap',
        o['lat'], o['lon'], o.get('osm', ''))

# ---------------------------------------------- 3. restaurants, cafes, bars
for k, o in osm.items():
    t = o.get('type')
    if t not in RESTAURANT_TYPES:
        continue
    if slugify(o['name']) in seen:
        continue
    province = prov_for(o.get('ville'))
    if not province:
        continue
    ville = (o.get('ville') or '').strip()
    quartier = (o.get('quartier') or '').strip()
    place = ', '.join([x for x in (quartier, ville) if x]) or province['capital']
    cat = 'restaurant' if t in ('restaurant', 'fast_food', 'pub', 'ice_cream',
                                'beverages', 'nightclub', 'internet_cafe') else t
    add(o['name'].strip(), cat, place, province,
        OSM_DESC.get(t, 'Établissement à %s.' % (ville or province['capital'])),
        'OpenStreetMap', o['lat'], o['lon'], o.get('osm', ''))

# ------------------------------------------------ 4. sites touristiques
for p in PROV:
    for s in p['sites']:
        lat, lon, display, osm_ref = geocode(s['name'])
        add(s['name'], 'attraction', s['place'], PROV_BY_SLUG[p['slug']],
            s['desc'], 'visitrdc.org', lat, lon, osm_ref)

# ---------------------------------------------------- 5. experiences
# circuits de l'index.html : D (destinations) et C (circuits)
index_html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()


def parse_js_array(name):
    """Parse un tableau JS de tableaux de valeurs (strings et nombres)."""
    m = re.search(r'const %s = (\[.*?\]);' % name, index_html, re.S)
    if not m:
        return []
    txt = m.group(1)

    rows = []
    depth = 0
    cur = ''
    instr = False
    esc = False
    for ch in txt:
        if instr:
            cur += ch
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                instr = False
            continue
        if ch == '"':
            instr = True
            cur += ch
        elif ch in '[{':
            depth += 1
            cur += ch
        elif ch in ']}':
            depth -= 1
            cur += ch
            if depth == 0:
                rows.append(cur)
                cur = ''
        elif ch == ',' and depth == 1:
            rows.append(cur)
            cur = ''
        else:
            cur += ch
    if cur.strip():
        rows.append(cur)

    out = []
    for r in rows:
        r = r.strip()
        if not (r.startswith('[') and r.endswith(']')):
            continue
        vals = []
        for m2 in re.finditer(r'"((?:[^"\\]|\\.)*)"|(-?\d+(?:\.\d+)?)', r):
            if m2.group(1) is not None:
                vals.append(m2.group(1).replace('\\"', '"').replace('\\u2019', '’'))
            else:
                v = float(m2.group(2))
                vals.append(int(v) if v == int(v) else v)
        if vals:
            out.append(vals)
    return out


D = parse_js_array('D')
C = parse_js_array('C')

# Les destinations/circuits sont localises dans leur province quand elle est connue.
CIRCUIT_PROV = {
    'Parc des Virunga': 'Nord-Kivu', 'Mont Nyiragongo': 'Nord-Kivu',
    'Chutes de Zongo': 'Kongo-Central', 'Lola ya Bonobo': 'Kinshasa',
    'Ascension du volcan': 'Nord-Kivu', 'Safari Savane Dorée': 'Haut-Katanga',
    'Cascades & forêt': 'Kasaï',
}

for d in D:
    name, country, days, level, price, stars = d[0], d[1], d[2], d[3], d[4], d[5]
    if country != 'RDC':
        continue
    prov_name = CIRCUIT_PROV.get(name)
    province = PROV_BY_NAME.get(prov_name) if prov_name else None
    place = province['capital'] if province else 'RD Congo'
    desc = ('Circuit %s — %s, %s jours, %s. Note %s/5.' %
            (level.lower(), place, days, level.lower(), stars))
    add(name, 'experience', place, province, desc, 'Lutete Travel')

for c in C:
    name, level, days, dist, price, places, guide = c[0], c[1], c[2], c[3], c[4], c[5], c[6]
    prov_name = CIRCUIT_PROV.get(name)
    province = PROV_BY_NAME.get(prov_name) if prov_name else None
    place = province['capital'] if province else 'RD Congo'
    desc = ('%s sur %s, %s — %s $, guide %s.' % (level, days, dist, price, guide))
    add(name, 'experience', place, province, desc, 'Lutete Travel')

# ------------------------------------------------------ categories finales
CATEGORIES = [
    {'slug': 'hotels', 'label': 'Hôtels', 'icon': 'bed-double',
     'desc': 'Hôtels, maisons d’hôtes et hébergements dans les 26 provinces.',
     'types': ['hotel', 'guest_house', 'hostel', 'motel', 'lodging',
               'apartments', 'house', 'apartment', 'camp_site']},
    {'slug': 'restaurants', 'label': 'Restaurants', 'icon': 'utensils',
     'desc': 'Tables, cafés et bars où goûter la cuisine congolaise.',
     'types': ['restaurant', 'cafe', 'bar', 'pub', 'fast_food', 'ice_cream',
               'beverages', 'nightclub', 'internet_cafe']},
    {'slug': 'sites', 'label': 'Sites', 'icon': 'landmark',
     'desc': 'Parcs, cascades, grottes et monuments à ne pas manquer.',
     'types': ['attraction', 'museum', 'artwork', 'viewpoint', 'park']},
    {'slug': 'experiences', 'label': 'Expériences', 'icon': 'compass',
     'desc': 'Circuits, treks et safaris encadrés par nos guides.',
     'types': ['experience']},
]

out = {'categories': CATEGORIES, 'items': items}

# ---------------------------------------------------------- images reelles
# tools/image_cache.json : slug -> nom de fichier dans assets/img/
# (genere par tools/fetch_images.py - sources Wikipedia / Wikimedia Commons)
IMG_CACHE = os.path.join(HERE, 'image_cache.json')
if os.path.exists(IMG_CACHE):
    img_cache = json.load(io.open(IMG_CACHE, encoding='utf-8'))
    n_img = 0
    for it in items:
        f = img_cache.get(it['slug'])
        if f and os.path.exists(os.path.join(ROOT, 'assets', 'img', f)):
            it['image'] = 'assets/img/' + f
            n_img += 1
    print('images attachees: %d/%d' % (n_img, len(items)))

# ecriture JS (window.ACTIVITES = ...)
with io.open(ACT_JS, 'w', encoding='utf-8') as f:
    f.write('/* Catalogue des activites : hotels, restaurants, sites, experiences.\n'
            '   Sources : visitrdc.org, OpenStreetMap (ODbL 1.0), circuits du site.\n'
            '   Genere par tools/build_activites.py - ne pas editer a la main. */\n')
    f.write('window.ACTIVITES = %s;\n' % json.dumps(out, ensure_ascii=False, separators=(',', ':')))

print('activites:', len(items))
print(Counter(i['cat'] for i in items).most_common())
print('avec coordonnees verifiees:', sum(1 for i in items if i['hasCoords']),
      '/', len(items))
for c in CATEGORIES:
    n = sum(1 for i in items if i['cat'] in c['types'])
    print('  %-14s %d' % (c['slug'], n))
print('written', ACT_JS)