/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/

commonNamespace = function() {
/**********************************************************************
 *
 * commonNamespace
 *
 * functions in this namespace are general routines that can be used by
 * more than one program in toybox.  Most of these are display routines or
 * coordinate conversion routines.  The general data that will be supplied
 * by another program would be a graphics context, a canvas, and horiziontal
 * and vertical dimensions of the display.
 *
 **********************************************************************/

var SIZE_EDGE = 10;             // Width of border
var SIZE_CELL = 40;             // Size of square
var X_CHAR_OFF = 11;            // Character offset in cell
var Y_CHAR_OFF = 31;            // Character offset in cell

var context;
var canvas;
var xdim;
var ydim;

function init(gcontext, gcanvas, x_dim, y_dim) {
    //
    // Initialize immutable values
    //
    context = gcontext;
    canvas = gcanvas;
    xdim = x_dim;
    ydim = y_dim;
}

function getSizes() {
    //
    // Return display related data (used to pass cell size information
    // back to a program
    //
    return [SIZE_EDGE, SIZE_CELL];
}

function getDispPos() {
    //
    // Handle a button click event by returning a cell adjusted
    // location (a click within the range of what is square 0,0 will
    // return coordinates of 0,0.
    var x = event.clientX + document.body.scrollLeft +
            document.documentElement.scrollLeft;
    var y = event.clientY + document.body.scrollTop +
            document.documentElement.scrollTop;
    x -= canvas.offsetLeft;
    y -= canvas.offsetTop;
    var xx = Math.floor((x - SIZE_EDGE) / SIZE_CELL);
    var yy = Math.floor((y - SIZE_EDGE) / SIZE_CELL);
    return [xx, yy]
}

function convert2sq(indx) {
    //
    // Given a pixel address, return square location in grid (local routine)
    //
    var retv = (indx * SIZE_CELL) + SIZE_EDGE + 1;
    var sizev = SIZE_CELL - 1;
    if (indx % 3 === 0) {
        retv += 1;
        sizev -= 1;
    }
    return [retv, sizev];
}

function setText(color, xparm, yparm, dispval) {
    //
    // Set dispval in the grid
    //
    context.font = '30px Arial';
    context.fillStyle = color;
    var xinfo = convert2sq(xparm);
    var yinfo = convert2sq(yparm);
    context.fillText(dispval, xinfo[0] + X_CHAR_OFF, yinfo[0] + Y_CHAR_OFF);
}

function colorSquare(color, xval, yval) {
    //
    // Color the square indicated by the xval and yval
    // parameters with the color indicated by the color
    // parameter.
    //
    context.fillStyle = color;
    if (xval < 0 || xval >= xdim || yval < 0 || yval >= ydim) {
        return;
    }
    var xinfo = convert2sq(xval);
    var yinfo = convert2sq(yval);
    context.fillRect(xinfo[0], yinfo[0], xinfo[1], yinfo[1]);
}

function sendpost(postdata, remProg, server, server_sent_response) {
    //
    // Handle the sending of a request across the net
    //
    server.onreadystatechange = server_sent_response;
    server.open("POST", remProg, 1);
    server.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    server.setRequestHeader("Content-length", postdata.length);
    server.setRequestHeader("Connection", "close");
    server.send(postdata);
}

    //
    // External entry points
    //
    return {
        init:init,
        getSizes:getSizes,
        getDispPos:getDispPos,
        setText:setText,
        colorSquare:colorSquare,
        sendpost:sendpost
    };
}();
