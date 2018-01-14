
var helpers = {
  gamesDropdown: document.getElementById("games-dropdown"),
  scrambler: document.getElementById("scrambler"),
  nameInput: document.getElementById("name-input"),
  setEventHandlers: function() {
    if (this.gamesDropdown){
      this.gamesDropdown.addEventListener('click', this.handleGamesDropdownClick.bind(this), false);
    }
    if (this.nameInput){
      this.nameInput.addEventListener('change', this.handleNameInputChange.bind(this), false);
    }
    this.scrambler.addEventListener('submit', this.handleScramblerSubmit.bind(this), false);
  },
  handleGamesDropdownClick: function(e) {
    e.preventDefault();
    if (e.target.attributes.hasOwnProperty('data-id')){
      var id = e.target.getAttribute('data-id');
      requests.loadGame(id, function (data) {
        game.load(data);
      });
    }
    if (e.target.id == "newGame") {
      var self = this;
      requests.createGame({name:"example"}, function (data) {
        console.log(self.gamesDropdown);
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.setAttribute("id", data.game.id);
        a.innerHTML = data.game.name;
        li.append(a);
        self.gamesDropdown.prepend(li);
        requests.loadGame(data.game.id, function (data) {
          game.load(data);

        });
      })
    }
  },
  handleNameInputChange: function(e) {
    console.log(this.nameInput.value);
    var data = {
      id: mapper.gameID,
      name: this.nameInput.value,
    };
    requests.updateGame(data, function (data) {
      console.log(data);
    });
  },
  handleScramblerSubmit: function(e) {
    e.preventDefault();
    var select = document.getElementById("endpoint-select");
    var key = select.options[select.selectedIndex].text;
    var text = document.querySelector("#endpoint-data [data-key='" + key + "']").innerHTML;
    var data = {
      text: text,
      gameID: mapper.gameID,
    };
    requests.generate(data, function (data) {
      document.getElementById("scrambler-content").innerHTML = data.detail;
    });
  },
  getCookie: function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = $.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
};