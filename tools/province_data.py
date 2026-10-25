# -*- coding: utf-8 -*-
"""Donnees canoniques des 26 provinces de la RDC pour Lutete Travel.

Sources :
  - chef-lieu / superficie / population 2015 : Wikipedia FR (table "Provinces de la
    République démocratique du Congo", recopiée de l'Annuaire statistique 2015 de l'INS).
  - sites touristiques : visitrdc.org/sites (liste "Sites touristiques de la RDC").
  - limites administratives : geoBoundaries ADM1 COD (ODbL 1.0).
"""

PROVINCES = [
    {
        'slug': 'kinshasa', 'name': 'Kinshasa', 'capital': 'Kinshasa',
        'area': 9965, 'pop': 11575000,
        'tagline': "La capitale, du fleuve Congo aux collines de Ngaliema",
        'circuits': ['Lola ya Bonobo'],
        'desc': "Capitale de la République, Kinshasa s'étire le long du fleuve Congo entre Gombe, Limete et les collines de Ngaliema. Musée national, marché de Zando, jardin botanique et chutes de la Lukaya : la ville se découvre à pied, entre art, Histoire et espaces verts.",
        'sites': [
            {'name': 'Lola ya Bonobo', 'place': 'Mont-Ngafula', 'desc': 'Seul sanctuaire au monde dédié aux bonobos orphelins.'},
            {'name': 'Parc de la Vallée de la Nsele', 'place': 'Nsele', 'desc': 'Grand parc animalier et de loisirs : safari, pique-nique et nature à 45 min du centre.'},
            {'name': 'Musée national de la RDC', 'place': 'Gombe', 'desc': "Collections d'art et d'histoire congolaises."},
            {'name': 'Jardin botanique de Kinshasa', 'place': 'Gombe', 'desc': 'Poumon vert du centre-ville.'},
            {'name': 'Marché central (Zando)', 'place': 'Gombe', 'desc': "Le plus grand marché de Kinshasa, ambiance et artisanat."},
            {'name': 'Cathédrale Notre-Dame du Congo', 'place': 'Lingwala', 'desc': 'Édifice religieux historique au cœur de la ville.'},
            {'name': 'Rapides de Kinsuka', 'place': 'Ngaliema', 'desc': 'Panorama sur les rapides du fleuve Congo.'},
            {'name': 'Chutes de la Lukaya', 'place': 'Mont-Ngafula', 'desc': 'Cascades et piscines naturelles en périphérie verdoyante.'},
        ],
    },
    {
        'slug': 'kongo-central', 'name': 'Kongo Central', 'capital': 'Matadi',
        'area': 53920, 'pop': 5575000,
        'tagline': "La façade atlantique et le berceau du royaume Kongo",
        'circuits': ['Chutes de Zongo', 'Cascades & forêt'],
        'desc': "Première façade maritime de la RDC, le Kongo Central aligne plages de Moanda et mangroves sur l'Atlantique, et cascades de Zongo sur les hauteurs de l'Inkumu. C'est aussi le berceau historique du royaume Kongo, de Mbanza-Ngungu à Matadi.",
        'sites': [
            {'name': 'Chutes de Zongo', 'place': 'Zongo', 'desc': "Cascade d'environ 65 m au cœur de la forêt."},
            {'name': 'Parc marin des Mangroves', 'place': 'Moanda', 'desc': 'Mangroves, lamantins et tortues marines.'},
            {'name': 'Plages de Moanda et Banana', 'place': 'Moanda / Banana', 'desc': 'Seule façade atlantique de la RDC.'},
            {'name': 'Jardin botanique de Kisantu', 'place': 'Kisantu', 'desc': "Un des plus beaux jardins d'Afrique centrale."},
            {'name': 'Grottes de Mbanza-Ngungu', 'place': 'Mbanza-Ngungu', 'desc': 'Grottes et collines verdoyantes.'},
            {'name': 'Pont Maréchal', 'place': 'Matadi', 'desc': 'Pont suspendu sur le fleuve Congo.'},
            {'name': 'Musée de Boma & baobab de Stanley', 'place': 'Boma', 'desc': 'Première capitale du Congo.'},
        ],
    },
    {
        'slug': 'kwango', 'name': 'Kwango', 'capital': 'Kenge',
        'area': 89974, 'pop': 2152000,
        'tagline': "La rivière large, la savane et les chutes du Tembo",
        'circuits': ['Cascades & forêt'],
        'desc': "À l'extrême ouest du pays, le Kwango suit une rivière large et lente, lifeline des villages de pêcheurs et de vastes plaines de savane. Les chutes Guillaume au Tembo marquent le paysage de cette province de plaines et de collines boisées.",
        'sites': [
            {'name': 'Chutes Guillaume (Tembo)', 'place': 'Tembo', 'desc': 'Puissantes chutes sur la rivière Kwango.'},
            {'name': 'Rivière Kwango', 'place': 'Popokabaka', 'desc': 'Paysages de savane et pêche.'},
        ],
    },
    {
        'slug': 'kwilu', 'name': 'Kwilu', 'capital': 'Bandundu',
        'area': 78219, 'pop': 5490000,
        'tagline': "Au carrefour des trois fleuves",
        'circuits': ['Cascades & forêt'],
        'desc': "Au confluent du Kwilu, du Kwango et du Kasaï, Bandundu est une ville de carrefours, porte d'entrée de laNavigation vers le fleuve Congo. La province étire ses plaines et ses forêts de savane jusqu'à Kikwit, d'où partent les bateaux.",
        'sites': [
            {'name': 'Rivière Kwilu à Kikwit', 'place': 'Kikwit', 'desc': 'Balade au bord de la rivière.'},
            {'name': 'Ville de Bandundu', 'place': 'Bandundu', 'desc': 'Confluence du Kwilu, du Kwango et du Kasaï.'},
        ],
    },
    {
        'slug': 'mai-ndombe', 'name': 'Mai-Ndombe', 'capital': 'Inongo',
        'area': 127465, 'pop': 1852000,
        'tagline': "Un monde d'eau, la plus grande réserve de bonobos",
        'circuits': ['Cascades & forêt'],
        'desc': "Littéralement « eau noire », le Mai-Ndombe est un monde d'eau : le lac du même nom, ses tourbières et ses villages flottants de pêcheurs. La province abrite l'une des plus grandes concentrations de bonobos du monde, dans des forêts encore peu fréquentées.",
        'sites': [
            {'name': 'Lac Mai-Ndombe', 'place': 'Inongo', 'desc': "Grand lac aux eaux noires."},
            {'name': "Forêts de Mai-Ndombe (REDD+)", 'place': 'Inongo', 'desc': 'Forêt et bonobos.'},
        ],
    },
    {
        'slug': 'kasai', 'name': 'Kasaï', 'capital': 'Tshikapa',
        'area': 95631, 'pop': 2801000,
        'tagline': "La rivière aux cascades, la ville du diamant",
        'circuits': ['Cascades & forêt'],
        'desc': "Le Kasaï doit son nom à la rivière qui le traverse avant de rejoindre le fleuve Congo. À Tshikapa, la ville du diamant, la rivière cascade entre les berges boisées ; plus au sud, Mweka offre un autre décor de chutes et de forêt.",
        'sites': [
            {'name': 'Chutes de la Tshikapa', 'place': 'Tshikapa', 'desc': 'Chutes sur la rivière Tshikapa.'},
            {'name': 'Chutes de Kamwanga', 'place': 'Mweka', 'desc': 'Chutes et forêt.'},
        ],
    },
    {
        'slug': 'kasai-central', 'name': 'Kasaï-Central', 'capital': 'Kananga',
        'area': 60958, 'pop': 3317000,
        'tagline': "Plaines fertiles, lacs et cascades autour de Kananga",
        'circuits': ['Cascades & forêt'],
        'desc': "Autour de Kananga, capitale du Kasaï historique, la province alterne plaines fertiles et plans d'eau. Les chutes de Katende, le lac Munkamba et le lac Fwa offrent des étapes nature pour les randonnées aquatiques et les baignades.",
        'sites': [
            {'name': 'Chutes de Katende', 'place': 'Kananga', 'desc': 'Chutes sur la rivière Lulua.'},
            {'name': 'Lac Munkamba', 'place': 'Kasaï-Central', 'desc': 'Lac paisible pour se reposer.'},
            {'name': 'Lac Fwa', 'place': 'Dibaya', 'desc': 'Lac et légendes locales.'},
        ],
    },
    {
        'slug': 'kasai-oriental', 'name': 'Kasaï-Oriental', 'capital': 'Mbuji-Mayi',
        'area': 9481, 'pop': 3145000,
        'tagline': "La région du diamant et de la canne",
        'circuits': ['Cascades & forêt'],
        'desc': "Autour de Mbuji-Mayi, la région du diamant, la province est marquée par l'exploitation minière et les plantations de canne. La rivière Sankuru la traverse vers le nord, reliant les marchés du sud aux grands fleuves.",
        'sites': [
            {'name': 'Mines de diamant (MIBA)', 'place': 'Mbuji-Mayi', 'desc': 'Histoire du diamant congolais.'},
            {'name': 'Rivière Sankuru à Lusambo', 'place': 'Mbuji-Mayi', 'desc': 'Paysages fluviaux.'},
        ],
    },
    {
        'slug': 'lomami', 'name': 'Lomami', 'capital': 'Kabinda',
        'area': 56426, 'pop': 2443000,
        'tagline': "Forêt profonde, bonobos et héritage songye",
        'circuits': ['Safari Savane Dorée'],
        'desc': "La Lomami est un vaste territoire forestier du bassin central, dont le parc national du même nom protège l'un des plus grands fronts de bonobos d'Afrique. Kabinda, ville songye et berceau de la musique chewa, en est la porte d'entrée.",
        'sites': [
            {'name': 'Parc national de la Lomami', 'place': 'Lomami', 'desc': 'Forêt, bonobos et singe lesula.'},
            {'name': 'Ville de Kabinda', 'place': 'Kabinda', 'desc': 'Patrimoine songye.'},
        ],
    },
    {
        'slug': 'sankuru', 'name': 'Sankuru', 'capital': 'Lusambo',
        'area': 104331, 'pop': 2110000,
        'tagline': "Le cœur de la forêt du bassin du Congo",
        'circuits': ['Cascades & forêt'],
        'desc': "Au cœur du bassin du Congo, le Sankuru est l'une des provinces les plus boisées, avec la partie sud du parc de la Salonga, plus grande réserve forestière d'Afrique. La rivière Sankuru et ses villages de piroguiers en sont l'épine dorsale.",
        'sites': [
            {'name': 'Parc national de la Salonga (sud)', 'place': 'Sankuru', 'desc': "Plus grand parc forestier d'Afrique, UNESCO."},
            {'name': 'Rivière Sankuru', 'place': 'Lusambo', 'desc': 'Pirogue et villages.'},
        ],
    },
    {
        'slug': 'maniema', 'name': 'Maniema', 'capital': 'Kindu',
        'area': 132520, 'pop': 2333000,
        'tagline': "Hautes terres boisées entre Kindu et le Congo",
        'circuits': ['Safari Savane Dorée'],
        'desc': "Entre le plateau de Kindu et les rives du fleuve Congo, le Maniema est un territoire de hautes terres couvert de forêt, traversé par la Lomami. Kindu, port sur le fleuve, ouvre la porte du parc national de la Lomami et de ses cerrados forestiers.",
        'sites': [
            {'name': 'Fleuve Congo à Kindu', 'place': 'Kindu', 'desc': 'Bords du fleuve et port.'},
            {'name': 'Kasongo', 'place': 'Kasongo', 'desc': 'Ancienne cité marchande.'},
        ],
    },
    {
        'slug': 'sud-kivu', 'name': 'Sud-Kivu', 'capital': 'Bukavu',
        'area': 65070, 'pop': 5772000,
        'tagline': "Lac Kivu, gorilles des plaines et forêts de montagne",
        'circuits': ['Ascension du volcan'],
        'desc': "Entre le lac Kivu et les crêtes du Rift, le Sud-Kivu mêle les presqu'îles de Bukavu, l'île d'Idjwi et les forêts d'Itombwe. Le parc de Kahuzi-Biega, aux gorilles des plaines de l'Est, en est la signature.",
        'sites': [
            {'name': 'Parc national de Kahuzi-Biega', 'place': 'Près de Bukavu', 'desc': "Gorilles des plaines de l'Est, UNESCO."},
            {'name': "Lac Kivu & presqu'îles de Bukavu", 'place': 'Bukavu', 'desc': 'Panoramas sur le lac.'},
            {'name': "Île d'Idjwi", 'place': 'Idjwi', 'desc': 'Grande île du lac Kivu.'},
            {'name': "Parc national d'Itombwe", 'place': 'Mwenga', 'desc': 'Forêts de montagne.'},
        ],
    },
    {
        'slug': 'nord-kivu', 'name': 'Nord-Kivu', 'capital': 'Goma',
        'area': 59483, 'pop': 6655000,
        'tagline': "Volcans, lave et sommets enneigés",
        'circuits': ['Parc des Virunga', 'Mont Nyiragongo', 'Ascension du volcan'],
        'desc': "Le Nord-Kivu porte les volcans et les sommets : Nyiragongo et son lac de lave, les Rwenzori enneigés, et les plaines du parc des Virunga. Autour de Goma, le lac Kivu et le lac Édouard prolongent la découverte.",
        'sites': [
            {'name': 'Parc national des Virunga', 'place': 'Rumangabo', 'desc': 'Patrimoine UNESCO, gorilles (accès selon sécurité).'},
            {'name': 'Volcan Nyiragongo', 'place': 'Goma', 'desc': 'Lac de lave (accès selon sécurité).'},
            {'name': 'Lac Kivu à Goma', 'place': 'Goma', 'desc': 'Plages et couchers de soleil.'},
            {'name': 'Monts Rwenzori', 'place': 'Mutwanga', 'desc': 'Sommets enneigés et glaciers.'},
            {'name': 'Lac Édouard', 'place': 'Vitshumbi', 'desc': 'Hippopotames et pêcheurs.'},
        ],
    },
    {
        'slug': 'ituri', 'name': 'Ituri', 'capital': 'Bunia',
        'area': 65658, 'pop': 3650000,
        'tagline': "Okapis, forêts des Grands Lacs et lac Albert",
        'circuits': ['Safari Savane Dorée'],
        'desc': "À l'est, l'Ituri garde l'une des plus grandes forêts de la région des Grands Lacs et la réserve à okapis d'Epulu, sanctuaire d'une espèce presque introuvable ailleurs. Le lac Albert et ses villages de pêcheurs ferment le tableau.",
        'sites': [
            {'name': 'Réserve de faune à okapis', 'place': 'Epulu', 'desc': 'Okapis, UNESCO.'},
            {'name': 'Lac Albert', 'place': 'Kasenyi', 'desc': 'Lac et villages de pêcheurs.'},
        ],
    },
    {
        'slug': 'haut-uele', 'name': 'Haut-Uele', 'capital': 'Isiro',
        'area': 89683, 'pop': 1864000,
        'tagline': "La Garamba et les derniers grands troupeaux d'éléphants",
        'circuits': ['Safari Savane Dorée'],
        'desc': "Le Haut-Uele va de la Station de domestication des éléphants de Gangala-na-Bodio au parc de la Garamba, l'un des plus grands sanctuaires d'éléphants d'Afrique. Un territoire de savane arborée où la grande faune circule encore librement.",
        'sites': [
            {'name': 'Parc national de la Garamba', 'place': 'Nagero', 'desc': 'Éléphants, girafes du Kordofan, UNESCO.'},
            {'name': "Station de domestication des éléphants", 'place': 'Gangala-na-Bodio', 'desc': 'Site historique.'},
        ],
    },
    {
        'slug': 'bas-uele', 'name': 'Bas-Uele', 'capital': 'Buta',
        'area': 148331, 'pop': 1138000,
        'tagline': "Savanes du nord et chimpanzés de Bili",
        'circuits': ['Safari Savane Dorée'],
        'desc': "Le Bas-Uele s'étend sur les savanes du nord, jusqu'au domaine de chasse de Bili-Uere et de ses chimpanzés. Buta, sur la Rubi, est le chef-lieu de ce territoire de prairies, de rivers et de pistes.",
        'sites': [
            {'name': 'Domaine de chasse de Bili-Uere', 'place': 'Bili', 'desc': 'Savanes et chimpanzés de Bili.'},
            {'name': 'Ville de Buta', 'place': 'Buta', 'desc': 'Rivière Rubi.'},
        ],
    },
    {
        'slug': 'tshopo', 'name': 'Tshopo', 'capital': 'Kisangani',
        'area': 199567, 'pop': 2352000,
        'tagline': "La plus vaste province, au cœur de la forêt équatoriale",
        'circuits': ['Safari Savane Dorée'],
        'desc': "Avec 199 567 km², le Tshopo est la plus vaste province du pays. Kisangani, à la confluence du Congo et du Tshopo, s'ouvre sur les chutes Wagenia, la réserve de Yangambi et les cataractes de la ville.",
        'sites': [
            {'name': 'Chutes Wagenia (Boyoma)', 'place': 'Kisangani', 'desc': 'Pêcheurs Wagenia et leurs nasses.'},
            {'name': 'Réserve de biosphère de Yangambi', 'place': 'Yangambi', 'desc': 'Forêt tropicale.'},
            {'name': 'Chutes de la Tshopo', 'place': 'Kisangani', 'desc': 'Chutes en pleine ville.'},
        ],
    },
    {
        'slug': 'mongala', 'name': 'Mongala', 'capital': 'Lisala',
        'area': 58141, 'pop': 1740000,
        'tagline': "Navigation sur le Congo et plaines inondées",
        'circuits': ['Cascades & forêt'],
        'desc': "Le Mongala s'étire le long du Congo, entre Lisala et le port de Bumba. Ses plaines inondées et ses forêts-galeries en font un territoire de navigation et de pêche, où le fleuve reste la voie la plus sûre.",
        'sites': [
            {'name': 'Fleuve Congo à Lisala', 'place': 'Lisala', 'desc': 'Bords du fleuve.'},
            {'name': 'Bumba', 'place': 'Bumba', 'desc': 'Port fluvial animé.'},
        ],
    },
    {
        'slug': 'nord-ubangi', 'name': 'Nord-Ubangi', 'capital': 'Gbadolite',
        'area': 56644, 'pop': 1269000,
        'tagline': "L'Ubangi et la résidence de Gbadolite",
        'circuits': ['Cascades & forêt'],
        'desc': "Au nord-ouest du pays, le Nord-Ubangi aligne les paysages de l'Ubangi et le palais de Gbadolite, résidence de Moïse Kotze et de la famille royale, inscrite au patrimoine mondial. Uncoin d'Histoire et de fleuve.",
        'sites': [
            {'name': 'Palais de Gbadolite & Kawele', 'place': 'Gbadolite', 'desc': 'Vestiges historiques.'},
            {'name': 'Rivière Ubangi', 'place': 'Mobayi-Mbongo', 'desc': "Pirogue sur l'Ubangi."},
        ],
    },
    {
        'slug': 'sud-ubangi', 'name': 'Sud-Ubangi', 'capital': 'Gemena',
        'area': 51648, 'pop': 2458000,
        'tagline': "Les grands espaces de l'Ubangi et les marchés ngbaka",
        'circuits': ['Cascades & forêt'],
        'desc': "Le Sud-Ubangi est la province des grands espaces : la rivière Ubangi vers Mobayi et Libenge, et les marchés de Gemena. Les paysages fluviaux dominent, avec de larges plaines cultivées et de vastes zones humides.",
        'sites': [
            {'name': 'Rivière Ubangi à Libenge', 'place': 'Libenge', 'desc': 'Paysages fluviaux.'},
            {'name': 'Gemena', 'place': 'Gemena', 'desc': 'Marchés et culture ngbaka.'},
        ],
    },
    {
        'slug': 'equateur', 'name': 'Équateur', 'capital': 'Mbandaka',
        'area': 103902, 'pop': 1528000,
        'tagline': "Le fleuve, le lac Tumba et la ligne de l'Équateur",
        'circuits': ['Cascades & forêt'],
        'desc': "À l'équateur, la province aligne le fleuve Congo et le lac Tumba. Le jardin botanique d'Eala et le monument de la ligne de l'Équateur rappellent que Mbandaka est l'une des portes de la forêt équatoriale.",
        'sites': [
            {'name': "Jardin botanique d'Eala", 'place': 'Mbandaka', 'desc': 'Jardin historique au bord du fleuve.'},
            {'name': "Ligne de l'Équateur", 'place': 'Mbandaka', 'desc': 'Monument de passage de l’Équateur.'},
            {'name': 'Lac Tumba', 'place': 'Bikoro', 'desc': 'Bonobos et pêcheurs.'},
        ],
    },
    {
        'slug': 'tshuapa', 'name': 'Tshuapa', 'capital': 'Boende',
        'area': 132957, 'pop': 1600000,
        'tagline': "Le cœur de la grande forêt du bassin du Congo",
        'circuits': ['Cascades & forêt'],
        'desc': "Le Tshuapa est le cœur de la grande forêt du bassin du Congo, avec la partie nord du parc de la Salonga. Boende, sur la rivière du même nom, est une porte d'entrée par la pirogue vers des villages de forêt.",
        'sites': [
            {'name': 'Parc national de la Salonga (nord)', 'place': 'Monkoto', 'desc': 'Bonobos et forêt primaire.'},
            {'name': 'Rivière Tshuapa', 'place': 'Boende', 'desc': 'Pirogue en forêt.'},
        ],
    },
    {
        'slug': 'tanganyika', 'name': 'Tanganyika', 'capital': 'Kalemie',
        'area': 134940, 'pop': 3062000,
        'tagline': "Le deuxième lac le plus profond du monde",
        'circuits': ['Safari Savane Dorée'],
        'desc': "Le lac Tanganyika, deuxième lac le plus profond du monde, borde la province côté zambian. À Kalemie, la rivière Lukuga — seul exutoire du lac — et les berges organisent la vie locale, la pêche et les départs en bateau.",
        'sites': [
            {'name': 'Lac Tanganyika', 'place': 'Kalemie', 'desc': 'Deuxième lac le plus profond du monde.'},
            {'name': 'Rivière Lukuga', 'place': 'Kalemie', 'desc': 'Seul exutoire du lac.'},
        ],
    },
    {
        'slug': 'haut-lomami', 'name': 'Haut-Lomami', 'capital': 'Kamina',
        'area': 108204, 'pop': 2957000,
        'tagline': "Le lac Upemba et la grande plaine de Lusaka",
        'circuits': ['Safari Savane Dorée'],
        'desc': "Le Haut-Lomami s'organise autour du lac Upemba et des plaines de Lusaka. Le parc national de l'Upemba protège zèbres, hippopotames et oiseaux autour d'une immense zone humide, l'un des plus beaux spectacles animaliers du sud du pays.",
        'sites': [
            {'name': "Parc national de l'Upemba", 'place': 'Lusinga', 'desc': 'Lacs, zèbres et plateaux.'},
            {'name': 'Lac Upemba', 'place': 'Bukama', 'desc': "Zone humide et oiseaux."},
        ],
    },
    {
        'slug': 'lualaba', 'name': 'Lualaba', 'capital': 'Kolwezi',
        'area': 121308, 'pop': 2570000,
        'tagline': "Savane, lac de barrage et chutes du fleuve Lualaba",
        'circuits': ['Ascension du volcan'],
        'desc': "Le Lualaba, autour de Kolwezi, associe la savane et les cours d'eau. Le lac de barrage Nzilo et les chutes du fleuve Lualaba offrent des balades au bord de l'eau, à portée immédiate de la ville.",
        'sites': [
            {'name': 'Lac Nzilo (Delcommune)', 'place': 'Kolwezi', 'desc': 'Lac de barrage entouré de collines.'},
            {'name': 'Chutes de Nzilo', 'place': 'Kolwezi', 'desc': 'Chutes du fleuve Lualaba.'},
        ],
    },
    {
        'slug': 'haut-katanga', 'name': 'Haut-Katanga', 'capital': 'Lubumbashi',
        'area': 132425, 'pop': 4617000,
        'tagline': "Les chutes de la Lofoi et le cœur minier du sud",
        'circuits': ['Safari Savane Dorée'],
        'desc': "Au sud de la RDC, le Haut-Katanga va des chutes de la Lofoi, parmi les plus hautes d'Afrique, aux lacs de Copperbelt, avec Lubumbashi comme capitale. Le musée national et les lacs de Kipopo et Moero complètent le séjour.",
        'sites': [
            {'name': 'Chutes de la Lofoi (Kundelungu)', 'place': 'Kundelungu', 'desc': "Parmi les plus hautes chutes d'Afrique (~340 m)."},
            {'name': 'Musée national de Lubumbashi', 'place': 'Lubumbashi', 'desc': 'Art et histoire du Katanga.'},
            {'name': 'Lac Kipopo', 'place': 'Lubumbashi', 'desc': 'Détente aux portes de la ville.'},
            {'name': 'Lac Moero', 'place': 'Pweto', 'desc': 'Grand lac à la frontière zambienne.'},
        ],
    },
]

# Verite terrain : provinces partageant une frontiere (calculee depuis le GeoJSON).
# Sert a proposer des provinces voisines sur la page de chaque province.
NEIGHBOURS = {}

# Banc d'images partage avec le reste du site (Unsplash) - visuels de substitution.
IMAGES = [
    'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=600&q=80',
    'https://images.unsplash.com/photo-1604537466608-109fa2f16c3b?w=600&q=80',
    'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=600&q=80',
    'https://images.unsplash.com/photo-1516526495688-8c4d10a4ac3e?w=600&q=80',
    'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600&q=80',
    'https://images.unsplash.com/photo-1564507592333-c60657eea523?w=600&q=80',
    'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=80',
    'https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=600&q=80',
    'https://images.unsplash.com/photo-1551632811-561732d1e306?w=600&q=80',
    'https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=600&q=80',
    'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=600&q=80',
    'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=600&q=80',
    'https://images.unsplash.com/photo-1448375240586-882707db888b?w=600&q=80',
    'https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=600&q=80',
    'https://images.unsplash.com/photo-1501854140801-50d01698950b?w=600&q=80',
    'https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=600&q=80',
]
