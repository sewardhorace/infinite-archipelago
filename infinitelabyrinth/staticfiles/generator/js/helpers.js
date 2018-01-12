
var helpers = {
  gamesDropdown: document.getElementById("games-dropdown"),
  scrambler: document.getElementById("scrambler"),
  setEventHandlers: function() {
    if (this.gamesDropdown){
      this.gamesDropdown.addEventListener('click', this.handleGamesDropdownClick.bind(this), false);
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