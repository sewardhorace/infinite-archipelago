//TODO: jquery to pure javascript

var requests = {
  componentUpdateTimeout: null,
  componentUpdateQueue: [],
  detailUpdateTimeout: null,
  detailUpdateQueue: [],
  URLS: {
    GAME: {
      GET: {
        URL: '/api/game/',
        TYPE: 'GET',
      },
    },
    COMPONENT: {
      CREATE: {
        URL: '/api/components/create/',
        TYPE: 'POST',
      },
      UPDATE: {
        URL: '/api/components/update/',
        TYPE: 'POST',
      },
      DELETE: {
        URL: '/api/components/delete/',
        TYPE: 'POST'
      },
    },
    DETAIL: {
      CREATE: {
        URL: '/api/details/create/',
        TYPE: 'POST',
      },
      UPDATE: {
        URL: '/api/details/update/',
        TYPE: 'POST',
      },
      DELETE: {
        URL: '/api/details/delete/',
        TYPE: 'POST',
      },
    },
    GENERATE: {
      URL: 'api/generate/',
      TYPE: 'POST',
    },
    SYNC: {
      URL: 'api/sync/',
      TYPE: 'POST',
    },
  },
  request: function (obj) {
    $.ajax({
      url: obj.url,
      type: obj.type,
      data: JSON.stringify(obj.data),
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      success: obj.callback
    });
  },
  loadGame: function (gameID, callback) {
    this.request({
      url: this.URLS.GAME.GET.URL + gameID,
      type: this.URLS.GAME.GET.TYPE,
      callback: callback,
    });
  },
  updateGame: function (data, callback) {
    //save current pan/zoom
  },
  createComponent: function (data, callback) {
    var componentData = {
      x : data.x,
      y : data.y,
      game: data.game,
    };
    this.request({
      url: this.URLS.COMPONENT.CREATE.URL,
      type: this.URLS.COMPONENT.CREATE.TYPE,
      data: componentData,
      callback: callback,
    });
  },
  updateComponent: function (data, callback) {
    var componentData = {
      id: data.id,
      name: data.name,
      x: data.x,
      y: data.y,
      category: data.category,
      isActive: data.isActive,
      game: data.game,
    };
    this.request({
      url: this.URLS.COMPONENT.UPDATE.URL,
      type: this.URLS.COMPONENT.UPDATE.TYPE,
      data: componentData,
      callback: callback,
    });
  },
  deleteComponent: function (data, callback) {
    var componentData = {
      id: data.id,
    };
    this.request({
      url: this.URLS.COMPONENT.DELETE.URL,
      type: this.URLS.COMPONENT.DELETE.TYPE,
      data: componentData,
      callback: callback,
    });
  },
  createDetail: function (data, callback) {
    var detailData = {
      component : data.component_id,
    };
    this.request({
      url: this.URLS.DETAIL.CREATE.URL,
      type: this.URLS.DETAIL.CREATE.TYPE,
      data: detailData,
      callback: callback,
    });
  },
  updateDetail: function (data, callback) {
    var detailData = {
      id: data.id,
      content: data.content,
      component: data.component_id,
    };
    this.request({
      url: this.URLS.DETAIL.UPDATE.URL,
      type: this.URLS.DETAIL.UPDATE.TYPE,
      data: detailData,
      callback: callback,
    });
  },
  deleteDetail: function (data, callback) {
    var detailData = {
      id: data.id,
    };
    this.request({
      url: this.URLS.DETAIL.DELETE.URL,
      type: this.URLS.DETAIL.DELETE.TYPE,
      data: detailData,
      callback: callback,
    });
  },
  generate: function (data, callback) {
    var textData = {
      text: data.text,
      game_id: data.gameID
    };
    this.request({
      url: this.URLS.GENERATE.URL,
      type: this.URLS.GENERATE.TYPE,
      data: textData,
      callback: callback,
    });
  },
  syncSheet: function (data, callback) {
    var URLData = {
      sheet_URL: data.sheetURL,
      game_id: data.gameID
    };
    this.request({
      url: this.URLS.SYNC.URL,
      type: this.URLS.SYNC.TYPE,
      data: URLData,
      callback: callback,
    });
  },
};