# -*- coding: utf-8 -*-
"""Genere les assets JS du site : carte SVG RDC + donnees des 26 provinces.

Sorties :
  assets/rdc-map.js      -> window.RDC_SVG (SVG inline, 26 <path>)
  assets/provinces.js     -> window.RDC_PROVINCES (donnees editorial + limitrophes)

Les frontieres sont calculees depuis le GeoJSON geoBoundaries ADM1 (ODbL 1.0) :
deux provinces sont limitrophes si leurs polygones se touchent (distance < 0.02 deg).
"""
import io, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from province_data import PROVINCES, IMAGES

TMP = os.environ.get('LOCALAPPDATA', os.path.expanduser('~')) + os.sep + 'Temp'
SRC_GEOJSON = os.path.join(TMP, 'drc_full.geojson')
if not os.path.exists(SRC_GEOJSON):
    SRC_GEOJSON = os.path.join(TMP, 'drc_adm1.geojson')

NAME_MAP = {
    'Upper Uele': 'haut-uele', 'Ituri': 'ituri', 'Tshopo': 'tshopo',
    'Lower Uele': 'bas-uele', 'Mongala': 'mongala', 'Nord-Ubangi': 'nord-ubangi',
    'Tshuapa': 'tshuapa', 'Équateur': 'equateur', 'Haut-Katanga': 'haut-katanga',
    'Haut-Lomami': 'haut-lomami', 'Kongo-Central': 'kongo-central',
    'Kwango': 'kwango', 'Sankuru': 'sankuru', 'Sud-Ubangi': 'sud-ubangi',
    'Tanganyika': 'tanganyika', 'Kasai': 'kasai', 'Kasai-Oriental': 'kasai-oriental',
    'Maniema': 'maniema', 'North Kivu': 'nord-kivu', 'South Kivu': 'sud-kivu',
    'Central Kasai': 'kasai-central', 'Lomami': 'lomami', 'Lualaba': 'lualaba',
    'Kinshasa': 'kinshasa', 'Kwilu': 'kwilu', 'Mai-Ndombe': 'mai-ndombe',
}

SCALE = 62.0
TOL = 0.55
NEIGHBOUR_TOL_DEG = 0.02   # ~2.2 km : contact de frontiere


# --------------------------------------------------------------- projection
def proj(lon, lat):
    return (lon * SCALE, -lat * SCALE)


def dp(points, tol):
    """Douglas-Peucker."""
    if len(points) < 3:
        return points
    dmax, idx = 0.0, 0
    x1, y1 = points[0]
    x2, y2 = points[-1]
    dx, dy = x2 - x1, y2 - y1
    den = math.hypot(dx, dy)
    for i in range(1, len(points) - 1):
        x0, y0 = points[i]
        if den == 0:
            d = math.hypot(x0 - x1, y0 - y1)
        else:
            d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / den
        if d > dmax:
            dmax, idx = d, i
    if dmax > tol:
        a = dp(points[:idx + 1], tol)
        b = dp(points[idx:], tol)
        return a[:-1] + b
    return [points[0], points[-1]]


def ring_to_path(ring, tol):
    pts = dp([proj(lon, lat) for lon, lat in ring], tol)
    if len(pts) < 3:
        return ''
    return ' '.join(('M' if i == 0 else 'L') + '%.1f %.1f' % p
                    for i, p in enumerate(pts)) + ' Z'


def geom_rings(geom):
    return [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']


# ------------------------------------------------------ frontieres partagees
def seg_dist(p, q, r, s):
    """Distance entre segments PQ et RS (0 si ils se croisent)."""
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    d1, d2 = cross(r, s, p), cross(r, s, q)
    d3, d4 = cross(p, q, r), cross(p, q, s)
    if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)):
        return 0.0
    def pt_seg(p, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        den = dx * dx + dy * dy
        if den == 0:
            return math.hypot(p[0] - a[0], p[1] - a[1])
        t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / den))
        return math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy))
    return min(pt_seg(p, r, s), pt_seg(q, r, s), pt_seg(r, p, q), pt_seg(s, p, q))


def rings_touch(a, b, tol):
    """True si deux anneaux (listes de points lon/lat) se touchent."""
    for i in range(len(a) - 1):
        for j in range(len(b) - 1):
            if seg_dist(a[i], a[i + 1], b[j], b[j + 1]) <= tol:
                return True
    return False


def bbox_close(a, b, pad):
    ax = [p[0] for p in a]; ay = [p[1] for p in a]
    bx = [p[0] for p in b]; by = [p[1] for p in b]
    if (max(ax) + pad < min(bx) or max(bx) + pad < min(ax) or
            max(ay) + pad < min(by) or max(by) + pad < min(ay)):
        return False
    return True


def cells(ring, size):
    """Cellules de la grille spatiale couvertes par une anneau."""
    out = set()
    for lon, lat in ring:
        out.add((int(math.floor(lon / size)), int(math.floor(lat / size))))
    return out


def coarse_rings(ring, tol_deg):
    """Anneau simplifie en degres (tolerance geographique)."""
    px = [(lon, -lat) for lon, lat in ring]
    return [(x, -y) for x, y in dp(px, tol_deg)]


# ------------------------------------------------------------------ build
data = json.load(io.open(SRC_GEOJSON, encoding='utf-8'))
prov_geo = {}
allpts = []
for feat in data['features']:
    slug = NAME_MAP[feat['properties']['shapeName']]
    parts = []
    rings = []
    for poly in geom_rings(feat['geometry']):
        parts.append(ring_to_path(poly[0], TOL) +
                     ''.join(ring_to_path(h, TOL) for h in poly[1:]))
        rings.append(poly[0])
        for lon, lat in poly[0]:
            allpts.append(proj(lon, lat))
    prov_geo[slug] = {'d': ''.join(parts), 'rings': rings}

minx = min(p[0] for p in allpts); maxx = max(p[0] for p in allpts)
miny = min(p[1] for p in allpts); maxy = max(p[1] for p in allpts)
PAD = 14
vb = (minx - PAD, miny - PAD, (maxx - minx) + 2 * PAD, (maxy - miny) + 2 * PAD)


def fmt(v):
    s = '%.1f' % v
    return s[:-2] if s.endswith('.0') else s


slugs = [p['slug'] for p in PROVINCES]
by_slug = {p['slug']: p for p in PROVINCES}

paths = []
for p in PROVINCES:
    d = prov_geo[p['slug']]['d']
    paths.append(
        '<path id="p-%s" data-province="%s" tabindex="0" role="link" '
        'aria-label="%s — voir la province" d="%s"/>' % (
            p['slug'], p['slug'], p['name'], d))

svg = ('<svg id="carte-rdc" viewBox="0 0 %s %s" role="img" '
       'aria-label="Carte interactive des 26 provinces de la République '
       'démocratique du Congo" xmlns="http://www.w3.org/2000/svg">'
       '<g id="carte-rdc-groupe" transform="translate(%s %s)">%s</g></svg>') % (
    fmt(vb[2]), fmt(vb[3]),
    fmt(-vb[0]), fmt(-vb[1]), ''.join(paths))

# ------------------------------------------------------ limitrophes (frontiere)
# Grille spatiale : on ne compare que les paires dont les cellules se recouvrent.
GRID = 0.25  # degres (~27 km)
COARSE_TOL = 0.01  # degres (~1.1 km) pour le test de contact

grid_index = {}   # slug -> set(cellules)
for slug, geo in prov_geo.items():
    cs = set()
    for ring in geo['rings']:
        cs |= cells(ring, GRID)
    grid_index[slug] = cs

coarse = {slug: [coarse_rings(r, COARSE_TOL) for r in geo['rings']]
          for slug, geo in prov_geo.items()}

neigh = {s: set() for s in slugs}
keys = slugs
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        a, b = keys[i], keys[j]
        # les deux provinces doivent partager au moins une cellule (ou etre
        # adjacentes : la simplification peut deplacer la frontiere d'une cellule)
        if not (grid_index[a] & grid_index[b]):
            continue
        touch = False
        for ra in coarse[a]:
            for rb in coarse[b]:
                if not bbox_close(ra, rb, COARSE_TOL):
                    continue
                if rings_touch(ra, rb, COARSE_TOL):
                    touch = True
                    break
            if touch:
                break
        if touch:
            neigh[a].add(b)
            neigh[b].add(a)

out = []
for p in PROVINCES:
    s = p['slug']
    q = dict(p)
    q['neighbours'] = sorted(neigh[s], key=lambda x: by_slug[x]['name'])
    q['image'] = IMAGES[slugs.index(s) % len(IMAGES)]
    out.append(q)

os.makedirs(os.path.join(ROOT, 'assets'), exist_ok=True)

with io.open(os.path.join(ROOT, 'assets', 'rdc-map.js'), 'w', encoding='utf-8') as f:
    f.write(u'/* Carte interactive RDC - 26 provinces.\n'
            u'   Limites : geoBoundaries ADM1 COD (ODbL 1.0).\n'
            u'   Genere par tools/build_map.py - ne pas editer a la main. */\n')
    f.write(u'window.RDC_SVG = %s;\n' % json.dumps(svg))

with io.open(os.path.join(ROOT, 'assets', 'provinces.js'), 'w', encoding='utf-8') as f:
    f.write(u'/* Donnees des 26 provinces de la RDC.\n'
            u'   Chefs-lieux / superficies / populations : Wikipedia FR (Annuaire\n'
            u'   statistique 2015, INS). Sites : visitrdc.org/sites.\n'
            u'   Genere par tools/build_map.py - ne pas editer a la main. */\n')
    f.write(u'window.RDC_PROVINCES = %s;\n' % json.dumps(out, ensure_ascii=False))

print('SVG   : %d provinces, %d octets' % (len(paths), len(svg)))
print('Donnees: %d provinces' % len(out))
for q in out:
    print('  %-16s %-13s limitrophes: %s' % (
        q['name'], q['capital'], ', '.join(by_slug[n]['name'] for n in q['neighbours'])))
