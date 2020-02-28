var options = {
    url: "/search_cell",
    getValue: "name",
    ajaxSettings: {
        dataType: "JSON",
        method: "POST",
        data: {
        dataType: "JSON",
            }
        },
    list: {
		onLoadEvent:function(element) {
		    alert(element);
        }
		},


  preparePostData: function(data) {
    data.phrase = $("#bazna").val();
    data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    console.log(data);
    return data;
  },

  requestDelay: 400
};


$('#bazna').easyAutocomplete(options);
