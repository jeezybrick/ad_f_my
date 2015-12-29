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