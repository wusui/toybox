/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
helpNamespace = function() {

var state;
var switch_array = [cmd_start, too_many_rs];
var helpTimer;
function help() {
    if (gameobjsNamespace.get_pbpw()) {
        helpTimer = setInterval(function() { helptimer(); }, 1000);
        return;
    }
    help_dialog();
}

function help_dialog() {
    var msg = switch_array[state]();
    document.getElementById("helpmessage").innerHTML = msg;
    $(function(){
        $("#helpmessage").dialog({
            modal: true,
            height: 400,
            width: 400,
            title: 'HELP',
            buttons: {
                "Okay": function () {
                    $(this).dialog('close');
                }
            }
        });
    });
}

function helptimer() {
    if (!gameobjsNamespace.get_pbpw()) {
        clearInterval(helpTimer);
        help_dialog();
    }
}

function get_state() {
    return state;
}

function set_state(s) {
    state = s;
}

function restart() {
    state = 0;
}

var STD_TXT_0 = ['one move', 'two moves', 'three moves', 'four moves'];
function cmd_start() {
    var ans;
    var hinfo = gameobjsNamespace.get_game_info();
    var playr = hinfo.states['turn'];
    var playa = hinfo.players[playr];
    person = graphNamespace.get_role_text(playa.role);
    mnumb = gameobjsNamespace.gpmoves() - 1;
    if (mnumb < 0) {
        mnumb = 0;
    }
    ans = "The " + person + " has " + STD_TXT_0[mnumb] + " left.<BR>";
    if (playa.role === 'D') {
        ans += "You can click on a player to move that player.<BR>";
    }
    ans += "<BR>To move to a city, click on that city.";
    ans += "<BR><BR>To play a card, click on that card.";
    ans += "<BR><BR>To perform another action, click on one of Special Action buttons.";
    return ans;
}

function too_many_rs() {
    return 'Too many research stations in use.<BR><BR>' +
           'Click on station to be moved to this new location.';
}

    return {
        set_state:set_state,
        get_state:get_state,
        help:help
    };
}();
