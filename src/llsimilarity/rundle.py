"""
Created on May 10, 2014

@author: Warren Usui
"""
from HTMLParser import HTMLParser
from llsimilarity.utilities import get_url_info
from llsimilarity.utilities import get_ll_url
from llsimilarity.league import get_league_number


def get_rundle_players(rundle):
    """
    Get players in a rundle
    """
    url_template = ''.join([get_ll_url(), "/standings.php?{}&"])
    url_head = url_template.format(get_league_number())
    url = ''.join([url_head, rundle])
    this_rundle = get_url_info(url, RundleParser())
    return this_rundle.players[:]


# pylint: disable=R0904
class RundleParser(HTMLParser, object):
    """
    Extract the league data
    """
    def  __init__(self):
        self.look_for = '/profiles.php?'
        self.players = []
        super(RundleParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        """
        Scan and set league_num
        """
        if tag == 'a':
            if attrs:
                if len(attrs) < 2:
                    return
                if attrs[0][0] == 'href':
                    if attrs[0][1].startswith(self.look_for):
                        tmp = attrs[0][1]
                        player = tmp[len(self.look_for):]
                        self.players.append(player)


class AllRundleParser(HTMLParser, object):
    """
    Extract the league data
    """
    def  __init__(self):
        template = '/standings.php?{}&'
        self.look_for = template.format(get_league_number())
        self.rundles = []
        super(AllRundleParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        """
        Scan and set rundle values
        """
        if tag == 'a':
            if attrs[0][0] == 'href':
                if attrs[0][1].startswith(self.look_for):
                    tmp = attrs[0][1]
                    rundle = tmp[len(self.look_for):]
                    if rundle.find('_') > 0:
                        self.rundles.append(rundle)


def get_rundle_list():
    """
    Get all the rundles as a list.  Examine allrundles.php to find the rundles.
    """
    url = "{}/allrundles.php".format(get_ll_url())
    rundle = get_url_info(url, AllRundleParser())
    return rundle.rundles[:]
