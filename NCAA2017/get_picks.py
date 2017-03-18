import json
from urllib2 import urlopen
from contextlib import closing
from HTMLParser import HTMLParser
from os import sep
from check_data import HandleEspnGroup

class ParseEntry(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.count = 0
        self.name = ''
        self.winner = ''
        self.abbrev = False
        self.title = False
        self.gname = False
        self.champ = False
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'title':
                self.title = True
            if attr[0] == 'class':
                if attr[1] == 'abbrev':
                    self.abbrev = True
                if attr[1] == 'entry-details-entryname':
                    self.gname = True
    def handle_data(self, data):
        if data == 'National Champion':
            self.champ = True
            return
        if data == 'Winning Score':
            self.champ = False
            return
        if self.gname:
            self.name = data
        self.gname = False
        if self.champ:
            if self.title and self.abbrev:
                self.winner = data
                self.title = False
                self.abbrev = False
                return
        if self.count >= 64:
            if self.title and self.abbrev:
                self.data.append(data)
        self.count += 1
        self.title = False
        self.abbrev = False

class ParseWins(HTMLParser):
    def __init__(self, rnd):
        HTMLParser.__init__(self)
        self.rnd = "match round%d" % rnd
        self.retvec = []
        self.find = False
        self.savedata = False
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'class':
                if attr[1] == self.rnd:
                    self.find = True
                else:
                    self.find = False
            if attr[0] == 'title':
                if self.find:
                    self.savedata = True
    def handle_data(self, data):
        if self.savedata:
            self.retvec.append(data)
        self.savedata = False

def get_reality():
    retv = []
    with closing(urlopen('http://www.espn.com/mens-college-basketball/tournament/bracket')) as page:
        httpdata = page.read()
    for cnt in range(2,7):
        parser = ParseWins(cnt)
        parser.feed(httpdata)
        if not parser.retvec:
            return retv
        retv.append(parser.retvec[:])
    return retv

def get_teams(in_url):
    parser = ParseEntry()
    with closing(urlopen(in_url)) as page:
        parser.feed(page.read())
    return (parser.name, [parser.data[64:96], parser.data[96:112], parser.data[112:120], parser.data[120:124], parser.data[124:126], [parser.winner]])

def get_picks(group):
    ret_data = []
    infile = sep.join(['data', group, 'numbs.txt'])
    with open(infile, 'r') as f:
        indata = f.read()
    idata = indata.strip().split('\n')
    for picks in idata:
        pinfo = "http://games.espn.com/tournament-challenge-bracket/2017/en/entry?entryID=%s" % picks
        tinfo = get_teams(pinfo)
        print "Getting picks for %s" % tinfo[0]
        ret_data.append(tinfo)
    with open(sep.join(['data', group, 'picks.json']), 'w') as f:
        json.dump(ret_data, f)

if __name__ == "__main__":
    HandleEspnGroup().caller(get_picks)
