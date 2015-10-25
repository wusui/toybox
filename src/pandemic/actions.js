/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
actionNamespace = function() {
    
    var operations;
    
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
    
    function Close() {
        this.verb = 'Close';
    }

    function closeaction(parms) {
        var ginfo = gameobjsNamespace.get_game_info();
        ginfo.states.research_stations.splice(activity.aparms[0], 1);
        helpNamespace.set_state(STATE_START_OF_TURN);
        build_it();
        show_pbp(operations.build, '2');
    }

    function make_proto(main_obj, action_rtn, descript_rtn) {
        main_obj.prototype = new Action();
        main_obj.prototype.action = action_rtn;
        main_obj.prototype.descript = descript_rtn;
    }
    
    function initialize() {
        operations = {};
        make_proto(Move, moveaction, movedesc);
        make_proto(Build, buildaction, builddesc);
        make_proto(Shuttle, moveaction, movedesc);
        make_proto(Close, closeaction, builddesc);
        Build.prototype.pastTense = function() { return 'built'; };
        operations.move = new Move();
        operations.build = new Build();
        operations.shuttle = new Shuttle();
        operations.close = new Close();
    }

    function checkWaits() {
        for (actn in operations) {
            if (operations[actn].wait) {
                return true;
            }
        }
        return false;
    }

    function clearWaits() {
        for (actn in operations) {
            operations[actn].wait = false;
        }
        //operations.move.wait = false;
        //operations.build.wait = false;
        //operations.shuttle.wait = false;
        //operations.close.wait = false;
    }
    
    function doAction(action, parms) {
        activity = operations[action];
        activity.aparms = parms;
        activity.wait = false;
        activity.text = activity.descript(parms);
        if (document.getElementById("careful").checked) {
            activity.wait = true;
            activity.careCallback = doAction2;
            carefulDialog(activity.getVerb() + ' ' + activity.text, activity);
            activity.carefulTimer = setInterval(function() { caretimer(activity); }, 1000);
            return;
        }
        helpNamespace.set_state(STATE_START_OF_TURN);
        doAction2(activity);
    }
    
    function doAction2(activity) {
        activity.action(activity.aparms);
        if (helpNamespace.get_state() !== STATE_START_OF_TURN) {
            return;
        }
        show_pbp(activity, '1');
    }
    
    function show_pbp(activity, pbpno) {
        var pbp_string = "pbpmessage" + pbpno;
        if (document.getElementById("playbyplay").checked) {
            var msg = "You "+activity.pastTense().toLowerCase()+" "+activity.text;
            document.getElementById(pbp_string).innerHTML = msg;
            activity.wait = true;
            $(function(){
                $("#"+pbp_string).dialog({
                    modal: true,
                    height: 300,
                    width: 400,
                    title: 'PLAY BY PLAY',
                    buttons: {
                        "Okay": function () {
                            $(this).dialog('close');
                            activity.wait = false;
                        }
                    }
                });
            });
            activity.pbpTimer = setInterval(function() { pbptimer(activity); }, 1000);
            return;
        }
        graphNamespace.redraw();
    }
    
    function pbptimer(activity) {
        if (!activity.wait) {
            clearInterval(activity.pbpTimer);
        }
    }
    
    function caretimer(activity) {
        if (!activity.wait) {
            clearInterval(activity.carefulTimer);
            if (!activity.careful) {
                graphNamespace.redraw();
                return;
            }
            activity.careCallback(activity);
        }
    }
    
    
    function carefulDialog(dtext, activity) {
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
                        set_careful(true, activity);
                    },
                    "No": function () {
                        $(this).dialog('close');
                        set_careful(false, activity);
                    }
                }
            });
        });
    }
    
    function set_careful(torf, activity) {
        activity.careful = torf;
        activity.wait = false;
    }

    return {
        initialize:initialize,
        checkWaits:checkWaits,
        clearWaits:clearWaits,
        doAction:doAction
    };
}();
