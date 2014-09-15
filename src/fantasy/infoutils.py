"""
Routines that use the parseutils classes to extract data
off of the text of web pages.

@author: Warren Usui
"""

import ConfigParser
from fantasy.urlutils import read_other_players
from fantasy.urlutils import read_league
from fantasy.urlutils import read_my_team
from fantasy.urlutils import read_matchup
from fantasy.dateutils import get_current_week
from fantasy.parseutils import ParseOtherPlayers
from fantasy.parseutils import ParseLeague
from fantasy.parseutils import ParseTeam
from fantasy.parseutils import ParseMatchup


CONFIG = ConfigParser.RawConfigParser()
CONFIG.read('config.cfg')
LEAGUE = CONFIG.getint('YahooFootball', 'league')
MY_TEAM = CONFIG.get('YahooFootball', 'my_team')


def get_other_players(position, last_week):
    """
    Return free players for the position specified.
    """
    parser = ParseOtherPlayers()
    week_no = get_current_week()
    if last_week:
        week_no -= 1
    in_data = read_other_players(LEAGUE, week_no, position)
    in_data = in_data.replace(u'&#8211;', u'-')
    parser.feed(in_data)
    return parser.results


def get_all_other_players(last_week=False):
    """
    Return a dictionary indexed by position.  Each entry is a list
    of player information.  The player information is stored as a list
    of Name, team, and score.
    """
    all_pos = {}
    for position in ['QB', 'WR', 'RB', 'TE', 'K', 'DEF']:
        all_pos[position] = get_other_players(position, last_week)
    return all_pos


def get_team_names_and_matches():
    """
    Return a table of team names and numbers
    """
    parser = ParseLeague()
    in_data = read_league(LEAGUE)
    parser.feed(in_data)
    return (unicode(MY_TEAM), LEAGUE, parser.team_table, parser.match_ups)


def get_team_number():
    """
    Return my team number from the information returned by
    get_team_names_and_matches()
    """
    my_name, _, t_list, _ = get_team_names_and_matches()
    return t_list[my_name]


def get_my_team():
    """
    Return free players for the position specified.
    """
    parser = ParseTeam()
    in_data = read_my_team(LEAGUE, get_team_number())
    in_data = in_data.replace(u'&#8211;', u'-')
    parser.feed(in_data)
    return parser.output


def get_matchup(last_week=False):
    """
    Use get_team_names_and_matches() to get matchups.
    """
    parser = ParseMatchup()
    in_data = read_matchup(get_team_names_and_matches(), last_week)
    in_data = in_data.replace(u'&#8211;', u'-')
    parser.feed(in_data)
    for indx in [16, 9]:
        del parser.data['score1'][indx]
        del parser.data['score2'][indx]
    result = []
    scorelist = ['score1', 'score2']
    for rteam in range(0, 2):
        this_tm = {}
        this_tm['name'] = parser.data['rotoname'][rteam]
        this_tm['players'] = []
        for pnumb in range(rteam, 30, 2):
            pl_ent = {}
            for field in ['opp', 'player', 'time', 'team']:
                pl_ent[field] = parser.data[field][pnumb]
            pl_ent['score'] = parser.data[scorelist[rteam]][pnumb // 2]
            this_tm['players'].append(pl_ent)
        result.append(this_tm)
    return result


if __name__ == '__main__':
    print get_all_other_players()
    print get_team_names_and_matches()
    print get_matchup()
