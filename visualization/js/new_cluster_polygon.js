let map = L.map('map_div', { zoomControl: true });
debugger;


map.setView([52.908902 , 9.294434], 10);


//add tile layers
var mapLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {

  attribution: '<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map)

var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

L.control.scale().addTo(map);

//group tile layers as baseMaps
let baseMaps = {
  "OSM": mapLayer,
  "Image": Esri_WorldImagery
}

//set global variables for layers
let ParkingSpotLayer //Point
 let ParkingAreaLayer//polygon
var spot = L.layerGroup();
var Clusters=L.layerGroup();



var Area = L.layerGroup();


// add search in top left corner
var lc = L.control.locate({
  position: 'topleft',
  strings: {
    setView: "once"
  }
}).addTo(map);

//add search in top left corner
map.addControl(new L.Control.Search({
  url: 'http://nominatim.openstreetmap.org/search?format=json&q={s}',
  jsonpParam: 'json_callback',
  propertyName: 'display_name',
  propertyLoc: ['lat', 'lon'],
  marker: L.marker([0, 0]),
  autoCollapse: true,
  autoType: false,
  minLength: 2
}));
//function to acquire point data from php
		var north=map.getBounds().getNorth();
		var south=map.getBounds().getSouth();
		var east=map.getBounds().getEast();
		var west=map.getBounds().getWest();
      
	  

//createParkingSpotFeatures();

 $(document).ready(function(){  
      
	createParkingSpotFeatures();
	createParkingAreaFeatures();

	
  });
  
    var ParkingAreastyle = {
    "color": "green"
  }
  
  
  // marker cluster
var markers = L.markerClusterGroup({spiderfyOnMaxZoom: false, showCoverageOnHover: false, zoomToBoundsOnClick: false});
map.addLayer(markers);

function createParkingSpotFeatures() {
	
	if (map.getZoom() >= 0) {
		var north=map.getBounds().getNorth();
		var south=map.getBounds().getSouth();
		var east=map.getBounds().getEast();
		var west=map.getBounds().getWest();
         
		$.ajax({method:'POST',
			url: '../php/db_ac.php',
			data: {
				var1:north, 
				var2:south, 
				var3:east, 
				var4:west
		}})
      //dataType:'json',
	 // success: function(query){
		//console.log(query);
	 //};
      .done(function(query){
	     console.log(query);
		 markers.clearLayers();
         ParkingSpotLayer = L.geoJSON(query, {
          id: 'ParkingSpotLayer',
          pointToLayer: function (feature, latlng) {
            return L.marker(latlng);
          },
          onEachFeature: onEachFeature
        });
        markers.addLayer(ParkingSpotLayer);
        //return spot;
	  
      });
	          
	};	//console.log(result);
};

//for polygon
//polygon
// marker cluster
var markers1 = L.markerClusterGroup({spiderfyOnMaxZoom: false, showCoverageOnHover: false, zoomToBoundsOnClick: false});
map.addLayer(markers1);

function createParkingAreaFeatures() {
	
	if (map.getZoom() >= 0) {
		var north=map.getBounds().getNorth();
		var south=map.getBounds().getSouth();
		var east=map.getBounds().getEast();
		var west=map.getBounds().getWest();
         
		$.ajax({method:'POST',
			url: '../php/db_polygon.php',
			data: {
				var1:north, 
				var2:south, 
				var3:east, 
				var4:west
		}})
      //dataType:'json',
	 // success: function(query){
		//console.log(query);
	 //};
      .done(function(query){
	     console.log(query);
		 markers1.clearLayers();
         ParkingAreaLayer = L.geoJSON(query, {
          id: 'ParkingAreaLayer',
          pointToLayer: function (feature, latlng) {
            return L.marker(latlng);
          },
          onEachFeature: onEachFeature
        });
        markers1.addLayer(ParkingAreaLayer);
        //return spot;
	  
      });
	          
	};	//console.log(result);
};



/*
		function populate() {
			for (var i = 0; i < 200; i++) {
				var m = L.marker(getRandomLatLng(map));
				markers.addLayer(m);
			}
			return false;
			
		}
		function getRandomLatLng(map) {
			var bounds = map.getBounds(),
				southWest = bounds.getSouthWest(),
				northEast = bounds.getNorthEast(),
				lngSpan = northEast.lng - southWest.lng,
				latSpan = northEast.lat - southWest.lat;

			return L.latLng(
					southWest.lat + latSpan * Math.random(),
					southWest.lng + lngSpan * Math.random());
		}

		markers.on('clusterclick', function (a) {
			a.layer.zoomToBounds();
		});

		populate();
		map.addLayer(markers);
*/

//clusters for spots
/*spotClusters = new L.MarkerClusterGroup({
		  spiderfyOnMaxZoom: true,
		  showCoverageOnHover: false,
		  zoomToBoundsOnClick: true,
		  disableClusteringAtZoom: 16
		});
		$.getJSON("ParkingSpotLayer", function (data) {
  		ParkingSpotLayer.addData(data);
			spotClusters.addLayer(ParkingSpotLayer);
		});.complete(function () {
    	map.fitBounds(ParkingSpotLayer.getBounds());
		});*/
		
//function on each feature
function onEachFeature(feature, layer) {
  if (feature.properties && feature.properties) {
      var popup = feature.properties.amenity + ": " + feature.properties.name;
      layer.bindPopup(popup);
  }
}

// function to  create polygon feature
let _createPolygonFeaturen = (entry) => {
    let temp = entry.geometry.value.split('(');
    let coordinatePairs = temp[1].split(',');
    let coordinates = [];
    coordinatePairs.forEach(pair => {
      let coordinatePair = [parseFloat(pair.split(' ')[0]), parseFloat(pair.split(' ')[1])];
      coordinates.push(coordinatePair);
    });
  
    let geojsonFeature = {
      "type": "Feature",
      "properties": {
        "name": entry.name.value,
        "id": entry.s.value,
        "entry": entry
      },
  
      "geometry": {
        "type": "Polygon",
        "coordinates": [coordinates]
      }
    };
    return geojsonFeature;
  };

  // function to create feature from json
var overlayMaps = {
    
	"Clusters":markers,
	"Area":markers1
    
  }
  
  //add layer control to map
let layerControl = L.control.layers(baseMaps, overlayMaps).addTo(map)

		map.on('zoom moved dragend',createParkingSpotFeatures);
        
        var ZoomViewer = L.Control.extend({
            onAdd: function() {
                var gauge = L.DomUtil.create('div');
                gauge.style.width = '200px';
                gauge.style.background = 'rgba(255,255,255,0.5)';
                gauge.style.textAlign = 'left';
                map.on('zoomstart zoom zoomend dragend moved', function(ev) {
                    gauge.innerHTML = 'Zoom level: ' + map.getZoom() + '<br>North:' + Math.round(map.getBounds().getNorth() * 1000) / 1000 + '  East:' + Math.round(map.getBounds().getEast() * 1000) / 1000 + '<br>South:' + Math.round(map.getBounds().getSouth() * 1000) / 1000 + '  West:' + Math.round(map.getBounds().getWest() * 1000) / 1000;
                })
                return gauge;
            }
        });

        (new ZoomViewer).addTo(map);

 
  
  
