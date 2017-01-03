#!/usr/bin/python
#    Copyright (C) 2016 Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license.

import cgi
import cgitb
import logging
from brains.wrapper import solver_filter

def getpost():
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
