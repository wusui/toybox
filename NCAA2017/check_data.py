#!/usr/bin/env python
"""
Check to make sure that all data/XXX/numbs.txt and data/XXX/peeps.txt files
are valid.
"""
from urllib2 import urlopen
from contextlib import closing
from HTMLParser import HTMLParser
from os import sep
from os import listdir
from os.path import isfile

ESPN = "http://games.espn.com/"
ENTRY = ESPN + "tournament-challenge-bracket/2017/en/entry?entryID=%s"
TOURNEY_DATA = ESPN + 'mens-college-basketball/tournament/bracket'


class ParseText(HTMLParser):
    # HTMLParser version used to parse web entries for individual brackets.
    def __init__(self):
        HTMLParser.__init__(self)
        self.glink = False
        self.elink = False
        self.ingroup = []
        self.href = ''
        self.name = ''

    def handle_starttag(self, tag, attrs):
        # Set entry names and groups associated with a page based on tag
        # metadata.
        for attr in attrs:
            if attr[0] == 'class':
                if attr[1] == 'group-link':
                    self.glink = True
                if attr[1] == 'entry-details-entryname':
                    self.elink = True
            if attr[0] == 'href':
                self.href = attr[1]

    def handle_data(self, data):
        # Find all group names on bracket page (saved in self.ingroup).
        # Find entryname and save in self.name.
        if self.glink:
            parts = self.href.split('=')
            if not parts[0] == 'group?groupID':
                print 'Invaid href'
            self.ingroup.append(parts[1])
        self.glink = False
        self.href = ''
        if self.elink:
            self.name = data.strip()
            self.elink = False


def chk_dups(alist):
    # Return true if the list specified contains duplicate entries, false
    # if it does not.
    #
    # alist -- list in question
    aset = set(alist)
    if len(aset) != len(alist):
        print 'list containing %s has dups' % alist[0]
        return True
    return False


def read_text(group_name, file_txt):
    # Called from check_data to read a text file.
    #
    # group_name -- group we are checking.
    # file_txt -- name of the file we are reading
    in_file = sep.join(['data', group_name, file_txt])
    with open(in_file, 'r') as f:
        data = f.read()
    return data.strip().split('\n')


class HandleEspnGroup(object):
    """
    Object created by all routines that will act on the directories saved
    in the data directory.
    """
    def __init__(self):
        """
        Self.rundles is a dictionary where each key is a group name and
        each entry is the group number used by ESPN.  This dictionary is
        iterated through whenever the main action of each python script
        is executed via the caller function.
        """
        self.rundles = {}
        for dname in listdir('data'):
            fname = sep.join(['data', dname, 'groupno.txt'])
            if isfile(fname):
                with open(fname, 'r') as f:
                    number = f.read().strip()
                    self.rundles[dname] = number

    def caller(self, func_to_call):
        """
        Call the passed in function for all groups found.

        func_to_call -- function that will be executed
        """
        for keyv in self.rundles.keys():
            func_to_call(keyv)


def check_data(group_name):
    """
    First make sure that both the number file and the entrant name file
    have the same number of lines.  Then make sure that there are no
    duplicates in each. After that each pair of lines from the two files
    is compared one by one to make sure that they match.

    group_name -- Group being tested
    """
    group_id = HandleEspnGroup().rundles[group_name]
    print "checking %s with group id %s" % (group_name, group_id)
    plist = read_text(group_name, 'peeps.txt')
    nlist = read_text(group_name, 'numbs.txt')
    if len(plist) != len(nlist):
        print 'Lengths of peeps and numbs do not match'
        return
    schk = chk_dups(plist)
    schk |= chk_dups(nlist)    
    if schk:
        return
    for i in range(0, len(plist)):
        parser = ParseText()
        in_url = ENTRY % nlist[i]
        with closing(urlopen(in_url)) as page:
            parser.feed(page.read())
        if parser.name != plist[i]:
            print 'Name and number do not match %s vs. %s' % (parser.name,
                                                              plist[i])
        if group_id not in parser.ingroup:
            print 'group number is not linked to bracket page'
            print '     bracket page number is probably wrong'

if __name__ == "__main__":
    HandleEspnGroup().caller(check_data)
