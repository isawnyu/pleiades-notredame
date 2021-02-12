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
    attributionControl: true,
    customAttribution: [
        'Map interaction design by Sean Gillies, David Glick, Alec Mitchell, Ryan M. Horne, and Tom Elliott.',
        'Base style derived from Mapbox Outdoors by Tom Elliott.'
    ],
    container: 'map',
    style: 'mapbox://styles/isawnyu/ckglabv7q0ald19mnlbluh4sn',
    maxBounds: max_bounds,
    bounds: bounds,
    renderWorldCopies: false,
    maxZoom: max_zoom,
};
var map = new mapboxgl.Map(mapOptionsInit);
map = map.addControl(new mapboxgl.NavigationControl({
    showCompass: false,
}), 'top-left');
map = map.addControl(new mapboxgl.ScaleControl());
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
    var sw = new mapboxgl.LngLat(where.bbox[0], where.bbox[1]);
    var ne = new mapboxgl.LngLat(where.bbox[2], where.bbox[3]);
    var bounds = new mapboxgl.LngLatBounds(sw, ne);
    console.debug(bounds);
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
        console.debug(j)
        return j;
    } else {
        return null;
    }
}