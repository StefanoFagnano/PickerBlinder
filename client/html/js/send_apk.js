// $('#first-attack').submit(function (e){
//     e.preventDefault();
//     const $form = $(this);
//     const url = 'http://localhost:5000/api/first/upload/';
//
//     let posting = $.post(url, {
//         apk: $('#apk_upload').val(),
//         //injecotions: $('#injecotions').val()
//     });
//
//     posting.done(function(data) {
//         $('#result').text('success');
//     });
//     posting.fail(function() {
//         $('#result').text('failed');
//     });
// })

$("#first-attack").submit(function(e) {

    var url = "http://localhost:5000/api/first/upload/";

    $.ajax({
        type: "POST",
        url: url,
        contentType: 'contentType:attr( "enctype", "multipart/form-data" ),',
        data: $("#first-attack").serialize(), // I've tried serializeArray() & serialize()
        success: function(data)
        {
            alert(data);
        }
    });

    e.preventDefault();
});