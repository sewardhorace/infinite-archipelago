
//TODO: draw component names on the map? checkbox to toggle on and off?
//TODO: persistent pan/zoom and add recenter button
//TODO: zoom relative to cursor, not upper left corner of map
//TODO: allow dragging scrambler text onto map to create new component/detail


var img = {
  location: new Image(),
  party: new Image(),
  creature: new Image(),
  transport: new Image(),
  other: new Image()
};
img.location.src = 'static/generator/img/location.png';
img.party.src = 'static/generator/img/party.png';
img.creature.src = 'static/generator/img/creature.png';
img.transport.src = 'static/generator/img/transport.png';
img.other.src = 'static/generator/img/other.png';


function Component (obj) {
  this.id = obj.id || null;
  this.name = obj.name || '';
  this.x = obj.x * 1; //for some reason this breaks if '* 1' is removed...
  this.y = obj.y * 1;
  this.isActive = obj.isActive || false;
  this.category = obj.category || '';
  this.details = obj.details || [];
  this.hover = false;
  this.width = 2;
  this.height = 2;
  this.contains = function (x, y) {
    return this.x <= x && x <= this.x + this.width &&
           this.y <= y && y <= this.y + this.height;
  };
  this.draw = function (ctx, drawName = false) {
    if (this.isActive) {
      ctx.beginPath();
      ctx.arc(this.x + 1, this.y + 1, 1.5, 0, 2*Math.PI, false);
      ctx.fillStyle="rgba(224, 255, 71, 0.55)";
      ctx.fill();
    } else if (this.hover) {
      ctx.beginPath();
      ctx.arc(this.x + 1, this.y + 1, 1.25, 0, 2*Math.PI, false);
      ctx.strokeStyle="rgba(224, 255, 71, 0.55)";
      ctx.lineWidth=0.5;
      ctx.stroke();
    } 
    if (this.category == 'L') {
      ctx.drawImage(img.location, this.x, this.y, this.width, this.height);
    } else if (this.category == 'P') {
      ctx.drawImage(img.party, this.x, this.y, this.width, this.height);
    } else if (this.category == 'C') {
      ctx.drawImage(img.creature, this.x, this.y, this.width, this.height);
    } else if (this.category == 'T') {
      ctx.drawImage(img.transport, this.x, this.y, this.width, this.height);
    } else if (this.category == 'O') {
      ctx.drawImage(img.other, this.x, this.y, this.width, this.height);
    }
    if (drawName) {
      ctx.font = ".75px Courier";
      ctx.fillStyle = "black";
      ctx.textAlign = "center";
      ctx.fillText(this.name, this.x + 1.1, this.y + 3);
    }
  };
};

var mapper = {
  canvas : document.getElementById("canvas"),
  componentForm : document.getElementById("component-form"),
  componentDeleteButton : document.getElementById('component-delete'),
  componentNameInput : document.getElementById('component-name'),
  componentCategorySelect : document.getElementById('component-category'),
  detailsDiv : document.getElementById("detail-display"),
  detailNewButton : document.getElementById('detail-new'),
  namesToggle : document.getElementById('mapper-names-toggle'),
  recenterButton : document.getElementById('mapper-recenter'),
  defaultTransforms : {
    scaleFactor : 20.00,
    panX : 0,
    panY : 0,
    prevPanX : 0,
    prevPanY : 0
  },
  load: function (data) {
    var components = data.components.map(function(c) {
      return new Component(c);
    });
    this.components = components;
    this.gameID = data.id;
    if (data.map_transforms.hasOwnProperty('panX')) {
      this.transforms = data.map_transforms
    } else {
      this.transforms = this.defaultTransforms
    }
    this.showNames = data.map_names_toggle || false;
    this.namesToggle.checked = this.showNames;
  },
  start: function (data) {
    this.load(data);
    this.context = this.canvas.getContext("2d");
    this.canvas.addEventListener('click', this.handleClick.bind(this), false);
    this.canvas.addEventListener('mousedown', this.handleMouseDown.bind(this), false);
    this.canvas.addEventListener('mouseup', this.handleMouseUp.bind(this), false);
    this.canvas.addEventListener('mouseout', this.handleMouseOut.bind(this), false);
    this.canvas.addEventListener('mousemove', this.handleMouseMove.bind(this), false);
    this.canvas.addEventListener('DOMMouseScroll', this.handleScroll.bind(this), false);
    this.canvas.addEventListener('mousewheel', this.handleScroll.bind(this), false);
    this.canvas.addEventListener('contextmenu', this.handleRightClick.bind(this), false);
    this.canvas.addEventListener('drop', this.handleDetailDrop.bind(this), false);
    this.canvas.addEventListener('dragover', function(e) {
      e.preventDefault();
    });

    this.componentForm.addEventListener('submit', function(e) {
      e.preventDefault();
    });
    this.componentDeleteButton.addEventListener("click", this.handleComponentDeleteButton.bind(this), false);
    this.componentNameInput.addEventListener('input', this.handleComponentNameInput.bind(this), false);
    this.componentCategorySelect.addEventListener('change', this.handleComponentCategorySelect.bind(this), false);
    this.detailNewButton.addEventListener("click", this.handleDetailNewButton.bind(this), false);

    this.namesToggle.addEventListener("change", this.handleNamesToggle.bind(this), false);
    this.recenterButton.addEventListener("click", this.handleRecenterButton.bind(this), false);

    this.displayComponent(this.getActiveComponent());
  },
  getMousePos: function (e, canvas) {
    var rect = canvas.getBoundingClientRect();
    var rawX = e.clientX - rect.left;
    var rawY = e.clientY - rect.top
    var transformedX = rawX/this.transforms.scaleFactor-this.transforms.prevPanX;
    var transformedY = rawY/this.transforms.scaleFactor-this.transforms.prevPanY;
    return {
      x: transformedX,
      y: transformedY
    };
  },
  checkCollisions: function (components, mousePos, callback) {
    //TODO: it is currently possible to hover/click on two neighboring components at once if they overlap
    for (var i=0; i<components.length; i++){
      var isColliding = components[i].contains(mousePos.x, mousePos.y) ? true : false;
      callback(components[i], isColliding);
    }
  },
  handleClick: function (e) {
    //TODO: should dragging a component to move it cause it to be the active component?
    e.preventDefault();
    var mousePos = this.getMousePos(e, this.canvas);
    var self = this;
    this.checkCollisions(this.components, mousePos, function(component, isColliding) {
      if (isColliding){
        self.setActiveComponent(component);
        self.displayComponent(component);
      }
    });
  },
  handleRightClick: function (e) {
    //TODO: click an existing component to delete it (with confirmation popup)
    e.preventDefault();
    var mousePos = this.getMousePos(e, this.canvas);
    this.addNewComponent(mousePos);
  },
  handleMouseDown: function (e) {
    e.preventDefault();
    this.mouseIsDown = true;
    var mousePos = this.getMousePos(e, this.canvas);
    this.prevMouseDownPos = mousePos;
    var self = this;
    this.checkCollisions(this.components, mousePos, function(component, isColliding) {
      if (isColliding){
        self.draggingComponent = component;
        component.prevPos = {
          x : component.x,
          y : component.y
        };
      }
    });
  },
  handleMouseUp: function (e) {
    e.preventDefault();
    if (this.mouseIsDown) {
      this.mouseIsDown = false;

      if (this.draggingComponent) {
        this.updateComponent(this.draggingComponent);
        this.draggingComponent = null;
      } else {
        var mousePos = this.getMousePos(e, this.canvas);
        this.transforms.prevPanX += mousePos.x - this.prevMouseDownPos.x;
        this.transforms.prevPanY += mousePos.y - this.prevMouseDownPos.y;
      }
    }
  },
  handleMouseOut: function (e) {
    this.handleMouseUp(e);
  },
  handleMouseMove: function (e) {
    e.preventDefault();
    var mousePos = this.getMousePos(e, this.canvas);
    if (this.mouseIsDown) {
      this.handleDrag(mousePos);
    } else {
      this.handleHover(mousePos);
    }
    this.draw(); //TODO: use animationFrame instead of manually calling draw()
  },
  handleDrag: function (mousePos) {
    var delta = {
      x : mousePos.x - this.prevMouseDownPos.x,
      y : mousePos.y - this.prevMouseDownPos.y
    };
    if (this.draggingComponent) {
      this.draggingComponent.x = this.draggingComponent.prevPos.x + delta.x;
      this.draggingComponent.y = this.draggingComponent.prevPos.y + delta.y;
    } else {
      this.panView(delta);
    }
  },
  handleHover: function (mousePos) {
    this.checkCollisions(this.components, mousePos, function(component, isColliding){
      if (isColliding) {
        component.hover = true;
      } else {
        component.hover = false;
      }
    });
  },
  handleScroll: function(e){
    //TODO: translate during zoom based on mouse position, instead of zooming relative to upper left corner
    e.preventDefault();
    var delta = e.wheelDelta ? e.wheelDelta/120 : 0;
    if (delta) {
      var factor = 1+delta/10;
      this.transforms.scaleFactor *= factor;
      this.updateGame();
      this.draw();
    }
  },
  updateGame: function () {
    var data = {
      id : this.gameID,
      map_transforms : this.transforms,
      map_names_toggle : this.showNames,
    };
    clearTimeout(requests.gameUpdateTimeout);
    requests.gameUpdateTimeout = setTimeout(function () {
      requests.updateGame(data, function (data) {
        console.log('success');
      });
    }, 1000);
  },
  addNewComponent: function (mousePos) {
    //TODO: display something while ajax request is in progress/confirm success
    //TODO: autofocus on name input field
    var componentData = new Component({
      x : mousePos.x,
      y : mousePos.y,
    });
    componentData.x -= componentData.width/2;
    componentData.y -= componentData.height/2;
    componentData.game = this.gameID;
    var self = this;
    requests.createComponent(componentData, function (data) {
      var component = new Component(data.component);
      self.components.push(component);
      self.setActiveComponent(component);
      self.displayComponent(component);
    });
  },
  updateComponent: function (component) {
    //TODO: is an updateQueue the best solution here?
    component.game = this.gameID;
    if (requests.componentUpdateQueue.indexOf(component) < 0) {
      requests.componentUpdateQueue.push(component);
    }
    clearTimeout(requests.componentUpdateTimeout);
    requests.componentUpdateTimeout = setTimeout(function () {
      for (var i=0; i<requests.componentUpdateQueue.length; i++) {
        requests.updateComponent(requests.componentUpdateQueue[i], function (data) {
          console.log('success');
        });
      }
      requests.componentUpdateQueue = [];
    }, 1000);
  },
  deleteComponent: function (component) {
    var components = this.components;
    for (var i=0; i<components.length; i++) {
      if (components[i].id == component.id) {
        var idx = i;
        var self = this;
        requests.deleteComponent({id:component.id}, function (data) {
          components.splice(idx, 1);
          self.draw();
          self.displayComponent(null);
        });
      }
    }
  },
  setActiveComponent: function (component) {
    for (var i=0; i<this.components.length; i++) {
      if (this.components[i].isActive) {
        this.components[i].isActive = false;
        this.updateComponent(this.components[i]);
      }
    }
    component.isActive = true;
    this.updateComponent(component);
  },
  getActiveComponent: function () {
    var c = this.components;
    for (var i=0; i<c.length; i++) if (c[i].isActive) return c[i];
  },
  handleComponentDeleteButton: function (e) {
    // TODO: add "are you sure?" dialogue(?)
    e.preventDefault();
    this.deleteComponent(this.getActiveComponent());
    //TODO: display something other than the now-deleted component
  },
  handleComponentNameInput: function (e) {
    e.preventDefault();
    var component = this.getActiveComponent()
    component.name = e.target.value;
    this.updateComponent(component);
  },
  handleComponentCategorySelect: function (e) {
    e.preventDefault();
    var component = this.getActiveComponent()
    component.category = e.target.value;
    this.updateComponent(component);
    this.draw();
  },
  displayComponent: function (component) {
    //TODO: display something when no component is active
    this.draw();
    if (component) {
      document.getElementsByClassName("component-none")[0].style.display = 'none';
      
      this.componentNameInput.value = component.name;
      this.componentCategorySelect.value = component.category;
      this.displayDetails(component.details);

      document.getElementsByClassName("component-header")[0].style.display = 'block';
      this.detailsDiv.style.display = 'block';
      document.getElementsByClassName("component-footer")[0].style.display = 'block';
    } else {
      this.detailsDiv.style.display = 'none';
      document.getElementsByClassName("component-header")[0].style.display = 'none';
      document.getElementsByClassName("component-footer")[0].style.display = 'none';
      document.getElementsByClassName("component-none")[0].style.display = 'block';
    }
  },
  addNewDetail: function () {
    var activeComponent = this.getActiveComponent();
    var detailData = {component_id: activeComponent.id};
    var self = this;
    requests.createDetail(detailData, function (data) {
      console.log('success');
      activeComponent.details.push(data.detail);
      self.displayDetails(activeComponent.details);
    });
  },
  updateDetail: function (detail) {
    //TODO: is an updateQueue the best solution here?
    if (requests.detailUpdateQueue.indexOf(detail) < 0) {
      requests.detailUpdateQueue.push(detail);
    }
    clearTimeout(requests.detailUpdateTimeout);
    requests.detailUpdateTimeout = setTimeout(function () {
      for (var i=0; i<requests.detailUpdateQueue.length; i++) {
        requests.updateDetail(requests.detailUpdateQueue[i], function (data) {
          console.log('success');
        });
      }
      requests.detailUpdateQueue = [];
    }, 1000);
  },
  deleteDetail: function (detailData) {
    this.popDetailFromComponent(detailData);
    var self = this;
    requests.deleteDetail(detailData, function (data) {
      console.log('success');
      self.displayDetails(self.getActiveComponent().details);
    });
  },
  moveDetail: function (detailData, component) {
    var detail = this.popDetailFromComponent(detailData);
    detail.component_id = component.id;
    this.updateDetail(detail);
    component.details.push(detail);
    this.displayDetails(this.getActiveComponent().details);
  },
  popDetailFromComponent: function (detailData) {
    var components = this.components;
    var component;
    for (var i=0; i<components.length; i++) {
      if (components[i].id == detailData.component_id) {
        component = components[i];
      }
    }
    for (var i=0; i<component.details.length; i++) {
      if (component.details[i].id == detailData.id) {
        var detail = component.details[i];
        component.details.splice(i, 1);
        return detail;
      }
    }
  },
  handleDetailDeleteButton: function (e) {
    e.preventDefault();
    var parent = e.target.parentElement;
    var id = Number(parent.getAttribute('data-id'));
    var componentID = Number(parent.getAttribute('data-component-id'));
    var content = parent.children[1].value;
    var detailData = {
      id: id,
      component_id: componentID,
      content: content
    };
    this.deleteDetail(detailData);
  },
  handleDetailNewButton: function (e) {
    e.preventDefault();
    this.addNewDetail();
  },
  handleDetailInput: function (e) {
    var divs = this.detailsDiv.children;
    for (var i=0; i<divs.length; i++) {
      var textarea = divs[i].children[1];
      if (textarea == e.target) {
        var detail = this.getActiveComponent().details[i];
        detail.content = e.target.value;
        this.updateDetail(detail);
      }
    }
  },
  handleDetailDragStart: function (e) {
    //TODO: allow dragging to rearrange details order in the component display (problem - will still be unordered in the database)
    console.log("drag start");
    //dragging the textarea's parent frame, rather than text inside the input
    if (e.target === e.currentTarget) {
      var id = Number(e.target.getAttribute('data-id'));
      var componentID = Number(e.target.getAttribute('data-component-id'));
      var content = e.target.children[1].value;
      var data = {
        id: id,
        component_id: componentID,
        content: content
      };
      e.dataTransfer.setData('text/plain', JSON.stringify(data));
    }
  },
  handleDetailDrop: function (e) {
    console.log("dropped");
    e.preventDefault();
    var detailData = JSON.parse(e.dataTransfer.getData('text/plain'));
    e.dataTransfer.clearData();
    var mousePos = this.getMousePos(e, this.canvas);
    var self = this;
    this.checkCollisions(this.components, mousePos, function(component, isColliding){
      if (isColliding) {
        self.moveDetail(detailData, component);
      }
    });
  },
  displayDetails: function (details) {
    this.detailsDiv.innerHTML = "";
    for (var i=0; i<details.length; i++) {
      var detail = details[i];

      var textarea = document.createElement('textarea');
      textarea.setAttribute('rows', 3);
      textarea.value = detail.content;
      textarea.addEventListener('input', this.handleDetailInput.bind(this), false);

      var deleteButton = document.createElement('button');
      deleteButton.innerHTML = '&#10006;';
      deleteButton.addEventListener('click', this.handleDetailDeleteButton.bind(this));

      var frame = document.createElement('div');
      frame.setAttribute('class', 'detail');
      frame.setAttribute('draggable', true);
      frame.setAttribute('data-id', detail.id);
      frame.setAttribute('data-component-id', detail.component_id);
      frame.addEventListener('dragstart', this.handleDetailDragStart.bind(this), false);
      frame.addEventListener('mousedown', function (e) {
        if (e.target !== this) {
          //clicked child element - select and drag text from the textarea instead
          e.stopPropagation();
        }
      });

      frame.addEventListener('drop', function (e) {
        //TODO: should be able to drop text into the textarea, but not the drop data
        console.log('dropped');
        var data = e.dataTransfer.getData('text/plain');
        var isJSON = true;
        try {
          JSON.parse(data);
        } catch (e) {
          isJSON  = false;
        }
        if (isJSON) {
          e.preventDefault();
          e.dataTransfer.clearData();
        }
      });

      frame.append(deleteButton);
      frame.append(textarea);
      this.detailsDiv.append(frame);
    }
  },
  handleNamesToggle: function (e) {
    if (this.namesToggle.checked == true){
      this.showNames = true;
    } else {
      this.showNames = false;
    }
    this.updateGame();
    this.draw();
  },
  handleRecenterButton: function (e) {
    e.preventDefault();
    this.transforms = this.defaultTransforms;
    this.updateGame();
    this.draw();
  },
  panView: function (delta) {
    this.transforms.panX = this.transforms.prevPanX + delta.x;
    this.transforms.panY = this.transforms.prevPanY + delta.y;
    this.updateGame();
  },
  drawGrid: function (ctx) {
    for (var i = (this.transforms.panX % 1) * this.transforms.scaleFactor; i < this.canvas.width; i+=this.transforms.scaleFactor) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, this.canvas.height);
      ctx.lineWidth = 0.05 * this.transforms.scaleFactor;
      ctx.strokeStyle = '#B3CAF5';
      ctx.stroke();
    }
    for (var i = (this.transforms.panY % 1) * this.transforms.scaleFactor; i < this.canvas.height; i+=this.transforms.scaleFactor) {
      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(this.canvas.width, i);
      ctx.lineWidth = 0.05 * this.transforms.scaleFactor;
      ctx.strokeStyle = '#B3CAF5';
      ctx.stroke();
    }
  },
  draw: function () {
    var ctx = this.context;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    ctx.fillStyle = '#FFFBD1';
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    this.drawGrid(ctx);
    ctx.save();

    ctx.scale(this.transforms.scaleFactor, this.transforms.scaleFactor);
    ctx.translate(this.transforms.panX, this.transforms.panY);
    for (var i = 0; i < this.components.length; i++) {
      this.components[i].draw(ctx, this.showNames);
    }
    ctx.restore();

  }
};