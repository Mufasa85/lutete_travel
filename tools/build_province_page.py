# -*- coding: utf-8 -*-
"""Genere province.html : page detaillee d'une province (province?p=<slug>).

Meme charte graphique que index.html (memes variables CSS, meme logo SVG).
Les donnees viennent de assets/provinces.js (genere par tools/build_map.py).
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from province_data import PROVINCES

OUT = os.path.join(ROOT, 'province.html')

raw = io.open(os.path.join(ROOT, 'assets', 'provinces.js'), encoding='utf-8').read()
DATA = json.loads(raw[raw.index('['):raw.rindex(']') + 1])
BY = {p['slug']: p for p in DATA}

CSS = """
        :root {
            --g: #1E7A46;
            --g2: #48B96C;
            --lime: #9ED03A;
            --bg: #fff;
            --bg2: #F5F7F6;
            --tx: #2F3437;
            --mut: #667074;
            --card: #fff;
            --gold: #C9A24B;
            --sh: 0 10px 30px rgba(20, 40, 30, .09);
            --r: 16px;
            box-sizing: border-box;
            padding-top: env(safe-area-inset-top, 0px);
            padding-bottom: env(safe-area-inset-bottom, 0px)
        }

        @media (prefers-color-scheme:dark) {
            :root:not([data-theme="light"]) {
                --bg: #121618;
                --bg2: #1a2023;
                --tx: #e8eeec;
                --mut: #9aa6a2;
                --card: #212a2d;
                --sh: 0 10px 30px rgba(0, 0, 0, .4)
            }
        }

        :root[data-theme="dark"] {
            --bg: #121618;
            --bg2: #1a2023;
            --tx: #e8eeec;
            --mut: #9aa6a2;
            --card: #212a2d;
            --sh: 0 10px 30px rgba(0, 0, 0, .4)
        }

        *,
        *::before,
        *::after {
            box-sizing: border-box
        }

        html {
            scroll-behavior: smooth
        }

        body {
            margin: 0;
            font-family: Poppins, Inter, system-ui, sans-serif;
            background: var(--bg);
            color: var(--tx);
            line-height: 1.6
        }

        a {
            color: inherit;
            text-decoration: none
        }

        img, svg {
            display: block
        }

        .wrap {
            max-width: 1180px;
            margin: 0 auto;
            padding: 0 22px
        }

        .eyebrow {
            color: var(--g2);
            font-weight: 600;
            letter-spacing: .14em;
            text-transform: uppercase;
            font-size: .78rem
        }

        h1 {
            font-size: clamp(2rem, 5vw, 3.2rem);
            line-height: 1.12;
            margin: .2em 0
        }

        h2 {
            font-size: clamp(1.6rem, 3.4vw, 2.3rem);
            line-height: 1.2;
            margin: .3rem 0 .5rem
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 0;
            cursor: pointer;
            font: 600 .95rem Poppins, sans-serif;
            padding: 14px 26px;
            border-radius: 999px;
            background: linear-gradient(135deg, var(--g), var(--g2));
            color: #fff;
            transition: .3s;
            box-shadow: 0 8px 20px rgba(30, 122, 70, .3)
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 14px 28px rgba(30, 122, 70, .4)
        }

        .btn.sm {
            padding: 10px 18px;
            font-size: .85rem
        }

        .btn.ghost {
            background: transparent;
            border: 1.5px solid var(--g2);
            color: var(--g);
            box-shadow: none
        }

        .btn.ghost:hover {
            background: var(--g2);
            color: #fff
        }

        :focus-visible {
            outline: 3px solid var(--gold);
            outline-offset: 3px
        }

        /* ------------------------------------------------------------ header */
        header {
            position: sticky;
            top: 0;
            z-index: 60;
            background: color-mix(in srgb, var(--bg) 88%, transparent);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--bg2)
        }

        header .nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
            padding: 14px 22px
        }

        .logo {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-weight: 800;
            font-size: 1.05rem;
            line-height: 1
        }

        .logo span {
            display: flex;
            flex-direction: column;
            line-height: 1.05
        }

        .logo small {
            font-size: .58rem;
            letter-spacing: .3em;
            color: var(--mut);
            font-weight: 600
        }

        header nav {
            display: flex;
            gap: 22px;
            font-size: .92rem;
            font-weight: 500
        }

        header nav a:hover {
            color: var(--g)
        }

        @media(max-width:700px) {
            header nav {
                display: none
            }
        }

        /* ------------------------------------------------------------- hero */
        .rhead {
            position: relative;
            overflow: hidden;
            color: #fff;
            padding: 130px 0 64px;
            background: linear-gradient(180deg, #1b3a2c, #1E7A46)
        }

        .rhead svg.bg {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 62%;
            opacity: .45
        }

        .rhead .wrap {
            position: relative
        }

        .rhead h1 {
            margin: .2em 0 .3em
        }

        .rhead .sub {
            opacity: .92;
            max-width: 640px;
            margin: 0
        }

        .bc {
            font-size: .85rem;
            opacity: .85;
            margin-bottom: 8px
        }

        .bc a:hover {
            text-decoration: underline
        }

        .rhead .eyebrow {
            color: var(--lime)
        }

        /* ------------------------------------------------------------ grille */
        .pgrid {
            display: grid;
            grid-template-columns: minmax(0, 1.6fr) minmax(280px, 1fr);
            gap: 40px;
            align-items: start;
            padding: 60px 0 80px
        }

        @media(max-width:900px) {
            .pgrid {
                grid-template-columns: 1fr;
                gap: 26px;
                padding: 36px 0 60px
            }
        }

        .pbox {
            background: var(--card);
            border-radius: var(--r);
            box-shadow: var(--sh);
            overflow: hidden
        }

        .pbox .ph {
            position: relative;
            aspect-ratio: 16/9;
            background: linear-gradient(135deg, var(--g), var(--g2))
        }

        .pbox .ph img {
            width: 100%;
            height: 100%;
            object-fit: cover
        }

        .pbox .pb {
            padding: 28px
        }

        .pbox h2 {
            margin-top: 0
        }

        .lead {
            color: var(--mut);
            max-width: 640px
        }

        .pstats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin: 24px 0;
            padding: 18px 0;
            border-top: 1px solid var(--bg2);
            border-bottom: 1px solid var(--bg2)
        }

        .pstats div {
            display: flex;
            flex-direction: column;
            gap: 3px
        }

        .pstats b {
            font-size: 1.1rem
        }

        .pstats span {
            font-size: .72rem;
            color: var(--mut);
            text-transform: uppercase;
            letter-spacing: .07em
        }

        @media(max-width:600px) {
            .pstats {
                grid-template-columns: 1fr 1fr
            }
        }

        .sites {
            list-style: none;
            margin: 18px 0 0;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 12px
        }

        .sites li {
            background: var(--bg2);
            border-radius: 12px;
            padding: 14px 16px 14px 38px;
            position: relative;
            font-size: .9rem
        }

        .sites li::before {
            content: "";
            position: absolute;
            left: 16px;
            top: 20px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--g2)
        }

        .sites b {
            display: block
        }

        .sites span {
            color: var(--mut);
            font-size: .84rem
        }

        .places {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0 0
        }

        .place {
            background: var(--bg2);
            border-radius: 99px;
            padding: 5px 13px;
            font-size: .78rem;
            color: var(--mut)
        }

        /* ------------------------------------------------------- aside carte */
        .aside {
            position: sticky;
            top: 88px;
            display: flex;
            flex-direction: column;
            gap: 18px
        }

        @media(max-width:900px) {
            .aside {
                position: static
            }
        }

        .minimap {
            background: var(--card);
            border-radius: var(--r);
            box-shadow: var(--sh);
            padding: 18px
        }

        .minimap h3 {
            margin: 0 0 6px;
            font-size: 1.02rem
        }

        .minimap p {
            margin: 0 0 14px;
            color: var(--mut);
            font-size: .84rem
        }

        .mapsrc {
            margin: 12px 0 0;
            font-size: .7rem;
            color: var(--mut);
            opacity: .8
        }

        .minimap svg {
            width: 100%;
            height: auto
        }

        .minimap path {
            fill: var(--bg2);
            stroke: var(--card);
            stroke-width: 1.4;
            stroke-linejoin: round;
            cursor: pointer;
            transition: fill .25s
        }

        .minimap path:hover {
            fill: var(--g2)
        }

        .minimap path.cur {
            fill: var(--g);
            stroke: var(--g2);
            stroke-width: 1.8
        }

        .nbr {
            background: var(--card);
            border-radius: var(--r);
            box-shadow: var(--sh);
            padding: 20px
        }

        .nbr h3 {
            margin: 0 0 12px;
            font-size: 1.02rem
        }

        .nbr ul {
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
            flex-wrap: wrap;
            gap: 8px
        }

        .nbr a {
            display: inline-block;
            background: var(--bg2);
            border-radius: 99px;
            padding: 7px 14px;
            font-size: .84rem;
            transition: .25s
        }

        .nbr a:hover {
            background: var(--g2);
            color: #fff
        }

        .cta {
            background: linear-gradient(180deg, var(--bg2), var(--bg));
            padding: 60px 0 80px;
            text-align: center
        }

        .cta .ctas {
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 22px
        }

        footer {
            background: #10251c;
            color: #cfe0d6;
            padding: 40px 0;
            font-size: .88rem
        }

        footer .copy {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
            border-top: 1px solid rgba(255, 255, 255, .1);
            padding-top: 18px;
            margin-top: 18px
        }

        footer a:hover {
            color: #fff
        }
"""

JS = """
        var $ = function (s) { return document.querySelector(s); };
        var nf = new Intl.NumberFormat("fr-FR");

        function fmtArea(km2) { return nf.format(km2) + " km²"; }
        function fmtPop(n) {
            if (n >= 1000000) {
                var v = (n / 1000000).toFixed(n >= 10000000 ? 0 : 1).replace(".0", "");
                return nf.format(Number(v.replace(",", "."))) + " M hab.";
            }
            return nf.format(n) + " hab.";
        }

        var PROV = window.RDC_PROVINCES || [];
        var BY = {};
        PROV.forEach(function (p) { BY[p.slug] = p; });

        function slug() {
            // Le serveur statique (npx serve) redirige /province.html vers
            // /province en perdant la query string : le fragment lui survit.
            var p = new URLSearchParams(location.search);
            if (!p.get("p") && location.hash && location.hash.length > 1) {
                var h = new URLSearchParams(location.hash.replace(/^#/, ""));
                if (h.get("p")) p.set("p", h.get("p"));
            }
            var q = p.get("p");
            if (q && BY[q]) return q;
            var h2 = (location.hash.match(/^#([\w-]+)$/) || [])[1];
            if (h2 && BY[h2]) return h2;
            return PROV.length ? PROV[0].slug : null;
        }

        function render(p) {
            document.title = p.name + " – Lutete Travel";
            $("#ptitle").textContent = p.name;
            $("#pbreadcrumb").textContent = p.name;
            $("#ptag").textContent = p.tagline;
            $("#pdesc").textContent = p.desc;
            $("#pcap").textContent = p.capital;
            $("#parea").textContent = fmtArea(p.area);
            $("#ppop").textContent = fmtPop(p.pop);
            $("#pimg").src = p.image;
            $("#pimg").alt = p.name;

            $("#psites").innerHTML = p.sites.map(function (s) {
                return "<li><b>" + s.name + "</b><span>" + s.desc + "</span></li>";
            }).join("");

            $("#pplaces").innerHTML = p.sites.map(function (s) {
                return '<span class="place">' + s.place + "</span>";
            }).join("");

            // circuits proposes dans la province
            $("#pcircuits").innerHTML = (p.circuits || []).length
                ? '<div class="places">' + p.circuits.map(function (c) {
                    return '<span class="place">' + c + "</span>";
                }).join("") + "</div>"
                : "";

            $("#pnbr").innerHTML = p.neighbours.map(function (n) {
                var q = BY[n];
                return '<li><a href="province?p=' + q.slug + '">' + q.name + "</a></li>";
            }).join("");

            // carte : on met la province courante en evidence
            document.querySelectorAll("#minimap-holder path").forEach(function (el) {
                el.classList.toggle("cur", el.getAttribute("data-province") === p.slug);
            });

            var link = $("#plink");
            link.href = "index#provinces";
            $("#pback").href = "index#provinces";
        }

        function load() {
            var s = slug();
            if (!s) return;
            render(BY[s]);
        }

        // mini-carte : on injecte le SVG complet et on masque tout sauf la province
        if (window.RDC_SVG) {
            var holder = $("#minimap-holder");
            holder.innerHTML = window.RDC_SVG;
            var svg = holder.querySelector("svg");
            svg.removeAttribute("id");
            svg.setAttribute("aria-label", "Carte des provinces de la RDC");
            svg.addEventListener("click", function (e) {
                var el = e.target.closest("path");
                if (!el) return;
                location.href = "province?p=" + el.getAttribute("data-province");
            });
        }

        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", load);
        } else {
            load();
        }
"""

MINI_JS = ""


def logo_svg():
    return ('<svg width="42" height="42" viewBox="0 0 100 100" aria-hidden="true">'
            '<defs><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#3dba4a"/><stop offset="1" stop-color="#b4d836"/>'
            '</linearGradient></defs><circle cx="50" cy="50" r="48" fill="url(#lg)"/>'
            '<path d="M8 78L34 52l10 10 14-26 12 20 8-8 8 30z" fill="#2F3437"/>'
            '<circle cx="56" cy="30" r="6" fill="#2F3437"/></svg>')


html = u"""<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>Province – Lutete Travel</title>
    <meta name="description"
        content="Découvrez les sites et paysages d'une province de la République démocratique du Congo avec Lutete Travel.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap"
        rel="stylesheet">
    <style>%(css)s    </style>
</head>

<body>
    <header>
        <div class="nav wrap">
            <a href="index" class="logo">%(logo)s<span>Lutete<small>TRAVEL</small></span></a>
            <nav aria-label="Navigation principale">
                <a href="index#destinations">Destinations</a>
                <a href="index#circuits">Circuits</a>
                <a href="index#provinces">Provinces</a>
                <a href="index#reservation">Réserver</a>
            </nav>
            <a class="btn sm" href="index#reservation">Réserver</a>
        </div>
    </header>

    <main>
        <section class="rhead">
            <svg class="bg" viewBox="0 0 1440 300" preserveAspectRatio="none" aria-hidden="true">
                <path d="M0 300V160l200-100 160 90 240-130 220 150 200-90 200 110 220-70v240z"
                    fill="#9ED03A" />
            </svg>
            <div class="wrap">
                <nav class="bc" aria-label="Fil d’Ariane">
                    <a href="index">Accueil</a> /
                    <a href="index#provinces">Provinces</a> / <span id="pbreadcrumb">Province</span>
                </nav>
                <span class="eyebrow">République démocratique du Congo</span>
                <h1 id="ptitle">Province</h1>
                <p class="sub" id="ptag"></p>
            </div>
        </section>

        <div class="wrap pgrid">
            <article class="pbox">
                <div class="ph"><img id="pimg" src="" alt=""></div>
                <div class="pb">
                    <h2>La province en bref</h2>
                    <div class="pstats">
                        <div><b id="pcap">—</b><span>Chef-lieu</span></div>
                        <div><b id="parea">—</b><span>Superficie</span></div>
                        <div><b id="ppop">—</b><span>Population</span></div>
                    </div>
                    <p class="lead" id="pdesc"></p>

                    <h2>Sites à découvrir</h2>
                    <ul class="sites" id="psites"></ul>
                    <div class="places" id="pplaces"></div>

                    <h2 style="margin-top:34px">Organiser votre séjour</h2>
                    <p class="lead">Nos conseillers construisent un circuit adapté à votre rythme, avec un guide
                        professionnel sur place.</p>
                    <div id="pcircuits" style="margin-top:16px"></div>
                    <div class="ctas" style="justify-content:flex-start;margin-top:20px">
                        <a class="btn" href="index#reservation">Réserver un circuit <i
                                data-lucide="arrow-right"></i></a>
                        <a class="btn ghost" id="pback" href="index#provinces">Voir toutes les provinces</a>
                    </div>
                </div>
            </article>

            <aside class="aside">
                <div class="minimap">
                    <h3>Situation dans la RDC</h3>
                    <p>Cliquez sur une province pour y aller.</p>
                    <div id="minimap-holder"></div>
                    <p class="mapsrc">Limites : geoBoundaries ADM1 (ODbL 1.0).</p>
                </div>

                <div class="nbr">
                    <h3>Provinces limitrophes</h3>
                    <ul id="pnbr"></ul>
                </div>
            </aside>
        </div>

        <section class="cta">
            <div class="wrap">
                <span class="eyebrow">Prêt à partir</span>
                <h2>Une autre province vous attire ?</h2>
                <p class="lead" style="margin-inline:auto">Parcourez la carte interactive et choisissez votre
                    destination.</p>
                <div class="ctas">
                    <a class="btn" id="plink" href="index#provinces">Explorer la carte de la RDC <i
                            data-lucide="map"></i></a>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <div class="wrap">
            <div class="copy">
                <span>© 2026 Lutete Travel. Tous droits réservés.</span>
                <span><a href="index#contact">Contact</a> · <a href="index#provinces">Provinces</a></span>
            </div>
        </div>
    </footer>

    <script src="assets/rdc-map.js"></script>
    <script src="assets/provinces.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/lucide@0.469.0/dist/umd/lucide.min.js"></script>
    <script>%(js)s    </script>
</body>

</html>
""" % {'css': CSS, 'js': JS, 'logo': logo_svg()}

with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

print('written:', OUT, '%.1f Ko' % (len(html.encode('utf-8')) / 1024.0))
print('provinces disponibles:', len(DATA))
