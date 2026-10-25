/* Section "Que souhaitez-vous explorer" - Lutete Travel.
 *
 * Affiche les categories d'activites (hotels, restaurants, sites, experiences)
 * avec le nombre reel d'entrees dans le catalogue. Chaque carte mene a
 * activite.html?cat=<slug>, ou la liste est filtrable et geolocalisee.
 *
 * Dependance : assets/activites.js (window.ACTIVITES).
 */
(function () {
    "use strict";

    var $ = function (s) { return document.querySelector(s); };

    function initExplorer() {
        var grid = $("#explorer-grid");
        if (!grid) return;
        var ACT = window.ACTIVITES;
        if (!ACT || !ACT.categories) return;

        grid.innerHTML = ACT.categories.map(function (c) {
            var n = ACT.items.filter(function (it) {
                return c.types.indexOf(it.cat) !== -1;
            }).length;
            return '<a class="excard rv" href="activite.html?cat=' + encodeURIComponent(c.slug) + '">' +
                '<span class="exn">' + n + "</span>" +
                '<div class="exic"><i data-lucide="' + (c.icon || "map-pin") + '"></i></div>' +
                "<h3>" + c.label + "</h3>" +
                "<p>" + c.desc + "</p>" +
                '<span class="excta">Explorer ' + n + " établissement" + (n > 1 ? "s" : "") +
                ' <i data-lucide="arrow-right"></i></span>' +
                "</a>";
        }).join("");

        if (window.lucide) window.lucide.createIcons();
        if (typeof observe === "function") observe();
    }

    window.initExplorer = initExplorer;
})();
