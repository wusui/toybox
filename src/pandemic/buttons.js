/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
buttonsNamespace = function() {
    
    function heal() {
        alert("heal");
        alert(JSON.stringify(gameobjsNamespace.get_game_info()));
    }
    
    function cure() {
        alert("cure");
    }
    
    function checkHeal(ginfo) {
        document.getElementById('healb').disabled = true;
        var plb = ginfo.states.turn;
        var spt = ginfo.players[plb].clocation;
        for (var i=0; i < ginfo.germs.length; i++) {
            if (ginfo.germs[i][0] == spt) {
                document.getElementById('healb').disabled = false;
                return;
            }
        }
    }
    
    function checkCure(ginfo) {
        document.getElementById('cureb').disabled = true;
        var cure_group = -1;
        var plb = ginfo.states.turn;
        var spt = ginfo.players[plb].clocation;
        for (var i=0; i < ginfo.states.research_stations.length; i++) {
            if (spt == ginfo.states.research_stations[i]) {
                cntr = [0, 0, 0, 0];
                for (var j=0; j < ginfo.players[plb].cards.length; j++) {
                    var indx = Math.floor(ginfo.players[plb].cards[i]/12);
                    if (indx < 4) {
                        cntr[indx] += 1;
                    }
                }
                var cind = -1;
                var xind = -1;
                for (j=0; j < cntr.length; j++) {
                    if (cntr[j] > cind) {
                        cind = cntr[j];
                        xind = j;
                    }
                }
                var flim = 5;
                if (ginfo.players[plb].role == 'O') {
                    flim = 4;
                }
                if (cind >= flim) {
                    if (ginfo.states.disease_status === 0) {
                        document.getElementById('cureb').disabled = false;
                        cure_group = xind;
                    }
                }
            }
        }
    }
    
    return {
        heal:heal,
        cure:cure,
        checkHeal:checkHeal,
        checkCure:checkCure
    };
}();
