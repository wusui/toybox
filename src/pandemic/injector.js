/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
injectorNamespace = function() {

    function set_starter(person) {
        lginfo = gameobjsNamespace.get_game_info();
        alert(JSON.stringify(lginfo));
        for (var i=1; i<lginfo.players.length; i++) {
            if (lginfo.players[i].role == person) {
                lginfo.players[i].role = lginfo.players[0].role;
                lginfo.players[0].role = person;
                return;
            }
        }
        lginfo.players[0].role = person;
    }

    function extra_stations(locations) {
        lginfo = gameobjsNamespace.get_game_info();
        for (var i=0; i<locations.length; i++) {
            if (i >= 5) break;
            lginfo.states.research_stations.push(locations[i]);
        }
    }

    return {
        set_starter:set_starter,
        extra_stations:extra_stations
    };
}();
