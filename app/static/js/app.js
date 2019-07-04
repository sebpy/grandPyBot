var submit = $('#submit')
var shoutbox = $('#shoutbox')
var shoutform = $('#shoutform')
var wait = $('#wait')
var msg = $('#msg')
var user_post = $('#user_post')
var count_answer = 0
var msg_id = "msg" + count_answer
var map_id = "map" + count_answer

wait.hide();
user_post.focus();

var api_gmap = URL_API_GMAPS + API_KEY_MAPS // à verifier



var lat = 48.852969;
var lon = 2.349903;
var map = null;
// Fonction d'initialisation de la carte
function initMap() {
    // Créer l'objet "map" et l'insèrer dans l'élément HTML qui a l'ID "map"
    map = new google.maps.Map(document.getElementById("map"), {
    // Nous plaçons le centre de la carte avec les coordonnées ci-dessus
    center: new google.maps.LatLng(lat, lon),
    // Nous définissons le zoom par défaut
    zoom: 11,
    // Nous définissons le type de carte (ici carte routière)
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    // Nous activons les options de contrôle de la carte (plan, satellite...)
    mapTypeControl: true,
    // Nous désactivons la roulette de souris
    scrollwheel: false,
    mapTypeControlOptions: {
    // Cette option sert à définir comment les options se placent
    style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR
    },
    // Activation des options de navigation dans la carte (zoom...)
    navigationControl: true,
    navigationControlOptions: {
    // Comment ces options doivent-elles s'afficher
    style: google.maps.NavigationControlStyle.ZOOM_PAN
    }
    });
}


submit.on('click', function (c) {
    c.preventDefault();

    if (user_post.val()) {
        $ajax({
            url: '/_answer',
            type: POST,
            data: $('form').serialize(),

            success: function (reponse, status){
                var input = $('<div>').text(user_post.val()).html();
                user_post =.val("");
                count_answer++;
                msg_id = "msg" + count_answer;
                map_id = "map" + count_answer;
            }
        })
    }


})
}
