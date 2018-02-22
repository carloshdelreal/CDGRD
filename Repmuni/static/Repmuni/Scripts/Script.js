$(function() {
    $("svg polygon").hover(function() {
        $(this).siblings().addClass('estrella-verde');
        $(this).addClass('estrella-verde');
    });
    $("svg polygon").mouseout(function() {

        $(this).siblings().removeClass('estrella-verde');
        $(this).removeClass('estrella-verde')
    });
    $("#mapanorte g > polygon").hover(function() {

        $(this).siblings().addClass('estrella-verde');
        $(this).siblings().removeClass('estrella-azul');
        $(this).addClass('estrella-verde');
        $(this).removeClass('estrella-azul')
    });
    $("#mapanorte g > polygon").mouseout(function() {
        $(this).siblings().removeClass('estrella-verde');
        $(this).siblings().addClass('estrella-azul');
        $(this).removeClass('estrella-verde');
        $(this).addClass('estrella-azul');
    });
    $("svg polygon").click(function(){
        alert("hello "+this.parentElement.getAttribute("name"));
    });
    $("svg polygon").click(function(){
        alert("hello "+this.parentElement.getAttribute("name"));
    });
    $("svg polygon").click(function(){
        alert("hello "+this.parentElement.getAttribute("name"));
    });
});

var map;

var markers = [];

var polygon = null;

function initMap(){
    var styles = [
        {
            featureType: 'administrative.province',
            elementType: 'geometry.stroke',
            stylers: [{color: '#5e3735'}]
        },{
            featureType: 'administrative.neighborhood',
            elementType: 'geometry.fill',
            stylers: [{color: '#5e3735'}]
        },{
            featureType: 'poi.medical',
            elementType: 'geometry.fill',
            stylers: [{color: '#1111ff'}]
        },
        
    ]
    
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 7.8940231, lng: -72.7578256} ,
        zoom: 7,
        styles: styles,
        mapTypeControl: true
    });

    var locations = [
        
        {title: 'Tibu', location: {lat: 8.6413342762, lng: -72.732154245}},
        {title: 'El Carmen', location: {lat: 8.53402482554, lng: -73.4568454812}},
        {title: 'Ocana', location: {lat: 8.24007035822, lng: -73.3465060431}},
        {title: 'Salazar', location: {lat: 7.77665688289, lng: -72.8135700188}},
        {title: 'Chinácota', location: {lat: 7.60370514094, lng: -72.6031172289}},
        {title: 'Pamplona', location: {lat: 7.3863612608, lng: -72.6550496324}},
        {title: 'Toledo', location: {lat: 7.30987114327, lng: -72.4831727537}},
         
        {title: 'Bilbao', location: {lat: 7.925964, lng: -72.499061}},
        {title: 'Cúcuta', location: {lat: 7.885684, lng: -72.503675}},
        //{title: 'Manhattan', location: {lat: 40.741267, lng: -73.988569}}
    ]
    
    var largeinfoWindow = new google.maps.InfoWindow();
    var drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.POLYGON,
        drawingControl: true,
        drawingControlOptions: {
          position: google.maps.ControlPosition.TOP_LEFT,
          drawingModes: [
            google.maps.drawing.OverlayType.POLYGON
          ]
        }
    });
    var defaultIcon = makeMarkerIcon('0091ff');
    var highlightedIcon = makeMarkerIcon('ffff24');
    var bounds = new google.maps.LatLngBounds();

    for (var i=0; i < locations.length; i++){
            var position = locations[i].location;
            var title = locations[i].title;
            
            var marker = new google.maps.Marker({
                position: position,
                title: title,
                icon: defaultIcon,
                animation: google.maps.Animation.DROP,
                id: i
            });
            //push the marker to our array of markers
            markers.push(marker);
            
            bounds.extend(marker.position);

            marker.addListener('click', function(){
                populateInfoWindow(this, largeinfoWindow);
            });
            marker.addListener('mouseover', function() {
                this.setIcon(highlightedIcon);
            });
            marker.addListener('mouseout', function(){
                this.setIcon(defaultIcon);
            });
    }

    map.fitBounds(bounds);
    document.getElementById('show-listings').addEventListener('click', showListings);
    document.getElementById('hide-listings').addEventListener('click', hideListings);
    
    document.getElementById('toggle-drawing').addEventListener('click', function() {
        toggleDrawing(drawingManager);
    });
    //Functions

    function populateInfoWindow(marker, infowindow) {
        // Check to make sure the infowindow is not already opened on this marker.
        if (infowindow.marker != marker) {
            infowindow.setContent('');
            infowindow.marker = marker;
            // Make sure the marker property is cleared if the infowindow is closed.
            infowindow.addListener('closeclick', function() {
                infowindow.marker = null;
            });

            var streetViewService = new google.maps.StreetViewService();
            var radius = 50;
            function getStreetView(data, status){
                if ( status == google.maps.StreetViewStatus.OK){
                    var nearStreetViewLocation = data.location.latLng;
                    var heading = google.maps.geometry.spherical.computeHeading(
                        nearStreetViewLocation, marker.position);
                    infowindow.setContent(                        
                        '<div>' + marker.title + '</div>'+
                        '<div>Lat: '+ marker.position.lat().toFixed(7) +'</div>' + 
                        '<div>Lat: '+ marker.position.lng().toFixed(7) +'</div>'
                        
                    );
                    var panoramaOptions = {
                        position: nearStreetViewLocation,
                        pov: {
                            heading: heading,
                            pitch: 30
                        }
                    };
                    var panorama = new google.maps.StreetViewPanorama(
                        document.getElementById('pano'), panoramaOptions);

                }else{
                    infowindow.setContent(
                        '<div>' + marker.title + '</div>'+
                        '<div>No Street View Found </div>'
                    );
                }

            }
            streetViewService.getPanoramaByLocation(marker.position, radius, getStreetView);
            infowindow.open(map, marker);   
        }
    }
    drawingManager.addListener('overlaycomplete', function(event) {
        // First, check if there is an existing polygon.
        // If there is, get rid of it and remove the markers
        if (polygon) {
          polygon.setMap(null);
          hideListings(markers);
        }
        // Switching the drawing mode to the HAND (i.e., no longer drawing).
        drawingManager.setDrawingMode(null);
        // Creating a new editable polygon from the overlay.
        polygon = event.overlay;
        polygon.setEditable(true);
        // Searching within the polygon.
        searchWithinPolygon();
        // Make sure the search is re-done if the poly is changed.
        polygon.getPath().addListener('set_at', searchWithinPolygon);
        polygon.getPath().addListener('insert_at', searchWithinPolygon);

        var area =google.maps.geometry.spherical.computeArea(polygon.getPath());
        window.alert(area.toFixed(2)+" metros cuadrados");
    });
}
    
function makeMarkerIcon(markerColor){
    var markerImage = new google.maps.MarkerImage(
        'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +'|40|_|%E2%80%A2',            
        new google.maps.Size(21,34),
        new google.maps.Point(0, 0),
        new google.maps.Point(10, 34),
        new google.maps.Size(21, 34));
    return markerImage;
}
function showListings(){
    var bounds = new google.maps.LatLngBounds();
    for ( var i = 0; i < markers.length; i++ ){
        markers[i].setMap(map);
        bounds.extend(markers[i].position);
    }
    map.fitBounds(bounds)
}

function hideListings(){
    for (var i = 0; i < markers.length; i++){
        markers[i].setMap(null);
    }
}
function toggleDrawing(drawingManager) {
    if (drawingManager.map) {
      drawingManager.setMap(null);
      // In case the user drew anything, get rid of the polygon
      if (polygon !== null) {
        polygon.setMap(null);
      }
    } else {
      drawingManager.setMap(map);
    }
}
function searchWithinPolygon() {
    for (var i = 0; i < markers.length; i++) {
      if (google.maps.geometry.poly.containsLocation(markers[i].position, polygon)) {
        markers[i].setMap(map);
      } else {
        markers[i].setMap(null);
      }
    }
}

    
    



