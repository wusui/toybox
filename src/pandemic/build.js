/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
buildNamespace = function() {

    var bld_plb;
    var bld_spt;
    
    function clickButton() {
        actionNamespace.doAction('build', [bld_plb, bld_spt]);
    }

    function fgbgButton(ginfo) {
        document.getElementById('buildb').disabled = true;
        bld_plb = ginfo.states.turn;
        bld_spt = ginfo.players[bld_plb].clocation;
        for (var i=0; i < ginfo.states.research_stations.length; i++) {
            if (bld_spt == ginfo.states.research_stations[i]) {
                return;
            }
        }
        if (ginfo.players[bld_plb].role == 'O') {
            document.getElementById('buildb').disabled = false;
            return;
        }
        for (i=0; i < ginfo.players[bld_plb].cards.length; i++) {
            if (bld_spt == ginfo.players[bld_plb].cards[i]) {
                document.getElementById('buildb').disabled = false;
                return;
            }
        }
    }
    
    return {
        clickButton:clickButton,
        fgbgButton:fgbgButton,
    };
}();
