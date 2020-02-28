
var gmarkers = {};
var dynamicMarker;
var token = $('input[name=csrfmiddlewaretoken]').val();

//Dodaje marker na mapu i u globalni dict "gmarkers" = {id:marker,... }
function addMarker(bazna) {
    //console.log(bazna);
    var MyLatLon = new google.maps.LatLng(bazna.lat, bazna.lon);
    var id = bazna.cell_id;
    try {
        if (id.length) {
            $.post("/lock_mngr", {cmd: 'add', cell_id: id, csrfmiddlewaretoken: token});
        }
        mark = new google.maps.Marker({
            position: MyLatLon,
            map: map,
            title: bazna.name.toLowerCase()
        });
        mark.setMap(map); // To add the marker to the map, call setMap();
        gmarkers[id] = mark;
        addElement(id, bazna.name); //dodaje dom u listu zaključanih elemenata
        //console.log('adding mark:', id, gmarkers);
    }
    catch (err) {
        alert("Nešto se iskundačilo !"+ "\n" +"pogledaj konzolu");
        console.log(err);
    }
}


//uklanja marker sa mape i iz globalnog gmarkers dict-a
function removeMarker(id) {
    console.log(gmarkers);
    try {
        gmarkers[id].setMap(null);
        $.post("/lock_mngr", {cmd: 'remove', cell_id: id, csrfmiddlewaretoken: token});
        delete gmarkers[id];
        var dom_elem = document.getElementById(id);
        document.getElementById('parent').removeChild(dom_elem);
    }
    catch (err) {
        alert("Nešto se iskundačilo !" + "\n" + "pogledaj konzolu");
        console.log(err);
    }
    console.log(gmarkers)
}


function addElement(id, naziv) {
    if (!document.body.contains(document.getElementById(id))) { //ako element ne postoji
        //console.log('adding element', id, naziv);
        var elemDescription = naziv.slice(-10);
        var domElem = '<div class="col-sm-12">';
        domElem +='<button class="btn btn-primary col-sm-12 butt1" id=${id} type="button" title="remove">'+elemDescription+'</button>';
        domElem +='</div>';

        var parentElem = document.getElementById('parent');     //instanca osnovnog element
        var org = document.getElementById('template');          //instanca template dom elementa
        //var newDiv = org.cloneNode(true);                       //kloniraj ga
        var newDiv = document.createElement("div");
        newDiv.className = "row input-group-text";              //dodaj atribute
        newDiv.id = id;
        newDiv.innerHTML = domElem;
        parentElem.appendChild(newDiv);                         //dodaj novi element u osnovni
        document.getElementById(id).addEventListener("mouseup", function() {removeMarker(id)});

    }
}


function populateData() {
    var bazna = $("#bazna").getSelectedItemData();
    console.log(bazna);
    document.getElementById("name").innerHTML = bazna.name.toLowerCase();
    document.getElementById("cell_id").innerHTML = bazna.cell_id;
    document.getElementById("azimuth").innerHTML = bazna.azimuth;
    document.getElementById("pow").innerHTML = bazna.pow;
    document.getElementById("lon").innerHTML = bazna.lon.slice(0,7);
    document.getElementById("lat").innerHTML = bazna.lat.slice(0,7);

    var MyLatLon = new google.maps.LatLng(bazna.lat.slice(0,-1), bazna.lon.slice(0,-1));
    // ukloniti prijašnji dinamički marker
    //dodati novi dinamički marker
    if (dynamicMarker) {dynamicMarker.setMap(null);}
    dynamicMarker = new google.maps.Marker({
        position: MyLatLon,
        map: map,
        title: bazna.name.toLowerCase()
    });
    dynamicMarker.setMap(map);
}


function onLoadFun() {
    //dodaj eventListener na "lock" dugme
    document.getElementById("lock").addEventListener("mouseup", function () {
        var bazna = {};
        bazna.name = document.getElementById('name').innerHTML;
        bazna.cell_id = document.getElementById('cell_id').innerHTML;
        bazna.lat = document.getElementById('lat').innerHTML;
        bazna.lon = document.getElementById('lon').innerHTML;
        addMarker(bazna)
    });
    //dodaj eventListener na "removeAll" dugme
    document.getElementById("removeAll").addEventListener("mouseup", function () {
        $("#parent").empty();
        $.post("/lock_mngr", {cmd: 'remove', cell_id: "all", csrfmiddlewaretoken: token});
        Object.keys(gmarkers).forEach(function (key) {
            console.log('brišem marker:', key);
            gmarkers[key].setMap(null);
        });
        gmarkers = {};
    });
}

var options = {
    url: "/search_cell",
    listLocation: "items",
    getValue: "name",
    template: {
        type: "description",
        fields: {
            description: "cell_id"
        }
    },
    ajaxSettings: {
        dataType: "JSON",
        method: "POST",
        data: {
        dataType: "JSON"
            }
        },
    list: {
        onChooseEvent: populateData

    },

  preparePostData: function(data) {
    data.phrase = $("#bazna").val();
    data.csrfmiddlewaretoken = token; //$('input[name=csrfmiddlewaretoken]').val();
    return data;
  },

  requestDelay: 400
};

$('#bazna').easyAutocomplete(options);

$(document).ready(function () {
    onLoadFun();
    $.post("/lock_mngr", {cmd: 'list', cell_id: '', csrfmiddlewaretoken: token}, function (responseData) {
        if (responseData.cells) {
            var responseLen = responseData.cells.length;
            for (var i = 0; i < responseLen; i++) {
                //addElement(responseData.cells[i].cell_id.slice, responseData.cells[i].name.toLowerCase());
                var bazna = responseData.cells[i];
                bazna.name = bazna.name.toLowerCase();
                bazna.lat = bazna.lat.slice(0,-1);
                bazna.lon = bazna.lon.slice(0,-1);
                addMarker(bazna);
            }
        }
    });

});