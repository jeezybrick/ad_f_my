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

        });


    $(".adf-modalbox").click(function () {
        // add js code for for when user clicks on widget here
    });
});


<!-- Jquery mask for phone input -->
$(document).ready(function () {
    $('#id_phone').mask('000-000-0000');
});

var forms = document.getElementsByTagName('form');
for (var i = 0; i < forms.length; i++) {
    forms[i].noValidate = true;

    forms[i].addEventListener('submit', function(event) {
        //Prevent submission if checkValidity on the form returns false.
        if (!event.target.checkValidity()) {
            event.preventDefault();
            //Implement you own means of displaying error messages to the user here.
        }
    }, false);
}
