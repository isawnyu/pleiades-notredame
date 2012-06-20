  var MTID = 'aw';
  var infowindow = new google.maps.InfoWindow();
  var map = null;
  var recent = null;


    function popup(evt) {
      var msg = document.createElement("div");
      msg.setAttribute("style", "overflow:auto");
      var head = document.createElement("h3");
      head.setAttribute("style", "margin-top:0.5em");
      var tail = document.createElement("p");
      var details = document.createElement("a");
      details.setAttribute("href", evt.featureData.author.uri);
      jq(details).text("Details");
      jq(tail).append(details);
      jq(head).text(evt.featureData.name);
      
      jq(msg).append(head);
      jq(msg).append(unescape(unescape(evt.featureData.description)));
      jq(msg).append(tail);

      infowindow.close();
      infowindow.setOptions({position: evt.latLng, content: msg});
      infowindow.open(map);
    }

  function initialize() {
    var latlng = new google.maps.LatLng(0.0, 0.0);

    var myOptions = {
      zoom: 10,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.TERRAIN
    };

    map = new google.maps.Map(document.getElementById("map"),
        myOptions);

    recent = new google.maps.KmlLayer("http://pleiades.stoa.org/news/changes.kml", {suppressInfoWindows: true});
    google.maps.event.addListener(recent, 'click', popup);
    recent.setMap(map);
  }

  registerPloneFunction(initialize);

