$('#first-attack').submit(function (e){
    e.preventDefault();
    const $form = $(this);
    url = 'http://localhost/api/first/upload';


    var posting = $.post(url, {
        apk: $('#apk_upload').val(),
        injecotions: $('#injecotions').val()
    });

    posting.done(function(data) {
        $('#result').text('success');
    });
    posting.fail(function() {
        $('#result').text('failed');
    });


})
