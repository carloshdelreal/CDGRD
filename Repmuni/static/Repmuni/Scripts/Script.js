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
function initMap(){
    var localizacion = {lat: 7.8940231, lng: -72.7578256};
    map = new google.maps.Map(document.getElementById('map'), {
        center: localizacion ,
        zoom: 8
    });
    var marcador = {lat: 7.924502, lng: -72.5019997}
    var marker = new google.maps.Marker({
          position: marcador,
          map: map,
          title: "Home Sweet Home!"
        });
    var infoWindow = new google.maps.InfoWindow({
        content: "Do you ever feel like an InfoWindow, floating through the wind," +
            'ready to start again?'
    });
    marker.addListener('click', function(){
        infoWindow.open(map, marker);
    });
}


