"""
Parse subclasses.
"""
from HTMLParser import HTMLParser

# pylint: disable=R0904
class ParseMatchup(HTMLParser):
    """
    Read a url and extract all team numbers in order that they first appear.
    This can be used to reconstruct the head to head matches for a given
    week.
    """
    def __init__(self, league):
        HTMLParser.__init__(self)
        self.results = []
        self.league = '/f1/%s/' % league
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    if attr[1].startswith(self.league):
                        fld = attr[1][len(self.league):]
                        if fld.isdigit():
                            fld = int(fld)
                            if fld not in self.results:
                                self.results.append(fld)

class ParsePlayers(HTMLParser):
    """
    Read a url and extract all data for a player on that page.
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.results = ([], {})
        self.lkey = ''
        self.headp = "http://sports.yahoo.com/nfl/players/"
        self.headt = "http://sports.yahoo.com/nfl/teams/"
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    value = '/news'
                    if attr[1].startswith(self.headp):
                        value = attr[1][len(self.headp):]
                    if attr[1].startswith(self.headt):
                        value = attr[1][len(self.headt):]
                    if not value.endswith('/news'):
                        self.results[0].append(value)
                        self.lkey = value
                        self.results[1][value] = []
    def handle_data(self, data):
        if self.lkey:
            data = data.strip()
            if data:
                self.results[1][self.lkey].append(data)
    def handle_endtag(self, tag):
        if tag == 'section':
            self.lkey = ''

class ParseTeams(HTMLParser):
    """
    Read a url and extract all team related data.
    This ends up being a table associating team names to team numbers.
    and a table associating team numbers to team names.
    """
    def __init__(self, league):
        HTMLParser.__init__(self)
        self.league = '/f1/%s/' % league
        self.results = ({}, {})
        self.ind = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    if attr[1].startswith(self.league):
                        self.ind = attr[1][len(self.league):]
    def handle_data(self, data):
        if self.ind:
            if self.ind.isdigit():
                if data:
                    self.results[0][data] = self.ind
                    self.results[1][self.ind] = data
        self.ind = ''
