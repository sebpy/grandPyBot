var wait = $('#wait');
var user_post = $('#user_post');
var shoutform = $('#shoutform');
var shb_msg = $("#msg");

wait.hide();
user_post.focus();

//var api_gmap = URL_API_GMAPS + API_KEY_MAPS // à verifier

shoutform.on('submit', function(e) {
    e.preventDefault();
    var text = user_post.val();
    if(text != ""){
        $.ajax({
            url: $SCRIPT_ROOT + '/_answer',
            type: 'POST',
            data: $('form').serialize(),

            success: function (test) {
                var input = $("<div>").text(text).html();

                if (input != '') {
                    $("<div class='row'><div class='message' >" + input + "</div></div>").hide().appendTo(shb_msg).show('slow');
                    $("<div class='row'><div class='message bot'>" + test['wiki_reply'] + "</div></div>").hide().appendTo(shb_msg).show('slow');
                }
            }
        })
    }
    else {
        alert("Vous devez compléter votre demande!");
    }
});

