"""
Created on May 9, 2014

@author: Warren Usui
"""
from HTMLParser import HTMLParser
from llsimilarity.utilities import get_url_info
from llsimilarity.utilities import get_ll_url


def get_league_number():
    """
    Extract the league number from the main Learned League page.
    Returns the number as a string.
    """
    url = get_ll_url()
    league = get_url_info(url, LeagueParser())
    return league.league_num


# pylint: disable=R0904
class LeagueParser(HTMLParser, object):
    """
    Extract the league data
    """
    def  __init__(self):
        self.league_num = ''
        self.look_for = '/standings.php?'
        super(LeagueParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        """
        Scan and set league_num
        """
        if tag == 'a':
            if attrs:
                if attrs[0][0] == 'href':
                    if attrs[0][1].startswith(self.look_for):
                        tmp = attrs[0][1]
                        self.league_num = tmp[len(self.look_for):]
