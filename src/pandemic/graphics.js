/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
graphNamespace = function() {

var SQUARESZ = 90;
var PICLEN = 990;
var CONTINGENCYCARD_LOC = 185;
var CSIZE = 40;
var COFFSZ = (SQUARESZ-CSIZE)/2;
var MIDSQ = SQUARESZ/2;
var HCSIZE = CSIZE/2;
var colors = ["#0000ff", "#000000", "#C08000", "#ff0000", '#00ff00'];

var ROLE_TXT = {'O': 'OPERATIONS EXPERT', 'R': 'RESEARCHER', 'M': 'MEDIC',
                'D': 'DISPATCHER', 'S': 'SCIENTIST',
                'Q': 'QUARANTINE SPECIALIST', 'C': 'CONTINGENCY PLANNER'};
var SPECIAL_CARDS = ['Quiet Night', 'Resillient Population', 'Forecast',
                     'Airlift', 'Government Grant'];
var canvas;
var canvas2;
var context;
var context2;
var context3;
var worldMap;

function draw_map() {
    for (var i=0; i < worldMap.length; i++) {
        drawCons(worldMap[i], true);
    }
    for (i=0; i < worldMap.length; i++) {
        drawCity(worldMap[i]);
    }
}

function get_role_text(indx) {
    return ROLE_TXT[indx];
}

var CITY_MAX = 48;
function draw_game_info() {
    var ginfo = gameobjsNamespace.get_game_info();
    context2.font="bold 18px Arial";
    var plist = [];
    var plen = [];
    for (var i=0; i < ginfo.players.length; i++) {
        plist[i] = get_role_text(ginfo.players[i].role);
        plen[i] = context2.measureText(plist[i]).width;
    }
    var dcards = [];
    var dcnum = [];
    for (i=0; i < ginfo.players.length; i++) {
        dcards.push([]);
        dcnum.push([]);
    }
    context3.font="bold 15px Arial";
    for (i=0; i < ginfo.players.length; i++) {
        var cards = ginfo.players[i].cards;
        cards.sort(function(a, b){return a-b;});
        for (var j=0; j < cards.length; j++) {
            var ctxt3f;
            if (cards[j] >= CITY_MAX) {
                ctxt3f = SPECIAL_CARDS[cards[j] - CITY_MAX];
            }
            else {
                ctxt3f = worldMap[cards[j]][1];
            }
            dcards[i].push(ctxt3f);
            dcnum[i].push(cards[j]);
            var tsize = context3.measureText(ctxt3f).width;
            if (tsize > plen[i]) {
                plen[i] = tsize;
            }
        }
    }
    var totlen = 0;
    for (i=0; i < ginfo.players.length; i++) {
        totlen += plen[i];
    }
    var spn = (PICLEN - totlen) / (ginfo.players.length + 1);
    var colhead = [];
    var spc = 0;
    for (i=0; i < ginfo.players.length; i++) {
        spc += spn;
        colhead.push(Math.floor(spc));
        spc += plen[i];
    }
    show_cards(ginfo, plist, colhead, dcnum, dcards);
    mark_research(ginfo);
    for (i=0; i < ginfo.germs.length; i++) {
        draw_germs(ginfo.germs[i]);
    }
    show_players(ginfo);
    ginfo.display = '';
    if (document.getElementById("playbyplay").checked) {
        ginfo.display += 'P';
    }
    if (document.getElementById("helpful").checked) {
        ginfo.display += 'H';
    }
    if (document.getElementById("careful").checked) {
        ginfo.display += 'C';
    }
    document.getElementById("stats").innerHTML = scoreboard(ginfo);
    context3.fillStyle = "#000000";
    context3.fillText("more stuff goes here",50,CONTINGENCYCARD_LOC);
    buttonsNamespace.checkBuild(ginfo);
    buttonsNamespace.checkHeal(ginfo);
    buttonsNamespace.checkCure(ginfo);
    if (document.getElementById("helpful").checked) {
        helpNamespace.help();
    }
}

var DCOUNT = 24;
var GERM_COUNT = 4;
function scoreboard(ginfo) {
    var dvector = [];
    for (var i=0; i < GERM_COUNT; i++) {
        dvector.push(0);
    }
    for (i=0; i < ginfo.germs.length; i++) {
        for (var j=0; j < GERM_COUNT; j++) {
            dvector[j] += ginfo.germs[i][1][j];
        }
    }
    var retv = "";
    for (i=0; i < GERM_COUNT; i++) {
        retv += score_pop(ginfo, i, DCOUNT-dvector[i]);
    }
    retv += '<BR><div class="xBLACK">OUTBREAKS: ';
    retv += ginfo.states.outbreak_count.toString();
    retv += '</div>';
    retv += '<div class="xBLACK">INFECTION RATE: ';
    retv += ginfo.states.infection_rate.toString();
    retv += '(';
    retv += ginfo.states.infection_count.toString();
    retv += ')</div>';
    retv += '<div class="xBLACK">CARDS LEFT: ';
    retv += ginfo.states.cards_left.toString();
    retv += '</div>';
    retv += '<div class="xBLACK">RESEARCH STATIONS: ';
    retv += ginfo.states.research_stations.length.toString();
    retv += '</div>';
    retv += '<BR><div class="xBLACK">ACTIONS LEFT: ';
    retv += gameobjsNamespace.gpmoves().toString();
    retv += '</div>';
    retv += '<div class="xBLACK">PLAYER: #';
    var plm = ginfo.states.turn + 1;
    retv += plm.toString();
    retv += '</div>';
    return retv;
}

var DCOLORS = ['BLUE', 'BLACK', 'YELLOW', 'RED'];
var STATES = ['ACTIVE', 'CURED', 'ERADICATED'];
function score_pop(ginfo, germ, count) {
    var retv = '<div class="x';
    var part2 = '">';
    var part3 = '</div>';
    var stat = STATES[ginfo.states.disease_status[germ]];
    var numbr = count.toString();
    return retv + DCOLORS[germ] + part2 + DCOLORS[germ] + '/' + stat + ': ' + numbr + part3;
}

var VERT_OFF_PLAYR = 56;
var PL_XOFF = [ [], [], [3,23], [-1,13,27], [-7,7,21,35]];
function show_players(ginfo) {
    var leng = ginfo.players.length;
    context.font="bold 18px Arial";
    context.fillStyle = "#000000";
    for (var i=0; i < leng; i++) {
        var txt = ginfo.players[i].role;
        var pt = worldMap[ginfo.players[i].clocation][3];
        var x = pt[0] * SQUARESZ + COFFSZ + PL_XOFF[leng][i];
        var y = pt[1] * SQUARESZ + COFFSZ + VERT_OFF_PLAYR;
        context.fillText(txt,x,y);
    }
}

var VERT_ROLE_LOC = 20;
var VERT_CARD_LOC = 40;
var VERT_CARD_SIZE = 15;
var card_cols;
function show_cards(ginfo, plist, colhead, dcnum, dcards) {
    card_cols = colhead;
    for (var i=0; i < ginfo.players.length; i++) {
        context2.fillStyle = "#000000";
        context2.font="normal 15px Arial";
	if (i == ginfo.states.turn) {
            context2.font="bold 18px Arial";
        }
        context2.fillText(plist[i],colhead[i],VERT_ROLE_LOC);
        context2.font="bold 15px Arial";
        horz = VERT_CARD_LOC;
        for (var j=0; j < dcnum[i].length; j++) {
            context3.fillStyle=colors[Math.floor(dcnum[i][j]/12)];
            context3.fillText(dcards[i][j],colhead[i],horz);
            horz += VERT_CARD_SIZE;
        }
    }
}

function mark_research(ginfo) {
    for (var i=0; i < ginfo.states.research_stations.length; i++) {
        var tindx = ginfo.states.research_stations[i];
        var pt = worldMap[tindx][3];
        var x = pt[0] * SQUARESZ + COFFSZ + 1;
        var y = pt[1] * SQUARESZ + COFFSZ + 1;
        context.fillStyle = "#C0FFC0";
        context.fillRect(x, y, CSIZE-2, CSIZE-2);
    }
}

var GERM_SIZE = 6;
var GERM_OFFSET = 30;
var GERM_GAP = 2;
var GERM_SPACE = 10;
function draw_germs(vector) {
    var pt = worldMap[vector[0]][3];
    var x = pt[0] * SQUARESZ + COFFSZ + GERM_GAP;
    var y = pt[1] * SQUARESZ + COFFSZ + GERM_OFFSET;
    for (var i=0; i < GERM_COUNT; i++) {
        for (var j=0; j < vector[1][i]; j++) {
            context.fillStyle = colors[i];
            context.fillRect(x, y, GERM_SIZE, GERM_SIZE);
            y -= GERM_SPACE;
        }
        y = pt[1] * SQUARESZ + COFFSZ + GERM_OFFSET;
        x += GERM_SPACE;
    }
}

function initialize(world_map) {
    worldMap = world_map;
    canvas=document.getElementById("myMap");
    context=canvas.getContext("2d");
    canvas2=document.getElementById("cardDex");
    context2=canvas2.getContext("2d");
    context3=canvas2.getContext("2d");
    canvas.addEventListener("mousedown", evntHandler, false);
    canvas2.addEventListener("mousedown", evntHandler, false);
}

var CANV_SPLIT = 460;
var C_XOFF = 40;
var C_YOFF = 60;
function evntHandler(event) {
    var ginfo = gameobjsNamespace.get_game_info();
    var x = event.clientX - C_XOFF;
    var y = event.clientY - C_YOFF;
    if (y > CANV_SPLIT) {
        // TO DO: Implement
        alert(x);
        alert(y);
        alert(JSON.stringify(card_cols));
        return;
    }
    var xind = Math.floor(x/SQUARESZ);
    var yind = Math.floor(y/SQUARESZ);
    if (x % SQUARESZ > 40) {
        return;
    }
    if (y % SQUARESZ > 40) {
        return;
    }
    var whereto = -1;
    for (var i=0; i < worldMap.length; i++) {
        if (xind == worldMap[i][3][0]) {
            if (yind == worldMap[i][3][1]) {
                whereto = i;
                break;
            }
        }
    }
    if (helpNamespace.get_state() == STATE_MUST_MOVE_RS) {
        actionNamespace.build_remove(whereto);
        return;
    }
    var plb = ginfo.states.turn;
    var spt = ginfo.players[plb].clocation;
    if (is_rs(spt) && is_rs(whereto)) {
        actionNamespace.doAction('shuttle', [plb,whereto]);
        return;
    }
    for (i=0; i < worldMap[spt][2].length; i++) {
        if (worldMap[spt][2][i] == whereto) {
            //gameobjsNamespace.make_move(plb, whereto);
            actionNamespace.doAction('move', [plb,whereto]);
            break;
        }
    }
}

function is_rs(cityloc) {
    var ginfo = gameobjsNamespace.get_game_info();
    for (var ii=0; ii < ginfo.states.research_stations.length; ii++) {
        if (cityloc === ginfo.states.research_stations[ii]) {
            return true;
        }
    }
    return false;
}

function drawCity(city) {
    var numb = city[0];
    var name = city[1];
    var loc = city[3];
    var xc = SQUARESZ * loc[0] + COFFSZ;
    var yc = SQUARESZ * loc[1] + COFFSZ;
    context.lineWidth=2;
    context.strokeStyle=colors[Math.floor(numb/12)];
    context.fillStyle = context.strokeStyle;
    context.font="bold 10px Arial";
    context.fillText(name, xc, yc-2);
    context.strokeRect(xc, yc, CSIZE, CSIZE);
}

function drawCons(city1, defskip) {
    var cons = city1[2];
    context.strokeStyle="#ff00ff";
    for (var j=0, jlen=cons.length; j < jlen; j++) {
        var city2 = worldMap[cons[j]];
        if (defskip & (city1[0] < city2[0])) {
            continue;
        }
        context.lineWidth=1;
        var cmp1 = Math.abs(city1[3][0]-city2[3][0]);
        var cmp2 = Math.abs(city1[3][1]-city2[3][1]);
        if (cmp1 == cmp2) {
            context.lineWidth=2;
        }
        if (city1[3][0] > city2[3][0]) {
            drawfrom(city2[3], city1[3]);
        }
        else {
            drawfrom(city1[3], city2[3]);
        }
    }
}

function drawfrom(locf, loct) {
    if ((locf[0] === 0) && (loct[0] == 10)) {
        var temp1 = [-1, loct[1]];
        drawline(temp1, locf);
        var temp2 = [11, locf[1]];
        drawline(loct, temp2);
    }
    else {
        drawline(locf, loct);
    }
}

function drawline(locf, loct) {
    var fc = [SQUARESZ * locf[0] + MIDSQ, SQUARESZ * locf[1] + MIDSQ];
    var tc = [SQUARESZ * loct[0] + MIDSQ, SQUARESZ * loct[1] + MIDSQ];
    var denom = tc[0] - fc[0];
    if (denom === 0) {
        var fcy = Math.min(fc[1], tc[1]) + HCSIZE;
        tc[1] = Math.max(fc[1], tc[1]) - HCSIZE;
        fc[1] = fcy;
    }
    else {
        var slope = (tc[1] - fc[1]) / denom;
        var bval = fc[1] - slope * fc[0];
        if (Math.abs(slope) > 1) {
            var factr = 1;
            if (slope < 0) {
                factr = -1;
            }
            var yoff = factr * HCSIZE;
            fc[1] += yoff;
            tc[1] -= yoff;
            fc[0] = (fc[1] - bval) / slope;
            tc[0] = (tc[1] - bval) / slope;
        }
        else {
            fc[0] += HCSIZE;
            tc[0] -= HCSIZE;
            fc[1] = slope * fc[0] + bval;
            tc[1] = slope * tc[0] + bval;
        }
    }
    context.moveTo(fc[0], fc[1]);
    context.lineTo(tc[0], tc[1]);
    context.stroke();
}


function redraw() {
    context.clearRect(0,0,canvas.width,canvas.height);
    context3.clearRect(0,0,canvas2.width,canvas2.height);
    draw_map();
    draw_game_info();
}

function special_cards() {
    return SPECIAL_CARDS;
}

function get_max_cities() {
    return CITY_MAX;
}

    return {
        initialize:initialize,
        special_cards:special_cards,
        get_max_cities:get_max_cities,
        draw_map:draw_map,
        draw_game_info:draw_game_info,
        get_role_text:get_role_text,
        redraw:redraw
    };
}();
