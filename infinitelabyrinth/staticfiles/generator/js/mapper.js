//TODO: clean up globals
//TODO: draw component names on the map? checkbox to toggle on and off?
//TODO: need to display something after active component is deleted

var SCALE = 1;
var LINEWIDTH = SCALE*0.05;
var SEACOLOR = '#42b3f4';
var GRIDCOLOR = '#418cf4';
var ACTIVECOLOR = 'green';
var HOVERCOLOR = 'white';
var INACTIVECOLOR = 'red';

function Component (obj) {
  this.id = obj.id || null;
  this.name = obj.name || '';
  this.x = obj.x*SCALE;
  this.y = obj.y*SCALE;
  this.isActive = obj.isActive || false;
  this.category = obj.category || '';
  this.details = obj.details || [];
  this.hover = false;
  this.colors = {
    active: ACTIVECOLOR,
    hover: HOVERCOLOR,
    inactive: INACTIVECOLOR
  };
  this.width = 1;
  this.height = 1;
  this.contains = function (x, y) {
    return this.x <= x && x <= this.x + this.width &&
           this.y <= y && y <= this.y + this.height;
  };
  this.draw = function (ctx) {
    if (this.isActive) {
      ctx.fillStyle = this.colors.active;
    } else if (this.hover) {
      ctx.fillStyle = this.colors.hover;
    } else {
      ctx.fillStyle = this.colors.inactive
    }
    ctx.fillRect(this.x, this.y, this.width, this.height);
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
  transforms : {
    scaleFactor : 10.00,
    panX : 0,
    panY : 0,
    prevPanX : 0,
    prevPanY : 0
  },
  start: function () {
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
      this.draw();
    }
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
  },
  displayComponent: function (component) {
    //TODO: display something when no component is active
    this.draw();
    if (component) {
      this.componentNameInput.value = component.name;
      this.componentCategorySelect.value = component.category;
      this.displayDetails(component.details);
    } else {
      console.log("ain't no component active");
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
    // this.displayDetails(this.getActiveComponent().details);
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
    //TODO: fix event bubbling so users can highlight text in the textarea (rather than dragging)
    this.detailsDiv.innerHTML = "";
    for (var i=0; i<details.length; i++) {
      var detail = details[i];

      var textarea = document.createElement('textarea');
      textarea.value = detail.content;
      textarea.addEventListener('input', this.handleDetailInput.bind(this), false);

      var deleteButton = document.createElement('button');
      deleteButton.innerHTML = 'x';
      deleteButton.addEventListener('click', this.handleDetailDeleteButton.bind(this));

      var frame = document.createElement('div');
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
  panView: function (delta) {
    this.transforms.panX = this.transforms.prevPanX + delta.x;
    this.transforms.panY = this.transforms.prevPanY + delta.y;
  },
  drawGrid: function () {
    var ctx = this.context;
    for (var i = SCALE; i < this.canvas.width; i+=SCALE) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, this.canvas.height);
      ctx.lineWidth = LINEWIDTH;
      ctx.strokeStyle = GRIDCOLOR;
      ctx.stroke();
    }
    for (var i = SCALE; i < this.canvas.height; i+=SCALE) {
      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(this.canvas.width, i);
      ctx.lineWidth=LINEWIDTH;
      ctx.strokeStyle = GRIDCOLOR;
      ctx.stroke();
    }
  },
  draw: function () {
    var ctx = this.context;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    ctx.fillStyle = SEACOLOR;
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    ctx.save();
    ctx.scale(this.transforms.scaleFactor, this.transforms.scaleFactor);
    ctx.translate(this.transforms.panX, this.transforms.panY);
    this.drawGrid();
    for (var i = 0; i < this.components.length; i++) {
      this.components[i].draw(ctx);
    }
    ctx.restore();
  }
};