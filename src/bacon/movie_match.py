#!/usr/bin/python
#    Copyright (C) 2017 Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license.
"""
Cgi script to collect movies in common information.
"""

import cgi
import cgitb
import logging
from find_common import find_movies_in_common

def getpost():
    """
    Input: Two actor's names, separated by '|'
    Output: Text from find_movies_in_common() [movies in common information]
    """
    logging.basicConfig(filename='results.log', level=logging.DEBUG)
    logging.info('next problem')
    cgitb.enable()
    form = cgi.FieldStorage()
    instr = form['data'].value
    logging.info(instr)
    name = instr.split('|')
    answer = find_movies_in_common(name[0], name[1])
    print 'Content-type: text/html'
    print
    print answer

if __name__ == "__main__":
    getpost()

