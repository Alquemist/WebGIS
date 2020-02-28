var map;

function initMap() {
    //var marker = new google.maps.marker(MyLatLon);

    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 44.397, lng: 17.644},
        zoom: 9,
        mapTypeId: google.maps.MapTypeId.HYBRID
    });

/*    var ctaLayer = new google.maps.KmlLayer({
        url: 'http://217.23.192.158:10080/kmzs/Mostar_sjever.kmz',
        map: map*/
 //   });
}