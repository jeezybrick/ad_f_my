(function($){   
    $(function(){
    	update_website();
        $("#id_publisher").bind('change', update_website);
	});  

    var update_website = function() {
		$.ajax({
			url: '/campaign/get-websites/',
			type: "GET",
			dataType: 'json',
			data: {
				'cid': window.location.pathname.split('/')[4],
				'pid': $("#id_publisher").val()
			},
			success: function(response) {
				$("#id_website option").remove();
				$("#id_website").append('<option value="">----</option>');
				$.each(response['website_list'], function( index, value ) {
				  	
					if (value[2]) {
						$("#id_website").append(
							'<option value="'+ value[0] +'" selected=selected>' + value[1] + '</option>');
					} else {
						$("#id_website").append(
							'<option value="'+ value[0] +'">' + value[1] + '</option>');
					}
				});
			}
		});
	};

})(django.jQuery);


