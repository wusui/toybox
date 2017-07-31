#!/usr/bin/python
"""
Copyright (C) 2016  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Under the Rainbow -- Project Euler Problem 493
"""
from datetime import datetime


def combo(whole, part):
    """
    Compute the number of combinations possible

    Returns: x!/(y!(x-y)!)

    Input: whole -- x in above equation
            part -- y in above equation
    """
    if part == 0:
        return 1
    rest = whole - part
    if rest > part:
        temp = part
        part = rest
        rest = temp
    numer = 1
    for i in range(whole, part, -1):
        numer *= i
    denom = 1
    for i in range(rest, 1, -1):
        denom *= i
    return numer/denom


def dec_div_disp(numer, denom, digits):
    """
    Perform a long division operation and return the result as text.

    Input:
        numer -- numerator
        denom -- denominator
        digits -- number of digits to display after the decimal point
    """
    numer *= 10**(digits+1)
    pansw = numer // denom
    pansw += 5
    pansw /= 10
    txt = str(pansw)
    return txt[0]+"."+txt[1:]


def problem493():
    """
    Pretty much brute force the solution.  There are probably more
    elegant ways of doing this.
    """
    roy = combo(30, 20) - combo(3, 2)
    royg = combo(40, 20) - combo(4, 3) * roy - combo(4, 2)
    roygb = (combo(50, 20) - combo(5, 4) * royg - combo(5, 3) *
             roy - combo(5, 2))
    roygbi = (combo(60, 20) - combo(6, 5) * roygb - combo(6, 4) *
              royg - combo(6, 3) * roy - combo(6, 2))
    roygbiv = (combo(70, 20) - combo(7, 6) * roygbi - combo(7, 5) *
               roygb - combo(7, 4) * royg - combo(7, 3) * roy - combo(7, 2))
    denom = combo(70, 20)
    numer = (2 * combo(7, 2) + 3 * combo(7, 3) * roy + 4 * combo(7, 4) *
             royg + 5 * combo(7, 5) * roygb + 6 * combo(7, 6) * roygbi + 7 *
             roygbiv)
    return dec_div_disp(numer, denom, 9)

if __name__ == "__main__":
    STRT = datetime.now()
    print problem493()
    print datetime.now() - STRT
