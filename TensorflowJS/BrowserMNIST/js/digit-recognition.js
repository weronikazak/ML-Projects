let model;
var canvawWidth = 150;
var canvawHeight = 150;
var canvasStrokeStyle = "white";
var canvasLineJoin = "round";
var canvasLineWidth = 10;
var canvasBackgroundColor = "black";
var canvasId = "canvas";

var clickX = new Array();
var clickY = new Array();
var clickD = new Array();

var drawing;

var canvasBox = document.getElementById('canvas_box');
var canvas = document.getElement("canvas");

canvas.setAttribute("width", canvawWidth);
canvas.setAttribute("height", canvawHeight);
canvas.setAttribute("id", canvasId);
canvas.style.backgroundColor = canvasBackgroundColor;
canvasBox.appendChild(canvas);

if (typeof C_vmlCanvasManager != 'undefined') {
	canvas = C_vmlCanvasManager.initElement(canvas);
}

ctx = canvas.getContext('2d');

// MOUSE DOWN
$("#canvas").mousedown(function(e) {
	var rect = canvas.getBoundingClientRect();
	var mouseX = e.clientX - rect.left;
	var mouseY = e.clientY - rect.top;
	drawing = true;
	addUserGesture(mouseX, mouseY);
	drawOnCanvas();
});


// TOUCH START
canvas.addEventListener("touchstart", function(e) {
	if (e.target == canvas) {
		e.preventDefault();
	}

	var rect = canvas.getBoundingClientRect();
	var touch = e.touches[0];

	var mouseX = touch.clientX - rect.left;
	var mouseY = touch.clientY - rect.top;

	drawing = true;

	addUserGesture(mouseX, mouseY);
	drawOnCanvas();
});


// MOUSE MOVE
$("#canvas").mousemove(function(e) {
	if (drawing) {
		var rect = canvas.getBoundingClientRect();
		var mouseX = e.clientX - rect.left;
		var mouseY = e.clientY - rect.top;
		addUserGesture(mouseX, mouseY);
		drawOnCanvas();
	}
});


// TOUCH MOVE
canvas.addEventListener("touchmove", function(e) {
	if (e.target == canvas) {
		e.preventDefault();
	}

	if (drawing) {
		var rect = canvas.getBoundingClientRect();
		var touch = e.touches[0];

		var mouseX = e.clientX - rect.left;
		var mouseY = e.clientY - rect.top;

		addUserGesture(mouseX, mouseY);
		drawOnCanvas();
	}
}, false);
