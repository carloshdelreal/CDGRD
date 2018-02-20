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

function initMap(){
    
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 7.8940231, lng: -72.7578256} ,
        zoom: 8
    });

    var locations = [
        {title: 'Tibu', location: {lat: 8.6413342762, lng: -72.732154245}},
        {title: 'El Carmen', location: {lat: 8.53402482554, lng: -73.4568454812}},
        {title: 'Ocana', location: {lat: 8.24007035822, lng: -73.3465060431}},
        {title: 'Salazar', location: {lat: 7.77665688289, lng: -72.8135700188}},
        {title: 'Chinácota', location: {lat: 7.60370514094, lng: -72.6031172289}},
        {title: 'Pamplona', location: {lat: 7.3863612608, lng: -72.6550496324}},
        {title: 'Toledo', location: {lat: 7.30987114327, lng: -72.4831727537}}
    ]
    
    var largeinfoWindow = new google.maps.InfoWindow();
    
    var bounds = new google.maps.LatLngBounds();

    for (var i=0; i < locations.length; i++){
            var position = locations[i].location;
            var title = locations[i].title;
            
            var marker = new google.maps.Marker({
                position: position,
                title: title,
                animation: google.maps.Animation.DROP,
                id: i
            });
            
            
            //push the marker to our array of markers
            markers.push(marker);
            
            bounds.extend(marker.position);

            marker.addListener('click', function(){
                populateInfoWindow(this, largeinfoWindow);
            });
        }
        map.fitBounds(bounds);

        document.getElementById('show-listings').addEventListener('click', showListings);
        document.getElementById('hide-listings').addEventListener('click', hideListings);
    }

    function populateInfoWindow(marker, infowindow) {
        // Check to make sure the infowindow is not already opened on this marker.
        if (infowindow.marker != marker) {
          infowindow.marker = marker;
          infowindow.setContent(
              '<h5>' + marker.title + '</h5>\n'+
              '<div>Lat: '+ marker.position.lat().toFixed(7) +'</div>' + 
              '<div>Lat: '+ marker.position.lng().toFixed(7) +'</div>'
        
        );
          infowindow.open(map, marker);
          // Make sure the marker property is cleared if the infowindow is closed.
          infowindow.addListener('closeclick', function() {
            infowindow.marker = null;
          });
        }
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
    



