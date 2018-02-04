
$(".messages").animate({ scrollTop: $(document).height() }, "fast");

function newMessage() {
    message = $(".message-input input").val();
    if ($.trim(message) == '') {
        return false;
    }
    $('<li class="sent"><img src="static/images/user.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
    $('.message-input input').val(null);
    $('.contact.active .preview').html('<span>You: </span>' + message);
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

function newReply() {
    message = "Have a Reply";
    if ($.trim(message) == '') {
        return false;
    }
    $('<li class="replies"><img src="static/images/watson_avatar.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
    $('.message-input input').val(null);
    $('.contact.active .preview').html('<span>You: </span>' + message);
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

$('.submit').click(function () {
    newMessage();
    newReply();
});

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        newMessage();
        newReply();
        return false;
    }
});