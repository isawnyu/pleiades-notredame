var $ = jQuery;
const boxpad = 50;
const max_zoom = 17;
const initial_zoom = 15;

/* Configure and initialize map and standard controls */
mapboxgl.accessToken = 'pk.eyJ1IjoiaXNhd255dSIsImEiOiJja2FlaWk4MG0yaHY0MnNvemRneWF0d2RnIn0.FgwFQtymPTHYPYYha5mfHw';

var max_bounds = new mapboxgl.LngLatBounds([
    [-45, -20],
    [160, 80]
]);
var bounds = new mapboxgl.LngLatBounds([
    [-20, 0],
    [85, 30]
])
var mapOptionsInit = {
    attributionControl: false,
    container: 'map',
    style: 'mapbox://styles/isawnyu/ckl55kmn63m7q17rmd7d47z2l',
    maxBounds: max_bounds,
    bounds: bounds,
    renderWorldCopies: false,
    maxZoom: max_zoom,
};
var map = new mapboxgl.Map(mapOptionsInit)
map.addControl(new mapboxgl.AttributionControl({
    compact: true,
    customAttribution: [
        'Functionality and interaction design for Pleiades by Sean Gillies, David Glick, Alec Mitchell, Ryan M. Horne, and Tom Elliott. © New York University',
        'Base style "2021 Pleiades Modern" was derived by Tom Elliott from Mapbox "Outdoors".',
    ]
}));
map.addControl(new mapboxgl.NavigationControl({
    showCompass: false,
}), 'top-left');
map.addControl(new mapboxgl.ScaleControl());
map.scrollZoom.disable();

/* Define and initialize custom controls */
/* Original class implementation by Kristjan Tallinn via https://codepen.io/kriz/pen/jdxYXY */

class MapboxGLButtonControl {
    constructor({
        className = "",
        title = "",
        eventHandler = mapboxgl.eventHandler,
        container = undefined
    }) {
        this._className = className;
        this._title = title;
        this._eventHandler = eventHandler;
        this._container = container;
    }
    onAdd(map) {
        this._btn = document.createElement("button");
        this._btn.className = "mapboxgl-ctrl-icon" + " " + this._className;
        this._btn.type = "button";
        this._btn.title = this._title;
        this._btn.onclick = this._eventHandler;

        this._wrapper = document.createElement("span");
        this._wrapper.className = "mapboxgl-ctrl-icon";
        this._wrapper.setAttribute('aria-hidden', true);
        this._wrapper.appendChild(this._btn);

        if (this._container === undefined) {
            this._container = document.createElement("div");
            this._container.className = "mapboxgl-ctrl-group mapboxgl-ctrl";
        } else {
            this._container = document.getElementById(this._containerID);
        }
        this._container.appendChild(this._wrapper);

        return this._container;
    }
    onRemove() {
        this._container.parentNode.removeChild(this._container);
        this._map = undefined;
    }
}
// Controls to reset zoom & pan

function hdlResetBox() {
    map.fitBounds(bounds, { 'padding': boxpad });
}
map = map.addControl(new MapboxGLButtonControl({
    className: "mapbox-gl-reset-box",
    title: "Reset Map View",
    eventHandler: hdlResetBox
}), 'top-left');

/* Define styles and layouts for the layers we will use */

/* populate the map */
if (map.loaded()) {
    populateMap(map);
} else {
    map.on('load', () => populateMap(map));
}
map.on('click', function(e) {
    var features = map.queryRenderedFeatures(e.point, {
        layers: ['layer-recent']
    });
    if (features.length > 0) {
        var feature = features[0];
        var snippet;
        if (feature.properties.link !== undefined) {
            snippet = '<dd><a href="' + feature.properties.link + '">' + feature.properties.title + '</a></dd>'
        } else {
            snippet = '<dd>' + feature.properties.title + '</dd>'
        }
        if (feature.properties.description !== undefined) {
            var desc;
            var words = feature.properties.description.split(' ');
            if (words.length > 25) {
                desc = words.slice(0, 26).join(' ') + '...'
            } else {
                desc = feature.properties.description;
            }
            snippet += '<dt>' + desc + '</dt>'
        }
        new mapboxgl.Popup()
            .setLngLat(e.lngLat)
            .setHTML(snippet)
            .addTo(map);
    }
});

function populateMap(map) {
    var where = getJSON("where");
    var features = Array();
    for (i = 0; i < where.features.length; i++) {
        var f = where.features[i];
        var feature = {
            'type': 'Feature',
            'geometry': f.geometry,
            'properties': {
                'title': f.properties.title,
                'description': f.properties.description,
                'link': f.properties.link
            }
        }
        features.push(feature);
    }
    map.addSource('recent', {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': features
        }
    });
    map.addLayer({
        'id': 'layer-recent',
        'source': 'recent',
        'type': 'symbol',
        'layout': {
            'icon-image': 'circle-orange-15',
            'icon-allow-overlap': true
        }
    });
    map.on('mouseenter', 'layer-recent', function() {
        map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', 'layer-recent', function() {
        map.getCanvas().style.cursor = '';
    });
    var sw = new mapboxgl.LngLat(where.bbox[0], where.bbox[1]);
    var ne = new mapboxgl.LngLat(where.bbox[2], where.bbox[3]);
    var bounds = new mapboxgl.LngLatBounds(sw, ne);
    map.fitBounds(bounds, { 'padding': boxpad, 'maxZoom': initial_zoom });
}

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
        j = JSON.parse(json);
        return j;
    } else {
        return null;
    }
}