const LAT = 41.491340;
const LONG = -71.313755; // Default longitude value

var mapsRef = [];

L.Map.addInitHook(function () {
    mapsRef.push(this); // Use whatever global scope variable you like.
});

function initMap() {
    let mapOptions = {
        worldCopyJump: false,
        zoom: 10,
        center: [LAT, LONG],
    };

    // Create a map instance
    var map = L.map('map', mapOptions);

    // Add the tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }).addTo(map);

    console.log('initMap');

    // Check if address, latitude, and longitude are available
    if (latitude && longitude) {
        console.log('Latitude:', latitude);
        console.log('Longitude:', longitude);

        var lat = parseFloat(latitude);
        var long = parseFloat(longitude);
        updateMap(lat, long);
    }

    if (restaurantData && Array.isArray(restaurantData)) {
        console.log('Restaurant Data:', restaurantData);

        restaurantData.forEach(function(restaurant) {
            var marker = L.marker([restaurant.coordinates.latitude, restaurant.coordinates.longitude]).addTo(map);
            marker.bindPopup(restaurant.name);
        });
    }
}

function updateMap(lat, long) {
    var map = mapsRef.pop();

    map.flyTo({lat: lat, lng: long}, 12);

    mapsRef.push(map);
}

initMap();