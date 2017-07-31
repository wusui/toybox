#!/usr/bin/python
"""
Copyright (C) 2016  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Sum of a Square and a Cube -- Project Euler Problem 348
"""
from datetime import datetime


def ispalin(val):
    """
    Return true only if number passed is a palindrome.
    """
    lval = str(val)
    if lval == lval[::-1]:
        return True
    return False


def problem348():
    """
    Generate all solution possible within a range.  Sort the result and take
    the first 5.

    Uplimit is a guess for a safe upper limit.
    """
    squarez = []
    cubez = []
    palindromes = {}
    uplimit = 10 ** 9
    i = 1
    sval = 1
    cval = 1
    while sval < uplimit:
        sval = i * i
        squarez.append(sval)
        if cval < uplimit:
            cval = i * i * i
            cubez.append(cval)
        i += 1
    for sq_ind in squarez:
        for cube_ind in cubez:
            key = sq_ind + cube_ind
            if ispalin(key):
                palindromes[key] = palindromes.get(key, 0) + 1
    solved = []
    for key in palindromes:
        if palindromes[key] >= 4:
            solved.append(key)
    ans = sorted(solved)
    return sum(ans[0:5])


if __name__ == "__main__":
    STRT = datetime.now()
    print problem348()
    print datetime.now() - STRT
