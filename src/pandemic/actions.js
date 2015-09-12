/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
actionNamespace = function() {

var operations;
var careful;
var carefulTimer;
var pbpTimer;
var wait;
var text;
var activity;
var aparms;

function Action() {
    this.verb = 'action';
}

Action.prototype.pastTense=function(){
    if (this.verb.endsWith('e')) {
        return this.verb + 'd';
    }
    return this.verb + 'ed';
};

Action.prototype.getVerb=function() {
    return this.verb;
};

function Move() {
    this.verb = 'Move';
}

function moveaction(parms) {
    var plb;
    var whereto;
    plb = parms[0];
    whereto = parms[1];
    var lginfo = gameobjsNamespace.get_game_info();
    lginfo.players[plb]['location'] = whereto;
    gameobjsNamespace.skip();
}

function movedesc(parms) {
    var desc = ' from ';
    var lginfo = gameobjsNamespace.get_game_info();
    var cnumb = lginfo.players[parms[0]]['location'];
    desc += gameobjsNamespace.get_city(cnumb);
    desc += ' to ';
    desc += gameobjsNamespace.get_city(parms[1]);
    return desc;
}

function Build() {
    this.verb = 'Build';
}

function buildaction(parms) {
    var lginfo = gameobjsNamespace.get_game_info();
    alert(JSON.stringify(parms));
    alert(JSON.stringify(lginfo['players'][parms[0]]['role']));
    alert(JSON.stringify(lginfo['players'][parms[0]]['cards']));
    // TO DO: if not 'O', get rid of card
    // TO DO: if too many research stattions, put us in erase state.
    lginfo.states['research_stations'].push(parms[1]);
}

function builddesc(parms) {
    desc = ' a research station at ';
    desc += gameobjsNamespace.get_city(parms[1]);
    return desc;
}

function initialize() {
    Move.prototype = new Action();
    Move.prototype.constructor = Move;
    Move.prototype.action = moveaction;
    Move.prototype.descript = movedesc;
    Build.prototype = new Action();
    Build.prototype.constructor = Build;
    Build.prototype.action = buildaction;
    Build.prototype.descript = builddesc;
    Build.prototype.pastTense = function() { return 'built'; };
    operations = {};
    operations['move'] = new Move();
    operations['build'] = new Build();
}

function doAction(action, parms) {
    activity = operations[action];
    aparms = parms;
    helpNamespace.set_state(0);
    wait = false;
    text = activity.descript(parms);
    if (document.getElementById("careful").checked) {
        wait = true;
        carefulDialog(activity.getVerb() + ' ' + text);
        carefulTimer = setInterval(function() { caretimer(); }, 1000);
        return;
    }
    doAction2();
}

function doAction2() {
    activity.action(aparms);
    if (document.getElementById("playbyplay").checked) {
        var msg = "You "+activity.pastTense().toLowerCase()+" "+text;
        document.getElementById("pbpmessage").innerHTML = msg;
        wait = true;
        $(function(){
            $("#pbpmessage").dialog({
                modal: true,
                height: 200,
                width: 400,
                title: 'PLAY BY PLAY',
                buttons: {
                    "Yes": function () {
                        $(this).dialog('close');
                        wait = false;
                    }
                }
            });
        });
        pbpTimer = setInterval(function() { pbptimer(); }, 1000);
        return;
    }
    graphNamespace.redraw();
}

function pbptimer() {
    if (!wait) {
        clearInterval(pbpTimer);
        graphNamespace.redraw();
    }
}

function caretimer() {
    if (!wait) {
        clearInterval(carefulTimer);
        if (!careful) {
            graphNamespace.redraw();
            return;
        }
        doAction2();
    }
}


function carefulDialog(dtext) {
    document.getElementById("dialogcareful").innerHTML = dtext;
    $(function(){
        $("#dialogcareful").dialog({
            resizable: false,
            modal: true,
            title: "Extra checking",
            height: 250,
            width: 500,
            buttons: {
                "Yes": function () {
                    $(this).dialog('close');
                    set_careful(true);
                },
                "No": function () {
                    $(this).dialog('close');
                    set_careful(false);
                }
            }
        });
    });
}

function set_careful(torf) {
    careful = torf;
    wait = false;
}

    return {
        initialize:initialize,
        doAction:doAction
    };
}();
