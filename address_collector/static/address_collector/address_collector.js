var NBT = NBT || {};

$(function(){ 
	
	if(!NBT.addressCollector){
        NBT.addressCollector = {}
    }

    var controller = this;
    var $multiple = $("#multiple");
    controller.addresses = [];
    var bounds = new google.maps.LatLngBounds();

    var updateList = function(){
    	$multiple.empty();
    	$.each(controller.addresses, function(){
    		var address = this;
    		$("<li>")
			.html(address.address)
			.appendTo($multiple);
    	});
    	
    };

    var getAddresses = function(){
		$.ajax({
            type: "GET",
            cache: false,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: "/api/v1/addresses/",
            beforeSend: function(request){
            }
        }).always(function(){
            
        }).done(function(data){
            console.log(data);
            controller.addresses = data;
            updateList();
            updateMarkers();
        });
	};

	var saveAddress = function(data){
  		$.ajax({
            type: "POST",
            cache: false,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: "/api/v1/addresses/"
        }).done(function(response){
            console.log(response);
            controller.addresses.push(response);
        }).fail(function(response, error){
            console.log(response.status);
            console.log(response.responseText);
        });
  	};

  	var updateMarkers = function(){
  		markers = []
  		for (index in controller.addresses) {
  			address = controller.addresses[index]
  			var pos = new google.maps.LatLng(address.latitude, address.longitude);
  			bounds.extend(pos);
  			var marker = new google.maps.Marker({
				        position: pos,
				        map: controller.map
				    });
  			controller.map.fitBounds(bounds);
		}
  	};


  	var loadMap = function(){
  		var myLatlng = new google.maps.LatLng(30.3753, 69.3451);
		var myOptions = {
		}

	    var map = new google.maps.Map($("#my_map")[0], myOptions);
	    var geocoder = new google.maps.Geocoder();
	    controller.map = map;

	    google.maps.event.addListener(map, 'click', function(event) {
		    var latitude = event.latLng.lat();
		    var longitude = event.latLng.lng();
		    console.log(event);

		    var position = event.latLng

		    geocoder.geocode({
				'latLng': position
			}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					if (results[0]) {
						console.log(results)
						$("<li>")
						.html(results[0].formatted_address)
						.appendTo($multiple);

						var marker = new google.maps.Marker({
					        position: position,
					        map: map
					    });
					    map.panTo(position);

					    saveAddress({
					    	"address": results[0].formatted_address,
					    	"latitude": event.latLng.lat(),
					    	"longitude": event.latLng.lng()
					    });
					}
				}
			});
		});
  	};

  	loadMap();
	getAddresses();


	
	
	
    
    /*
	var $geocomplete = $('#geocomplete'),
		$multiple = $("#multiple");


	$geocomplete.geocomplete({
		map: "#my_map",
		location: "Pakistan",
		details: "form",
		mapOptions:{
			scrollwheel: true,
			zoomControl: false
		},
		markerOptions: {
			draggable: false
		}
	}).bind("geocode:click", function(event, result){
		//$geocomplete.geocomplete("find", result.lat()+","+result.lng());
		console.log(result);
		console.log(event);
		$geocomplete.geocomplete("find", result.lat()+","+result.lng());

	}).bind("geocode:result", function(event, result){
		//saveToDB(result);
		console.log(result)


		

    	console.log(result.geometry.location.lat(), result.geometry.location.lng());
    	var marker = new google.maps.Marker({
	        position: new google.maps.LatLng(result.geometry.location.lat(), result.geometry.location.lng()),
	        map: $geocomplete.geocomplete("map")
	    });

	    console.log(marker);
	    $("<li>")
		.html(result.formatted_address)
		.appendTo($multiple);

  	}).bind("geocode:error", function(event, result){
    	console.log(result);
  	}).bind("geocode:multiple", function(event, results){
        $.each(results, function(){
			var result = this;
			$("<li>")
			.html(result.formatted_address)
			.appendTo($multiple)
			.click(function(){
				$geocomplete.geocomplete("update", result)
			});
        });
    });
	
	*/
	
  	
});