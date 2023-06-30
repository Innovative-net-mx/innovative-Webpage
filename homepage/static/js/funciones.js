/*Animacion servicio SCROLL*/

window.addEventListener('scroll', function() {
    let elements = document.getElementsByClassName('scroll-content');
    let screenSize = window.innerHeight;

    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];

        if (element.getBoundingClientRect().top < screenSize) {

            element.classList.add('visible');

        } else {

            element.classList.remove('visible');

        }

    }

});

window.addEventListener('scroll', function() {
    let elements = document.getElementsByClassName('scroll-content2');
    let screenSize = window.innerHeight;

    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];

        if (element.getBoundingClientRect().top < screenSize) {

            element.classList.add('visible1');

        } else {

            element.classList.remove('visible1');

        }

    }

});

/*FIN animacion servicio SCROLL*/

/*Apis mapas*/
var map, map2;

function initMap() {

    var coord = { lat: 32.4837952, lng: -116.9475872 },
        map = new google.maps.Map(document.getElementById('map'), {
            center: coord,
            zoom: 10
        });
    new google.maps.Marker({
        position: coord,
        map: map,
        title: "Innovative net Tijuana",
    });
    var coorden = { lat: 32.6000276, lng: -115.3721117 },
        map2 = new google.maps.Map(document.getElementById('map2'), {
            center: coorden,
            zoom: 10
        });
    var marker = new google.maps.Marker({
        position: coorden,
        title: "Innovative net Mexicali",
    });
    marker.setMap(map2);
}
/*Fin Apis mapas*/

