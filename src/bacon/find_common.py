#!/usr/bin/python
#    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license. 
"""
Find the movies that two actors both appeared in.  Extract the information
from the IMDb movie pages.
"""
from HTMLParser import HTMLParser
from urllib2 import urlopen
from contextlib import closing

def read_data(real_url, in_parser): 
    """
    Read the url (real_url) and extract the data using the in_parser
    class passed.  All the in_parser classes are assumed to pass the
    expected result back in self.data.
    """
    parser = in_parser()
    with closing(urlopen(real_url)) as page:
        ldata = page.read()
        parser.feed(ldata)
    return parser.data

class NameSearchPageToActorPage(HTMLParser):
    """
    Extract the url of the actor's page from the actor's given name.
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = ''
    def handle_starttag(self, tag, attrs):
        """
        Find the first entry that looks reasonable.
        """
        if self.data:
            return
        if tag == 'a':
            for atp in attrs:
                if atp[0] == "href":
                    if atp[1].startswith("/name/"):
                        self.data = atp[1]
                        return

def name_to_actor_page(name):
    """
    Given an actor's name, return the url of that person's IMDb page.
    """
    pname = name.split(' ')
    sname = '+'.join(pname)
    wpage = "http://www.imdb.com/find?ref_=nv_sr_fn&q=%s&s=all" % sname
    return read_data(wpage, NameSearchPageToActorPage)

class ActorPageToMovieList(HTMLParser):
    """
    For a given actor, extract that person's movie list.
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.active = False
    def handle_starttag(self, tag, attrs):
        """
        First scan for the corresponding acting information for a given
        person.  The extract the urls of the movies that that person
        appeared in.
        """
        if tag == 'a':
            for atp in attrs:
                if atp[0] == "name":
                    if atp[1] in ['actor', 'actress']:
                        self.active = True
                    else:
                        self.active = False
                if atp[0] == "href":
                    if self.active:
                        if atp[1].startswith("/title/"):
                            tpart = atp[1].split('?')
                            self.data.append(tpart[0])

def actor_page_to_movie_list(apage):
    """
    Extract a list of movie url's from an actor's page.
    """
    wpage = "http://www.imdb.com%s" % apage
    return read_data(wpage, ActorPageToMovieList)

class MoviePageToTitle(HTMLParser):
    """
    Given a movie page, find the title.
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = ''
        self.title = False
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.title = True
    def handle_endtag(self, tag):
        if tag == 'title':
            self.title = False
    def handle_data(self, data):
        """
        Only find movies with year's given (this works out to be
        theatrical releases.
        """
        if self.title:
            dloc = data.rfind('(')
            if data[dloc+1] in ['1', '2']:
                if data[dloc+5] == ')':
                    self.data = data[:dloc].strip() 

def movie_page_to_title(movie):
    """
    Given a movie's url, find the title.
    """
    mpage = "http://www.imdb.com%s" % movie
    return read_data(mpage, MoviePageToTitle)

def get_movies_in_common(actor1, actor2):
    """
    Given the names of two actors, find the movies that they
    both appeared in.
    """
    p1 = name_to_actor_page(actor1) 
    list1 = actor_page_to_movie_list(p1)
    p2 = name_to_actor_page(actor2)
    list2 = actor_page_to_movie_list(p2)
    return list(set(list1) & set(list2))

def find_movies_in_common(actor1, actor2):
    """
    Given the names of two actors, find the movies that they
    both appeared in.  Return result in appropriate HTML text.
    """
    common = get_movies_in_common(actor1, actor2)
    titles = []
    for movie in common:
        mtitle = movie_page_to_title(movie)
        if len(mtitle) > 0:
            titles.append(mtitle)
    header = "<p><b>%s</b> and <b>%s</b>" % (actor1, actor2)
    if not titles:
        return "%s appeared in no movies together</p>" % header
    if len(titles) == 1:
        return "%s both appeared in <b>%s</b></p>" % (header, titles[0])
    out_txt = "%s both appeared in the following films:" % header
    for mname in titles:
        out_txt += "<li><b>%s</b></li>" % mname
    out_txt += "</p>"
    return out_txt

if __name__ == "__main__":
    """
    Unit Tests
    """
    print find_movies_in_common('Woody Allen', 'Diane Keaton')
    print find_movies_in_common('Shelley Long', 'Kevin Costner')
    print find_movies_in_common('Sean Connery', 'Kevin Costner')
    print find_movies_in_common('Joan Heal', 'Audrey Hepburn')
    print find_movies_in_common('Mary Elizabeth Mastrantonio', 'Tom Cruise')
    print find_movies_in_common('Kevin Costner', 'Audrey Hepburn')
    print find_movies_in_common('Sally Field', 'Tom Hanks')
    print find_movies_in_common('Meg Ryan', 'Tom Hanks')
