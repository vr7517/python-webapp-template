
// run on ducument read
$('document').ready(function () {

});

// Text input and GET request
function loading(ennable) {
    if (ennable) {
        $('#text-loader').removeClass('gone');
        $('#text-input').attr('disabled', "");
        $('#text-submit').prop('disabled', true);
    } else {
        $('#text-loader').addClass('gone');
        $('#text-input').removeAttr('disabled');
        $('#text-submit').prop('disabled', false);
    }
}

function sendRequest(request) {
    loading(true);
    $('#text-input').val('');
    $.ajax({
        method: "GET",
        url: "./api/get-api",
        contentType: "application/text",
        data: { "request": request }
    })
        .done(function (response) {
            doSomething(response);
            loading(false);
        });
}

function doSomething(response) {
    console.log(response)
    $('#text-result').text(response);
};


$('#text-input').keydown(function (e) {
    var data = $('#text-input').val();
    if (e.which == 13 && data.length > 0) {
        sendRequest(data);
    }
});

$('#text-submit').click(function (e) {
    var data = $('#text-input').val();
    if (data.length > 0) {
        sendRequest(data);
    }
});


// Image input and POST request 

$("#img-input").change(function () {
    var preview = document.getElementById('img');

    $('#img-results').html('')
    $('#img-loader').removeClass('gone')

    var file = document.getElementById('img-input').files[0];
    var isSuccess = checkFileType(file);
    var reader = new FileReader();

    if (isSuccess) {
        reader.addEventListener("load", function () {
            preview.src = reader.result;
            preview.style.display = 'inline'
            preview.style.height = '100%';

            var form = new FormData($('#form')[0]);
            
            $.ajax({
                url: '/api/post-api',
                type: 'POST',
                data: form,
                cache: false,
                processData: false,
                contentType: false,
                success: function (result) {
                    update(result);
                }
            });


        }, false);

        if (file) {
            reader.readAsDataURL(file);
        }

    } else {
        alert('incorrect file type, please upload a JPG, JPEG, or PNG image.')
    }

});

function checkFileType(file){
    fileTypes = ['jpg', 'jpeg', 'png'];
    extension = file.name.split('.').pop().toLowerCase()
    return fileTypes.indexOf(extension) > -1;
}

function update(result) {
    console.log(result);
    $('#img-results').html(result)
    $('#img-loader').addClass('gone')
}