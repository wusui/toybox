"""
Read matchups.
"""
import re
from calendar import day_abbr
from yahoofoot.utilities import parse_url
from yahoofoot.parsers import ParseMatchup
from yahoofoot.parsers import ParsePlayers
from yahoofoot.parsers import ParseTeams
from yahoofoot.utilities import MY_BEST_TEAM
from yahoofoot.utilities import BEST_FREE_AGENTS

DAYSOFTHEWEEK = [d for d in day_abbr]

def get_teams(league):
    """
    Generate a url for teams

    Input:
        League number

    Outputs two dictionaries.  One associated team names with numbers.
    The other associates team numbers with team names, the numbers to
    names dictionary also contains entries used for titling my best
    team and best free agent tables.
    """
    xtra_data = "/teams"
    team_tabs = parse_url(league, xtra_data, ParseTeams(league))
    team_tabs[1][MY_BEST_TEAM[0]] = MY_BEST_TEAM[1]
    team_tabs[1][BEST_FREE_AGENTS[0]] = BEST_FREE_AGENTS[1]
    return team_tabs

def get_matchups(league, week):
    """
    Get matchups:

    Input:
        league -- league number
        week -- week number

    This method returns a list of 5 tuples.  Each tuple has two numbers
    representing teams that are playing each other.
    """
    week_data = "?matchup_week=%d" % week
    matchup_data = parse_url(league, week_data, ParseMatchup(league))
    return zip(*[iter(matchup_data)] * 2)

def get_players(league, week, team):
    """
    Get the players on a team

    Input:
        league -- league number
        week -- week number
        team -- team number

    The team information created here consists of two items.  The first
    is an ordered list of player ids representing how those players are
    placed on a roster.  The second is a dictionary keyed on player id's
    whose values are PlayerInfo objects representing a player.
    """
    team_data = "/%d/team?&week=%d" % (team, week)
    return cleanup(*parse_url(league, team_data, ParsePlayers()))

def get_all_players(league, week, position, page=0):
    """
    Find all players.

    Input:
        league -- league number
        week -- week number
        position -- player position (QB, WR, RB, TE, K, DEF)
        page -- page in Yahoo display (25 are displayed at a time)

    A list of players pointing to a dictionary of PlayerInfo objects is
    created by this routine (Identical to the data returned from get_players
    except that this information is for all players of a given position
    rather than all players on a team).
    """
    pagept = ''
    if page > 0:
        pagept = '&count=%d' % (page * 25)
    pg_data = '/players?status=ALL&pos=%s&stat1=S_W_%d&sort=PTS&%s' \
                % (position, week, pagept)
    return cleanup(*parse_url(league, pg_data, ParsePlayers()))

def set_color(time_in):
    """
    Set a potential table row color based on the status of a game that a
    player is in.

    Input:
        time_in -- time/date indicator of a game.  Examples of
        possible formats are:
             (Sun 5:00, Final 31-0, Bye, Q1: 10:15)

    This returns a game status: green if not started,
    red if in progress, blue if finished.
    """
    if time_in.startswith('Final') or time_in.startswith('Bye'):
        return 'blue'
    if time_in[0:3] in DAYSOFTHEWEEK:
        return 'green'
    return 'red'

class PlayerInfo(object):
    """
    Represent a player (name, team, points, and game status)
    """
    def __init__(self, key, in_list):
        self.key = key
        self.name = in_list[0]
        parts = in_list[1].split('-')
        self.team = parts[0].strip()
        self.pos = parts[1].strip()
        self.color = set_color(in_list[2])
        self.score = in_list[3]
        if self.color == 'green':
            self.score = 0.00

    def __lt__(self, other):
        return self.score > other.score

    def __repr__(self):
        return "%s:%s:%s:%s:%.2f:%s" % (self.name, self.team, self.pos,
                                   self.color, self.score, self.key)

    def get_name(self):
        """ Player name extracted (Full name or First Initial and Last) """
        return self.name

    def get_team(self):
        """ Actual NFL team the player is on """
        return self.team

    def get_score(self):
        """ Float value of score """
        return self.score

    def get_color(self):
        """ Color of text in table"""
        return self.color


def cleanup(keys, values):
    """
    Depending on the page that a player's data comes from, some fields
    may be extraneous as far as this program is concerned.  This method
    should reduce all information to player, team - position, game status,
    and fantasy points)

    Input:
        keys -- player id's taken from the team list.
        values -- dictionary of lists of data extracted from web pages.

    Returns cleaned up team data.
    """
    newvals = {}
    pattern = re.compile(r'^-?[0-9]+\.[0-9][0-9]$')
    for key in values:
        if values[key][2] in ['Out', 'Injured Reserve', 'Doubtful',
                              'Questionable', 'Probable']:
            del values[key][2]
        if values[key][5] != '-':
            if not pattern.search(values[key][5]):
                del values[key][5]
        del values[key][3]
        del values[key][3]
        if values[key][3] == '-':
            values[key][3] = 0.0
        else:
            values[key][3] = float(values[key][3])
        newvals[key] = PlayerInfo(key, values[key][0:4])
    return keys, newvals
