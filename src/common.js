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

var SIZE_CELL = 40;             // Size of square
var X_CHAR_OFF = 11;            // Character offset in cell
var Y_CHAR_OFF = 31;            // Character offset in cell
var WHITE_BG = '#FFFFFF';       // White (used in background)
var BLACK_FG = '#000000';       // Black (used in numbers)

var context;
var canvas;
var edge_size;
var xdim;
var ydim;
var board = [];
var lastx;
var lasty;
var cadjust = { 'M': 4, 'W': 6, 'I' : -5, 'N' : 2, 'Q' : 2, 'G' : 3, 'D' : 2};

function init(gcontext, gcanvas, x_dim, y_dim, edge) {
    //
    // Initialize immutable values
    //
    context = gcontext;
    canvas = gcanvas;
    xdim = x_dim;
    ydim = y_dim;
    edge_size = edge;
    setLast(x_dim, y_dim);
}

function setLast(xval, yval) {
    //
    // Save global coordinate values last used.
    //
    lastx = xval;
    lasty = yval;
}

function getSizes() {
    //
    // Return display related data (used to pass cell size information
    // back to a program
    //
    return [edge_size, SIZE_CELL];
}

function clearSquare(xmax, ymax) {
    //
    // Clear a square on the display
    //
    if (lastx < xmax  && lastx >= 0 && lasty < ymax && lasty >= 0) {
        setValue(commonNamespace.getBoard(lastx, lasty), WHITE_BG);
    }
}

function cleanBoard(xsize, ysize) {
    //
    // Remove all entries from the display and from the local board
    //
    board = [];
    for (var i = 0; i < ysize; i++) {
        board[i] = [];
        for (var j = 0; j < xsize; j++) {
            board[i].push(' ');
            colorSquare(WHITE_BG, i, j);
        }
    }
}

function allBoard() {
    //
    // Return the whole board
    //
    return board;
}

function getBoard(xcoord, ycoord) {
    //
    // Return the contents of a square
    //
    return board[xcoord][ycoord];
}

function setBoard(value, xcoord, ycoord) {
    //
    // Set a square on the board
    //
    board[xcoord][ycoord] = value;
}

function outaBounds(xbound, ybound) {
    //
    // Return true if click is outside of input grid
    //
    return (lastx < 0 || lastx >= xbound || lasty < 0 || lasty >= ybound) 
}

function gotoNext() {
    //
    // Skip to the next square on the grid
    //
    lastx++;
    if (outaBounds(xdim, ydim)) {
        lastx = 0;
        lasty++;
        if (outaBounds(xdim, ydim)) {
            lasty = 0;
        }
    }
    return [lastx, lasty];
}

function setValue(charv1, color) {
    //
    // Set the character in charv1 as a square value, after
    // setting the square's color to the color parameter.
    //
    colorSquare(color, lastx, lasty);
    setText(BLACK_FG, lastx, lasty, charv1);
    setBoard(charv1, lastx, lasty);
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
    var xx = Math.floor((x - edge_size) / SIZE_CELL);
    var yy = Math.floor((y - edge_size) / SIZE_CELL);
    return [xx, yy]
}

function convert2sq(indx) {
    //
    // Given a pixel address, return square location in grid (local routine)
    //
    var retv = (indx * SIZE_CELL) + edge_size + 1;
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
    if (dispval in cadjust) {
        xinfo[0] -= cadjust[dispval];
    }
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
        setLast:setLast,
        getSizes:getSizes,
        clearSquare:clearSquare,
        cleanBoard:cleanBoard,
        allBoard:allBoard,
        getBoard:getBoard,
        setBoard:setBoard,
        outaBounds:outaBounds,
        gotoNext:gotoNext,
        setValue:setValue,
        getDispPos:getDispPos,
        setText:setText,
        colorSquare:colorSquare,
        sendpost:sendpost
    };
}();
