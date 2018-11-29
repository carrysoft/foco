var key = ''
$.ajax({
    type: "GET",
    dataType: 'json',
    url: '/get_api_key',
    data: {},
    async: false,
    success: function(success) {
        if (success){
            key = success.key;
        }
    },
});
document.write('<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=places&amp;key='+key+'"></script>');
var script = '<script type="text/javascript" src="/aspl_employee_attendance_map/static/src/js/markerclusterer';
if (document.location.search.indexOf('compiled') !== -1) {
    script += '_compiled';
}
script += '.js"><' + '/script>';
document.write(script);

function initialize_gmap(lat_long) {
    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap',
        streetViewControl: true,
        fullscreenControl: true
    };
    // Display a map on the page
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
    map.setTilt(45);
    markers = lat_long
    var infoWindow = new google.maps.InfoWindow(), marker, i;
    for( i = 0; i < markers.length; i++ ) {
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            map: map,
        });
        marker.setAnimation(google.maps.Animation.DROP);
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoWindow.setContent("<b>"+lat_long[i][0]+"</b>");
                infoWindow.open(map, marker);
            }
        })(marker, i));
        map.fitBounds(bounds);
    }
    // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        this.setZoom(7);
        google.maps.event.removeListener(boundsListener);
    });
}
