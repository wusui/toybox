/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
actionNamespace = function() {
    
    var operations;
    var careful;
    var carefulTimer;
    var careCallback;
    var pbpTimer;
    var wait;
    var text;
    var rs_index;
    var rs_whereto;
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
    
    function Shuttle() {
        this.verb = 'Shuttle';
    }
    
    function Move() {
        this.verb = 'Move';
    }
    
    function moveaction(parms) {
        var plb;
        var whereto;
        plb = parms[0];
        whereto = parms[1];
        var lginfo = gameobjsNamespace.get_game_info();
        lginfo.players[plb].clocation = whereto;
        gameobjsNamespace.skip();
    }
    
    function movedesc(parms) {
        var desc = ' from ';
        var lginfo = gameobjsNamespace.get_game_info();
        var cnumb = lginfo.players[parms[0]].clocation;
        desc += gameobjsNamespace.get_city(cnumb);
        desc += ' to ';
        desc += gameobjsNamespace.get_city(parms[1]);
        return desc;
    }
    
    function Build() {
        this.verb = 'Build';
    }
    
    var MAX_STATIONS = 6;
    function buildaction(parms) {
        loc_pnumb = parms[0];
        loc_city = parms[1];
        var lginfo = gameobjsNamespace.get_game_info();
        if (lginfo.states.research_stations.length >= MAX_STATIONS) {
            helpNamespace.set_state(STATE_MUST_MOVE_RS);
            helpNamespace.help();
            return;
        }
        build_it();
    }
    
    var loc_pnumb;
    var loc_city;
    function build_it() {
        var lginfo = gameobjsNamespace.get_game_info();
        var pval = lginfo.players[loc_pnumb].role;
        if (pval !== 'O') { 
            gameobjsNamespace.dump_card(loc_pnumb, loc_city); 
        }
        lginfo.states.research_stations.push(loc_city);
        gameobjsNamespace.skip();
    }
    
    function builddesc(parms) {
        desc = ' a research station at ';
        desc += gameobjsNamespace.get_city(parms[1]);
        return desc;
    }
    
    function build_remove(whereto) {
        var ginfo = gameobjsNamespace.get_game_info();
        wait = false;
        for (var ii=0; ii < ginfo.states.research_stations.length; ii++) {
            if (ginfo.states.research_stations[ii] == whereto) {
                rs_index = ii;
                rs_whereto = whereto;
                if (document.getElementById("careful").checked) {
                    wait = true;
                    careCallback = build_rm;
                    var rs_nmb = ginfo.states.research_stations[rs_index];
                    carefulDialog('Remove research station at '+gameobjsNamespace.get_city(rs_nmb)+'?');
                    carefulTimer = setInterval(function() { caretimer(); }, 1000);
                    return;
                }
                build_rm();
                break;
            }
        }
    }
    
    function build_rm() {
        var ginfo = gameobjsNamespace.get_game_info();
        ginfo.states.research_stations.splice(rs_index, 1);
        helpNamespace.set_state(STATE_START_OF_TURN);
        build_it();
        if (document.getElementById("playbyplay").checked) {
            gameobjsNamespace.set_pbpw(true);
            text += "<BR><BR>Research station removed from ";
            text += gameobjsNamespace.get_city(rs_whereto);
            show_pbp();
        }
    }
    
    function make_proto(main_obj, action_rtn, descript_rtn) {
        main_obj.prototype = new Action();
        main_obj.prototype.action = action_rtn;
        main_obj.prototype.descript = descript_rtn;
    }
    
    function initialize() {
        make_proto(Move, moveaction, movedesc);
        make_proto(Build, buildaction, builddesc);
        make_proto(Shuttle, moveaction, movedesc);
        Build.prototype.pastTense = function() { return 'built'; };
        operations = {};
        operations.move = new Move();
        operations.build = new Build();
        operations.shuttle = new Shuttle();
    }
    
    function doAction(action, parms) {
        activity = operations[action];
        aparms = parms;
        wait = false;
        text = activity.descript(parms);
        if (document.getElementById("careful").checked) {
            wait = true;
            careCallback = doAction2;
            carefulDialog(activity.getVerb() + ' ' + text);
            carefulTimer = setInterval(function() { caretimer(); }, 1000);
            return;
        }
        helpNamespace.set_state(STATE_START_OF_TURN);
        doAction2();
    }
    
    function doAction2() {
        if (document.getElementById("playbyplay").checked) {
            gameobjsNamespace.set_pbpw(true);
        }
        activity.action(aparms);
        if (helpNamespace.get_state() !== STATE_START_OF_TURN) {
            return;
        }
        show_pbp();
    }
    
    function show_pbp() {
        if (document.getElementById("playbyplay").checked) {
            var msg = "You "+activity.pastTense().toLowerCase()+" "+text;
            document.getElementById("pbpmessage").innerHTML = msg;
            wait = true;
            $(function(){
                $("#pbpmessage").dialog({
                    modal: true,
                    height: 300,
                    width: 400,
                    title: 'PLAY BY PLAY',
                    buttons: {
                        "Okay": function () {
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
            gameobjsNamespace.set_pbpw(false);
        }
    }
    
    function caretimer() {
        if (!wait) {
            clearInterval(carefulTimer);
            if (!careful) {
                graphNamespace.redraw();
                return;
            }
            careCallback();
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
        wait:wait,
        initialize:initialize,
        build_remove:build_remove,
        doAction:doAction
    };
}();
