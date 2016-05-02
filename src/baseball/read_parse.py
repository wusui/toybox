#!/usr/bin/env python
from HTMLParser import HTMLParser
import contextlib
import urllib2

def read_parse(html_file):
    """Return table information

    Input: html file
    Returns: A list of tables parsed from the html file.
    """
    return gen_parse(html_file, tableParser())

def get_team_names(league):
    """Get teams in this league.

    Input: league number
    Returns: Dictionary keyed by team-name whose values are the correspoding
             team number
    """
    html_name = "http://baseball.fantasysports.yahoo.com/b1/%d" % league
    return gen_parse(html_name, hrefFinder())

def gen_parse(html_file, parser):
    """Html file reader and parser.

    Input:
        html_file: Path of the html file to parse
        parser: tableParser or hrefFinder
    Returns: get_result value for the corresponding parser.
    """
    with contextlib.closing(urllib2.urlopen(
            urllib2.Request(html_file))) as response:
        parser.feed(response.read())
    return parser.get_result()

class tableParser(HTMLParser, object):
    """Table parsing object.

    When parsing is finished, get_result will return a list of tables.
    Each table is extracted from the html file and consists of a list of rows.
    Each row is a list of fields in that row.
    """
    def __init__(self):
        self.retv = []
        self.row = []
        self.table = []
        self.collect = False
        super(tableParser, self).__init__()
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.collect = True
    def handle_endtag(self, tag):
        if tag == 'tr':
            self.collect = False
            self.table.append(self.row)
            self.row = []
        if tag == 'table':
            self.retv.append(self.table)
            self.table = []
    def handle_data(self, data):
        if self.collect:
            self.row.append(data.strip())
    def get_result(self):
        return self.retv

class hrefFinder(HTMLParser, object):
    """Team name parser/finder

    When parsing is completed, get_result will return a dictionary.
    Each key will be a team name, each value will be the corresponding
    number of that team in the league.
    """
    def __init__(self):
        self.retv = {}
        self.save = -1
        super(hrefFinder, self).__init__()
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'href':
               parts = attr[1].split('/')
               if len(parts) != 4:
                   continue
               if parts[1] == "b1":
                   if parts[2].isdigit():
                       if parts[3].isdigit():
                           self.save = int(parts[3])
    def handle_data(self, data):
        if self.save > 0:
            self.retv[data] = self.save
            self.save = -1
    def get_result(self):
        return self.retv
