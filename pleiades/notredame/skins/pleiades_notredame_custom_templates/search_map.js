PLZoom = L.Control.Zoom.extend({
    onAdd: function (map) {
        var className = 'leaflet-control-zoom',
            container = L.DomUtil.create('div', className);
        this._map = map;
        this._createButton('Zoom reset', 
            className + '-reset', 
            container, 
            this._zoomReset, 
            this );
        this._createButton('Zoom in', 
            className + '-in', 
            container, 
            this._zoomIn, 
            this );
        this._createButton('Zoom out', 
            className + '-out', 
            container, 
            this._zoomOut, 
            this );
        return container;
    },

    _zoomReset: function (e) {
        this._map.fitBounds(this.options.initialBounds); 
    },

    _zoomIn: function (e) {
        this._map.zoomIn(e.shiftKey ? 3 : 1);
    },

    _zoomOut: function (e) {
        this._map.zoomOut(e.shiftKey ? 3 : 1);
    },

    _createButton: function (title, className, container, fn, context) {
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

pl_zoom = function (options) {
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
    return jq.parseJSON(json);
  }
  else {
    return null;
  }
}

var where = getJSON("where");
var bounds = [
  [where.bbox[1]-0.125, where.bbox[0]-0.125],
  [where.bbox[3]+0.125, where.bbox[2]+0.125] ];

var map = L.map('map', {maxZoom: 12, zoomControl: false, attributionControl: false}).fitBounds(bounds);
L.control.attribution({prefix: false}).addTo(map);
pl_zoom({initialBounds: bounds}).addTo(map);

var awmcterrain = L.tileLayer(
    'http://api.tiles.mapbox.com/v3/isawnyu.map-knmctlkh/{z}/{x}/{y}.png', {
        attribution: 'Powered by <a href="http://leaflet.cloudmade.com/">Leaflet</a> and <a href="https://www.mapbox.com/">Mapbox</a>. Map base by <a title="Ancient World Mapping Center (UNC-CH)" href="http://awmc.unc.edu">AWMC</a>, 2014 (cc-by-nc).'
        });
awmcterrain.addTo(map);

/* Not added by default, only through user control action */
var terrain = L.tileLayer(
    'http://api.tiles.mapbox.com/v3/isawnyu.map-p75u7mnj/{z}/{x}/{y}.png', {
        attribution: 'Powered by <a href="http://leaflet.cloudmade.com/">Leaflet</a> and <a href="https://www.mapbox.com/">Mapbox</a>. Map base by <a title="Institute for the Study of the Ancient World (ISAW)" href="http://isaw.nyu.edu">ISAW</a>, 2014 (cc-by).'
        });

var streets = L.tileLayer(
    'http://api.tiles.mapbox.com/v3/isawnyu.map-zr78g89o/{z}/{x}/{y}.png', {
        attribution: 'Powered by <a href="http://leaflet.cloudmade.com/">Leaflet</a> and <a href="https://www.mapbox.com/">Mapbox</a>. Map base by <a title="Institute for the Study of the Ancient World (ISAW)" href="http://isaw.nyu.edu">ISAW</a>, 2014 (cc-by).'
        });

var imperium = L.tileLayer(
    'http://pelagios.dme.ait.ac.at/tilesets/imperium//{z}/{x}/{y}.png', {
        attribution: 'Powered by <a href="http://leaflet.cloudmade.com/">Leaflet</a> and <a href="https://www.mapbox.com/">Mapbox</a>. Map base: <a href="http://pelagios.dme.ait.ac.at/maps/greco-roman/about.html">Pelagios</a>, 2012; Data: NASA, OSM, Pleiades, DARMC (cc-by).',
        maxZoom: 11
        });

L.control.layers({
    "Ancient Terrain (default)": awmcterrain,
    "Modern Terrain": terrain,
    "Modern Streets": streets,
    "Roman Empire": imperium,
    }).addTo(map);


function setupFeature(f) {
  var layer = L.GeoJSON.geometryToLayer(f);
  layer.bindPopup(
    '<dt><a href="' + f.properties.link + '">' + f.properties.title + '</a></dt>'
    + '<dd>' + f.properties.description + '</dd>' );
  layer.addTo(map);
  jq("dt#" + f.id + " a").mouseover(
    function() { layer.openPopup(); } );
  jq("dt#" + f.id + " a").mouseout(
    function() { layer.closePopup(); } );
}

for (i=0; i<where.features.length; i++) {
  var f = where.features[i];
  setupFeature(f);
}
