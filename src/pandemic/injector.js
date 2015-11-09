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
            if (i >= 5) {
                break;
            }
            var cityNumb = gameobjsNamespace.get_city_numb(locations[i]);
            lginfo.states.research_stations.push(cityNumb);
        }
    }
    
    function add_city_cards(city_list) {
        lginfo = gameobjsNamespace.get_game_info();
        for (var i=0; i<city_list.length; i++) {
            var cardn = gameobjsNamespace.get_city_numb(city_list[i]);
            var not_found = true;
            for (var j=0; j<lginfo.players[0].cards; j++) {
                if (lginfo.players[0].cards[j] === cardn) {
                    var not_found = false;
                    break;
                }
            }
            if (not_found) {
                lginfo.players[0].cards.push(cardn);
            }
        }
    }

    return {
        set_starter:set_starter,
        extra_stations:extra_stations,
        add_city_cards:add_city_cards
    };
}();
