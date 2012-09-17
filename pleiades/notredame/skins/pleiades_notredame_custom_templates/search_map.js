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
var bounds = where.bbox;

var map = L.map('map', {maxZoom: 12}).fitBounds([
  [bounds[1]-0.125, bounds[0]-0.125],
  [bounds[3]+0.125, bounds[2]+0.125] ]);

var terrain = L.tileLayer(
    'http://api.tiles.mapbox.com/v3/sgillies.map-ac5eaoks/{z}/{x}/{y}.png', {
        attribution: "ISAW, 2012"
        });
terrain.addTo(map);

/* Not added by default, only through user control action */
var imperium = L.tileLayer(
    'http://static.ahlfeldt.se/srtm/imperium/{z}/{x}/{y}.png', {
        attribution: "Johan Ahlfeldt, 2012",
        minZoom: 5,
        maxZoom: 11
        });

L.control.layers({
    "Pelagios": imperium,
    "Pleiades (default)": terrain
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

