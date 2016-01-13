$(document).ready(function () {

    $('.navbar-toggle').click(function () {
        /*$('#navbar').slideToggle();*/
        $('.main-content').toggleClass('sidebar-menu-is-open');
        $('header').toggleClass('sidebar-menu-is-open');
        $('#sidebar-nav').toggleClass('sidebar-menu-is-open');
        $('.header-bars-wrapper i').toggleClass('fa-times').toggleClass('fa-bars');
    });


    <!-- Custom ADF Widget JS  =============================-->
    $(".adf-blackbox ").hide();
    $(".adf-mbox .collect").hide();
    $(".adf-modalbox").hover(
        function () {
            $(".adf-main").fadeToggle("slow", "swing");
            $(".adf-blackbox").fadeToggle("slow", "swing", function () {
                $(".adf-mbox .collect").slideToggle("fast", "swing");

            });
        }, function () {
            $(".adf-mbox .collect").slideToggle("fast", "swing", function () {
                $(".adf-blackbox").fadeToggle("slow", "swing");
                $(".adf-main").fadeToggle("slow", "swing");

            });

        }).click(function () {
            document.getElementById('section-form').scrollIntoView();
        });
});


<!-- Jquery mask for phone input -->
$(document).ready(function () {
    $('#id_phone, #id_telephone').mask('000-000-0000');
});

$("form").submit(function (e) {

    var ref = $(this).find("[required]");

    $(ref).each(function () {
        if ($(this).val() == '') {
            alert("Required field should not be blank.");

            $(this).focus();

            e.preventDefault();
            return false;
        }
    });
    return true;
});

$(document).ready(function () {

    $("#how-it-works-link, .header-contact-as, #sidebar-how-it-works, #sidebar-contact-as").on("click", "a", function (event) {

        //отменяем стандартную обработку нажатия по ссылке

        event.preventDefault();


        //забираем идентификатор бока с атрибута href

        var id = $(this).attr('href'),


        //узнаем высоту от начала страницы до блока на который ссылается якорь

            top = $(id).offset().top;


        //анимируем переход на расстояние - top за 1500 мс

        $('body,html').animate({scrollTop: top}, 700);

    });

});
