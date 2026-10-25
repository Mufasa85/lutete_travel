# -*- coding: utf-8 -*-
"""Recupere les POI (hotels, restaurants, cafes, sites) de la RDC via OpenStreetMap / Nominatim.

Cache JSON incremental dans le fichier de sortie : le script peut etre relance
sans refaire les requetes deja faites.
"""
import json, os, sys, time, urllib.parse, urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'osm_poi.json')

VILLES = {
    'Kinshasa': 'Kinshasa', 'Lubumbashi': 'Lubumbashi', 'Goma': 'Goma',
    'Bukavu': 'Bukavu', 'Likasi': 'Likasi', 'Kolwezi': 'Kolwezi',
    'Matadi': 'Matadi', 'Kisangani': 'Kisangani', 'Mbandaka': 'Mbandaka',
    'Kananga': 'Kananga', 'Mbuji-Mayi': 'Mbuji-Mayi', 'Bunia': 'Bunia',
    'Uvira': 'Uvira', 'Kindu': 'Kindu', 'Kalemie': 'Kalemie', 'Bandundu': 'Bandundu',
    'Tshikapa': 'Tshikapa', 'Ibuti': None,
}
VILLES = {k: v for k, v in VILLES.items() if v}

SKIP_TYPES = {
    'bus_stop', 'bus_station', 'station', 'stop_position', 'platform', 'mobile_phone',
    'stationery', 'educational_institution', 'yes', 'attraction', 'artwork', 'viewpoint',
    'park', 'museum', 'monument', 'memorial', 'place_of_worship', 'school', 'university',
    'library', 'townhall', 'police', 'hospital', 'clinic', 'pharmacy', 'bank', 'atm',
    'supermarket', 'convenience', 'marketplace', 'bus', 'taxi', 'car_rental', 'fuel',
    'parking', 'fountain', 'waterfall', 'spring', 'peak', 'cave', 'crater', 'river',
    'lake', 'wetland', 'forest', 'hill', 'ridge', 'valley', 'plain', 'island',
    'bus_station', 'intersection', 'traffic_signals', 'crossing', 'turning_circle',
    'motorway_junction', 'milestone', 'emergency_phone', 'fire_hydrant', 'power_tower',
}

CATS = ['restaurant', 'cafe', 'bar', 'fast_food', 'hotel', 'guest_house', 'hostel',
        'lodging', 'motel', 'museum', 'attraction', 'artwork', 'viewpoint', 'park']


def norm_type(r):
    """Nominatim renvoie 'category' (large) et 'type' (precis) ; on garde le type."""
    t = r.get('type') or r.get('category') or ''
    if t in ('tourism', 'amenity', 'leisure'):
        t = r.get('type') or ''
    return t


def is_interesting(r):
    t = r.get('type') or ''
    cat = r.get('category') or ''
    if t in SKIP_TYPES:
        return False
    if cat == 'tourism' and t not in ('hotel', 'guest_house', 'hostel', 'motel',
                                      'museum', 'attraction', 'artwork', 'viewpoint',
                                      'theme_park', 'zoo', 'aquarium'):
        return False
    if cat == 'amenity' and t not in ('restaurant', 'cafe', 'bar', 'fast_food',
                                      'ice_cream', 'pub', 'beverages', 'nightclub'):
        return False
    if cat == 'shop' and t not in ('beverages', 'convenience', 'supermarket'):
        return False
    return True


def nominatim(q, limit=30):
    url = ("https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote(q) +
           "&format=json&limit=%d&extratags=1&addressdetails=1" % limit)
    req = urllib.request.Request(
        url, headers={'User-Agent': 'LuteteTravelMaquette/1.0 (static site mockup)'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception as e:
            print('   retry %d (%s)' % (attempt + 1, e), flush=True)
            time.sleep(6 * (attempt + 1))
    return []


def main():
    data = {}
    if os.path.exists(OUT):
        data = json.load(open(OUT, encoding='utf-8'))
    print('cache existant:', len(data), flush=True)

    done = set(data.keys())
    for cat in CATS:
        for ville in VILLES.values():
            key = cat + '|' + ville
            if key in done:
                continue
            res = nominatim('%s %s' % (cat, ville))
            n = 0
            for r in res:
                nm = r.get('name')
                if not nm or len(nm) < 3:
                    continue
                low = nm.lower().strip()
                if low in ('restaurant', 'hotel', 'bar', 'cafe', 'café', 'hôtel', 'hostel'):
                    continue
                if not is_interesting(r):
                    continue
                k = low + '|' + ville
                if k in data:
                    continue
                a = r.get('address', {})
                data[k] = {
                    'name': nm,
                    'cat': r.get('category'),
                    'type': norm_type(r),
                    'lat': float(r['lat']),
                    'lon': float(r['lon']),
                    'ville': a.get('city') or a.get('town') or a.get('village') or ville,
                    'quartier': a.get('neighbourhood') or a.get('suburb') or '',
                    'pays': a.get('country', 'RD Congo'),
                    'osm': r.get('osm_type', '') + '/' + str(r.get('osm_id', '')),
                }
                n += 1
            print('%-14s %-14s -> %d' % (cat, ville, n), flush=True)
            json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            time.sleep(1.3)

    print('TOTAL:', len(data), flush=True)


if __name__ == '__main__':
    main()
