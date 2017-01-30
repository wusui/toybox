/**********************************************************************
    Copyright (C) 2017  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
**********************************************************************/
movie_matchNamespace = function() {
    
function handle_text(fname) {
    var astr = document.getElementById(fname);
    var rettxt = astr.value
    if (rettxt.length == 0) {
        $("<div>Both actor fields must be filled</div>").dialog(
            {modal: true, height: 100, width: 380, title: "Error"});
        return ''
    }
    return rettxt
}

function doit() {
    var actor1 = handle_text('actor1')
    if (actor1.length == 0) {
        return;
    }
    var actor2 = handle_text('actor2')
    if (actor2.length == 0) {
        return;
    }
    cmdstr = 'data='+actor1+'|'+actor2;
    server = new XMLHttpRequest();
    sendpost(cmdstr, 'movie_match.py', server, hndl_svr_resp);
}

function sendpost(postdata, remProg, server, server_sent_response) {
    //
    // Handle the sending of a request across the net
    //
    server.onreadystatechange = server_sent_response;
    server.open("POST", remProg, true);
    server.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    server.setRequestHeader("Content-length", postdata.length);
    server.setRequestHeader("Connection", "close");
    server.send(postdata);
}

function hndl_svr_resp() {
    //
    // When the server responds, display the output in a modal dialog.
    // The response is an or-bar separated set of fields.  See chess.py
    // for a further description of the format
    //
    if (server.readyState==4 && server.status==200)
    {
        $("<div>"+server.responseText+"</div>").dialog(
            {modal: true, height: 300, width: 800, title: 'ANSWER'});
    }
}

    //
    // Returns for the chessNamespace wrapper
    //
    return {
        doit:doit
    };
}();
