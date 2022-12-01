odoo.define('ctdac.Thema', function (require) {
    'use strict';   

    require('web.dom_ready');
    var ajax = require('web.ajax');


    

    var listBox1 = $(".estados")
    var _changeestado = function(e){
        if(e.target.value>0){
            ajax.jsonRpc('/get_main_municipality', 'call', {
                method: 'get',
                args: [{'id': e.target.value,}],
            })
            .then(function (data) {
                $(".municiopio").empty()
                $(".municiopio").append('<option value="0"></option>');
                $.each(data, function( index, value ) {
                    $(".municiopio").append('<option value="'+value.id+'">'+value.municipio+'</option>');
                });
            });
        }
    }


    var listBoxAliado1 = $(".estados-aliados")
    var _changeestadoAliado = function(e){
        if(e.target.value>0){
            ajax.jsonRpc('/get_main_municipality', 'call', {
                method: 'get',
                args: [{'id': e.target.value,}],
            })
            .then(function (data) {
                $(".municiopio_aliado").empty()
                $(".municiopio_aliado").append('<option value="0"></option>');
                $.each(data, function( index, value ) {
                    $(".municiopio_aliado").append('<option value="'+value.id+'">'+value.municipio+'</option>');
                });
            });
        }
    }

    var listBox2 = $("#municiopio");
    var we = null
    var _changemuniciopio = async function(e){
        
        if(e.target.value>0){
           we = await ajax.jsonRpc('/get_list_cliente', 'call', {
                method: 'get',
                args: [{'id': e.target.value,}],
            })
            

            var _mapLocateg=  function(id){
                
                var lat = 10.474754,
                lng = -66.955545,
                size = '100%';
                var mymap = null

                ajax.jsonRpc('/get_map_cliente', 'call', {
                    method: 'get',
                    args: [{'id': id}],
                })
                .then(function (data) {
                    lat = data[0].lat != '0'? data[0].lat:lat
                    lng = data[0].log != '0'? data[0].log: lng
                    console.log(lat,lng)
                    var container = L.DomUtil.get('map'); if(container != null){ container._leaflet_id = null; }
                    let point = new L.LatLng(lat, lng);
                    mymap = L.map('map').setView(point, 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
                    }).addTo(mymap);
                    let marker = new L.Marker([lat, lng]);
                    marker.addTo(mymap);
                    $('#map').css('width',size);
                    $('#map').css('height',size);
                    // hide google icon
                    $('.img-fluid').hide();
                    setTimeout(function () { mymap.invalidateSize();}, 400);

                })
                
               }
            function runlist(){

                $("#cradincer").empty()
            $.each(we, function( index, value ) {
                $("#cradincer").append(`
                    <a href="#"  class="seltMap" data-id="${value.id}">
                    
                    <div class="row border rounded shadow seltMapa">
                        <div class="col-4  p-3 mb-3 bg-white">
                        <img src="data:image/png;base64,${value.imgen? value.imgen:'' } " alt="${value.name}"  />
                        </div>
                        <div class="col-8  p-3 mb-3 bg-white">
                        <h3>${value.name}</h3>
                        <span>${value.hours? value.hours: ""}</span>
                        <p >${value.address}</p>
                        </div>
                    
                    </div>
                    </a>
                    <br/>
    
                        `
                        );
    
                        
                    });
                }
                runlist()   

            $(".seltMap").click(function(){    
                _mapLocateg($(this).data("id"))

            });
        
        }
    }

    // ------------------------------------------------------------------------------------------------><-------------------------------------------------------------------------------------------------------//
    var listBoxAliado2  = $("#municiopio_aliado");
    var we = null
    var _changemuniciopioAliado = async function(e){
        
        if(e.target.value>0){
           we = await ajax.jsonRpc('/get_list_aliado', 'call', {
                method: 'get',
                args: [{'id': e.target.value,}],
            })
            

            var _mapLocategMeta=  function(id){
                
                var lat = 10.474754,
                lng = -66.955545,
                size = '100%';
                var mymap = null

                ajax.jsonRpc('/get_map_aliado', 'call', {
                    method: 'get',
                    args: [{'id': id}],
                })
                .then(function (data) {
                    lat = data[0].lat != '0'? data[0].lat:lat
                    lng = data[0].log != '0'? data[0].log: lng
                    console.log(lat,lng)
                    var container = L.DomUtil.get('map_aliado'); if(container != null){ container._leaflet_id = null; }
                    let point = new L.LatLng(lat, lng);
                    mymap = L.map('map_aliado').setView(point, 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
                    }).addTo(mymap);
                    let marker = new L.Marker([lat, lng]);
                    marker.addTo(mymap);
                    $('#map_aliado').css('width',size);
                    $('#map_aliado').css('height',size);
                    // hide google icon
                    $('.img-fluid').hide();
                    setTimeout(function () { mymap.invalidateSize();}, 400);

                })
                
               }
            function runlistaliado(){

                $("#cradincer_aliado").empty()
            $.each(we, function( index, value ) {
                console.log(value)
                $("#cradincer_aliado").append(`
                    <a href="#"  class="seltMap" data-id="${value.id}">
                    
                    <div class="row border rounded shadow seltMapa">
                        <div class="col-4  p-3 mb-3 bg-white">
                        <img src="data:image/png;base64,${value.imgen? value.imgen:'' } " alt="${value.name}"  />
                        </div>
                        <div class="col-8  p-3 mb-3 bg-white">
                        <h3>${value.name}</h3>
                        <span>${value.hours? value.hours: "" }</span>
                        <p >${value.address}</p>
                        </div>
                    
                    </div>
                    </a>
                    <br/>
    
                        `
                        );
    
                        
                    });
                }
                runlistaliado()   

            $(".seltMap").click(function(){    
                _mapLocategMeta($(this).data("id"))

            });
        
        }
    }
    // ------------------------------------------------------------------------------------------------><--------------------------------------------------------------------------------------------------------//
    listBoxAliado1.change(_changeestadoAliado);
    listBox1.change(_changeestado);
    listBoxAliado2.change(_changemuniciopioAliado);
    listBox2.change(_changemuniciopio);


    
    });

    

    
    