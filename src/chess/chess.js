/**********************************************************************
    Copyright (C) 2017  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
**********************************************************************/
chessNamespace = function() {
/**********************************************************************
 *
 * Chess solver -- chessNamespace
 *
 * The general layout of this program is:
 *   1. RenderBoard function.
 *   2. Entry points except for convertCanvasToBoard.
 *      Functions called from the HTML code.
 *   3. Event handlers.  Mouse click and Key click event handlers.
 *   4. Support functions called from previous functions.
 *   5. convertCanvasToBoard and associated server communication functions.
 *
 * Global variables (ChessNamespace-wide variables):
 *   imageStack -- pieces on the board.
 *
 **********************************************************************/

var imageStack = [];
requestAnimationFrame(renderBoard);
window.addEventListener("load", mouseoncanvas, false);

function renderBoard() {
    // Clear all the images from the canvas, and redraw each image
    // based on the data saved in imageStack
    requestAnimationFrame(renderBoard);
    var canvas = document.getElementById('mycanvas');
    var context = canvas.getContext('2d');
    context.clearRect(0,0,
        canvas.width,
        canvas.height
    );
    for(var i = 0,len = imageStack.length; i < len; i++) {
        var obj = imageStack[i];
        obj.context.drawImage(obj.image,obj.x,obj.y);
    }
}

/**********************************************************************
 *
 * Entry points
 *
 **********************************************************************/
function startMe() {
    // Makes sure the requestAnimationFrame value is set for every
    // reasonable browser.
    var requestAnimationFrame = window.requestAnimationFrame ||
                                window.mozRequestAnimationFrame ||
                                window.webkitRequestAnimationFrame ||
                                window.msRequestAnimationFrame;
    window.requestAnimationFrame = requestAnimationFrame;
}

function drag(event)
{
    // Drag a piece
    event.dataTransfer.setData("mposx",event.clientX - event.target.offsetLeft );
    event.dataTransfer.setData("mposy",event.clientY - event.target.offsetTop  );
    event.dataTransfer.setData("image_id",event.target.id);
}

function drop(event)
{
    // Drop a piece.  push this piece onto the imageStack.
    event.preventDefault();
    var canvas = document.getElementById('mycanvas');
    var image = document.getElementById( event.dataTransfer.getData("image_id") );
    var mposx = event.dataTransfer.getData("mposx");
    var mposy = event.dataTransfer.getData("mposy");
    var context = canvas.getContext('2d');
    var xpos = locAdjust(event.clientX - canvas.offsetLeft - mposx);
    var ypos = locAdjust(event.clientY - canvas.offsetTop - mposy);
    cleanPrev(xpos, ypos);
    imageStack.push({
        context: context,
        image: image,
        x: xpos,
        y: ypos
    });
}

function allowDrop(event)
{
    // Make sure unwanted events do not occur.
    event.preventDefault();
}

/**********************************************************************
 *
 * Event Handlers
 *
 **********************************************************************/
function mouseoncanvas(event) {
    // Handle the mouse when it is no the chessboard
    var canvas = document.getElementById('mycanvas');
    canvas.addEventListener("mousedown", mousedownoncanvas, false);
}

function mousedownoncanvas(event) {
    // Handle the mouse when it selects a piece on the chessboard.
    var dwnX = event.offsetX;
    var dwnY = event.offsetY;
    for(var x = 0,len = imageStack.length; x < len; x++) {
        var obj = imageStack[x];
        if (dwnX < obj.x || dwnX > obj.x + obj.width) {
            continue;
        }
        if (dwnY < obj.y || dwnY > obj.y + obj.height) {
            continue;
        }
        startMove(obj,dwnX,dwnY);
        break;
    }
}

function startMove(obj,dwnX,dwnY) {
    // Handle the movement of a piece on the canvas (called from the
    // previous function.
    var canvas = document.getElementById('mycanvas');
    var origX = obj.x;
    var origY = obj.y;
    canvas.onmousemove = function(e) {
        var moveX = e.offsetX;
        var moveY = e.offsetY;
        var diffX = moveX-dwnX;
        var diffY = moveY-dwnY;
        obj.x = origX+diffX;
        obj.y = origY+diffY;
    }
    canvas.onmouseup = function() {
        var tx = locAdjust(obj.x);
        var ty = locAdjust(obj.y);
        cleanPrev(tx,ty);
        obj.x = tx;
        obj.y = ty;
        canvas.onmousemove = function(){};
    }
}

/**********************************************************************
 *
 * Support functions
 *
 **********************************************************************/
function cleanPrev(x,y) {
    // When a piece is placed on a square, make sure that the previous
    // piece is removed from imageStack.
    for(var v = 0,len = imageStack.length; v < len; v++) {
        var obj = imageStack[v];
        if (obj.x == x && obj.y == y) {
            imageStack.splice(v,1);
        }
    }
}

function locAdjust(x) {
    // Align a dropped piece to be on a sqaure.
    var v = x + 30;
    var soff = Math.floor(v / 60);
    v = soff * 60;
    v += 4 - soff;
    return v;
}

/**********************************************************************
 *
 * THe rest of these functions support I/O to and from the server
 *
 **********************************************************************/
function convertCanvasToBoard()
{
    // Generate a message to the the server.
    // The string sent is a slash separated set of text consisting of the
    // number of moves, white piece positions, and black piece positions.
    // See chess.py for more details
    var movez = document.getElementById('moves');
    var black = [];
    var white = [];
    var matein = movez.value.toString();
    for(var x = 0,len = imageStack.length; x < len; x++) {
        var obj = imageStack[x];
        var piece = obj.image.id.slice(-1);
        var pattrn = "123456";
        if (pattrn.indexOf(piece) < 0) {
            pattrn = "ABCDEF";
        }
        var numb = pattrn.indexOf(piece);
        var dpiece = "PNBRQK".substr(numb, 1);
        var ploc = [];
        if (numb > 0) {
            ploc.push(dpiece);
        }
        var xind = Math.floor((obj.x + 30) / 60);
        ploc.push("abcdefgh".substr(xind,1));
        var yind = Math.floor((obj.y + 30) / 60);
        yind = 8 - yind;
        ploc.push(yind.toString());
        pdata = ploc.join("");
        if (pattrn.startsWith('A')) {
            black.push(pdata);
        }
        else {
            white.push(pdata);
        }
    }
    wstr = ["W:", white.join(",")].join("");
    bstr = ["B:", black.join(",")].join("");
    ostr = [matein, wstr, bstr,].join("/");
    cmdstr = 'data='+ostr;
    server = new XMLHttpRequest();
    sendpost(cmdstr, 'chess.py', server, hndl_svr_resp);
}

function sendpost(postdata, remProg, server, server_sent_response) {
    //
    // Handle the sending of a request across the net
    //
    server.onreadystatechange = server_sent_response;
    server.open("POST", remProg, true);
    server.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    server.setRequestHeader("Content-length", postdata.length);
    server.setRequestHeader("Connection", "close");
    server.send(postdata);
}

function hndl_svr_resp() {
    //
    // When the server responds, display the output in a modal dialog.
    // The response is an or-bar separated set of fields.  See chess.py
    // for a further description of the format
    //
    if (server.readyState==4 && server.status==200)
    {
        var mparts = server.responseText.split("|");
        $("<div>"+mparts[1]+"</div>").dialog(
            {modal: true, height: mparts[2], width: mparts[3], title: mparts[0]});
    }
}

    //
    // Returns for the chessNamespace wrapper
    //
    return {
        startMe:startMe,
        drag:drag,
        drop:drop,
        allowDrop:allowDrop,
        convertCanvasToBoard:convertCanvasToBoard
    };
}();
