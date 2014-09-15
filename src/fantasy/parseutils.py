"""
Parse html files.

YahooParser is a superclass of the other parsing classes.
All classes defined here use the HTMLParser to extract
data off of web pages.

The parsers are:
    ParseOtherPlayers -- extract info from free agent list.
    ParseLeague -- extract team name information and a week's
                   matchups.
    ParseTeam -- extract information from a fantasy team page.
    ParseMatchup -- extract information from a matchup page
                    (fantasy matchup for a given team on a given week)
"""


# pylint: disable=R0904
from HTMLParser import HTMLParser


def extract_attr(attrs, attr_name):
    """
    Return the value of the attribute name passed
    """
    for attr in attrs:
        if attr[0] == attr_name:
            return attr[1]


class YahooParser(HTMLParser):
    """
    Generalized portion of all Yahoo Page parsers.
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.last_tag = ''
        self.last_ind = ''

    def check_tag(self, tag, attrs, parms):
        """
        Set specific tag values.  This only sets last_tag
        if the tag matches and the attribute specified matches attr_val
        """
        if tag == parms[0]:
            for attr in attrs:
                if attr[0] == parms[1]:
                    if attr[1] == parms[2]:
                        if len(parms) == 3:
                            self.last_tag = tag
                            return
                        else:
                            self.last_ind = parms[3]


class ParseOtherPlayers(YahooParser):
    """
    Scan for free agent players that did well.
    """
    def __init__(self):
        YahooParser.__init__(self)
        self.person = []
        self.results = []

    def handle_starttag(self, tag, attrs):
        """
        A player's name is in the data after specific 'a' tags.
        The player's team is in the data after specific 'span' tags.
        The player's score is in the <div> data after sepcific 'td' tags.
        """
        self.check_tag(tag, attrs, ['a', 'onclick', 'pop(this)', 'time'])
        self.check_tag(tag, attrs, ['a', 'class', 'Nowrap name'])
        self.check_tag(tag, attrs, ['span', 'class', 'Fz-xxs'])
        self.check_tag(tag, attrs, ['td', 'class',
                                   'Alt Fw-b Ta-end Nowrap Selected'])
        if tag == 'div':
            if self.last_tag == 'td':
                self.last_tag = tag

    def handle_data(self, data):
        """
        Stash the data into a list for each player.  self.results
        is a list of player lists.
        """
        if self.last_ind == 'time':
            self.person.append(data.encode('utf-8'))
            self.last_ind = ''
        if self.last_tag in ['div', 'span', 'a']:
            self.person.append(data.encode('utf-8'))
        if self.last_tag == 'div':
            self.results.append(self.person)
            self.person = []
        self.last_tag = ''


class ParseLeague(YahooParser):
    """
    Get league team and matchup information
    """
    def __init__(self):
        YahooParser.__init__(self)
        self.team_table = {}
        self.match_ups = []
        self.numb = -1
        self.one_match = []

    def handle_starttag(self, tag, attrs):
        """
        Extract the team number from the appropriate tags.
        """
        self.check_tag(tag, attrs, ['div', 'class', 'Fz-sm Ell Mawpx-175'])
        if tag == 'a':
            if self.last_tag == 'div':
                self.last_tag = tag
                tnumb = extract_attr(attrs, 'href').split('/')
                self.numb = int(tnumb[-1])

    def handle_data(self, data):
        """
        Set up an list of matchups where each entry matches up two numbered
        teams.
        """
        if self.last_tag == 'a':
            self.team_table[data] = self.numb
            self.one_match.append(self.numb)
            if len(self.one_match) == 2:
                self.match_ups.append(self.one_match)
                self.one_match = []
        self.last_tag = ''


class ParseTeam(YahooParser):
    """
    Get information for my team.
    """
    def __init__(self):
        YahooParser.__init__(self)
        self.d_flag = 0
        self.n_flag = False
        self.output = {}
        self.current_key = ''
        self.pos_track = {}
        self.pcount = 0

    def handle_starttag(self, tag, attrs):
        """
        Find unique attribute names and values to set appropriate data
        reading flags.
        """
        self.check_tag(tag, attrs, ['span', 'class', 'Fz-xxs'])
        for attr in attrs:
            if attr[0] == 'data-pos':
                if attr[1] in self.pos_track:
                    self.pos_track[attr[1]] += 1
                else:
                    self.pos_track[attr[1]] = 1
                self.current_key = "%s%d" % (attr[1], self.pos_track[attr[1]])
                self.output[self.current_key] = {}
            if attr[1] == \
                    'ysf-player-name Nowrap Grid-u Relative Lh-xs Ta-start':
                self.d_flag = True
            if attr[1] == 'Alt Fw-b Ta-end Nowrap Bdrstart':
                self.n_flag = True

    def handle_data(self, data):
        if self.pcount >= 15:
            return
        if self.last_tag == 'span':
            self.output[self.current_key]['position'] = data.encode('utf-8')
            self.last_tag = ''
        if self.d_flag:
            self.output[self.current_key]['name'] = data.encode('utf-8')
            self.d_flag = False
        if self.n_flag:
            self.output[self.current_key]['data'] = data.encode('utf-8')
            self.n_flag = False
            self.pcount += 1


class ParseMatchup(YahooParser):
    """
    Get information from a matchup page
    """
    def __init__(self):
        YahooParser.__init__(self)
        self.data = {}

    def handle_starttag(self, tag, attrs):
        self.check_tag(tag, attrs, ['div', 'class', 'Fz-lg Ell', 'rotoname'])
        self.check_tag(tag, attrs, ['a', 'onclick', 'pop(this)', 'time'])
        self.check_tag(tag, attrs, ['span', 'class', 'Fz-xxs', 'team'])
        self.check_tag(tag, attrs, ['div', 'class',
                    'ysf-player-name Nowrap Grid-u Relative Lh-xs Ta-start',
                    'player'])
        self.check_tag(tag, attrs, ['td', 'class',
                    'Pend-lg Ta-end Fw-b Nowrap Va-top', 'score1'])
        self.check_tag(tag, attrs, ['td', 'class',
                    'Ta-end Fw-b Nowrap Va-top', 'score2'])

    def handle_data(self, data):
        if not self.last_ind:
            return
        if data == 'Fan Pts':
            self.last_ind = ''
            return
        if self.last_ind in self.data:
            self.data[self.last_ind].append(data)
        else:
            self.data[self.last_ind] = [data]
        if self.last_ind == 'time':
            self.last_ind = 'opp'
            return
        self.last_ind = ''
