"""
Generate the information to be displayed.

Teams in this module usually consist of a list and a dictionary.  The
dictionary entries contains the vital information for a player (name,
position, team, and fantasy score).  The list is an ordered set of keys
into the player dictionary.
"""
from yahoofoot.utilities import MY_BEST_TEAM
from yahoofoot.utilities import BEST_FREE_AGENTS
from yahoofoot.extract_data import get_players
from yahoofoot.extract_data import get_matchups
from yahoofoot.extract_data import get_all_players
from yahoofoot.extract_data import get_teams

POS_SIZE = (('QB', 1), ('WR', 3), ('RB', 2), ('TE', 1), ('K', 1), ('DEF', 1))

def get_tables(league, week, my_team):
    """
    Generate the tables to be displayed.

    Input:
        league -- id of this league (string)
        week -- week number
        my_team -- my team number

    Returns a list of tuples.  Each tuple contains a header number and
    a list of data.  The header corresponds to a set of text representing
    the data in the box (in many cases, this is a team name).  The data
    consists of 9 players that represent a team's starters.

    The four tables represented in the return list are:
        1. My team.
        2. This week's opponents team.
        3. What would be my highest scoring team.
        4. The highest possible scoring team of free players.
    """
    result = []
    teams = []
    for cnt in range(10):
        teams.append(get_players(league, week, cnt + 1))
    my_opp = 0
    for pair in get_matchups(league, week):
        if my_team in pair:
            my_opp = sum(pair) - my_team
            break
    picked = []
    for t_m in teams:
        picked.extend(t_m[0])
    team_names = get_teams(league)
    result.append((team_names[1][str(my_team)],
                   drop_subs(teams[my_team - 1])))
    result.append((team_names[1][str(my_opp)],
                   drop_subs(teams[my_opp - 1])))
    result.append((team_names[1][MY_BEST_TEAM[0]],
                   optimize_me(teams[my_team - 1])))
    result.append((team_names[1][BEST_FREE_AGENTS[0]],
                   get_best_unpicked(league, week, picked)))
    return result

def get_first(in_list, in_dict, in_pos):
    """
    Get the first player in the team's list for a position.  This ends up
    being the starter.

    Input:
        in_list -- list of player id's
        in_dict -- dictionary of player information, indexed by the elements
                    in in_list;
        in_pos -- position (quarterback, kicker...) we are trying to find.
    """
    for entry in in_list:
        if in_dict[entry].pos == in_pos:
            return entry
    return 'invalid'

def drop_subs(in_team):
    """
    Remove benched players from the list.

    Input:
        in_team -- team information, passed as a list of keys representing
                    the order of players listed, and a dictionary of player
                    information.

    The team information passed back consists of the same dictionary, but
    the pointer list is modified to only be starters.
    """
    ddict = in_team[1]
    origlist = in_team[0]
    newlist = origlist[0:7]
    newlist.append(get_first(origlist[7:], ddict, 'K'))
    newlist.append(get_first(origlist[7:], ddict, 'DEF'))
    return (newlist, ddict)

def optimize_me(myteam):
    """
    Find my highest scoring team

    Input: team (my team)

    When completed, the starting lineup will be the highest scoring team
    possible (substituting higher scoring bench players for the lower
    scoring players that I started)
    """
    hist = {}
    for entry in POS_SIZE:
        hist[entry[0]] = []
    for key in myteam[1]:
        hist[myteam[1][key].pos].append(myteam[1][key])
    for entry in POS_SIZE:
        hist[entry[0]].sort()
    rlist = []
    for entry in POS_SIZE:
        for cnt in range(entry[1]):
            rlist.append(hist[entry[0]][cnt].key)
    return (rlist, myteam[1])

def get_best_unpicked(league, week, picked):
    """
    Find the best free agents.

    Input:
        league -- this league
        week -- this week
        picked -- a list of player id's of players on other teams.

    This method looks through the list of players available and constructs
    the highest scoring team using those available players.
    """
    retval = ([], {})
    for entry in POS_SIZE:
        alist = []
        adict = {}
        cnt = 0
        while True:
            plist = get_all_players(league, week, entry[0], cnt)
            for key in plist[0]:
                if not key in picked:
                    alist.append(key)
                    adict[key] = plist[1][key]
                    if len(alist) == entry[1]:
                        break
            cnt += 1
            if len(alist) == entry[1]:
                break
        retval[0].extend(alist)
        retval[1].update(adict)
    return retval

