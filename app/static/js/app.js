var submit = $('#submit');
var user_message = $('#user_message');
var chatbox = $('#chatbox');
var chat_msg = $("#chatmsg");
var wait = $('#wait');
var nb_responses = 0;
var id_msg = "msg"+nb_responses;
var id_map = "map"+nb_responses;

wait.hide();
user_message.focus();
var maps_api_url = "https://maps.googleapis.com/maps/api/js?key="+$GMAPS_KEY;

$.getScript(maps_api_url, function() {
 //using getscript to ensure gmaps api is loaded
    function initializeMap(name, json, id) {

        var myLatLng = json.candidates[0].geometry.location;

        var map = new google.maps.Map(id, {
            zoom: 15,
            center: myLatLng
        });

        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: name,
            animation: google.maps.Animation.DROP
        });

        function toggleBounce() {
            if (marker.getAnimation() !== null) {
                marker.setAnimation(null);
            } else {
                marker.setAnimation(google.maps.Animation.BOUNCE);
            }
        }

        var ne_lat = json.candidates[0].geometry.viewport.northeast.lat;
        var ne_lng = json.candidates[0].geometry.viewport.northeast.lng;
        var sw_lat = json.candidates[0].geometry.viewport.southwest.lat;
        var sw_lng = json.candidates[0].geometry.viewport.southwest.lng;

        var ne_bound = new google.maps.LatLng(ne_lat, ne_lng);
        var sw_bound = new google.maps.LatLng(sw_lat, sw_lng);
        var bounds = new google.maps.LatLngBounds();

        bounds.extend(ne_bound);
        bounds.extend(sw_bound);

        map.fitBounds(bounds);

        setTimeout(function(){
            marker.setMap(map);
            toggleBounce(); }, 3000);

    }


    submit.on('click', function (e) {
        //function to handle form submission
        e.preventDefault();

        if (user_message.val()) {
            $.ajax({
                url: $SCRIPT_ROOT + '/_response',
                type: 'POST',
                data: $('form').serialize(),

                success: function (response, status) {

                    // Ajax call successful : handle the response.
                    var input = $("<div>").text(user_message.val()).html();
                    user_message.val("");
                    nb_responses++;
                    id_msg = "msg" + nb_responses;
                    id_map = "map" + nb_responses;

                    if (input !== "") { //second check of input content in case of multiple sending of the message

                        //Add message in chatbox
                        $("<div class='row'><div class='message' id='" + id_msg + "'>" + input + "</div></div>").hide().appendTo(chat_msg).show('slow');

                        //Display wait message for 1.2 secs, then display response
                        wait.delay(200).fadeIn(1200).fadeOut('slow', function () {

                            if (response['gmaps_reply'] !== "No result") {

                                $("<div class='row'><div class='message bot'>" +
                                    "Voici une carte de " + response['gmaps_name'] + " à l'adresse : " + response['gmaps_address'] +
                                    "<div class='map' id='" + id_map + "'></div></div></div>").hide().appendTo(chat_msg).fadeIn('slow', function(){

                                    initializeMap(response['gmaps_name'],
                                        response['gmaps_json'],
                                        document.getElementById(id_map));


                                });

                            }
                            else {
                                $("<div class='row'><div class='message bot'>Je n'ai pas trouvé de carte à ce sujet.</div></div>").hide().appendTo(chat_msg).show('slow');
                            }

                            $("<div class='row'><div class='message bot'>" + response['wiki_reply'] + "</div></div>").hide().appendTo(chat_msg).show('slow');

                            chatbox.animate({scrollTop: chatbox[0].scrollHeight}, 1000);
                        });
                    }
                },

                error: function (response, status, error) {
                    alert("There was a problem with the ajax request: " + error);

                },

                complete: function () {
                    //scroll to the bottom to see input form
                    chatbox.animate({scrollTop: chatbox[0].scrollHeight}, 1000);
                }
            });
        }
    });
});