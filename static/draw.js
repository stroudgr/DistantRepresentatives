/*
// reference canvas element (with id="c")
var canvasEl = document.getElementById('canvas');

// get 2d context to draw on (the "bitmap" mentioned earlier)
var ctx = canvasEl.getContext('2d');

// set fill color of context
ctx.fillStyle = 'red';

// create rectangle at a 100,100 point, with 20x20 dimensions
ctx.fillRect(100, 100, 20, 20);
*/


//https://stackoverflow.com/questions/22910496/move-object-within-canvas-boundary-limit/36011859#36011859

// create a wrapper around native canvas element (with id="c")
var canvas = new fabric.Canvas('canvas');

var rects = [];
var points = [];

for (var i=1; i < 10; i++) {
  var line =  new fabric.Rect({
    left: 100*i-1,
    top: 0,
    fill: 'black',
    width: 2,
    height: 1000,
    selectable: true,
    lockRotation:true,
    lockMovementX:true,
    lockMovementY:true,
    padding:0,
    selectable:false
  });
  canvas.add(line);


  var line =  new fabric.Rect({
    left: 0,
    top: 100*i-1,
    fill: 'black',
    width: 1000,
    height: 2,
    selectable: true,
    lockRotation:true,
    lockMovementX:true,
    lockMovementY:true,
    padding:0,
    selectable:false
  });
  canvas.add(line);



}



function addRectangle() {

  removeReps();

  // create a rectangle object
  var rect = new fabric.Rect({
    left: 100,
    top: 100,
    fill: 'red',
    width: 100,
    height: 70,
    selectable: true,
    lockRotation:true,
    padding:0,
  });

  // "add" rectangle onto canvas
  canvas.add(rect);

  rects.push(rect);
  //console.log(rect.currentHeight); rect.canvas.height || rect.currentWidth > .canvas.width)
 
  var halfw = canvas.currentWidth/2;
  var halfh = canvas.currentHeight/2;



  canvas.on("object:modified", function(e) {
    
    removeReps();

    var obj = e.target;
    
    //canvas.height;
    //canvas.width;
    
    
    boundingRect = obj.getBoundingRect(true);

    //console.log(boundingRect.left);
    //console.log(boundingRect.right);
    
    //console.log(boundingRect.top);
    
    
    //if(obj.currentHeight > obj.canvas.height || obj.currentWidth > obj.canvas.width){
    //    return;
    //}
    //obj.setCoords();
    
    // top-left  corner
    if(obj.getBoundingRect().left < 0){
        //obj.top = 0;//Math.max(obj.top, obj.top-obj.getBoundingRect().top);
        obj.left = 0;//Math.max(obj.left, obj.left-obj.getBoundingRect().left);
    }
    if (obj.getBoundingRect().top < 0) {
      obj.top = 0;
    }
    
    // bot-right corner
    if(obj.getBoundingRect().top+obj.getBoundingRect().height  > obj.canvas.height || obj.getBoundingRect().left+obj.getBoundingRect().width  > obj.canvas.width){
      obj.top = Math.min(obj.top, obj.canvas.height-obj.getBoundingRect().height+obj.top-obj.getBoundingRect().top);
      obj.left = Math.min(obj.left, obj.canvas.width-obj.getBoundingRect().width+obj.left-obj.getBoundingRect().left);
    }
     

  });
}

function removeReps(){
  
  for (let x in points) {
    canvas.remove(points[x]);
  }  
  //canvas.renderAll();
  points = [];
}


function addPointsToDrawing(data) {

  document.getElementById("blah").innerHTML = "&delta;* = " + data["delta"];

  let pointsRadius = 10;
  //console.log("adding points....");
  for (var i = 0; i < data["p"].length; i++) {

    //console.log(data["p"][i]);

    var circle = new fabric.Circle({
      radius: pointsRadius, fill: 'green', left: data["p"][i][0]-pointsRadius, top: data["p"][i][1]-pointsRadius,
      lockRotation:true,
      lockMovementX:true,
      lockMovementY:true,
      selectable:false
    });
    //var circle = new fabric.Circle({
    //  radius: 50, fill: 'green', left: -50, top: -50
    //});

    canvas.add(circle);
    //console.log(circle);
    points.push(circle);
  }

}





function computeDistantReps(computation_url="/listening") {
  removeReps();
  var sendIt = [];
  for (var i=0; i < rects.length; i++) {
    //var r = {width:0, height: 0, cx:0, cy: 0};
    var r = rects[i];
    var rect = [r.left + r.width/2, r.top + r.height/2, r.width/2, r.height/2];
    //console.log(rect);
    sendIt.push(rect);
  }

  var jobj = {
    "rects":JSON.stringify(sendIt)
  };

  console.log("Sending ", jobj);

  /*postData(computation_url, jobj).then(data=> {
  //postData("https://127.0.0.1/listening", jobj).then(data=> {
    //document.getElementById("blah").innerHTML = "&delta;* = " + data["098"];
    console.log(data);
    addPointsToDrawing(data);
    //document.getElementById("blah").innerHTML = "&delta;* = " + data["delta"];

  }).catch(function (error) {
    console.log(error);
  });;

  */

  console.log(computation_url + "/" + JSON.stringify(sendIt) );
  //return;

  getResult(computation_url + "/" + JSON.stringify(sendIt)).then(data=> {
    //document.getElementById("blah").innerHTML = "&delta;* = " + data["098"];
    console.log(data);
    addPointsToDrawing(data);
    //document.getElementById("blah").innerHTML = "&delta;* = " + data["delta"];

  }).catch(function (error) {
    console.log(error);
  });;

}

async function getResult(url='') {
  const response = await fetch(url);
  return response.json();
}


// Example POST method implementation:
async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });

  return response.json(); // parses JSON response into native JavaScript objects
}



/*function basicCommunication() {

  fetch('http://localhost:5000/listening')
  .then(response => response.json())
  .then(data => console.log(data)); 
              //document.getElementById("blah").innerHTML = data);

}

*/