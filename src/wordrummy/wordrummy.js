/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/

wordrummyNamespace = function() {
/**********************************************************************
 *
 * Word Rummy solver -- wordrummyNamespace
 *
 * The general layout of this program is:
 *   1. Entry points.  Functions called from the HTML code.
 *   2. Event handlers.  Mouse click and Key click event handlers.
 *   3. GUI Utilities.
 *
 * Global variables (SudokuNamespace-wide variables):
 *   canvas -- canvas declared in HTML
 *   context -- 2d context derived from canvasname
 *   size_edge -- pixel size of edge
 *   size_cell -- pixel size of cell
 *   psuits -- suits that get printed in the display
 *   server -- http server variable used for POST
 *
 * The layout of the 13x4 board array is from left to right, top to
 * bottom.  The upper-left square is at 0,0.
 *
 **********************************************************************/
//
// Constants
//
var X_SIZE = 13;
var Y_SIZE = 4;
var ULC_OFFSET = 90;
var LEFT_COL = 60;
var RIGHT_COL = 620;
var TOP_ROW = 85;
var BOT_ROW = 280;
var COL_START = 120;
var ROW_START = 100;
var WHITE_BG = '#FFFFFF';       // White (used in background)
var YELLOW = '#FFFF00';         // High-lighter

//
// Values that will be modified.
//
var canvas;
var context;
var size_edge;
var size_cell;
var psuits;
var server;

/**********************************************************************
 *
 * Entry points:
 *     wordrummy -- primary entry point (from body of html)
 *     solver -- entry point from SOLVE button
 *     hndl_svr_resp -- server  response handler
 *
 **********************************************************************/

function wordrummy(){
    //
    // Initialize canvas and context
    // Draw the layout on the canvas, initialize board
    // Setup event handlers
    //
    canvas = document.getElementById('mycanvas');
    canvas.setAttribute("tabindex", 0);
    context = canvas.getContext('2d');
    commonNamespace.init(context, canvas, X_SIZE, Y_SIZE, ULC_OFFSET);
    dims = commonNamespace.getSizes();
    size_edge = dims[0];
    size_cell = dims[1];
    suits = [9824, 9829, 9830, 9827];
    psuits = [];
    for (var i in suits) {
        psuits.push(String.fromCharCode(suits[i]));
    }
    drawBoard();
    commonNamespace.cleanBoard(Y_SIZE, X_SIZE);
    canvas.addEventListener("mousedown", getPosition, false);
    canvas.addEventListener("keydown", doKeyDown, false);
}

function solver() {
    //
    // Solver button has been clicked on.
    // 
    // Make sure that the board is completely filled
    // Send data to the server as rows of letters concatenated together
    //
    var inboard = commonNamespace.allBoard();
    oboard = []
    for (var j=0; j < Y_SIZE; j++) {
        oboard.push([])
    }
    for (var i=0; i < X_SIZE; i++) {
        for (var j=0; j < Y_SIZE; j++) {
            if (inboard[i][j] == ' ') {
                $("<div>Grid is not filled.</div>").dialog({modal: true,
                    height: 100, width: 400, title: 'INPUT ERROR'});
                return;
            }
            oboard[j].push(inboard[i][j]);
        }
    }
    var compress = oboard[0].join('');
    var columns = [];
    for (var i=0; i < Y_SIZE; i++) {
        var compress = oboard[i].join('');
        columns.push(compress);
    }
    var allcells = columns.join('');
    var cmdinfo = 'data=' + allcells;
    server = new XMLHttpRequest();
    commonNamespace.sendpost(cmdinfo, 'wordrummy.py', server, hndl_svr_resp);
}

function hndl_svr_resp() {
    //
    // Get input (from solver) and draw on screeen.
    //
    if (server.readyState==4 && server.status==200)
    {
        document.getElementById('answer').innerHTML = server.responseText;
    }
}

/**********************************************************************
 *
 * Event Handlers
 *     getPosition -- handle mouse click
 *     doKeyDown -- handle keyboard input
 *
 **********************************************************************/

function getPosition(event) {
    //
    // Mouse click handler
    //     Convert mouse click coordinates to location on the grid.
    //     Un-highlight the previous location.
    //     Highlight the new location.
    //
    document.getElementById('answer').innerHTML = '';
    coords = commonNamespace.getDispPos();
    commonNamespace.clearSquare(X_SIZE, Y_SIZE);
    commonNamespace.setLast(coords[0], coords[1]);
    if (commonNamespace.outaBounds(X_SIZE, Y_SIZE)) {
        return;
    }
    commonNamespace.setValue(commonNamespace.getBoard(coords[0], coords[1]), YELLOW);
}

function doKeyDown(event) {
    //
    // Handle keyboard input, skipping invalid keys.
    // Add new character to grid.
    //
    if (commonNamespace.outaBounds(X_SIZE, Y_SIZE)) {
        return;
    }
    var inp = String.fromCharCode(event.keyCode).toUpperCase();
    if (/[A-Z ]/.test(inp)) {
        commonNamespace.setValue(inp, WHITE_BG);
        coords = commonNamespace.gotoNext();
        commonNamespace.setValue(commonNamespace.getBoard(coords[0], coords[1]), YELLOW);
    }
}

/**********************************************************************
 *
 * GUI Utilities (drawBoard and functions called from drawBoard)
 *
 **********************************************************************/

function drawBoard() {
    //
    // Draw the 13x4 word rummy grid
    //
    var p = size_edge;
    var ssize = Y_SIZE * size_cell;
    var wsize = X_SIZE * size_cell;
    for (var x = 0; x <= wsize; x += size_cell) {
        context.moveTo(0.5 + x + p, p);
        context.lineTo(0.5 + x + p, ssize + p);
    }
    for (var x = 0; x <= ssize; x += size_cell) {
        context.moveTo(p, 0.5 + x + p);
        context.lineTo(wsize + p, 0.5 + x + p);
    }
    context.strokeStyle = "black";
    context.stroke();
    context.font = "bolder 30px Arial";
    fillColumns(LEFT_COL);
    fillColumns(RIGHT_COL);
    fillRows(TOP_ROW);
    fillRows(BOT_ROW);
}

function fillColumns(xcoord) {
    //
    // Get suit text onto the canvas.
    //
    var yval = COL_START;
    for (var i in psuits) {
        context.fillText(psuits[i], xcoord, yval);
        yval += size_cell;
    }
}

function fillRows(ycoord) {
    //
    // Get card rank text onto the canvas.
    //
    var xval = ROW_START;
    var wrange = Array.apply(null, Array(X_SIZE)).map(function (_, i) {return i;});
    for (var i in wrange) {
        var last = parseInt(i) + 1;
        context.fillText('A23456789TJQK'.substring(i, last), xval, ycoord);
        xval += size_cell;
    }
}

//
// Returns for wordrummyNamespace wrapper
//
    return {
        wordrummy:wordrummy,
        solver:solver,
        hndl_svr_resp:hndl_svr_resp
    };
}();
