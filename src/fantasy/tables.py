"""
Generate tables.

A table in this modules refers to a set of information
related to a fantasy team.  Each table consists of a
team name followed by a set of players representing
a team.  The data in the line for a player includes
the player's position, name, real life team, and points
scored.

There are two types of tables written -- tables for this
week, and tables for last week.  Last week's table entries
are all black except for the winning fantasy team that
week.  This week's table entries are green if the player's game
is not yet played, red if the game is currently happening, and
blue if the game has been completed.

PlayerInfo is a class used to store the statistics for an
individual player.

The main routine here is generate_tables.  It generates the
four tables that are displayed in the html files (my team,
my opponent's team, the best possible team I could have
(using the right subs), and the best possible team assembled
from available players).
"""

from copy import deepcopy
from calendar import day_abbr
from fantasy.infoutils import get_all_other_players
from fantasy.infoutils import get_team_names_and_matches
from fantasy.infoutils import get_matchup
from fantasy.htmlgen import display_new_page
from fantasy.htmlgen import create_new_page

DAYSOFTHEWEEK = [d for d in day_abbr]


def get_color(time_in):
    """
    Game status: green if not started, red if in progress, blue if finished.
    """
    if time_in.startswith('Final'):
        return 'blue'
    if time_in[0:3] in DAYSOFTHEWEEK:
        return 'green'
    return 'red'


def get_score(score_txt):
    """
    Convert score to integer number
    """
    if score_txt == '-':
        return 0
    nparts = score_txt.split('.')
    fact = 1
    wholen = nparts[0]
    if wholen.startswith('-'):
        wholen = wholen[1:]
        fact = -1
    return (int(nparts[0]) * 100 + int(nparts[1])) * fact


class PlayerInfo(object):
    """
    Represent a player (name, team, points, and game status)
    """
    def __init__(self, pdata, last_week):
        self.name = pdata['player']
        parts = pdata['team'].split('-')
        self.team = parts[0].strip()
        self.pos = parts[1].strip()
        if last_week:
            self.color = 'black'
        else:
            self.color = get_color(pdata['time'])
        self.score = get_score(pdata['score'])

    def __lt__(self, other):
        return self.score > other.score

    def __repr__(self):
        return "%s:%s:%s:%s:%d" % (self.name, self.team, self.pos,
                                   self.color, self.score)

    def get_color(self):
        """ Return game Status """
        return self.color

    def get_name(self):
        """ Player name extracted (Full name or First Initial and Last) """
        return self.name

    def get_team(self):
        """ Actual NFL team the player is on """
        return self.team

    def get_score(self):
        """ Integer value of score """
        return self.score


def optimize_team(in_lineup):
    """
    Arrange players on a team by score.  Select the top ones as starters.
    """
    pl_info = {'QB': [], 'WR': [], 'RB': [], 'TE': [], 'K': [], 'DEF': []}
    for plyr in in_lineup[1]:
        pl_info[plyr.pos].append(plyr)
    num = {'QB': 1, 'WR': 3, 'RB': 2, 'TE': 1, 'K': 1, 'DEF': 1}
    out_list = []
    for key in ['QB', 'WR', 'RB', 'TE', 'K', 'DEF']:
        pl_info[key].sort()
        for plyr in range(0, num[key]):
            out_list.append(pl_info[key][plyr])
    in_lineup[1] = out_list
    return in_lineup


def use_last_week(mtchup):
    """
    If no game has started this week, do calculations for last week.
    """
    for team in mtchup:
        for entry in team['players']:
            if not entry['time'][0:3] in DAYSOFTHEWEEK:
                return False
    return True


def get_plist(team, last_week):
    """
    Select players on team and return a list of PlayerInfo representations.
    """
    ret_team = []
    for pdata in team['players']:
        ret_team.append(PlayerInfo(pdata, last_week))
    return [team['name'], ret_team]


def get_best_available(last_week):
    """
    Construct a list of the best free agents (10 per position).
    """
    others = get_all_other_players(last_week)
    o_plist = []
    for key in others:
        for indv in range(0, 10):
            pldef = {}
            for indx, pkey in enumerate(['player', 'team', 'time', 'score']):
                pldef[pkey] = others[key][indv][indx]
            o_plist.append(pldef)
    o_list = get_plist({'name': 'Free Agents', 'players': o_plist}, last_week)
    return o_list


def generate_tables(out_file):
    """
    Generate the table of tables to be displayed.  Entries are included
    for my team, my opponent, my best possible team, and the best free agent
    team.  
    """
    mtchup = get_matchup()
    last_week = False
    if use_last_week(mtchup):
        last_week = True
        mtchup = get_matchup(last_week)
    tblz = []
    ordr = 1
    if mtchup[1]['name'] == get_team_names_and_matches()[0]:
        ordr = -1
    set_my_best = True
    for team in mtchup[::ordr]:
        tblz.append(get_plist(team, last_week))
        if set_my_best:
            my_best = deepcopy(team)
            set_my_best = False
    my_best['name'] = 'My Best Team'
    for b_list in [get_plist(my_best, last_week),
                   get_best_available(last_week)]:
        b_list = optimize_team(b_list)
        tblz.append(b_list)
    if not last_week:
        display_new_page(last_week, tblz)
    else:
        create_new_page(last_week, tblz, out_file)
    return last_week

if __name__ == '__main__':
    generate_tables(None)
