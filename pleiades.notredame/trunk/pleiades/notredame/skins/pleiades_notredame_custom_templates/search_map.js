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
//var bounds = where.bbox;
var bounds = [
  [where.bbox[1]-0.125, where.bbox[0]-0.125],
  [where.bbox[3]+0.125, where.bbox[2]+0.125] ];

var map = L.map('map', {maxZoom: 12, zoomControl: false}).fitBounds(bounds);
pl_zoom({initialBounds: bounds}).addTo(map);

var terrain = L.tileLayer(
    'http://api.tiles.mapbox.com/v3/sgillies.map-ac5eaoks/{z}/{x}/{y}.png', {
        attribution: "ISAW, 2012"
        });
terrain.addTo(map);

/* Not added by default, only through user control action */
var streets = L.tileLayer(
    'http://api.tiles.mapbox.com/v3/sgillies.map-pmfv2yqx/{z}/{x}/{y}.png', {
        attribution: "ISAW, 2012"
        });

var imperium = L.tileLayer(
    'http://static.ahlfeldt.se/srtm/imperium/{z}/{x}/{y}.png', {
        attribution: "Johan Ahlfeldt, 2012",
        minZoom: 5,
        maxZoom: 11
        });

L.control.layers({
    "Terrain (default)": terrain,
    "Streets": streets,
    "Imperium": imperium,
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

