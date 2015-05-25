#!/usr/bin/python
#    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license. 
"""
Cgi script to collect word rummy input.  Returns a solution, if possible.
"""

import cgi
import cgitb
import logging
from solver import solver

def getpost():
    """
    Stdin comes from the web page and is a set of letters.

    Call solver and send the solution (an html table) to stdout.
    """
    logging.basicConfig(filename='results.log',level=logging.DEBUG)
    cgitb.enable()
    form = cgi.FieldStorage()
    instr = form["data"].value.replace(' ','0')
    pieces = list(instr)
    logging.info(pieces)
    answer = solver(pieces)
    print "Content-type: text/html"
    print
    logging.info('response: ')
    logging.info(answer)
    print answer

if __name__ == "__main__":
    getpost()

