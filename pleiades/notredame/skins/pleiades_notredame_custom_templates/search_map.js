var L, PLZoom;
var $ = jQuery;
var target = null;

PLZoom = L.Control.Zoom.extend({
    onAdd: function(map) {
        var className = 'leaflet-control-zoom',
            container = L.DomUtil.create('div', className);
        this._map = map;
        this._createButton('Zoom reset',
            className + '-reset',
            container,
            this._zoomReset,
            this);
        this._createButton('Zoom in',
            className + '-in',
            container,
            this._zoomIn,
            this);
        this._createButton('Zoom out',
            className + '-out',
            container,
            this._zoomOut,
            this);
        return container;
    },

    _zoomReset: function(e) {
        this._map.fitBounds(this.options.initialBounds);
    },

    _zoomIn: function(e) {
        this._map.zoomIn(e.shiftKey ? 3 : 1);
    },

    _zoomOut: function(e) {
        this._map.zoomOut(e.shiftKey ? 3 : 1);
    },

    _createButton: function(title, className, container, fn, context) {
        var link = L.DomUtil.create('a', className, container);
        link.href = '#';
        link.title = title;
        L.DomEvent
            .on(link, 'click', L.DomEvent.stopPropagation)
            .on(link, 'mousedown', L.DomEvent.stopPropagation)
            .on(link, 'dblclick', L.DomEvent.stopPropagation)
            .on(link, 'click', L.DomEvent.preventDefault)
            .on(link, 'click', fn, context);
        return link;
    }
});

pl_zoom = function(options) {
    return new PLZoom(options);
};

function getJSON(rel) {
    var documentNode = document;
    var linkNode = documentNode.evaluate(
        '//a[@rel="' + rel + '" and @type="application/json"]',
        documentNode,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null).singleNodeValue;
    if (linkNode != null) {
        var uri = linkNode.getAttribute("href");
        var json = unescape(uri.split(',').pop());
        return JSON.parse(json);
    } else {
        return null;
    }
}

$(function() {
    var where = getJSON("where");

    var bounds = null;
    var baselineBounds = null;

    var map = L.map('map', { attributionControl: false });
    L.control.attribution({ prefix: false, position: 'bottomright' }).addTo(map);

    var outdoors2020 = L.tileLayer(
        'https://api.mapbox.com/styles/v1/isawnyu/ckglabv7q0ald19mnlbluh4sn/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaXNhd255dSIsImEiOiJja2FlaWk4MG0yaHY0MnNvemRneWF0d2RnIn0.FgwFQtymPTHYPYYha5mfHw', {
            attribution: 'Powered by <a href="http://leafletjs.com/">Leaflet</a> and <a href="https://www.mapbox.com/">Mapbox</a>. Map base from MapBox "Streets v8" and "Terrain v2" datasets using a modified "Outdoors" style in MapBox Studio.',
        });
    outdoors2020.addTo(map);

    /* Not added by default, only through user control action */
    var satellite2020 = L.tileLayer(
        'https://api.mapbox.com/styles/v1/isawnyu/ckg9eqejk2j4a19oexu5ywrqu/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaXNhd255dSIsImEiOiJja2FlaWk4MG0yaHY0MnNvemRneWF0d2RnIn0.FgwFQtymPTHYPYYha5mfHw', {
            attribution: 'Powered by <a href="http://leafletjs.com/">Leaflet</a> and <a href="https://www.mapbox.com/">Mapbox</a>. Map base from MapBox "Streets v8" and "Satellite" datasets using a modified "Satellite Streets" style in MapBox Studio.',
        });

    var imperium = L.tileLayer(
        'http://dh.gu.se/tiles/imperium/{z}/{x}/{y}.png', {
            attribution: 'Powered by <a href="http://leafletjs.com/">Leaflet</a> and <a href="https://www.mapbox.com/">DARE</a>. Map base by Johan Åhlfeldt for the <a href="https://dh.gu.se/dare/">Digital Atlas of the Roman Empire</a>.',
            maxZoom: 11
        });

    var baseLayers = {
        "Modern Landscape (default)": outdoors2020,
        "Satellite": satellite2020,
        "DARE Roman Empire": imperium,
    };

    var overlays = null;
    L.control.layers(baseLayers, overlays).addTo(map);

    function rebound() {
        /* If there's no spatial context at all, set large bounds. */
        if (!bounds) {
            bounds = L.latLngBounds([
                [20.0, -5.0],
                [50.0, 45.0]
            ]);
        }
        /* map.setView(bounds.getCenter(), Math.min(map.getBoundsZoom(bounds), 101), true); */
        map.fitBounds(bounds, { maxZoom: 10 });
        pl_zoom({ initialBounds: bounds }).addTo(map);
    }

    function setupFeature(f) {
        var layer = L.GeoJSON.geometryToLayer(f);
        layer.bindPopup(
            '<dt><a href="' + f.properties.link + '">' + f.properties.title + '</a></dt>' +
            '<dd>' + f.properties.description + '</dd>');
        layer.addTo(map);
        jQuery("dt#" + f.id + " a").mouseover(
            function() { layer.openPopup(); });
        jQuery("dt#" + f.id + " a").mouseout(
            function() { layer.closePopup(); });
    }

    for (i = 0; i < where.features.length; i++) {
        var f = where.features[i];
        setupFeature(f);
    }
    rebound();
});