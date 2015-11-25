var debug = false;

if (debug) {
	domain = 'localhost';
	base_url = 'http://localhost:8888/';
} else {
	domain = '23.239.11.140';
	base_url = 'http://23.239.11.140:8050/';
}

require.config({
	"baseUrl": base_url,	
  	paths: {
    	jquery: "//code.jquery.com/jquery-1.10.1.min",
    	gapi: 'https://apis.google.com/js/client'
 	}
});

var docCookies = {
	get_item: function (cookie_key) {
    	return decodeURIComponent(
    		document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(
    			cookie_key
    		).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")
    	) || null;
  	},
  	set_item: function (cookie_key, value, end, path, domain, secure) {

    	if (!cookie_key || /^(?:expires|max\-age|path|domain|secure)$/i.test(cookie_key)) {
    		return false; 
    	}

    	var expires = "";

    	if (end) {
      		switch (end.constructor) {
        		case Number:
          			expires = end === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + end;
          			break;
        		case String:
          			expires = "; expires=" + end;
          			break;
        		case Date:
          			expires = "; expires=" + end.toUTCString();
          			break;
      		}
    	}
    	document.cookie = encodeURIComponent(
    		cookie_key
    	) + "=" + encodeURIComponent(
    		value
    	) + expires + (
    		domain ? "; domain=" + domain : ""
    	) + (
    		path ? "; path=" + path : ""
    	) + (
    		secure ? "; secure" : ""
    	);
    	return true;
  	},
  	remove_item: function (cookie_key, path, domain) {
    	if (!cookie_key || !this.has_item(cookie_key)) {
    		return false; 
    	}
    	document.cookie = encodeURIComponent(
    		cookie_key
    	) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + (
    		domain ? "; domain=" + domain : ""
    	) + ( 
    		path ? "; path=" + path : ""
    	);
    	return true;
  	},
  	has_item: function (cookie_key) {
    	return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(
    		cookie_key
    	).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
  	},
  	keys: function () {
    	var keys = document.cookie.replace(
    		/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, ""
    	).split(/\s*(?:\=[^;]*)?;\s*/);

    	for (var nindex = 0; nindex < keys.length; nindex++) {
    		keys[nindex] = decodeURIComponent(keys[nindex]); 
    	}
    	return keys;
  	}
};

var JQAjax = (function() {
	var xdr;
	var success_func = '';
	var is_IE = window.XDomainRequest ? true : false;

	var invocation = function() {
		var request;

		if (is_IE) {
			request = new XDomainRequest();
		} else {
			request = new XMLHttpRequest();
		}
		return request;
	};

	var output_result = function() {
		return;
	};

	var handler = function () {
		if (xdr.readyState === 4) {
			if (xdr.status === 200) {
				if (success_func !== '') {
					success_func(JSON.parse(xdr.responseText));
					success_func = '';
				} else {
					output_result();	
				}
			}
		}
	};

	var ajax = function(options) {
		var url;
		var options = options || {};
		var data = options['data'] || '';
		var callback = options['callback'];
		xdr = invocation();

		if (callback && options['method'] == 'GET') {
			data = "callback=" + callback + '&' + data
		}

		if (options['method'] == 'GET' && data) {
			url = options['url'] + '?' + data + "&rand="+Math.random()+Date.parse(Date());
		} else {
			url = options['url'];
		}

		if (options['success']) {
			success_func = options['success'];
		}

		if(xdr) {
			xdr.onreadystatechange = handler;
			xdr.open(options['method'], url, true);

			if (options['method'] == 'GET'){
				xdr.send();	
			} else if (options['method'] == 'POST') {
				xdr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
				xdr.send(data);
			} else {
				return false;
			}
		}
	};

	return {
		'ajax': ajax
	};
})();

require(['jquery', 'gapi'] , function($) {
	var AdFits = (function($) {
		var required_css = [
			'http://fonts.googleapis.com/css?family=Open+Sans:400,600,700',
			base_url + 'static/css/style.css?v=' + Math.random()
		];

		var required_js = [
			base_url + 'static/js/flatui-radio.js?v=' + Math.random(),
			base_url + 'static/js/flatui-checkbox.js?v=' + Math.random()
		]

		var sponsor_logo;
		var publisher_logo;
		var campaign_img;
		var adfits_logo;
		var coupons_left;
		var money_box_position;
		var radio_pattern;
		var mboxcolor;
		var adftoken;
		var adfdy;
		var days_left;
		var message_class;
		var dollars_rewarded;
		var show_modal;
		var publisher_name;
		var sponsor_name;
		var landing_url;

		var load_css = function(url) {
	    	var link = document.createElement("link");
	    	link.type = "text/css";
	    	link.rel = "stylesheet";
	    	link.href = url;
	    	document.getElementById("ad-adfits").appendChild(link);
		}

		var load_script = function(script_url) {
			var script = document.createElement('script')
			script.type = "text/javascript";
			script.src = script_url
			document.getElementById("ad-adfits").appendChild(script);
		}

		var get_campaign_data = function(campaign_url) {
			var data_string = 'wid=' + adwidget + '&ref_url=' + window.location.origin;

			if (docCookies.get_item('adftoken')) {
				data_string += '&adftoken=' + docCookies.get_item('adftoken');
			}

			JQAjax.ajax({
				'url': campaign_url + 'getContent/',
				'method': 'GET',
				'data': data_string,
				'success': function (response) {
					if (response['status']) {
						sponsor_logo = response['sponsor_logo'];
						publisher_logo = response['publisher_logo'];
						campaign_img = response['campaign_img'];
						adfits_logo = response['adfits_logo'];
						coupons_left = response['coupons_left'];
						money_box_position = response['money_box_position'];
						radio_pattern = response['radio_pattern'];
						mboxcolor = response['money_box_color'];
						message_class = response['message_class'];
						dollars_rewarded = response['dollars_rewarded'],
						adftoken = response['adftoken'];
						adfday = response['adfdy'];
						docCookies.set_item('adftoken', adftoken);
						docCookies.set_item('adfday', adfday);
						days_left = 5 - parseInt(adfday);
						publisher_name = response['publisher_name'];
						sponsor_name = response['sponsor_name'];
						landing_url = response['landing_url'] || '#';
						load_ad();
					}
				}
			});
		};

		var social_share = function () {
			var adf_share_url = window.location.href;
		    var request = gapi.client.urlshortener.url.insert({
		        'resource': { 'longUrl': adf_share_url }
		    });

		    request.execute(function(response) {
		        
		        if(response.id != null) {
		            make_shorten_url(response.id)
		        } else {
		            make_shorten_url(adf_share_url)
		        }
		    });
		};

		var make_shorten_url = function(adf_share_url) {
			var adf_share_text = 'I earned it! Showing some love to @' + publisher_name + ' for the @' + sponsor_name + ' reward via '

			window.open(
				"https://twitter.com/intent/tweet?url=" + adf_share_url + "&text="+ adf_share_text, 
				"_blank"
			);

			var data_string = 'wid=' + adwidget + '&ref_url=' + window.location.origin + '&social_type="twitter"';

			if (docCookies.get_item('adftoken')) {
				data_string += '&adftoken=' + docCookies.get_item('adftoken');
			}

			JQAjax.ajax({
				'url': base_url + 'socalShare/',
				'method': 'POST',
				'data': data_string,
			});
		};
		
		var load_modal = function() {
			var API_KEY = 'AIzaSyDJ2mmEIfwXGgznXvbNJBdElu2x_d4D520';
		    gapi.client.setApiKey(API_KEY);
		    gapi.client.load('urlshortener', 'v1');

			$("#adfits-app").remove();			
			$("body").append('<div id="adfits-app" ></div>');
			$("#adfits-app").append("<div class='static-modal-backdrop overlay' id='adfits-modal'></div>");
			$("#adfits-modal").append("<div class='modal'></div>");
			$('.modal').append('<div class="modal-dialog adf-modaldialog" id="modal-dialog"></div>');
			$('#modal-dialog').append('<button type="button" class="close fui-cross adf-close"' +
				'data-dismiss="modal" aria-hidden="true" id="adf-btn-close"></button>');
			$('#modal-dialog').append('<div class="modal-content adf-modalbox" id="modalbox"></div>');
			$('#modalbox').append('<div class="modal-header adf-header" id="modal-header"></div>');
			$('#modal-header').append('<div class="adf-logos" id="logo-holder"></div>');
			$('#logo-holder').append('<a href=' + window.location.origin + ' target="_blank" title="' + publisher_name + '">'+
				'<div class="adf-hostlogo"></div></a><adf-h4 class="and-height">&amp;</adf-h4>'+
				'<a href="" title="Visit Sponsors Website" target="_blank">'+
				'<div class="adf-sponsorlogo"></div></a>');
			$(".adf-sponsorlogo").css('background-image', 'url('+ sponsor_logo +')');
			$(".adf-hostlogo").css('background-image', 'url('+ publisher_logo +')');
			$('#modal-header').append('<div id="form-info" class="adf-modaltitle title1 ">'+
				'<b class="adf-color">Fill out</b> the form to claim your reward!</div>');
			$('#modal-header').append('<div id="congrats" class="adf-modaltitle title2 adf-hidden">'+
				'<center><b class="adf-color">Congratulations!</b></center></div>');
			$('#modal-header').append('<div class="adf-progress"><div class="adf-dayC"></div></div>');
			$('#modalbox').append('<div class="adf-bottom"></div>');
			$('#modalbox').append('<div class="modal-body adf-mainback"></div>');
			$(".adf-mainback").css('background-image', 'url('+ campaign_img +')');
			$('.adf-mainback').append('<div class="adf-piccover"></div>');
			$('.adf-piccover').append('<div class="adf-main"></div>');
			$('.adf-main').append('<div class="adf-inputs adf-modal1 " id="adf-modal1"></div>');
			$('#adf-modal1').append('<div class="form-group" id="adf-form">');
			$('#adf-form').append('<div id="email-div" class="form-group"><input type="text" value="" id="adf-email" placeholder="Email" class="form-control input-sm"></div>');
			$('#adf-form').append('<div id="fname-div" class="form-group"><input type="text" value="" id="adf-fname" placeholder="First Name" class="form-control input-sm"></div>');
			$('#adf-form').append('<div id="lname-div" class="form-group"><input type="text" value="" id="adf-lname" placeholder="Last Name" class="form-control input-sm"></div>');
			$('#adf-form').append('<div id="loc-div" class="form-group"><input id="adf-location" type="text" value="" placeholder="Location" class="form-control input-sm"></div>');
			$('#adf-form').append('<div id="age-div" class="form-group"><input id="adf-age"  type="text" placeholder="Age" class="form-control input-sm"></div><br>');
			$('#adf-form').append('<label class="radio adf-color"><input type="radio" name="optionsRadios" id="gendermale" value="male" data-toggle="radio" checked="">Male</label>');
			$('#adf-form').append('<label class="radio adf-color"><input type="radio" name="optionsRadios" id="genderfemale" value="female" data-toggle="radio" checked="">Female</label>');
			$('[data-toggle="radio"]').radio();
			$('#adf-form').append('<div id="checkbox_notify"><label class="checkbox " for="checkbox5"><input type="checkbox" value="" id="checkbox5" data-toggle="checkbox">Notify me of future rewards</label></div>');
			$('#adf-form').append('<div id="checkbox_agree"><label class="checkbox " for="checkbox6"><input type="checkbox" value="" id="checkbox6" data-toggle="checkbox">I Accept the <a href="http://webstarresearch.com/adfits/terms.html" target="_blank" Title="Read the Terms and Aggreements">Terms and Agreements</a></label></div>');
			$('[data-toggle="checkbox"]').checkbox();
			$('#adf-modal1').append('<adf-h5 class="error-message adf-hidden" id="errormessage"><b class="adf-alert">Error:</b> Form not filled out properly, please try again.</adf-h5>');
			$('#adf-modal1').append('<button id="btn-redeem1" class="btn btn-block btn-embossed btn-default ">Redeem</button>');
			$('.adf-main').append('<div class="adf-modal2 adf-hidden"><adf-h3>Superb!</adf-h3><p>Your reward card will be sent to your email address!</p><adf-h5>In the meantime, tweet some love with your friends.</adf-h5></div>');
			$('.adf-modal2').append('<a id="btn-twitter" href="#" class="btn btn-default btn-sm btn-emebossed btn-social-twitter"><span class="fui-twitter"></span>Connect with Twitter</a>');
			$('#modalbox').append('<div class="adf-footer" id="footer-main"></div>');
			$('#footer-main').append('<a class="adf-footerlink" href="http://webstarresearch.com/adfits/home.html" title="Visit AdFits" target="_blank"></a>');
			$('#footer-main').append('<div class="adf-footerinfo"><adf-h6><a href="http://webstarresearch.com/adfits/faq.html" target="_blank" title="More Info">?</a></adf-h6></div>');
			
			$('#btn-redeem1').bind('click', function() {
				save_coupon();
			});
		
			$("#btn-twitter").bind('click', social_share);
			$('#adf-btn-close').on('click',function(){
				$("#adfits-app").remove();
				load_ad();
				toggle_checkbox();
			});
			$('#adf-email, #adf-location, #adf-age, #checkbox_agree, #adf-fname').bind('change', function() {
				enable_btn();
			});
			
		};
		
		var load_ad = function() {
			
			for (var pos in required_css) {
				load_css(required_css[pos]);
			}

			for (var pos in required_js) {
				load_script(required_js[pos]);
			}
				
			$("#ad-adfits").append("<div id='adfits-app'></div>");
			$("#adfits-app").append('<div id="adf-base-div" class="static-modal-backdrop static-widget-backdrop"></div>');
			$("#adf-base-div").append('<div class="modal" id="adf-modal"></div>');
			$("#adf-modal").append('<div class="modal-dialog adf-widgetdialog" id="adf-dialog"></div>');
			$("#adf-dialog").append('<div class="modal-content adf-modalbox" id="adf-body"></div>');
			$("#adf-body").append('<div class="adf-blackbox"></div>');
			$(".adf-blackbox ").hide();
			$("#adf-body").append('<div class="adf-top"></div>');
			$("#adf-body").append('<div class="modal-header adf-header" id="adf-header-top"></div>');
			$("#adf-header-top").append('<div class="adf-logos"></div>');
			$(".adf-logos").append('<a href=' + window.location.origin + ' target="_blank" title="' + publisher_name + '"><div class="adf-hostlogo"></div></a>');
			$(".adf-hostlogo").css('background-image', 'url('+ publisher_logo +')');
			$(".adf-logos").append('<adf-h4 class="height">&amp;</adf-h4>');
			$(".adf-logos").append('<a href="'+ landing_url +'" title="Visit Sponsor\'s Website"'+ 
				'target="_blank"><div class="adf-sponsorlogo"></div></a>');
			$(".adf-sponsorlogo").css('background-image', 'url('+ sponsor_logo +')');
			$("#adf-header-top").append('<div class="adf-progress"></div>');
			
			//progress bar
			$(".adf-progress").append('<div class="adf-day1 "><div class="adf-circle"><div id="tcircle"></div></div></div>');
			$(".adf-progress").append('<div class="adf-day2 "><div class="adf-bar"></div><div class="adf-circle"><div id="tcircle"></div></div></div>');
			$(".adf-progress").append('<div class="adf-day3 "><div class="adf-bar"></div><div class="adf-circle"><div id="tcircle"></div></div></div>');
			$(".adf-progress").append('<div class="adf-day4"><div class="adf-bar"></div><div class="adf-circle"><div id="tcircle"></div></div></div>');
			$(".adf-progress").append('<div class="adf-day5"><div class="adf-bar"></div><div class="adf-gift"></div></div>');
			
			$("#adf-header-top").append('<div class="adf-mboxwrapper"></div>');
			$(".adf-mboxwrapper").append('<div class="mbox-arrow"></div>');
			$(".adf-mboxwrapper").append('<div class="adf-mbox"></div>');
			$(".adf-mbox").append('<div class="collect"><adf-h5>Collect<br>your new<br><b>Dollar</b></adf-h5></div>');
			$(".adf-mbox").append('<div class="mbox-total adf-bcolor"><adf-h4><span>$</span>' + adfday + '</adf-h4></div>');
			$("#adf-body").append('<div class="modal-body adf-mainback"></div>');
			$(".adf-mainback").css('background-image', 'url('+ campaign_img +')');
			$("#adf-dialog").append('<div class="adf-footer"></div>');
			$(".adf-footer").append('<a class="adf-footerlink" href="http://webstarresearch.com/adfits/home.html" title="Visit AD fits" target="_blank"></a>');
			$(".adf-footer").append('<div class="adf-footerinfo"></div>');
			$(".adf-footerinfo").append('<adf-h6 class="card-color"><bold class="adf-color" id="adf-coupon-left">' + coupons_left + '</bold> cards left <a href="http://webstarresearch.com/adfits/faq.html" title="More Info" target="_blank"> ?</a></adf-h6>');
			$(".adf-mainback").append('<div class="adf-piccover"></div>');
			$(".adf-piccover").append('<div class="adf-main"></div>');
			$(".adf-main").append('<div class="main1">' +		
				'<div class="anime-text"><adf-h3>$' + dollars_rewarded + '</adf-h3><p class="inblock p-height"><b>&nbsp  to Give Away</b></p></div>'+
				'<p><b>Earn $1</b> for every consecutive daily visit of ' + publisher_name +
				'</p></div>');
			$(".adf-main").append('<div class="main2">' + 
				'<p>Keep adding money to your gift card by visiting <b>' + publisher_name +
				' </b><br> every day for the next <b>' + days_left + ' days</b>!' +
			    '</p></div>');
			$(".adf-main").append('<div class="main3">' +
				'<div class="adf-message adf-hidden"><adf-h5>' +
				'Your email has been successfuly registered.</adf-h5></div>' +
				'<adf-h3>' + days_left + ' days left</adf-h3>' +
				'<p>to Redeem your Reward</p>' + 
				'<adf-h5>Send me a daily reminder</adf-h5>' +
		  		'<div class="form-group">' +
			  		'<div id="notifier-div" class="input-group input-group">' +
				        '<input class="form-control input-sm" id="adf-reminderemail" type="text" placeholder="Email">' +
				            '<span class="input-group-btn">' +
				            	'<button class="btn btn-default adf-btn" id="reminder" type="button"><span class="fui-arrow-right pull-right"></span></button>' +
							'</span>' +
						'</div>'+
					'</div>' +  
				'</div>');
			$(".adf-main").append('<div class="main4">' +
				'<adf-h1><span>$</span>' + adfday + ' </adf-h1>' +
				'</div>');
			$(".adf-main").append('<div class="main5">' +
				'<adf-h3>COMPLETED!</adf-h3>' +
				'<p>Well Done!</p>' +
				'<button id="btn-redeem" class="btn btn-block btn-embossed btn-primary">Redeem $5</button> ' +
				'</div>');		
			$(".adf-main").append('<div class="main6">' +
				'<div class="adf-message adf-hidden"><adf-h5>' +
				'Your email has been successfuly registered.</adf-h5></div>' +
				'<adf-h3>Thank You for <br />Partcipating</adf-h3><br>' + 
				'<adf-h5>Notify me for future rewards.</adf-h5>' +
					'<div class="form-group">' +
						'<div id="cam-notify-div" class="input-group input-group">' +
				        '<input class="form-control input-sm" id="adf-reminderemail1" type="text" placeholder="Email">' +
				            '<span class="input-group-btn">' +
				            	'<button class="btn btn-default adf-btn" id="remind-campaign" type="button"><span class="adf-arrowsize fui-arrow-right pull-right"></span></button>' +
							'</span>' +
						'</div>'+
					'</div>' +  
				'</div>');
			$(".adf-main").append('<div class="main7">' +
				'<div class="adf-message adf-hidden"><adf-h5>' +
				'Your email has been successfuly registered.</adf-h5></div>' +
				'<adf-h3>Rewards Closed </adf-h3>' + 
				'<adf-h5>Notify me for future rewards.</adf-h5>' +
					'<div class="form-group">' +
						'<div id="cam-close-notify" class="input-group input-group">' +
				        '<input class="form-control input-sm" id="adf-reminderemail2" type="text" placeholder="Email">' +
				            '<span class="input-group-btn">' +
				            	'<button class="btn btn-default adf-btn" id="remind-campaign-close" type="button"><span class="adf-arrowsize fui-arrow-right pull-right"></span></button>' +
							'</span>' +
						'</div>'+
					'</div>' +  
				'</div>');	
			$('#btn-redeem').css({"background": mboxcolor, "color": "rgb(231, 231, 241)"});
			$('.adf-btn').css({"background": mboxcolor, "color": "rgb(231, 231, 241)"});
			assign_events();
		};

		var assign_events = function() {
			$(".adf-modalbox").unbind("mouseenter mouseleave");
			$("." + message_class).css('display', 'block');
			$(".adf-mboxwrapper").addClass(money_box_position);
			$(".adf-bcolor").css("background", mboxcolor);
			$("#adf-coupon-left").css("color", mboxcolor);
			$(".card-color").css("color", "#34495E");
			$('#reminder').bind('click', notify_coupon);
			$('#remind-campaign').bind('click', notify_campaign);
			$('#remind-campaign-close').bind('click', notify_campaign_close);
			$('#adf-reminderemail').bind('keyup', function () {
				change_color('#adf-reminderemail', "#reminder");
			});
			$('#adf-reminderemail1').bind('keyup', function () {
				change_color('#adf-reminderemail1', "#remind-campaign");
			});
			$('#adf-reminderemail2').bind('keyup', function () {
				change_color('#adf-reminderemail2', "#remind-campaign-close");
			});
			
			for(var pos in radio_pattern) {
		 		if (radio_pattern[pos] !== '' && radio_pattern[pos] == 'active') {
		 			var radio_pos = pos;
		 			$("." + radio_pos).addClass(radio_pattern[radio_pos]);
		 			//$('.'+radio_pos).next().append('<div id="tcircle"></div>');
		 			$("#ad-adfits").css("cursor", "pointer");
		 			$("#ad-adfits").bind('click', function() {
		 				get_dollars("." + radio_pos);
		 			});
		 		} else if (radio_pattern[pos] !== '') {
					$("." + pos).addClass(radio_pattern[pos]);			 			
		 		}
		 	}
		 	$("#adfits-app .received .adf-circle").css("background", mboxcolor);
		 	$("#adfits-app .received .adf-bar").css("background", mboxcolor);

		 	if(message_class == "main1") {
				$(".adf-modalbox").hover(function() {  
					$(".adf-main").fadeOut("slow", "swing", function(){
						$(".adf-blackbox").fadeIn("slow", "swing", function() {
							$(".adf-mbox .collect").slideDown("fast", "swing");
						});	 		
					});
			   	}, function(){  
			  		$(".adf-mbox .collect").slideUp("fast", "swing", function () {
				 	 	$(".adf-blackbox").fadeOut("slow", "swing", function(){
				 	 		$(".adf-main").fadeIn("slow", "swing");	
				 	 	});
				  	});
			 	});
			} else if(message_class == "main5" || message_class == "main6") {
				$("#ad-adfits").unbind('click');
				$("#ad-adfits").css('cursor', '');
				$(".adf-mboxwrapper").addClass('adf-mboxwrapper-day5');
				$("#btn-redeem").bind("click", load_modal);
			} else if(message_class == "main7") {
				$(".adf-mboxwrapper").addClass('adf-mboxwrapper-day5');
			} else {
				$(".adf-mboxwrapper").addClass('adf-mboxwrapper-day5');
				message_toggle();
			}
		};

		var sleep = function (milliseconds) {
			var start = new Date().getTime();
			for (var i = 0; i < 1e7; i++) {
				if ((new Date().getTime() - start) > milliseconds){
					break;
				}
			}
		};

		var get_dollars = function(active_id) {
			$("#ad-adfits").unbind('click');
			$("#ad-adfits").css('cursor', '');
			$(active_id).removeClass('active').addClass('received');
			$(".adf-mboxwrapper").addClass('adf-mboxwrapper-day5');
			$(".adf-modalbox").unbind("mouseenter mouseleave");
			$("#adfits-app .received .adf-circle").css("background", mboxcolor);
			$("#adfits-app .received .adf-bar").css("background", mboxcolor);
			$(".main1").hide();

			var data_string = 'wid=' + adwidget + '&ref_url=' + window.location.origin;

			if (docCookies.get_item('adftoken')) {
				data_string += '&adftoken=' + docCookies.get_item('adftoken');
			}

			JQAjax.ajax({
				'url': base_url + 'saveDollar/',
				'method': 'POST',
				'data': data_string,
				'success': function (response) {
				  	$(".adf-main").css({'top': '90%'});
				 	$(".main2").show();
					$(".adf-main").stop().animate(
						{ "opacity": "show", top:"50"} , "5" 
					).delay(4000).animate( 
						{ "opacity": "hide", top:"200"} , "5",
					function() {
					 	$(".main2").hide();
					 	$(".main3").show();	
					 	$(".adf-main").animate( 
					 		{ "opacity": "show", top:"40"} , "5",
					 	function() {
					 		if (!$(".adf-modalbox").is("div:hover")) {
					 			sleep(4000);
					 			$(".adf-main").stop().animate(
					 				{ "opacity": "hide", top:"210"} , "5", 
					 			function() {
					 				$(".adf-blackbox").fadeToggle("slow", "swing");
						 			$(".main3").hide();
							 		$(".main4").show();
							 		$(".adf-main").stop().animate(
							 			{ "opacity": "show", top:"50"} , "5",
							 	function () {
							 			message_toggle();
							 		});
					 			});
						 	} else {
						 		message_toggle();
						 	}
						});
			   		});
				}
			});
		};

		var message_toggle = function() {
			$(".adf-modalbox").unbind("mouseenter mouseleave"); 
			$(".adf-modalbox").hover(function() {
				$(".adf-blackbox").fadeIn("slow", "swing");
				$(".adf-main").stop().animate({ "opacity": "hide", top:"210"} , "5", function() {
		 			$(".main3").show();
			 		$(".main4").hide();	
			 		$(".adf-main").stop().animate({ "opacity": "show", top:"50"} , "5");	
				});
			}, function() {
				$(".adf-main").stop().animate({ "opacity": "hide", top:"210"} , "5", function() {
					$(".adf-blackbox").fadeOut("slow", "swing");
	 				$(".main3").hide();
		 			$(".main4").show();	
		 			$(".adf-main").stop().animate({ "opacity": "show", top:"50"} , "5");	
				});
			}); 
		}

		var validate_fields = function(){
			var valid = true;			
			errorMessage = "";
			var data_string;
				
			agree = $('#checkbox_agree input[type="checkbox"]:checked').val();
				if (agree==""){
					agreed = true;
					valid =true;
					$("#checkbox_agree").removeClass('has-error');
				}
				else {
						agreed = false; 
						valid = false;
						$("#checkbox_agree").addClass('has-error');
					}  //agree check
				
				if ($.trim($('#adf-location').val()) == '') {
					errorMessage  = "Please enter Location \n";
					$("#loc-div").addClass('has-error');
					$('#location').attr('placeholder',errorMessage);
					valid = false;
				}
				else {
					var nameReg = /^([a-zA-Z]+(?:\.)?(?: [a-zA-Z]+(?:\.)?)*)$/;
					if (!validateName($('#adf-location').val())) {
						errorMessage = "Enter a valid Location\n";
						$("#loc-div").addClass('has-error');
						$('#location').attr('placeholder',errorMessage);
						valid = false;
					}					 
					else {   
						$("#loc-div").removeClass('has-error');
					}
				}  //location check
				
				var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;  
				if ($.trim($("#adf-email").val())==""){
					errorMessage = "Please enter Email address.\n";
					$("#email-div").addClass('has-error');
					$('#email').empty();
					$('#email').attr('placeholder',errorMessage);
					valid = false;
				}
				else {
					if (!validateEmail($('#adf-email').val())) {
						errorMessage = "Enter a valid email\n";
						$("#email-div").addClass('has-error');
						$('#email').attr('placeholder',errorMessage);
						valid = false;
					}
					else {
						$("#email-div").removeClass('has-error');
					}
				}  //email check
				
				var agereg = /^[0-9]{2}$/;
				if($.trim($('#adf-age').val()) == '') {
					errorMessage = "Enter Age!!!"
					$("#age-div").addClass('has-error');
					$('#age').attr('placeholder',errorMessage);
					valid = false;
				}
				else {
					if (!validateAge($('#adf-age').val())) {
						errorMessage = "Enter a valid age\n";
						$("#age-div").addClass('has-error');
						$('#age').attr('placeholder',errorMessage);
						valid = false;
					}
					else {
						$("#age-div").removeClass('has-error');
					}
				}  //age check					
				
				if(($('#adf-fname').val()) == '') {
					$("#fname-div").addClass('has-error');
					valid = false;
				} 
				else {
					$("#age-div").removeClass('has-error');
				}//name check					
		
			function validateAge(age){
				var reg = /^[0-9]{2}$/;
				if(!reg.test(age)){
					return false;
				}
				return true;
			}
			
			function validateEmail(emailaddress){  
			   var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;  
			   if(!emailReg.test(emailaddress)) {  
					return false;
			   }       
			   return true;
			}

			function validateName(name){  
			   var nameReg = /^([a-zA-Z]+(?:\.)?(?: [a-zA-Z]+(?:\.)?)*)$/;  

			   if(!nameReg.test(name)) {  
					return false;
			   }       
			   return true;
			}
		return valid;
		
		};
		
		var save_coupon = function() {
			
			var valid = false;
			valid = validate_fields();
			if (valid) { 
				$("#errormessage").addClass('adf-hidden');
				var notify_me;
				var email = ($('#adf-email').val());
				var loc = ($('#adf-location').val());
				var fname = ($('#adf-fname').val());
				var lname = ($('#adf-lname').val());
				var age = ($('#adf-age').val());
				var sex = $('#adf-form input[type="radio"]:checked').val();
				var notify = $('#checkbox_notify input[type="checkbox"]:checked').val();
				var data_string = "email="+email+"&location="+loc+"&fname="+fname+"&lname="+lname+"&age="+age+"&sex="+sex+"&notify_me="+notify_me+"&agreed=true";

				data_string += '&wid='+adwidget+'&ref_url='+window.location.origin;
				if (docCookies.get_item('adftoken')) {
					data_string += '&adftoken=' + docCookies.get_item('adftoken');
				} else {
					//error
				}

				if (notify == "" ) {
					notify_me = true;
				} else {
					notify_me = false;
				}
				
				JQAjax.ajax({
					'url': base_url + 'saveRedeemed/',
					'method': 'POST',
					'data': data_string,
					'success': function(response) {
						if (response['status']) {
							sponsor_logo = response['sponsor_logo'];
							publisher_logo = response['publisher_logo'];
							campaign_img = response['campaign_img'];
							adfits_logo = response['adfits_logo'];
							coupons_left = response['coupons_left'];
							money_box_position = response['money_box_position'];
							radio_pattern = response['radio_pattern'];
							mboxcolor = response['money_box_color'];
							message_class = response['message_class'];
							dollars_rewarded = response['dollars_rewarded'],
							adftoken = response['adftoken'];
							adfday = response['adfdy'];
							docCookies.set_item('adftoken', adftoken);
							docCookies.set_item('adfday', adfday);
							days_left = 5 - parseInt(adfday);
							$("#adf-modal1").hide();
							$("#form-info").addClass("adf-hidden");
							$(".adf-modal2").removeClass("adf-hidden");
							$("#congrats").removeClass("adf-hidden");
							$("#adf-coupon-left").text(coupons_left);
						}
					}
				});
			}
			else {
				$("#errormessage").removeClass('adf-hidden');
			}
		};	
		
		var save_notify = function(text_id, notify_type) {
			var email = ($('#' + text_id).val());
			var valid = email_check(email);

			if (email != '' && valid) {
				
				var day = docCookies.get_item('adfday');
				var token = docCookies.get_item('adftoken');
				var data_string = 'wid='+adwidget+'&ref_url='+window.location.origin;
				data_string += '&adftoken='+token+'&adfdy='+day;
				data_string += '&email='+email+'&notify_type='+notify_type;
	
				JQAjax.ajax({
					'url': base_url + 'notifyMe/',
					'method': 'POST',
					'data': data_string,
				});
				$('.adf-message').removeClass('adf-hidden');
				$('#adf-reminderemail1').val('');
                $('#adf-reminderemail1').attr('placeholder', 'Email.');
                
			} else {
				$('#'+ id).val('');
				$('#'+ id).attr('placeholder', 'Enter a valid email.');
			}
		};

		var notify_coupon = function() {
			save_notify("adf-reminderemail", "coupon");
		};

		var notify_campaign = function() {
			save_notify("adf-reminderemail1", "campaign");
		};

		var notify_campaign_close = function() {
			save_notify("adf-reminderemail2", "campaign");
		};

		var email_check = function(email){  
			var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;  
			
			if(!emailReg.test(email)) {  
				return false;
			}       
		    
		    return true;
		}
		
		var change_color = function(input_id, btn_id) {
			if ($.trim($(input_id).val()) == '') {
				$(btn_id).css({"background": "", "color": ""});
			} else {
				$(btn_id).css({
					"background": mboxcolor, 
					"color": "rgb(231, 231, 241)"
				});
			}
		}
		
		var toggle_checkbox = function() {
		    $('body').on('click.checkbox.data-api', '[data-toggle^=checkbox], .checkbox', function (e) {
			var $checkbox = $(e.target);
			e && e.preventDefault() && e.stopPropagation();

			if (!$checkbox.hasClass('checkbox')) {
			    $checkbox = $checkbox.closest('.checkbox');
			}
			$checkbox.find(':checkbox').checkbox('toggle');
		    });
		}
				
		var enable_btn = function(valid) {
			var agree = $('#checkbox_agree input[type="checkbox"]:checked').val();
			if (($("#adf-email").val() != "") && ($('#adf-location').val() != '') 
				&& ($('#adf-age').val() != '') && (agree == '')){
				$('#btn-redeem1').css({
					"background": mboxcolor,
					 "color": "rgb(231, 231, 241)"
				});
			} else {
				$('#btn-redeem1').css({"background": "", "color": ""});
			}
		}
		return {
			'get_campaign_data': get_campaign_data,
		};
	})($, JQAjax);
	AdFits.get_campaign_data(base_url);
});


