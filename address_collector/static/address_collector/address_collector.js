var NBT = NBT || {};

$(function(){ 
	
	if(!NBT.addressCollector){
        NBT.addressCollector = {}
    }

    var controller = this;
    var $multiple = $("#multiple");
    controller.addresses = [];
    controller.markers = [];
    controller.bounds = new google.maps.LatLngBounds();

    var UpdateView = function(){
    	$multiple.empty();
    	$.each(controller.addresses, function(){
    		var address = this;
    		$("<div>")
			.html(address.address)
			.appendTo($multiple);
    	});
    	
    };

    var getAddresses = function(){
		$.ajax({
            type: "GET",
            cache: false,
            contentType: "application/json; charset=utf-8",
            url: "/api/v1/addresses/",
            beforeSend: function(request){
            }
        }).always(function(){
            
        }).done(function(data){
            controller.addresses = data;
            UpdateView();
            updateMarkers(controller.map);
            setMapOnAll(controller.map)
        });
	};

	var saveAddress = function(data){
  		$.ajax({
            type: "POST",
            cache: false,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            url: "/api/v1/addresses/"
        }).done(function(address){
            controller.addresses.push(address);
        }).fail(function(response, error){
            console.log(response.responseText);
        });
  	};

  	var deleteAddresses = function(){
  		$.ajax({
            type: "DELETE",
            cache: false,
            url: "/api/v1/addresses/"
        }).done(function(response){
            setMapOnAll(null);
            controller.addresses = [];
            UpdateView();
        }).fail(function(response, error){
            console.log(response.responseText);
        });
  	};

    var getNewMarker = function(address, position, myMap) {
        var pos = position;
        if (!position){
            pos = new google.maps.LatLng(address.latitude, address.longitude)
        }
        controller.bounds.extend(pos);
        var marker = new google.maps.Marker({
                position: pos,
                map: myMap
            });
        return marker;
    };

  	var updateMarkers = function(myMap){
  		
  		for (index in controller.addresses) {
  			address = controller.addresses[index]
            controller.markers.push(getNewMarker(address, null, myMap));
		}
  	};

    var setMapOnAll = function(myMap) {
        for (var i = 0; i < controller.markers.length; i++) {
            controller.markers[i].setMap(myMap);
            controller.map.fitBounds(controller.bounds);
        }
    };


  	var loadMap = function(){
  		var myLatlng = new google.maps.LatLng(30.3753, 69.3451);
		var myOptions = {
			zoom:1,
			center:myLatlng
		}
	    var map = new google.maps.Map($("#my_map")[0], myOptions);
	    var geocoder = new google.maps.Geocoder();
	    controller.map = map;

	    google.maps.event.addListener(map, 'click', function(event) {
		    var latitude = event.latLng.lat(),
		      longitude = event.latLng.lng(),
		      position = event.latLng;

		    //Validate that location has a real address and it’s not some wood/mountain/ocean
		    geocoder.geocode({
				'latLng': position
			}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					if (results[0]) {
						$("<div>")
						.html(results[0].formatted_address)
						.appendTo($multiple);

                        var marker = getNewMarker(null, position, controller.map)
					    controller.map.panTo(position);
                        controller.markers.push(marker);

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

  	$(document).on("click", "#reset", function(ev){
        ev.preventDefault();
    	deleteAddresses();
	});

  	loadMap();
	getAddresses();
	
  	
});