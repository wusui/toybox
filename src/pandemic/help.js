/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
var STATE_START_OF_TURN = 0;
var STATE_MUST_MOVE_RS = 1
helpNamespace = function() {
/**
 * Help Message and Help States
 *
 * Help dialogs are used to inform the player of the current state of the
 * game from a move parsing perspective.  Depending on circumstatnces, the
 * program may expect the player to choose specific options (card to discard,
 * city to charter for a flight, disease to cure).  In these cases, a help
 * message will tell the user what needs to be done in the current state. 
 *
 * Entry points either set or return the current state (set_state or get_state)
 * or produce an appropriate help dialog message help.
 *
 * States are numbered as follows:
 *   0 -- Start state.  It is the start of an action and all the moves
 *        should be available to the player.
 *   1 -- Delete a research stations.  All six research stations have been
 *        built, so a build request requires the player to click on a
 *        station to be moved.
 *
 * If the helpful checkbox is marked, the help dialog should automatically
 * appear before the start of a turn.  A callback was implemented here to
 * insure that help dialogs do not interfere with play-by-play dialogs.
 * 
 * Namespace-wide variables:
 *      state -- integer value of the current help state.
 *      switch_array -- array of routines that generate appropriate dialog
 *                      messages (switch_array[0] generates the dialog message
 *                      when in state 0.
 *      helpTimer -- namespace-wide reference to interval timer.
 *
 * @exports get_state, set_state, restart, help
 *
 * @author Warren Usui
 */
    var state;
    var switch_array = [cmd_start, too_many_rs];
    var helpTimer;

    /**
     * Wrapper for help
     *
     * Setup callback if we are going to display a play-by-play dialog first.
     */
    function help() {
        if (actionNamespace.checkWaits() && state === STATE_START_OF_TURN) {
            helpTimer = setInterval(function() { helptimer(); }, 1000);
            return;
        }
        help_dialog();
    }

    /**
     * Actual dialog.
     *
     * Display dialog message based on the state.
     */
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

    /**
     * Stop timer loop when play-by-play dialog is done.
     */
    function helptimer() {
        if (!gameobjsNamespace.checkWaits()) {
            clearInterval(helpTimer);
            help_dialog();
        }
    }

    /**
     * @returns state number
     */
    function get_state() {
        return state;
    }

    /**
     * @param  new state number to set
     */
    function set_state(s) {
        state = s;
    }

    /**
     * set conditions back to the start of the command (most notably, the state
     * is 0).
     */
    function restart() {
        if (state != STATE_START_OF_TURN) {
            $(function(){
                $("#restartmsg").dialog({
                    modal: false,
                    height: 200,
                    width: 400,
                    title: 'HELP',
                    buttons: {
                        "Okay": function () {
                            $(this).dialog('close');
                            gameobjsNamespace.clearWaits();
                            actionNamespace.clearWaits();
                            state = STATE_START_OF_TURN;
                            if (document.getElementById("helpful").checked) {
                                help_dialog();
                            }
                        }
                    }
               });
            });
        }
    }

    var STD_TXT_0 = ['one move', 'two moves', 'three moves', 'four moves'];
    /**
     * @returns dialog text at the start of a command.
     */
    function cmd_start() {
        var ans;
        var hinfo = gameobjsNamespace.get_game_info();
        var playr = hinfo.states.turn;
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
        ans += "<BR><BR>To perform another action, click on one ";
        ans += " of Special Action buttons.";
        return ans;
    }

    /**
     * @returns dialog text if the user needs to delete a research station.
     */
    function too_many_rs() {
        return 'Too many research stations in use.<BR><BR>' +
               'Click on station to be moved to this new location.';
    }

    return {
        set_state:set_state,
        get_state:get_state,
        restart:restart,
        help:help
    };
}();
