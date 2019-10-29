let map = L.map('map_div', { zoomControl: true });
debugger;


map.setView([52.908902 , 9.294434], 6.4);





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
let ParkingAreaLayer //polygon
var spot = L.layerGroup();
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

//var query = '<?php echo $query ?>' ;

//function to acquire point data from php
		var north=map.getBounds().getNorth();
		var south=map.getBounds().getSouth();
		var east=map.getBounds().getEast();
		var west=map.getBounds().getWest();
      var geojson = 0;
//createParkingSpotFeatures();

 $(document).ready(function(){  

	createParkingSpotFeatures();
	createParkingAreaFeatures();
  });
  
    var ParkingAreastyle = {
    "color": "green"
  }
  
function createParkingSpotFeatures() {
	
	if (map.getZoom() >= 12) {
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

         ParkingSpotLayer = L.geoJSON(query, {
          id: 'ParkingSpotLayer',
          pointToLayer: function (feature, latlng) {
            return L.marker(latlng);
          },
          onEachFeature: onEachFeature
        });
        spot.addLayer(ParkingSpotLayer);
        //return spot;
	  
      });
	          
	};	//console.log(result);
};

// function to acquire ParkingArea from php (polygon)

function createParkingAreaFeatures() {
  
  
    $.ajax({method:'POST',
      url: '../php/db_polygon.php',
      data: {
			var1:north, 
			var2:south, 
			var3:east, 
			var4:west
	}})
 /* success: function(query){
        var obj = eval('('+query +')');

        ParkingAreaLayer = L.geoJson(obj,{style: function(){
            return {color:'darkgray',fillColor:'white',weight:1};
        }}).addTo(map);
        Area.addLayer(ParkingAreaLayer);
        }   
                  
     });
*/
      //dataType:'json'})
     .done(function(query){
		  console.log(query);
		  query.forEach(function(obj){
			 
			  obj = obj.geometry.replace("\[\[\[", "\[\[").replace("\]\]\]","\]\]");
			  L.geoJSON(obj).addTo(map);
			   Area.addLayer(obj);
			  
			  
			  // geojson= L.geoJson(obj,{style: function(){
                    //return {color:'darkgray',fillColor:'white',weight:1};
               // }}).addTo(map);
			  /*ParkingAreaLayer = L.geoJSON(obj,{
                id: 'ParkingAreaLayer',
                style:styleA,
              }).addTo(map);*/
		  });
			  	
			 // obj = obj.geometry.replace("\[\[\[", "\[\[").replace("\]\]\]","\]\]");
			  
			 
			 //L.geoJSON(obj).addTo(map);
		  //});
		 
        /*ParkingAreaLayer = L.geoJSON(query, {
          id: 'ParkingAreaLayer'
		  
        }).then((Area) => {
          Area.results.bindings.forEach(Area => {
            ParkingAreaLayer.addData(_createPolygonFeaturen(Area));
          });          
        });*/
       
        
    //});
}); 
};


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
    "Spots": spot,
    "Area": Area,    
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

 
  
  
