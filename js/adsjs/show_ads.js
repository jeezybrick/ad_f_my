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

var CountDown = function(){
	
	var id;
	var targetdate;
	var coupons;
	var current_time = new Date();
	var target_date;
	var timesup = false;
	 	 
	var update_time = function (current_time, target_date){
		current_time.setSeconds(current_time.getSeconds()+1)
		setTimeout(function(){update_time(current_time, target_date);}, 1000) 							//update time every second
	};
	
	var display_countdown = function(baseunit, functionref, id, target_date, current_time, coupons){
		var baseunit = baseunit
		var format_results = functionref
		show_results(target_date, current_time, baseunit, id, coupons);
	};
	
	var show_results = function(target_date, current_time, baseunit, id, coupons) {
		var container = document.getElementById(id)
		var timediff = (target_date - current_time)/1000 												//difference btw target date and current date, in seconds
		if (timediff < 0){								 												//if time is up
			timesup = true
			container.innerHTML = format_results();
			return
		}

		var one_minute = 60 																			//minute unit in seconds
		var one_hour = 60 * 60 																			//hour unit in seconds
		var one_day = 60 * 60 * 24 																		//day unit in seconds
		var dayfield = Math.floor(timediff / one_day)
		var hourfield = Math.floor((timediff - dayfield * one_day) / one_hour)
		var minutefield = Math.floor((timediff - dayfield * one_day - hourfield * one_hour) / one_minute)
		var secondfield = Math.floor((timediff - dayfield * one_day - hourfield * one_hour - minutefield * one_minute))

		if (baseunit == "hours"){ 																		//if base unit is hours, set "hourfield" to be topmost level
			hourfield = dayfield * 24 + hourfield
			dayfield = "n/a"
		} else if (baseunit == "minutes"){ 																//if base unit is minutes, set "minutefield" to be topmost level
			minutefield = dayfield * 24 * 60 + hourfield * 60 + minutefield
			dayfield = hourfield = "n/a"
		} else if (baseunit == "seconds"){ 																//if base unit is seconds, set "secondfield" to be topmost level
			var secondfield = timediff
			dayfield = hourfield = minutefield = "n/a"
		}	
	
		container.innerHTML = format_results(dayfield, hourfield, minutefield, secondfield, coupons)
		setTimeout(function(){
		show_results(target_date, current_time, baseunit, id, coupons);}, 1000) 						//update results every second
	};
		
	var format_results = function() {
	
		if (timesup == false) {																			//if target date/time not yet met
			var displaystring = "Collect & Redeem this Gift in " + 
				arguments[0]+" days "+arguments[1]+" hours "+arguments[2]
				+" minutes "+arguments[3]+
				" seconds! <br>Learn more:"+
				" <a href='http://www.AdFits.com' target='_blank'>www.AdFits.com</a> "+
				"| Does it Fit?  Only "+ arguments[4]+" coupons available..."
		} else { 																						//else if target date/time met
			var displaystring = "Future date is here!"
		}
		return displaystring
	};
		
	return {
		set_data : function(_id , _targetdate, _coupons) {
			id = _id;
			coupons = _coupons;
			t_date = _targetdate.split(',')
			target_date = new Date(t_date[0],t_date[1]-1,t_date[2],t_date[3],t_date[4],t_date[5]);
			update_time(current_time, target_date);
			display_countdown("days", format_results, id, target_date, current_time, coupons);
		}	
	}
	
};


var adFits = (function() {
	var adfits_campaign_data;
	var adfits_redirect_url;
	var adfits_height;
	var adfits_width;
	var adfits_token;
	var adfits_day;
	var domain;
	
	var set_data = function (data) {
		if (docCookies.get_item('adftoken')) {
			if (docCookies.get_item('adftoken') !== data['adftoken']) {
				docCookies.set_item('adftoken', data['adftoken'], null, '/', domain);
			}
		} else if (data['adftoken'] !== '') {
			docCookies.set_item('adftoken', data['adftoken'], null, '/', domain);
		}

		docCookies.set_item('adfdy', data['adfdy'], null, '/', domain);
		adfits_day = parseInt(docCookies.get_item('adfdy'));
		adfits_campaign_data = data['response_data'];
		adfits_redirect_url = data['redirect_url'];
		adfits_height = parseInt(data['height']);
		adfits_width = parseInt(data['width']);
		adfits_end_date = data['end_date'];
		adfits_coupons_available = data['coupons_available'];
		load_ad();
	};

	var redirect = function() {
		window.open(
			adfits_redirect_url + '?wid=' + adwidget + '&ref_url=' + 
			window.location.hostname + '&adpart=' + this.alt + 
			'&adftoken=' + docCookies.get_item('adftoken'),
			'_blank'
		);
  		window.focus();
	};

	var load_ad = function () {
		var main_div_height = adfits_height + 30;
		var main_div_width = adfits_width + 3;
		var main_ad_div = document.getElementById("ad-adfits");
		main_ad_div.style.border = "1px solid black";
		main_ad_div.style.height = main_div_height + "px";
		main_ad_div.style.width = main_div_width + "px";
		main_ad_div.style.position = "relative";
		main_ad_div.onmouseover = handle_mouseover_in;
		main_ad_div.onmouseout = handle_mouseover_out;

		var ad_div = document.createElement('div');
		ad_div.id = 'ad-adfits-top';
		ad_div.style.position = "absolute";
		ad_div.style.height = "10px";
		ad_div.style.left = "2px";
		ad_div.style.textAlign = "left";
		ad_div.style.fontSize = "0.7em";
		ad_div.style.width = adfits_width;
		ad_div.innerHTML = "You have 5 visits remaining to redeem this Gift for FREE!"
		document.getElementById("ad-adfits").appendChild(ad_div);

		var ad_div = document.createElement('div');
		ad_div.id = 'ad-adfits-id';
		ad_div.style.position = "absolute";
		ad_div.className = 'ad-adfits-class';
		ad_div.style.top = "5px";
		ad_div.style.height = adfits_height + "px";
		ad_div.style.width = adfits_width + "px";
		document.getElementById("ad-adfits").appendChild(ad_div);

		for(var key in adfits_campaign_data) {
			var img_src = document.createElement('img');
			img_src.src = adfits_campaign_data[key]['img_src'];
			img_src.style.position = adfits_campaign_data[key]['position'];
			img_src.style.width = adfits_campaign_data[key]['width'];
			img_src.style.top = adfits_campaign_data[key]['top'];
			img_src.style.left = adfits_campaign_data[key]['left'];
			img_src.style.marginLeft = adfits_campaign_data[key]['margin-left'];
			img_src.alt = adfits_campaign_data[key]['name'];
			
			if (adfits_campaign_data[key]['height'] !== '') {
				img_src.style.height = adfits_campaign_data[key]['height'];
			}

			if (adfits_token !== '' && adfits_day !== '' && parseInt(key) + 1 <= adfits_day) {
				img_src.onclick = redirect;
				img_src.style.cursor = "pointer";
			} else if (key + 1 <= adfits_day && adfits_day == 1) {
				img_src.onclick = redirect;
				img_src.style.cursor = "pointer";
			} else if (adfits_campaign_data[key]['class'] !== '' 
				|| adfits_campaign_data[key]['class'] !== 'undefined') {
				img_src.className = adfits_campaign_data[key]['class'];
			}

			document.getElementById("ad-adfits-id").appendChild(img_src); 
		};

		var ad_div = document.createElement('div');
		ad_div.id = 'ad-adfits-down';
		ad_div.style.position = "absolute";
		ad_div.style.height = "10px";
		ad_div.style.top = adfits_height+"px";
		ad_div.style.left = "2px";
		ad_div.style.textAlign = "left";
		ad_div.style.fontSize = "0.6em";
		ad_div.style.width = adfits_width;
		ad_div.style.resize = "both";
		document.getElementById("ad-adfits").appendChild(ad_div);
		CountDown().set_data("ad-adfits-down", adfits_end_date, adfits_coupons_available);
	};	
	
	var handle_mouseover_in = function() {
			var next_day = document.getElementsByClassName("adfits-next-day");

			for(var i = 0; i < next_day.length; i++) {
    			next_day[i].style.opacity = "0.5";
				next_day[i].style.filter  = 'alpha(opacity=50)';
			}
	};

	var handle_mouseover_out = function() {
		var next_day = document.getElementsByClassName("adfits-next-day");

		for(var i = 0; i < next_day.length; i++) {
			next_day[i].style.opacity = "1";
			next_day[i].style.filter  = 'alpha(opacity=100)';
		}
	};

	return {
		init: function(data) {
			set_data(data);
		},

		get_ad_data: function(script_url) {
			var script = document.createElement('script')
			var query_url = 'callback=get_data&wid=' + adwidget + '&ref_url=' + window.location.hostname;

			if (docCookies.get_item('adftoken')) {
				var query_url = query_url + '&adftoken=' + docCookies.get_item('adftoken');
			}

			script.src = script_url + 'getContent/?' + query_url;
			document.body.appendChild(script);
		}
	}

})();

var debug = true;

if (debug) {
	domain = 'localhost';
	url = 'http://localhost:8888/';
} else {
	domain = '23.239.11.140';
	url = 'http://23.239.11.140:8050/';
}

function get_data(data) {
	adFits.init(data);
}

adFits.get_ad_data(url);
