
/**********************************************************************
    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
    Licensed under the GPL 3 license.
 **********************************************************************/
moveNamespace = function() {

    function moveaction(parms) {
        var plb;
        var whereto;
        plb = parms[0];
        whereto = parms[1];
        var lginfo = gameobjsNamespace.get_game_info();
        lginfo.players[plb].clocation = whereto;
        gameobjsNamespace.skip();
    }
    
    function movedesc(parms) {
        var desc = ' from ';
        var lginfo = gameobjsNamespace.get_game_info();
        var cnumb = lginfo.players[parms[0]].clocation;
        desc += gameobjsNamespace.get_city(cnumb);
        desc += ' to ';
        desc += gameobjsNamespace.get_city(parms[1]);
        return desc;
    }
    
    return {
        moveaction:moveaction,
        movedesc:movedesc
    };
}();
