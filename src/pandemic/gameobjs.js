/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
gameobjsNamespace = function() {
    
    var MAX_GERMS = 3;
    var worldMap;
    var cityNameInfo;
    var ginfo;
    var pmoves;
    var w4pbp;
    
    function process_map() {
        cityNameInfo = {};
        worldMap=[];
        var panMap = document.getElementById("worldmap").innerHTML.split("+");
        for (var i=0; i < panMap.length; i++) {
            var parts = panMap[i].split(":");
            var tclinks = parts[1].split(",");
            var clinks = [];
            for (var j=0; j < tclinks.length; j++) {
                clinks.push(tclinks[j].trim());
            }
            var coords = mkInts(parts[2].split(","));
            worldMap.push([i, parts[0].trim(), clinks, coords]);
        }
        for (i=0; i < worldMap.length; i++) {
            var tstr = worldMap[i][1];
            cityNameInfo[tstr] = i;
        }
        for (i=0; i < worldMap.length; i++) {
            var newlist = [];
            var prev = worldMap[i][2];
            for (j=0; j < prev.length; j++) {
                newlist.push(cityNameInfo[prev[j]]);
            }
            worldMap[i][2] = newlist;
        }
        return worldMap;
    }
    
    function strt_game() {
        var city_max = graphNamespace.get_max_cities();
        var pl_deck = mkdeck(city_max + graphNamespace.special_cards().length);
        var ct_deck = mkdeck(city_max);
        var cnt = 0;
        var grms = [];
        var ct_disc = [];
        for (var i=0; i < MAX_GERMS; i++) {
            gcount = MAX_GERMS - i;
            for (var j=0; j < MAX_GERMS; j++) {
                var vec = [0, 0, 0, 0];
                var indx = Math.floor(ct_deck[cnt]/12);
                vec[indx] = gcount;
                var grmdata = [ct_deck[cnt], vec];
                grms.push(grmdata);
                ct_disc.push(ct_deck[cnt]);
                cnt++;
            }
        }
        ct_deck.splice(0, MAX_GERMS * MAX_GERMS);
        var city_deck = {'play': ct_deck, 'disc': ct_disc};
        //alert(JSON.stringify(city_deck));
        var scanner = location.search.split('?');
        var parsur = {};
        for (var sind=0; sind < scanner.length; sind++) {
            var brkr = scanner[sind].split('=');
            parsur[brkr[0]] = brkr[1];
        }
        var disply = parsur.display;
        var roles = parsur.roles;
        var noofplyrs = Number(parsur.plyrs);
        rlist = [];
        for (i=0; i<roles.length; i++) {
            rlist.push(roles.substring(i,i+1));
        }
        shuffle(rlist);
        var lplayers = [];
        for (i=0; i<noofplyrs; i++) {
            lplayers.push({"cards": [], "role": rlist[i], "clocation": 0 });
        }
        cnt = 0;
        for (j=0; j<(6 - noofplyrs); j++) {
            for (i=0; i<noofplyrs; i++) {
                lplayers[i].cards.push(pl_deck[cnt]);
                cnt++;
            }
        }
        pl_deck.splice(0,noofplyrs*(6 - noofplyrs));
        var epids = Number(parsur.epid);
        var stcksize = Math.floor(pl_deck.length/epids);
        var extra = pl_deck.length % epids;
        var ssizes = [];
        var stkstrt = [];
        for (i=0; i<epids; i++) {
            stkstrt.push(0);
            ssizes.push(stcksize);
        }
        for (i=0; i<extra; i++) {
            ssizes[i]++;
        }
        for (i=1; i<epids; i++) {
            for (j=0; j<i; j++) {
                stkstrt[i] += ssizes[j];
            }
        }
        for (i=(epids-1); i >= 0; i--) {
            var offset = Math.floor(Math.random() * (ssizes[i]+1));
            pl_deck.splice(stkstrt[i]+offset,0,-1);
        }
        //alert(JSON.stringify(pl_deck));
        var lstates = {'research_stations': [0], 'outbreak_count': 0,
                       'infection_count': 0, 'turn': 0,
                       'disease_status': [0,0,0,0],
                       'infection_rate': 2, 'cards_left': pl_deck.length};
        play_deck = {'play': pl_deck, 'disc': []};
        if (disply.indexOf('P') >= 0) {
            document.getElementById("playbyplay").checked = true;
        }
        if (disply.indexOf('H') >= 0) {
            document.getElementById("helpful").checked = true;
        }
        if (disply.indexOf('C') >= 0) {
            document.getElementById("careful").checked = true;
        }
        gdecks = {'player': play_deck, 'city': city_deck};
        ginfo = {'states': lstates, 'display': disply, 
                 'germs': grms, 'players': lplayers};
        helpNamespace.set_state(STATE_START_OF_TURN);
        //alert(JSON.stringify(ginfo));
        injectorNamespace.set_starter('O');
        injectorNamespace.extra_stations([5,13,17,28,38,40,])
    }
    
    function get_game_info() {
        return ginfo;
    }
    
    function gpmoves() {
        return pmoves;
    }
    
    function get_city(number) {
        return worldMap[number][1];
    }
    
    function get_pbpw() {
        return w4pbp;
    }
    
    function set_pbpw(tfval) {
        w4pbp = tfval;
    }
    
    function initialize() {
        var wrld_map = process_map();
        w4pbp = false;
        graphNamespace.initialize(wrld_map);
        graphNamespace.draw_map();
        pmoves = 4;
        strt_game();
        graphNamespace.draw_game_info();
        actionNamespace.initialize();
    }
    
    function skip() {
        pmoves--;
        graphNamespace.redraw();
    }
    
    function mkdeck(size) {
        var deck = [];
        for (var i = 0; i < size; i++) {
            deck.push(i);
        }
        shuffle(deck);
        return deck;
    }
    
    function shuffle(lyst) {
        for (var lim = lyst.length; lim > 1; lim--) {
            var indx = Math.floor(Math.random() * lim);
            var tmp = lyst[lim-1];
            lyst[lim-1] = lyst[indx];
            lyst[indx] = tmp;
        }
    }
    
    function mkInts(charv) {
        retv = [];
        for (var i=0, len=charv.length; i < len; i++) {
            retv[i] = parseInt(charv[i], 10);
        }
        return retv;
    }
    
    function dump_card(ply_no, card) {
        var hand = ginfo.players[ply_no].cards;
        for (var i=0; i < hand.length; i++) {
            if (hand[i] == card) {
                hand.splice(i,1);
                break;
            }
        }
    }
    
    return {
        initialize:initialize,
        get_game_info:get_game_info,
        gpmoves:gpmoves,
        get_city:get_city,
        shuffle:shuffle,
        dump_card:dump_card,
        get_pbpw:get_pbpw,
        set_pbpw:set_pbpw,
        skip:skip
    };
}();
