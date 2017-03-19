#!/usr/bin/env python
"""
Read bracket entries and generate list of picks that are saved in a file named
picks.json
"""
import json
from urllib2 import urlopen
from contextlib import closing
from HTMLParser import HTMLParser
from os import sep
from check_data import HandleEspnGroup
from check_data import ENTRY
from check_data import TOURNEY_DATA


class ParseEntry(HTMLParser):
    # Parse a player's entry, extracting the name, selected winner, and
    # teams picked in order.
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
        # Find the entry name and appropriate team indicators in the metadata
        for attr in attrs:
            if attr[0] == 'title':
                self.title = True
            if attr[0] == 'class':
                if attr[1] == 'abbrev':
                    self.abbrev = True
                if attr[1] == 'entry-details-entryname':
                    self.gname = True

    def handle_data(self, data):
        # Skip the first 64 entries (all teams on the bracket).  Then find
        # teams in order.  Handle the` National Champion as a special case.
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
    # Scan for teams matching up in the next round to determine winners.
    def __init__(self, rnd):
        HTMLParser.__init__(self)
        self.rnd = "match round%d" % rnd
        self.retvec = []
        self.find = False
        self.savedata = False

    def handle_starttag(self, tag, attrs):
        # Set indicators when text data should be extracted.
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
        # Exxtract text data corresponding to selected teams.
        if self.savedata:
            self.retvec.append(data)
        self.savedata = False


def get_reality():
    """
    Get the wins and losses from the latest tournament page.  Loop through the
    same tournament data text for each round.

    Returns: List whose entries are: a list of first round winners, a list of
             second round winners, a list of third round winners...  Number of
             entries here depends on how deep we are in the tournament at this
             time.
    """
    retv = []
    with closing(urlopen(TOURNEY_DATA)) as page:
        httpdata = page.read()
    for cnt in range(2, 7):
        parser = ParseWins(cnt)
        parser.feed(httpdata)
        if not parser.retvec:
            return retv
        retv.append(parser.retvec[:])
    return retv


def get_teams(in_url):
    # Pass the individual bracket through an html parser.  This extracts
    # a list of teams that needs to get reformatted into the right order
    # for the picks.json file.
    #
    # in_url -- url of this bracket / entry
    parser = ParseEntry()
    with closing(urlopen(in_url)) as page:
        parser.feed(page.read())
    return (parser.name, [parser.data[64:96], parser.data[96:112],
            parser.data[112:120], parser.data[120:124],
            parser.data[124:126], [parser.winner]])


def get_picks(group):
    """
    Read the entries in the numbs.txt file for this group, and extract the
    names of winning teams from the corresponding url.  Generate appropriately
    formatted values for the picks.json file.

    group -- group name (pool/rundle name)
    """
    ret_data = []
    infile = sep.join(['data', group, 'numbs.txt'])
    with open(infile, 'r') as f:
        indata = f.read()
    idata = indata.strip().split('\n')
    for picks in idata:
        pinfo = ENTRY % picks
        tinfo = get_teams(pinfo)
        print "Getting picks for %s" % tinfo[0]
        ret_data.append(tinfo)
    with open(sep.join(['data', group, 'picks.json']), 'w') as f:
        json.dump(ret_data, f)

if __name__ == "__main__":
    HandleEspnGroup().caller(get_picks)
