pentominoNamespace = function() {
var canvas;
var context;
var counter;
var dtime;
var stopped;
var timert;
var pentsize;
var solutions;
var solstring;
var solindex;
var solstep;
var outstring;
var palette;
var pletters;

function pentomino(){
    canvas = document.getElementById('mycanvas');
    context = canvas.getContext('2d');
    context.font = "30px Arial";
    counter = 0;
    stopped = true;
    pentsize = 0;
    timert = -1;
    palette = ["#c4453f", "#70cd57", "#9846cf", "#cbca57", "#5a4ca1", "#c18340", "#7c9ac3", "#c5579d", "#86ccaf", "#4f3040", "#cb9b9c", "#50643a"];
    pletters = 'pnuylvitzfwx';
    get_solutions();
}

function get_solutions() {
    solutions = [];
    var template = ['http://www.warrensusui.com/toybox/src/pentomino/normal/output.', '0', '.txt'];
    for (i=3; i<7; i++) {
        template[1] = i.toString();
        jQuery.get(template.join(''), function(data) {
            solutions.push(data);
        });
    }
}

function radioget() {
    var rbuttons = document.getElementsByName('radioradio');
    for (var i=0; i < rbuttons.length; i++) {
        if (rbuttons[i].checked) {
            return i+3;
        }
    }
    return 0;
}

function stepdisp() {
    var pntval = radioget();
    if (pntval !== pentsize) {
        stopped = true;
        pentsize = pntval;
        if (timert >= 0) {
            clearInterval(timert);
        }
        counter = 0;
        context.clearRect(0,0,840,420);
        solindex = 0;
        solstep = 61 + pentsize;
        solstring = solutions[pentsize-3];
    }
    if (solindex >= solstring.length) {
        return;
    }
    outstring = solstring.substring(solindex,solindex+solstep);
    outstring = outstring.replace(/\s+/g,'');
    solindex += solstep;
    counter++;
    context.clearRect(0,0,840,420)
    context.textAlign = "center";
    context.fillStyle = "#000000";
    context.fillText(counter,420,400);
    drawfigure();
}

function drawfigure() {
    context.textAlign = "left";
    var tot_cols = 60 / pentsize;
    var tot_rows = pentsize;
    var lpos = (840 - tot_cols*40)/2;
    var upos = (400 - tot_rows*40)/2;
    for (var i=0; i<tot_rows; i++) {
        for (var j=0; j<tot_cols; j++) {
            var lindx = i * tot_cols + j;
            context.beginPath();
            context.rect(lpos+j*40, upos+i*40, 40, 40);
            context.fillStyle = palette[pletters.indexOf(outstring.substring(lindx,lindx+1))];
            context.fill();
        }
    }
}

function startdisp() {
    var dtime = document.getElementById("pslider").value;
    if (stopped) {
        stopped = false;
        timert = setInterval(stepdisp, dtime * 1000);
    }
    else {
        stopped = true;
        clearInterval(timert);
    }
}
    return {
        pentomino:pentomino,
        startdisp:startdisp,
        stepdisp:stepdisp,
    };
}();
