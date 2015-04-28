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
 *   board -- user's representation of the sudoku board. A 9x9 array
 *            of blanks and digits.
 *   lastx -- x-coordinate of the last key-click
 *   lasty -- y-coordinate of the last key-click
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
var SIZE_EDGE = 10;             // Width of border
var SIZE_CELL = 40;             // Size of Sudoku Square
var X_CHAR_OFF = 11;            // Character offset in cell
var Y_CHAR_OFF = 31;            // Character offset in cell
var ONE_CHAR = 49;              // Keycode for '1'
var NINE_CHAR = 57;             // Keycode for '9'
var BLANK_CHAR = 32;            // Keycode for ' '

//
// Values that will be modified.
//
var canvas;
var context;
var board = [];
var groups = [];
var lastx = SUDOKU_SIZE;
var lasty = SUDOKU_SIZE;
var server;
//

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
    drawBoard();
    cleanBoard();
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
        alert('Not enough numbers provided');
        return;
    }
    findSol(board);
}

function cleanBoard() {
    //
    // Remove all entries from the display and from the local board
    //
    board = [];
    for (var i = 0; i < SUDOKU_SIZE; i++) {
        board[i] = [];
        for (var j = 0; j < SUDOKU_SIZE; j++) {
            board[i].push(' ');
            colorSquare(WHITE_BG, i, j);
        }
    }
}

function cleanOther() {
    //
    // Clear the board of all computer generated data
    //
    if (lastx < SUDOKU_SIZE  && lastx >= 0 && lasty < SUDOKU_SIZE && lasty >= 0) {
        setNumbers(board[lastx][lasty], WHITE_BG);
    }
    for (var i = 0; i < SUDOKU_SIZE; i++) {
        for (var j = 0; j < SUDOKU_SIZE; j++) {
            colorSquare(WHITE_BG, i, j);
            setText(BLACK_FG, i, j, board[i][j]);
        }
    }
}

function help() {
    //
    // Display the help message (gotten from HTML data)
    // in a dialog.  Toggles on and off on subsequent
    // calls.
    //
    var helpmessage = document.getElementById("helpme");
    var helpbtn = document.getElementById("helpbutton");
    if (helpbtn.textContent == "HELP") {
        helpbtn.textContent = "CLOSE";
        helpmessage.show();
    }
    else {
        helpbtn.textContent = "HELP";
        helpmessage.close();
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
    var x = event.clientX + document.body.scrollLeft +
            document.documentElement.scrollLeft;
    var y = event.clientY + document.body.scrollTop +
            document.documentElement.scrollTop;
    x -= canvas.offsetLeft;
    y -= canvas.offsetTop;
    var xx = Math.floor((x - SIZE_EDGE) / SIZE_CELL);
    var yy = Math.floor((y - SIZE_EDGE) / SIZE_CELL);
    if (xx >= SUDOKU_SIZE  || xx < 0 || yy >= SUDOKU_SIZE || yy < 0) {
        return;
    }
    if (lastx < SUDOKU_SIZE  && lastx >= 0 && lasty < SUDOKU_SIZE && lasty >= 0) {
        setNumbers(board[lastx][lasty], WHITE_BG);
    }
    lastx = xx;
    lasty = yy;
    setNumbers(board[lastx][lasty], YELLOW);
}

function doKeyDown(event) {
    //
    // Handle keyboard input, skipping invalid keys.
    // Add new character to grid.
    //
    if (lastx < 0 || lastx >= SUDOKU_SIZE || lasty < 0 || lasty >= SUDOKU_SIZE) {
        return;
    }
    if (event.keyCode < ONE_CHAR || event.keyCode > NINE_CHAR) {
        if (event.keyCode != BLANK_CHAR) {
            return;
        }
    }
    var charv = String.fromCharCode(event.keyCode);
    setNumbers(charv, YELLOW);
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
    var p = SIZE_EDGE;
    var ssize = SUDOKU_SIZE * SIZE_CELL;
    for (var x = 0; x <= ssize; x += SIZE_CELL) {
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

function convertLoc(indx) {
    //
    // Given a pixel address, return square location in grid.
    //
    var retv = (indx * SIZE_CELL) + SIZE_EDGE + 1;
    var sizev = SIZE_CELL - 1;
    if (indx % 3 === 0) {
        retv += 1;
        sizev -= 1;
    }
    return [retv, sizev];
}

function colorSquare(color, xval, yval) {
    //
    // Color the square indicated by the xval and yval
    // parameters with the color indicated by the color
    // parameter.
    //
    context.fillStyle = color;
    if (xval < 0 || xval >= SUDOKU_SIZE || yval < 0 || yval >= SUDOKU_SIZE) {
        return;
    }
    var xinfo = convertLoc(xval);
    var yinfo = convertLoc(yval);
    context.fillRect(xinfo[0], yinfo[0], xinfo[1], yinfo[1]);
}

function setNumbers(charv1, color) {
    //
    // Set the character in charv1 as a square value, after
    // setting the square's color to the color parameter.
    //
    colorSquare(color, lastx, lasty);
    setText(BLACK_FG, lastx, lasty, charv1);
    board[lastx][lasty] = charv1;
}

function setText(color, xparm, yparm, dispval) {
    //
    // Set dispval in the grid
    //
    context.font = '30px Arial';
    context.fillStyle = color;
    var xinfo = convertLoc(xparm);
    var yinfo = convertLoc(yparm);
    context.fillText(dispval, xinfo[0] + X_CHAR_OFF, yinfo[0] + Y_CHAR_OFF);
}
//

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
    // Step 3: Highlight the bad cells in red and alert the user if
    //         any invalid entries are found.  Return true if everything
    //         is valid.
    //
    var loc_array = {};
    for (var i=0; i < SUDOKU_SIZE; i++) {
        for (var j=0; j < SUDOKU_SIZE; j++) {
            chr = board[i][j];
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
            colorSquare(LIGHTRED, tmp_x, tmp_y);
            setText(BLACK_FG, tmp_x, tmp_y, board[tmp_x][tmp_y]);
        }
        alert('Input is invalid.  Check the squares marked in red');
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
    sendpost(cmdinfo);
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
            if (board[i][j] !== ' ') {
                givens++;
            }
        }
    }
    if (givens < 17) {
        return true;
    }
    return false;
}

function server_sent_response() {
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
                if (board[i][j] === ' ') {
                    setText(BLUE, i, j, answer[indx]);
                }
                if (answer[indx] == ' ') {
                    complain = true;
                }
                indx++;
            }
        }
        if (complain) {
            alert('No complete solution could be found');
        }
    }
}

function sendpost(postdata) {
    //
    // Handle the sending of a request across the net
    //
    server = new XMLHttpRequest();
    server.onreadystatechange = server_sent_response;
    server.open("POST", "sudoku.py", 1);
    server.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    server.setRequestHeader("Content-length", postdata.length);
    server.setRequestHeader("Connection", "close");
    server.send(postdata);
}

//
// Returns for SudokuNamespace wrapper
//
    return {
        sudoku:sudoku,
        solver:solver,
        cleanBoard:cleanBoard,
        cleanOther:cleanOther,
        help:help
    };
}();


// Jquery code to handle HELP button
$(document).ready(function(){
    $("#helpbutton").click(function(){
        $("#helpme").toggle();
    });
});
