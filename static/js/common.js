$(window).scroll(function () {
    if ($(window).scrollTop() >= 300) {
        $('header').addClass('header-is-scrolled');
    }
    else {
        $('header').removeClass('header-is-scrolled');
    }
});
