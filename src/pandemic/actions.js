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
    
    function Build() {
        this.verb = 'Build';
    }
    
    function Close() {
        this.verb = 'Close';
    }

    function make_proto(main_obj, action_rtn, descript_rtn) {
        main_obj.prototype = new Action();
        main_obj.prototype.action = action_rtn;
        main_obj.prototype.descript = descript_rtn;
    }
    
    function initialize() {
        operations = {};
        make_proto(Move, moveNamespace.moveaction, moveNamespace.movedesc);
        make_proto(Build, buildNamespace.buildaction, buildNamespace.builddesc);
        make_proto(Shuttle, moveNamespace.moveaction, moveNamespace.movedesc);
        make_proto(Close, buildNamespace.closeaction, buildNamespace.builddesc);
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
    
    function close_pbp() {
        show_pbp(operations.build, '2');
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
        close_pbp:close_pbp,
        doAction:doAction
    };
}();
