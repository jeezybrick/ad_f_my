$(document).ready(function () {

    /*$.ajax({
     url: "http://127.0.0.1:8000/static/pages/widget.html",
     dataType: "text",
     success: function (data) {
     $("#ad-adfits").html(data);
     }
     });*/


    var pub_id = $('#ad-adfits').attr('pub_id'),
        api_url = 'http://adfits.com/api/';

    $.ajax({
        url: api_url,
        data: data,
        success: success,
        dataType: 'json'
    });
});

$(document).ready(function () {
    $.ajax({
        url: '//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js',
        dataType: 'script',
        beforeSend: function (xhr, opts) {

            console.log(xhr);
            if (1 == 1) //just an example
            {
                xhr.abort();
            }
        },
        complete: function () {
            console.log('DONE');
        }
    });

    $(".adsbygoogle").remove();
    $("ins[data-ad-client]").remove();
    $("ins[data-ad-slot]").remove();
    $("ins[data-ad-format]").remove();
    //$( 'script[src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]' ).remove();
});