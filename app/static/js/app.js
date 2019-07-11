var wait = $('#wait');
var user_post = $('#user_post');
var shoutform = $('#shoutform');
var shb_msg = $("#msg");

wait.hide();
user_post.focus();

//var api_gmap = URL_API_GMAPS // à verifier
function initMaps(lat, lng, name, place_id) {

    var myLatLng = {lat: lat, lng: lng};

    var map = new google.maps.Map(document.getElementById(place_id), {
        zoom: 15,
        center: myLatLng,
        disableDefaultUI: true
    });

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: name
    });
}

shoutform.on('submit', function(e) {
    e.preventDefault();
    wait.show();
    var text = user_post.val();
    if(text != ""){
        $.ajax({
            url: $SCRIPT_ROOT + '/_answer',
            type: 'POST',
            data: $('form').serialize(),

            success: function (reply) {
                wait.hide();
                var input = $("<div>").text(text).html();

                if (input != '') {
                    $("<div class='row'><div class='message' >" + input + "</div></div>").hide().appendTo(shb_msg).show('slow');

                    // Google map api reply
                    var lat = reply['map_reply']['candidates'][0]['geometry']['location']['lat'];
                    var lng = reply['map_reply']['candidates'][0]['geometry']['location']['lng'];
                    var name = reply['map_reply']['candidates'][0]['name'];
                    var place_id = reply['map_reply']['candidates'][0]['place_id'];

                    $("<div class='row'><div class='message bot'>" +
                      "<div class='map' id='"+ place_id + "'></div>" +
                      "</div></div>").hide().appendTo(shb_msg).show('slow');

                    initMaps(lat, lng, name, place_id)

                    // Wikipedia api reply
                    if (reply['wiki_reply'] != ""){
                        $("<div class='row'><div class='message bot'>" + reply['wiki_reply'] + "</div></div>").hide().appendTo(shb_msg).show('slow');
                    }
                    else {
                        $("<div class='row'><div class='message bot'>Une erreur est survenue :(</div></div>").hide().appendTo(shb_msg).show('slow');
                    }
                }
            }
        })
    }
    else {
        alert("Vous devez compléter votre demande!");
    }
});

