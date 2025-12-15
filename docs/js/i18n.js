// py-osrm-backend Documentation - Internationalization System

const translations = {
    en: {
        // Navigation
        "nav.features": "Features",
        "nav.installation": "Installation",
        "nav.quickstart": "Quick Start",
        "nav.architecture": "Architecture",
        "nav.api": "API",
        
        // Hero
        "hero.badge": "🗺️ Open Source Routing",
        "hero.subtitle": "A Python implementation of OSRM backend core functionality. Build routing applications with OpenStreetMap data.",
        "hero.version": "Latest Release",
        "hero.getstarted": "🚀 Get Started",
        
        // Features
        "features.badge": "Capabilities",
        "features.title": "Features",
        "features.subtitle": "Everything you need to build routing applications in Python",
        "features.osm.title": "OSM Parsing",
        "features.osm.desc": "Parse OpenStreetMap data in both XML (.osm) and PBF formats to extract nodes and ways for routing.",
        "features.graph.title": "Graph Building",
        "features.graph.desc": "Build a routable graph with haversine distance weights automatically calculated from coordinates.",
        "features.dijkstra.title": "Dijkstra Routing",
        "features.dijkstra.desc": "Find shortest paths using Dijkstra's algorithm with efficient priority queue implementation.",
        "features.ch.title": "Contraction Hierarchies",
        "features.ch.desc": "Speed up queries with Contraction Hierarchies preprocessing for faster route computation.",
        "features.api.title": "REST API",
        "features.api.desc": "Flask-based REST API compatible with OSRM-like endpoints for easy integration.",
        "features.python.title": "Pure Python",
        "features.python.desc": "No complex dependencies, easy to install and extend. Works with Python 3.8+.",
        
        // Installation
        "install.badge": "Setup",
        "install.title": "Installation",
        "install.subtitle": "Get started in seconds with pip",
        "install.pypi": "Install from PyPI:",
        "install.deps.title": "📦 Dependencies",
        "install.deps.desc": "py-osrm-backend requires only two dependencies:",
        "install.deps.flask": "- For the REST API server",
        "install.deps.osmium": "- For parsing PBF files",
        "install.dev.title": "🔧 Development",
        "install.dev.desc": "For development, install with extras:",
        
        // Quick Start
        "quickstart.badge": "Tutorial",
        "quickstart.title": "Quick Start",
        "quickstart.subtitle": "Build your first routing application in minutes",
        "quickstart.step1.title": "1️⃣ Load OSM Data",
        "quickstart.step1.desc": "Use <code>GraphBuilder</code> to parse OSM files and build a routable graph. Supports both .osm (XML) and .pbf formats.",
        "quickstart.step2.title": "2️⃣ Create Engine",
        "quickstart.step2.desc": "Initialize <code>DijkstraEngine</code> with your graph. For faster queries on large graphs, use <code>CHEngine</code> instead.",
        "quickstart.step3.title": "3️⃣ Compute Routes",
        "quickstart.step3.desc": "Call <code>shortest_path()</code> with start and end node IDs. Returns the total distance in kilometers and the path as a list of node IDs.",
        
        // Architecture
        "arch.badge": "Overview",
        "arch.title": "Architecture",
        "arch.subtitle": "Modular design for flexibility and extensibility",
        "arch.osm.title": "OSM Data",
        "arch.osm.desc": ".osm / .pbf files<br>OpenStreetMap",
        "arch.extractor.title": "Extractor",
        "arch.extractor.desc": "Parse & Build<br>Graph Structure",
        "arch.graph.title": "Graph",
        "arch.graph.desc": "Nodes & Edges<br>Weighted Network",
        "arch.engine.title": "Engine",
        "arch.engine.desc": "Dijkstra / CH<br>Route Computation",
        "arch.server.title": "API Server",
        "arch.server.desc": "Flask REST<br>HTTP Endpoints",
        "arch.structures": "Core data structures including <code>Graph</code>, <code>Node</code>, and <code>Edge</code> classes.",
        "arch.extractor.card": "OSM parsing and graph building utilities. Handles XML and PBF formats.",
        "arch.engine.card": "Routing algorithms: Dijkstra and Contraction Hierarchies implementations.",
        
        // API
        "api.badge": "REST API",
        "api.title": "HTTP Endpoints",
        "api.subtitle": "OSRM-compatible REST API for web applications",
        "api.route.title": "📍 Route Endpoint",
        "api.route.desc": "Get a route between coordinates:",
        "api.route.returns": "Returns distance, duration, and geometry in GeoJSON format.",
        
        // Footer
        "footer.text": "py-osrm-backend — Open Source Routing Engine by GalTechDev"
    },
    fr: {
        // Navigation
        "nav.features": "Fonctionnalités",
        "nav.installation": "Installation",
        "nav.quickstart": "Démarrage Rapide",
        "nav.architecture": "Architecture",
        "nav.api": "API",
        
        // Hero
        "hero.badge": "🗺️ Routage Open Source",
        "hero.subtitle": "Une implémentation Python des fonctionnalités principales d'OSRM. Créez des applications de routage avec les données OpenStreetMap.",
        "hero.version": "Dernière Version",
        "hero.getstarted": "🚀 Commencer",
        
        // Features
        "features.badge": "Capacités",
        "features.title": "Fonctionnalités",
        "features.subtitle": "Tout ce dont vous avez besoin pour créer des applications de routage en Python",
        "features.osm.title": "Parsing OSM",
        "features.osm.desc": "Analysez les données OpenStreetMap aux formats XML (.osm) et PBF pour extraire les nœuds et les chemins.",
        "features.graph.title": "Construction de Graphe",
        "features.graph.desc": "Construisez un graphe routable avec des poids de distance haversine calculés automatiquement.",
        "features.dijkstra.title": "Routage Dijkstra",
        "features.dijkstra.desc": "Trouvez les plus courts chemins avec l'algorithme de Dijkstra et une file de priorité efficace.",
        "features.ch.title": "Contraction Hierarchies",
        "features.ch.desc": "Accélérez les requêtes avec le prétraitement Contraction Hierarchies pour un calcul plus rapide.",
        "features.api.title": "API REST",
        "features.api.desc": "API REST Flask compatible avec les endpoints OSRM pour une intégration facile.",
        "features.python.title": "Python Pur",
        "features.python.desc": "Pas de dépendances complexes, facile à installer et étendre. Fonctionne avec Python 3.8+.",
        
        // Installation
        "install.badge": "Installation",
        "install.title": "Installation",
        "install.subtitle": "Démarrez en quelques secondes avec pip",
        "install.pypi": "Installer depuis PyPI :",
        "install.deps.title": "📦 Dépendances",
        "install.deps.desc": "py-osrm-backend ne nécessite que deux dépendances :",
        "install.deps.flask": "- Pour le serveur API REST",
        "install.deps.osmium": "- Pour le parsing des fichiers PBF",
        "install.dev.title": "🔧 Développement",
        "install.dev.desc": "Pour le développement, installez avec les extras :",
        
        // Quick Start
        "quickstart.badge": "Tutoriel",
        "quickstart.title": "Démarrage Rapide",
        "quickstart.subtitle": "Créez votre première application de routage en quelques minutes",
        "quickstart.step1.title": "1️⃣ Charger les Données OSM",
        "quickstart.step1.desc": "Utilisez <code>GraphBuilder</code> pour parser les fichiers OSM et construire un graphe routable. Supporte les formats .osm (XML) et .pbf.",
        "quickstart.step2.title": "2️⃣ Créer le Moteur",
        "quickstart.step2.desc": "Initialisez <code>DijkstraEngine</code> avec votre graphe. Pour des requêtes plus rapides sur de grands graphes, utilisez <code>CHEngine</code>.",
        "quickstart.step3.title": "3️⃣ Calculer les Itinéraires",
        "quickstart.step3.desc": "Appelez <code>shortest_path()</code> avec les IDs des nœuds de départ et d'arrivée. Retourne la distance totale en kilomètres et le chemin.",
        
        // Architecture
        "arch.badge": "Vue d'ensemble",
        "arch.title": "Architecture",
        "arch.subtitle": "Conception modulaire pour flexibilité et extensibilité",
        "arch.osm.title": "Données OSM",
        "arch.osm.desc": "Fichiers .osm / .pbf<br>OpenStreetMap",
        "arch.extractor.title": "Extracteur",
        "arch.extractor.desc": "Parse & Construit<br>Structure de Graphe",
        "arch.graph.title": "Graphe",
        "arch.graph.desc": "Nœuds & Arêtes<br>Réseau Pondéré",
        "arch.engine.title": "Moteur",
        "arch.engine.desc": "Dijkstra / CH<br>Calcul d'Itinéraire",
        "arch.server.title": "Serveur API",
        "arch.server.desc": "Flask REST<br>Endpoints HTTP",
        "arch.structures": "Structures de données incluant les classes <code>Graph</code>, <code>Node</code> et <code>Edge</code>.",
        "arch.extractor.card": "Utilitaires de parsing OSM et construction de graphe. Gère les formats XML et PBF.",
        "arch.engine.card": "Algorithmes de routage : implémentations Dijkstra et Contraction Hierarchies.",
        
        // API
        "api.badge": "API REST",
        "api.title": "Endpoints HTTP",
        "api.subtitle": "API REST compatible OSRM pour applications web",
        "api.route.title": "📍 Endpoint Route",
        "api.route.desc": "Obtenir un itinéraire entre coordonnées :",
        "api.route.returns": "Retourne la distance, la durée et la géométrie au format GeoJSON.",
        
        // Footer
        "footer.text": "py-osrm-backend — Moteur de Routage Open Source par GalTechDev"
    }
};

// Current language
let currentLang = localStorage.getItem('lang') || 'en';

// Apply translations
function applyTranslations(lang) {
    currentLang = lang;
    localStorage.setItem('lang', lang);
    document.documentElement.lang = lang;
    
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            el.innerHTML = translations[lang][key];
        }
    });
    
    // Update language switcher active state
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', () => {
    // Detect browser language
    const browserLang = navigator.language.substring(0, 2);
    const savedLang = localStorage.getItem('lang');
    const initialLang = savedLang || (translations[browserLang] ? browserLang : 'en');
    
    applyTranslations(initialLang);
});

// Language switch function (called from HTML)
function switchLanguage(lang) {
    if (translations[lang]) {
        applyTranslations(lang);
    }
}
