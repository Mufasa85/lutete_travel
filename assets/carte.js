/* Carte interactive des 26 provinces de la RDC - Lutete Travel.
 *
 * Dependances : assets/rdc-map.js (window.RDC_SVG) et assets/provinces.js
 * (window.RDC_PROVINCES), generes par tools/build_map.py.
 *
 * Comportement :
 *  - injection du SVG de la carte dans #map-holder ;
 *  - survol / focus clavier : apercu de la province dans la fiche de droite ;
 *  - clic sur une province (ou sur une puce de la liste) : redirection vers
 *    la page de la province (province.html?p=<slug>) ;
 *  - bouton "Reserver dans la province" : pre-remplit le formulaire de
 *    reservation sur index.html.
 *
 * Initialisation : window.initRDCMap() (appele en fin du script principal,
 * pour disposer de toast() et sum()).
 */
(function () {
    "use strict";

    var $ = function (s) { return document.querySelector(s); };

    function initRDCMap() {
        var holder = $("#map-holder");
        var cardBox = $("#map-card");
        var chipBox = $("#map-chips");
        if (!holder || !cardBox || !chipBox) return;
        if (!window.RDC_SVG || !window.RDC_PROVINCES) return;
        if (holder.dataset.ready) return;
        holder.dataset.ready = "1";

        var PROV = window.RDC_PROVINCES;
        var bySlug = {};
        PROV.forEach(function (p) { bySlug[p.slug] = p; });

        var nf = new Intl.NumberFormat("fr-FR");

        /* ------------------------------------------------------------ carte */
        holder.innerHTML = window.RDC_SVG;
        var svg = $("#carte-rdc");
        var paths = Array.prototype.slice.call(svg.querySelectorAll("path"));

        /* ------------------------------------------------------ fiche province */
        function fmtArea(km2) {
            return nf.format(km2) + " km²";
        }

        function fmtPop(n) {
            if (n >= 1000000) {
                var v = (n / 1000000).toFixed(n >= 10000000 ? 0 : 1).replace(".0", "");
                return nf.format(Number(v.replace(",", "."))) + " M hab.";
            }
            return nf.format(n) + " hab.";
        }

        function renderCard(p) {
            var sites = p.sites.map(function (s) {
                return "<li><b>" + s.name + "</b> <span>— " + s.place +
                    " · " + s.desc + "</span></li>";
            }).join("");

            cardBox.innerHTML =
                '<div class="mph">' +
                '<img src="' + p.image + '" alt="' + p.name + '" loading="lazy">' +
                '<span class="badge">Province</span>' +
                "</div>" +
                '<div class="mcb">' +
                "<h3>" + p.name + "</h3>" +
                '<p class="tagline">' + p.tagline + "</p>" +
                '<div class="mstats">' +
                "<div><b>" + p.capital + "</b><span>Chef-lieu</span></div>" +
                "<div><b>" + fmtArea(p.area) + "</b><span>Superficie</span></div>" +
                "<div><b>" + fmtPop(p.pop) + "</b><span>Population</span></div>" +
                "</div>" +
                '<p class="mdesc">' + p.desc + "</p>" +
                (sites ? '<ul class="msites">' + sites + "</ul>" : "") +
                '<div class="mcta">' +
                '<a class="btn sm" href="province.html?p=' + p.slug + '">Voir la province <i data-lucide="arrow-right"></i></a>' +
                '<button class="btn sm ghost2" data-res-prov="' + p.slug + '">Réserver dans la province</button>' +
                "</div>" +
                "</div>";
            if (window.lucide) window.lucide.createIcons();
        }

        /* --------------------------------------------------------- apercu */
        function preview(slug) {
            var p = bySlug[slug];
            if (!p) return;
            paths.forEach(function (el) {
                el.classList.toggle("on", el.getAttribute("data-province") === slug);
            });
            Array.prototype.forEach.call(chipBox.children, function (c) {
                c.classList.toggle("on", c.getAttribute("data-slug") === slug);
            });
            renderCard(p);
        }

        /* ------------------------------------------------------ navigation */
        function goTo(slug) {
            if (!bySlug[slug]) return;
            location.href = "province.html?p=" + slug;
        }

        /* ------------------------------------------------------------ chips */
        chipBox.innerHTML = PROV.map(function (p) {
            return '<button type="button" class="mchip" data-slug="' + p.slug + '">' +
                p.name + "</button>";
        }).join("");

        chipBox.addEventListener("click", function (e) {
            var c = e.target.closest(".mchip");
            if (!c) return;
            goTo(c.getAttribute("data-slug"));
        });

        chipBox.addEventListener("mouseover", function (e) {
            var c = e.target.closest(".mchip");
            if (c) preview(c.getAttribute("data-slug"));
        });

        /* --------------------------------------------------- interactions */
        svg.addEventListener("mouseover", function (e) {
            var el = e.target.closest("path");
            if (el) preview(el.getAttribute("data-province"));
        });

        svg.addEventListener("click", function (e) {
            var el = e.target.closest("path");
            if (!el) return;
            goTo(el.getAttribute("data-province"));
        });

        svg.addEventListener("keydown", function (e) {
            var el = e.target.closest("path");
            if (!el) return;
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                goTo(el.getAttribute("data-province"));
            }
        });

        /* ------------------------------------------------- bouton "reserver" */
        cardBox.addEventListener("click", function (e) {
            var b = e.target.closest("[data-res-prov]");
            if (!b) return;
            e.preventDefault();
            e.stopPropagation();
            var slug = b.getAttribute("data-res-prov");
            var p = bySlug[slug];
            var sel = $("#rc");
            var chosen = "";
            if (sel && p && p.circuits && p.circuits.length) {
                for (var i = 0; i < sel.options.length; i++) {
                    var txt = sel.options[i].text;
                    for (var k = 0; k < p.circuits.length; k++) {
                        if (txt.indexOf(p.circuits[k]) !== -1) {
                            sel.selectedIndex = i;
                            chosen = p.circuits[k];
                            break;
                        }
                    }
                    if (chosen) break;
                }
            }
            location.hash = "reservation";
            if (typeof sum === "function") sum();
            if (typeof toast === "function") {
                toast(chosen
                    ? chosen + " — finalisez votre demande."
                    : "Circuit proposé en " + p.name + " — finalisez votre demande.");
            }
        });

        /* ---------------------------------------------------------- init */
        var fromHash = (location.hash.match(/^#province=([\w-]+)$/) || [])[1];
        var initial = fromHash && bySlug[fromHash] ? fromHash : PROV[0].slug;
        preview(initial);
    }

    window.initRDCMap = initRDCMap;
})();
