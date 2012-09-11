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

var map = L.map('map').fitBounds([
  [bounds[1], bounds[0]],
  [bounds[3], bounds[2]] ]);

L.tileLayer(
    'http://api.tiles.mapbox.com/v3/sgillies.map-ac5eaoks/{z}/{x}/{y}.png', {
        maxZoom: 18,
        }).addTo(map);

function setupFeature(f) {
  var layer = L.GeoJSON.geometryToLayer(f);
  layer.bindPopup(
    '<dt><a href="' + f.properties.link + '">' + f.properties.title + '</a></dt>'
    + '<dd>' + f.properties.description + '</dd>' );
  layer.addTo(map);
  jq("dt#" + f.id + " a").mouseover(
    function() { layer.openPopup(); } );
}

for (i=0; i<where.features.length; i++) {
  var f = where.features[i];
  setupFeature(f);
}

/*L.geoJson(where, {
    style: function (feature) {
        return {color: feature.properties.color};
    },
    onEachFeature: function (feature, layer) {
        layer.bindPopup(feature.properties.description);
        jq("#" + feature.properties.link)
    }
}).addTo(map);*/

