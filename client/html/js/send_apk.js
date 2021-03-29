$('#first-attack').submit(function (e){
    e.preventDefault();
    const $form = $(this);
    const url = 'http://localhost:5000/api/first/upload';

    let posting = $.post(url, {
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
