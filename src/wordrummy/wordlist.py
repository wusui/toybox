#!/usr/bin/python
#    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license. 
"""
Get a list of seven letter words off of the internet.
"""
from HTMLParser import HTMLParser
from urllib2 import urlopen
from contextlib import closing
from re import findall


WORD_LIST = "http://www.allscrabblewords.com/7-letter-words/"
WORD_LENGTH = 7

class ParseFindWords(HTMLParser):
    """
    HTMLParser class used by WordList to extract data.
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = ""
        self.getit = False
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    if attr[1].startswith('/word-description/'):
                        self.getit = True
    def handle_data(self, data):
        if self.getit:
            self.data += " %s" % data.strip().upper()
        self.getit = False
            
class WordList():
    """
    Seven letter word list generator
    """
    def __init__(self):
        """
        Extract data from a website.
        """
        real_url = WORD_LIST
        parser = ParseFindWords()
        with closing(urlopen(real_url)) as page:
            self.data = page.read()
            parser.feed(self.data)
        self.wordlist = parser.data

    def findStart(self, runstr):
        """
        Find all words that begin with the sequence passed.
        """
        dots = '.......'[0: WORD_LENGTH - len(runstr)]
        retv = []
        for wurd in findall(' %s%s' % (runstr, dots), self.wordlist):
            retv.append(wurd.strip()[len(runstr):])
        return retv
    def findEnd(self, runstr):
        """
        Find all words that end with the sequence passed.
        """
        dots = '......'[0: WORD_LENGTH - len(runstr)]
        retv = []
        for wurd in findall(' %s%s' % (dots, runstr), self.wordlist):
            retv.append(wurd.strip()[0:WORD_LENGTH - len(runstr)])
        return retv

if __name__ == "__main__":
    w = WordList()
    print w.findStart('CON')
    print w.findEnd('WING')
    print w.findStart('COND')
    print w.findEnd('CAL')
