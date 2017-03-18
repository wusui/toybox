from urllib2 import urlopen
from contextlib import closing
from HTMLParser import HTMLParser
from os import sep
from os import listdir
from os.path import isfile

class ParseText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.glink = False
        self.elink = False
        self.ingroup = []
        self.href = ''
        self.name = ''
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'class':
                if attr[1] == 'group-link':
                    self.glink = True
                if attr[1] == 'entry-details-entryname':
                    self.elink = True
            if attr[0] == 'href':
                self.href = attr[1]
    def handle_data(self, data):
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
    aset = set(alist)
    if len(aset) != len(alist):
        print 'list containing %s has dups' % alist[0]
        return True
    return False

def read_text(group_name, file_txt):
    in_file = sep.join(['data',group_name, file_txt])
    with open(in_file, 'r') as f:
        data = f.read()
    return data.strip().split('\n')

class HandleEspnGroup(object):
    def __init__(self):
        self.rundles = {}
        for dname in listdir('data'):
            fname = sep.join(['data', dname, 'groupno.txt'])
            if isfile(fname):
                with open(fname, 'r') as f:
                    number = f.read().strip()
                    self.rundles[dname] = number;
    def caller(self, func_to_call):
        for keyv in self.rundles.keys():
            func_to_call(keyv)
        
def check_data(group_name):
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
        in_url = "http://games.espn.com/tournament-challenge-bracket/2017/en/entry?entryID=%s" % nlist[i]
        with closing(urlopen(in_url)) as page:
            parser.feed(page.read())
        if parser.name != plist[i]:
            print 'Name and number do not match %s vs. %s' % (parser.name, plist[i])
        if group_id not in parser.ingroup:
            print 'group number is not linked to bracket page -- bracke page number is probably wrong'

if __name__ == "__main__":
    HandleEspnGroup().caller(check_data)

