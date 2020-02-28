$( document ).ready(function() {
    console.log( "ready!" );

    var options = {
	url: function(phrase) {
    return "/search_cell";
  },

  getValue: function(element) {
    return element.name;
  },

  ajaxSettings: {
    dataType: "json",
    method: "POST",
    data: {
      dataType: "json",
    }
  },

  preparePostData: function(data) {
    data.phrase = $("#bazna").val();
    return data;
  },

  requestDelay: 400

}
console.log(options)
$('#bazna').easyAutocomplete(options)


});