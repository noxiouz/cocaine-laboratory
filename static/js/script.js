jQuery(document).ready(function() {

    $('#uploadInput').change(function(r) {
        var file = this.files[0];
        var type = file.type;

        var typeKey = type.split('/')[0];
        var typeValue = type.split('/')[1];

        if (typeKey != 'image' || ['png', 'jpg', 'jpeg'].indexOf(typeValue) < 0) {
            alert('Wrong image type!');
            var formData = new FormData($('#superForm')[0]);
            formData.reset();
        } else {
            // var reader = new FileReader();
            // reader.onload = (function(theFile) {
            //     return function(e) {
            //         $.ajax({
            //             url: '/filter/list', //server script to process data
            //             type: 'GET',
            //             dataType: 'json',
            //             data: {
            //                 'img': e.target.result
            //             },
            //             success: function(data) {
            //                 $('.filter-thumbnails').empty();
            //                 $.each(data, function(k, val) {
            //                     $('.filter-thumbnails').append(val);
            //                 });
            //             }
            //         });
            //     };
            // })(file);
            // reader.readAsDataURL(file);
        }
    });

    $('#uploadDialog .btn-primary').click(function() {
        console.log("govno", $('#superForm'));
        var formData = new FormData($('#superForm')[0]);
        $('body').append(formData);
        console.log(formData);
        $('#superForm').submit();
        // var formData = new FormData($('#superForm')[0]);
        // $.ajax({
        //     url: '/upload',
        //     type: 'POST',
        //     data: formData,
        //     cache: false,
        //     contentType: false,
        //     processData: false,
        //     success: function(response) {
        //         console.log(response);
        //     }
        // });
    });

    $('#uploadFileButton').click(function() {
        var formData = new FormData($('#superForm')[0]);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(response) {}
        });
    });

    $('#uploadDialogButton').click(function() {
        $.getJSON('/filter/list', function(data) {
            $('.filter-thumbnails').empty();
            $.each(data, function(k, val) {
                $('.filter-thumbnails').append(val);
            });
        });
    });

    $('.thumbnails .thumbnail').click(function() {
        var uid = $(this).attr("id");
        $.ajax({
            url: '/apply/' + uid,
            type: 'GET',
            cache: false,
            contentType: false,
            processData: false,
            success: function(response) {
                console.log("OK", response);
                window.location.replace("/");
            }
        });
    });
});
