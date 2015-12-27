$(document).ready(function () {
    $.ajax({
        url: "http://127.0.0.1:8000/static/pages/widget.html",
        dataType: "text",
        success: function (data) {
            $("#ad-adfits").html(data);
        }
    });
}); 