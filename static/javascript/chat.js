
$(".messages").animate({ scrollTop: $(document).height() }, "fast");

function newMessage() {
    message = $(".message-input input").val();
    if ($.trim(message) == '') {
        return false;
    }
    $('<li class="sent"><img src="static/images/user.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
    $('.message-input input').val(null);
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");

    sendRequest(message);
};

function sendRequest(message) {
    $.ajax({
        method: "GET",
        url: "./api/message",
        contentType: "application/text",
        data: { "msg": message }
    })
        .done(function (response) {
            newReply(response);
        });
}

function newReply(message) {

    if ($.trim(message) == '') {
        return false;
    }

    $('<li class="replies"><img src="static/images/watson_avatar.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
    $('.message-input input').val(null);
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

$('.submit').click(function () {
    newMessage();
});

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        newMessage();
        return false;
    }
});