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

        if (element.getBoundingClientRect().top < screenSize/2) {

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

/*Video promocional automatico*/


window.addEventListener('load', videoScroll);
window.addEventListener('scroll', videoScroll);

function videoScroll() {

  if ( document.querySelectorAll('video[autoplay]').length > 0) {
    var windowHeight = window.innerHeight,
        videoEl = document.querySelectorAll('video[autoplay]');

    for (var i = 0; i < videoEl.length; i++) {

      var thisVideoEl = videoEl[i],
          videoHeight = thisVideoEl.clientHeight,
          videoClientRect = thisVideoEl.getBoundingClientRect().top;

      if ( videoClientRect <= ( (windowHeight) - (videoHeight*.5) ) && videoClientRect >= ( 0 - ( videoHeight*.5 ) ) ) {
        thisVideoEl.play();
      } else {
        thisVideoEl.pause();
      }

    }
  }

}

/*Fin video promocional automatico*/

/*Animaciones scroll ultimas tres imagenes*/

window.addEventListener("scroll", function(){
    let animacion = document.getElementById("animado");
    if(animacion){
    let posicionObj1 = animacion.getBoundingClientRect().top;
    console.log(posicionObj1);
    let tamañoDePantalla = window.innerHeight;

    if(posicionObj1 < tamañoDePantalla){

      animacion.style.animation = "mover2 1s ease-out"

    }}
})

window.addEventListener("scroll", function(){
    let animacion = document.getElementById("animadosegundo");
    if(animacion){
    let posicionObj1 = animacion.getBoundingClientRect().top;
    console.log(posicionObj1);
    let tamañoDePantalla = window.innerHeight;

    if(posicionObj1 < tamañoDePantalla){

      animacion.style.animation = "mover 1s ease-out"

    }}
})

window.addEventListener("scroll", function(){
    let animacion = document.getElementById("animadotercero");
    if(animacion){
    let posicionObj1 = animacion.getBoundingClientRect().top;
    console.log(posicionObj1);
    let tamañoDePantalla = window.innerHeight;

    if(posicionObj1 < tamañoDePantalla){

      animacion.style.animation = "mover2 1s ease-out"

    }}
})

/*Fin animaciones scroll ultimas tres imagenes*/


window.addEventListener('scroll', function() {
    let elements = document.getElementsByClassName('scroll-content3');
    let screenSize = window.innerHeight;

    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];

        if (element.getBoundingClientRect().top < screenSize) {

            element.classList.add('visible3');

        } else {

            element.classList.remove('visible3');

        }

    }

});