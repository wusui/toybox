#!/usr/bin/python
#    Copyright (C) 2016 Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license.
"""
Cgi script to collect chess problem data.  Returns a solution, if possible.
"""

import cgi
import cgitb
import logging
from brains.wrapper import solver_filter

def getpost():
    """
    Given the cgi input, call solve_filter in brains/wrapper.  Return the
    result.
    
    The data field in the form sent by the html page and associated javascript
    represents a chess problem.  This field is a single string separated by
    slashes into three substrings.  Those substrings are:
        - The number of moves White needs to checkmate Black
        - W: followed by algebraic notation for the location of each white
             piece.   
        - B: followed by algebraic notation for the location of each black
             piece.   
   
    The returned data is a single string separated by or-bars into four
    substrings.  The substrings are:
        - Header label of the dialog box to be displayed on the remote site.
        - Text to be displayed on the remote site.
        - Dialog box height.
        - Dialog box width.
    """
    logging.basicConfig(filename='results.log',level=logging.DEBUG)
    logging.info('new message')
    cgitb.enable()
    form = cgi.FieldStorage()
    instr = form['data'].value
    logging.info(instr)
    answer = solver_filter(instr)
    logging.info(answer)
    print 'Content-type: text/html'
    print
    print answer

if __name__ == "__main__":
    getpost()
