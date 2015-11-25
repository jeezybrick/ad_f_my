adFitsApp = (function() {
	return {
		set_app_cookie: function(adftoken, adfdy) {

			if (!$.cookie('adftoken')) {
				$.cookie('adftoken')
				$.cookie('adftoken', adftoken, { expires: 7, path: '/' });
				$.cookie('adfdy', adfdy, { expires: 7, path: '/' });
				console.log($.cookie('adftoken'));
			}
		},
	}
})();