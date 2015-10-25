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
    
    function builddesc(parms) {
        desc = ' a research station at ';
        desc += gameobjsNamespace.get_city(parms[1]);
        return desc;
    }
    
    function closeaction(parms) {
        var ginfo = gameobjsNamespace.get_game_info();
        ginfo.states.research_stations.splice(activity.aparms[0], 1);
        helpNamespace.set_state(STATE_START_OF_TURN);
        build_it();
        actionNamespace.close_pbp();
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
    
    return {
        buildaction:buildaction,
        builddesc:builddesc,
        closeaction:closeaction,
        clickButton:clickButton,
        fgbgButton:fgbgButton,
    };
}();
