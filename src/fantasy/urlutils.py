"""
Read URL information into local strings
"""
import urllib2
from contextlib import closing
from fantasy.dateutils import get_current_week

YAHOO_URL = 'http://football.fantasysports.yahoo.com/f1/'


def _read_url(in_url):
    """
    Read the url passed in.  Return the text read
    in utf-8 format.
    """
    with closing(urllib2.urlopen(in_url)) as page:
        data = page.read()
    return unicode(data, 'utf-8')


def read_league(league_no):
    """
    Given a league number, read the information from that
    league's web page.
    """
    return _read_url("%s%d" % (YAHOO_URL, league_no))


def read_my_team(league_no, team_no):
    """
    Get the web page of the team number specified in the
    the league specified.
    """
    mt_url = "%s%d/%d" % (YAHOO_URL, league_no, team_no)
    return _read_url(mt_url)


def read_other_players(league_no, week_no, position):
    """
    Get the list of other players (players in the league
    that are free agents) Position can be one of the
    standard positions in the Yahoo non-flex league.
    """
    pattern = "%s%d/players?status=A&pos=%s&stat1=S_W_%d&sort=PTS&sdir=1"
    other_url = pattern % (YAHOO_URL, league_no, position, week_no)
    return _read_url(other_url)


def read_matchup(matchup_bundle, last_week=False):
    """
    Read a matchup based on info in bundle (my_name, _, number_dict, matches)
        my_name -- My team name
        number_dict -- table associating team names with numbers.
        matches -- this weeks matchups, expressed as a list of two item
                   lists.  Each two item list is a matchup based on
                   team numbers.
    """
    my_name = matchup_bundle[0]
    my_numb = matchup_bundle[2][my_name]
    my_opp = 0
    for match in matchup_bundle[3]:
        if my_numb in match:
            my_opp = sum(match) - my_numb
            break
    week_no = get_current_week()
    if last_week:
        week_no -= 1
        teams = "&mid1=%d" % my_numb
    else:
        teams = "&mid1=%d&mid2=%d" % (my_numb, my_opp)
    pattern = "%s%d/matchup?week=%d%s"
    match_url = pattern % (YAHOO_URL, matchup_bundle[1],
                           week_no, teams)
    return _read_url(match_url)
