#!/usr/bin/python
#    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license. 
"""
Cgi script to collect sudoku puzzle data.  Returns a solution, if possible.
"""

from solver import solver

import cgi
import cgitb

def getpost():
    """
    Stdin comes from the web page and is a set of sudoku numbers.

    Call solver and send the solution as a set of cell values to stdout.
    """
    cgitb.enable()
    form = cgi.FieldStorage()
    instr = form["data"].value.replace(' ','0')
    pieces = list(instr);
    tplate = []
    indx = 0
    for i in range(0,9):
        tplate.append([])
        for j in range(0,9):
           tplate[i].append(pieces[indx])
           indx += 1
    _, result = solver(tplate)
    outstr = []
    for i in range(0,9):
        for j in range(0,9):
            outstr.append(result[i][j])
    print "Content-type: text/html"
    print
    print ''.join(outstr).replace('0',' ')

if __name__ == "__main__":
    getpost()
