// TODO: UI for viewing all components/details as a list

var game = {
	load: function(data) {
		this.loadName(data);
		this.loadMap(data);
		this.loadScrambler(data);
		if (document.getElementById('sync')){
			this.loadSyncUI(data);
		}
		console.log("loaded game " + data.game.name);
	},
	loadName: function(data) {
		document.getElementById("name-input").value = data.game.name;
	},
	loadMap: function(data) {
		var components = data.game.components.map(function(c) {
      return new Component(c);
    });
    mapper.components = components;
    mapper.gameID = data.game.id;
    mapper.start();
	},
	loadScrambler: function(data) {
		var endpoints = data.game.endpoints;
		var endpointSelect = "";
		var endpointHiddenData = "";
		for (var key in endpoints){
			endpointSelect += "<option>" + key + "</option>";
			endpointHiddenData += '<div data-key="' + key + '">' + endpoints[key] + '</div>';
		}
		document.getElementById("endpoint-select").innerHTML = endpointSelect;
		document.getElementById("endpoint-data").innerHTML = endpointHiddenData;
	},
	loadSyncUI: function(data) {
		document.getElementById("inputSheetGameID").value = data.game.id;
		var input = document.getElementById("inputSheetURL");
		if (data.game.sheet_url) {
			input.setAttribute("placeholder", data.game.sheet_url);
			input.value = data.game.sheet_url;
		} else {
			input.setAttribute("placeholder", "www.example.com/sheet");
		}
	},
};