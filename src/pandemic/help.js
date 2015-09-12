/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
helpNamespace = function() {

var state;
var switch_array = [cmd_start, oddness];
function help_example() {
    var msg = switch_array[state]();
    document.getElementById("helpmessage").innerHTML = msg;
    $(function(){
        $("#helpmessage").dialog({
            modal: true,
            height: 200,
            width: 400,
            title: 'HELP',
            buttons: {
                "Yes": function () {
                    $(this).dialog('close');
                }
            }
        });
    });
}

function set_state(s) {
    state = s;
}

function restart() {
    state = 0;
}

function cmd_start() {
    return 'Start of a command';
}

function oddness() {
    return 'Some other command';
}

    return {
        set_state:set_state,
        help:help_example
    };
}();
