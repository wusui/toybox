/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/

sudokuNamespace = function() {
/**********************************************************************
 *
 * Sudoku solver -- sudokuNamespace
 *
 * The general layout of this program is:
 *   1. Entry points.  Functions called from the HTML code.
 *   2. Event handlers.  Mouse click and Key click event handlers.
 *   3. GUI Utilities.
 *   4. Functions that solve the puzzle.
 *
 * Global variables (SudokuNamespace-wide variables):
 *   canvas -- canvas declared in HTML
 *   context -- 2d context derived from canvasname
 *   size_edge -- pixel size of edge
 *   size_cell -- pixel size of cell
 *   server -- http server variable used for POST
 *
 * The layout of the 9x9 board array is from left to right, top to
 * bottom.  The upper-left square is at 0,0.
 *
 **********************************************************************/
//
// Constants
//
var SUDOKU_SIZE = 9;            // Board size, largest number value
var WHITE_BG = '#FFFFFF';       // White (used in background)
var BLACK_FG = '#000000';       // Black (used in numbers)
var YELLOW = '#FFFF00';         // High-lighter
var LIGHTRED = '#FF8080';       // Bad entry indicator
var BLUE = '#0000FF';           // Square found by solver
var ONE_CHAR = 49;              // Keycode for '1'
var NINE_CHAR = 57;             // Keycode for '9'
var BLANK_CHAR = 32;            // Keycode for ' '
var EDGE_SIZE = 10;             // Border around grid.

//
// Values that will be modified.
//
var canvas;
var context;
var size_edge;
var size_cell;
var server;

/**********************************************************************
 *
 * Entry points:
 *     sudoku -- primary entry point (from body of html)
 *     solver -- entry point from SOLVE button
 *     cleanBoard -- entry point from ERASE button (also called
 *                   from sudoku().)
 *     cleanOther -- entry point from CLEAN button.
 *     help -- entry point from HELP button.
 *
 **********************************************************************/

function sudoku(){
    //
    // Initialize canvas and context
    // Draw the layout on the canvas, initialize board
    // Setup event handlers
    //
    canvas = document.getElementById('mycanvas');
    canvas.setAttribute("tabindex", 0);
    context = canvas.getContext('2d');
    commonNamespace.init(context, canvas, SUDOKU_SIZE, SUDOKU_SIZE, EDGE_SIZE);
    dims = commonNamespace.getSizes();
    size_edge = dims[0];
    size_cell = dims[1];
    drawBoard();
    commonNamespace.cleanBoard(SUDOKU_SIZE, SUDOKU_SIZE);
    canvas.addEventListener("mousedown", getPosition, false);
    canvas.addEventListener("keydown", doKeyDown, false);
}

function solver() {
    //
    // Make sure user input has no errors.
    // Call solver routine.
    // If solution is found, store results on canvas.
    //
    if (!validate()) {
        return;
    }
    cleanOther();
    if (not_enough_givens()) {
        $("<div>Not enough numbers provided</div>").dialog(
            {modal: true, height: 100, width: 320, title: 'INPUT ERROR'});
        return;
    }
    findSol(commonNamespace.allBoard());
}

function cleanBoard() {
    //
    // Remove all entries from the display and from the local board
    //
    commonNamespace.cleanBoard(SUDOKU_SIZE, SUDOKU_SIZE);
}

function cleanOther() {
    //
    // Clear the board of all computer generated data
    //
    commonNamespace.clearSquare(SUDOKU_SIZE, SUDOKU_SIZE);
    for (var i = 0; i < SUDOKU_SIZE; i++) {
        for (var j = 0; j < SUDOKU_SIZE; j++) {
            commonNamespace.colorSquare(WHITE_BG, i, j);
            commonNamespace.setText(BLACK_FG, i, j, commonNamespace.getBoard(i, j));
        }
    }
}

function help() {
    //
    // Display the help message (gotten from HTML data)
    // in a dialog.  Toggles on and off on subsequent
    // calls.
    //
    var helpbtn = document.getElementById("helpbutton");
    if (helpbtn.textContent == "HELP") {
        helpbtn.textContent = "CLOSE";
    }
    else {
        helpbtn.textContent = "HELP";
    }
}
//

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
    coords = commonNamespace.getDispPos();
    if (coords[0] >= SUDOKU_SIZE  || coords[0] < 0 || coords[1] >= SUDOKU_SIZE || coords[1] < 0) {
        return;
    }
    commonNamespace.clearSquare(SUDOKU_SIZE, SUDOKU_SIZE);
    commonNamespace.setLast(coords[0], coords[1]);
    commonNamespace.setValue(commonNamespace.getBoard(coords[0], coords[1]), YELLOW);
}

function doKeyDown(event) {
    //
    // Handle keyboard input, skipping invalid keys.
    // Add new character to grid.
    //
    if (commonNamespace.outaBounds(SUDOKU_SIZE, SUDOKU_SIZE)) {
        return;
    }
    if (event.keyCode < ONE_CHAR || event.keyCode > NINE_CHAR) {
        if (event.keyCode != BLANK_CHAR) {
            return;
        }
    }
    var charv = String.fromCharCode(event.keyCode);
    commonNamespace.setValue(charv, YELLOW);
}
//

/**********************************************************************
 *
 * GUI Utilities
 *
 **********************************************************************/

function drawBoard(){
    //
    // Draw the 9x9 sudoku grid (complicated by drawing thick 3x3 lines)
    //
    var p = size_edge;
    var ssize = SUDOKU_SIZE * size_cell;
    for (var x = 0; x <= ssize; x += size_cell) {
        if (x % (ssize / 3) === 0) {
            context.fillRect(x+p, p, 2, ssize);
            context.fillRect(p, x+p, ssize+2, 2);
            continue;
        }
        context.moveTo(0.5 + x + p, p);
        context.lineTo(0.5 + x + p, ssize + p);
        context.moveTo(p, 0.5 + x + p);
        context.lineTo(ssize + p, 0.5 + x + p);
    }
    context.strokeStyle = "black";
    context.stroke();
}


/**********************************************************************
 *
 * Solver Functions
 *
 **********************************************************************/
function validate() {
    //
    // Make sure that the board is valid.
    //
    // Step 1: Initialize loc_array -- Loc_array will be indexed
    //         by number value, and will contain entries for each
    //         cell having that value.  The cell entries will consist
    //         of 3 items -- the x-coordinate of the cell,
    //         the y-coordinate of the cell, and a numeric
    //         representation of that cell's 3x3 square.
    // Step 2: Initialize bad_ones -- Find every cell that is on the same
    //         same row, column, or in the same 3x3 square as another
    //         cell with the same numeric value.  These cells (with
    //         duplicate entries), get pushed onto bad_ones.
    // Step 3: Highlight the bad cells in red and tell the user if
    //         any invalid entries are found.  Return true if everything
    //         is valid.
    //
    var loc_array = {};
    for (var i=0; i < SUDOKU_SIZE; i++) {
        for (var j=0; j < SUDOKU_SIZE; j++) {
            chr = commonNamespace.getBoard(i, j);
            if (chr != ' ') {
                sqloc = get3x3number(i, j);
                if (loc_array[chr] === undefined) {
                    loc_array[chr] = [[i,j,sqloc]];
                }
                else {
                    loc_array[chr].push([i,j,sqloc]);
                }
            }
        }
    }
    var bad_ones = [];
    for (key in loc_array) {
        lsize = loc_array[key].length;
        xchkr = [{}, {}, {}];
        for (var ii=0; ii < lsize; ii++) {
            for (var k=0; k < 3; k++) {
                viq = loc_array[key][ii][k];
                if (xchkr[k][viq] === undefined) {
                    xchkr[k][viq] = [loc_array[key][ii]];
                }
                else {
                    xchkr[k][viq].push(loc_array[key][ii]);
                }
            }
        }
        for (var kk=0; kk < 3; kk++) {
            for (skey in xchkr[kk]) {
                if (xchkr[kk][skey].length > 1) {
                    for (var v=0; v<xchkr[kk][skey].length; v++) {
                        bad_ones.push(xchkr[kk][skey][v]);
                    }
                }
            }
        }
    }
    if (bad_ones.length > 0) {
        for (var i2=0; i2<bad_ones.length; i2++) {
            var tmp_x = bad_ones[i2][0];
            var tmp_y = bad_ones[i2][1];
            commonNamespace.colorSquare(LIGHTRED, tmp_x, tmp_y);
            commonNamespace.setText(BLACK_FG, tmp_x, tmp_y, commonNamespace.getBoard(tmp_x, tmp_y));
        }
        $("<div>Input is invalid.  Check the squares marked in red</div>").dialog(
            {modal: true, height: 100, width: 500, title: 'INPUT ERROR'});
        return false;
    }
    return true;
}

function findSol(inboard) {
    //
    // Marshall the board into a string of values and POST it.
    //
    var columns = [];
    for (var i=0; i < SUDOKU_SIZE; i++) {
        var compress = inboard[i].join('');
        columns.push(compress);
    }
    var allcells = columns.join('');
    var cmdinfo = 'data=' + allcells;
    server = new XMLHttpRequest();
    commonNamespace.sendpost(cmdinfo, 'sudoku.py', server, hndl_svr_resp);
}

function get3x3number(xparm, yparm) {
    //
    // Get the 3x3 square number of the cell specified
    //
    var xval = Math.floor(xparm / 3);
    var yval = Math.floor(yparm / 3);
    return xval * 3 + yval;
}

function not_enough_givens() {
    //
    // Seventeen is the minimum number of set values in a solvable
    // sudoku.  Make sure we have at least that many values.
    //
    var givens = 0;
    for (var i=0; i<SUDOKU_SIZE; i++) {
        for (var j=0; j<SUDOKU_SIZE; j++) {
            if (commonNamespace.getBoard(i, j) !== ' ') {
                givens++;
            }
        }
    }
    if (givens < 17) {
        return true;
    }
    return false;
}

function hndl_svr_resp() {
    //
    // Handle the response from the net.  Fill in the
    // grid if a solution is returned.
    //
    if (server.readyState==4 && server.status==200)
    {
        var answer = server.responseText.split("");
        var indx = 0;
        var complain = false;
        for (var i=0; i<SUDOKU_SIZE; i++) {
            for (var j=0; j<SUDOKU_SIZE; j++) {
                if (commonNamespace.getBoard(i, j)  === ' ') {
                    commonNamespace.setText(BLUE, i, j, answer[indx]);
                }
                if (answer[indx] == ' ') {
                    complain = true;
                }
                indx++;
            }
        }
        if (complain) {
            $("<div>No complete solution could be found</div>").dialog(
               {modal: true, height: 100, width: 400, title: 'INPUT ERROR'});
        }
    }
}

//
// Returns for SudokuNamespace wrapper
//
    return {
        sudoku:sudoku,
        solver:solver,
        cleanBoard:cleanBoard,
        cleanOther:cleanOther,
        help:help,
        hndl_svr_resp:hndl_svr_resp
    };
}();


// Jquery code to handle HELP button
$(document).ready(function(){
    $("#helpbutton").click(function(){
        $("#helpme").toggle();
    });
});
