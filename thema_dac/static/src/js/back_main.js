"use strict";
odoo.define('thema_dac.back_maint', function (require) {
   
    // require('web.dom_ready')
    var basic_fields = require("web.basic_fields");
    var viewRegistry = require('web.view_registry');
    
    //Changing Sales Team Graph color
    
        console.log(viewRegistry.map)
        var lat = 55.505,
            lng = 38.6611378,
            enable = true,
            size = 230;

            if (enable && viewRegistry.map.length){
                let point = new L.LatLng(lat, lng);
                let mymap = L.map('map').setView(point, 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
                }).addTo(mymap);
                console.log()
                let marker = new L.Marker([lat, lng]);
                marker.addTo(mymap);
                $('#map').css('width',size);
                $('#map').css('height',size);
                // hide google icon
                $('.img-fluid').hide();
                setTimeout(function () { mymap.invalidateSize() }, 400);
            }


    

        
    
});


