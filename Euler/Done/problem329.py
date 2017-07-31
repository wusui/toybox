#!/usr/bin/python
"""
Copyright (C) 2016  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Prime Frog -- Project Euler Problem 329
"""
from datetime import datetime
from array import array


def bigsieve(size):
    """
    Prime number sieve -- from a common library

    Input: size of table (prime numbers up to size are found).

    Returns: List of prime numbers.

    Uses the Sieve of Eratosthenes to find prime numbers.  Table only
    saves numbers whose last digit is 1, 3, 7, or 9.

    This routine is a generator function.  It uses one sieve if the number
    of primes generate are below 10 million.  If more primes are generated,
    it sieves for 10 million and reuses the sieve space for numbers greater
    than 10 million
    """
    def conv(number):
        """
        Given a number, find the table index for that number
        """
        row = number // 10
        col = {1: 0, 3: 1, 7: 2, 9: 3}[number % 10]
        return row * 4 + col

    def unconv(number):
        """
        Given a table index, find the corresponding numeric value
        """
        row = number // 4
        col = {0: 1, 1: 3, 2: 7, 3: 9}[number % 4]
        return row * 10 + col

    def fill_first(tlim):
        """
        Fill the sieve for the first time
        """
        for i in range(3, tlim, 2):
            if i % 5 == 0:
                continue
            ind = conv(i)
            if table[ind]:
                continue
            if i*i > tlim:
                break
            for j in range(i*i, tlim, i*2):
                if j % 5 == 0:
                    continue
                table[conv(j)] = True

    def fill_section(start):
        """
        Refill the sieve after the first time that it was filled.
        """
        tlim = 10**7
        for fctor in listr:
            if fctor * fctor > start + tlim:
                break
            offset = fctor - (start % fctor)
            if offset % 2 == 0:
                offset += fctor
            for j in range(offset, tlim, fctor*2):
                if j % 5 == 0:
                    continue
                table[conv(j)] = True

    yield 2
    yield 5
    tlim = 10**7
    if size <= tlim:
        tlim = size
    tsize = (tlim * 2) / 5
    table = array("B", b"\x00" * tsize)
    listr = []
    fill_first(tlim)
    table[0] = True
    for count, entry in enumerate(table):
        if not entry:
            tval = unconv(count)
            listr.append(tval)
            yield tval
        table[count] = False
    if size <= tlim:
        return
    for szv in range(tlim, size, tlim):
        fill_section(szv)
        for count, entry in enumerate(table):
            if not entry:
                yield szv+unconv(count)
            table[count] = False


def gcd(big, little):
    """
    Return the gcd of two numbers
    """
    while little > 0:
        rem = big % little
        big = little
        little = rem
    return big


def frac_disp(numer, denom):
    """
    Display a fraction as a reduced numerator  / denominator value
    """
    if numer > denom:
        factor = gcd(numer, denom)
    else:
        factor = gcd(denom, numer)
    return "%s/%s" % (numer // factor, denom // factor)


def problem329inner(psize, fstring):
    """
    Generate values for every starting square.

    For each square in the sequence, the denominator should go up by a power
    of 3.  After the first square, every subsequent set of possible squares
    is twice as large, so the denominator should go up by a power of 2.  The
    unreduced denominator will be that number multiplied by the total number
    of squares (500 in this problem's case).

    For every prime / non-prime match, the numerator should go up by 2.
    Boundary cases (1 and 500) are handled by bouncing the frog back and
    treating the new square like any other.
    """
    plist = []
    for i in bigsieve(psize):
        plist.append(i)
    numer = 0
    for i in range(0, psize):
        curv = [[i + 1, 1]]
        for cnt in range(0, len(fstring)):
            for loc in curv:
                myc = 'N'
                if loc[0] in plist:
                    myc = 'P'
                if myc == fstring[cnt]:
                    loc[1] *= 2
            if cnt == len(fstring) - 1:
                break
            ncurv = []
            for pair in curv:
                nleft = pair[0] - 1
                if nleft == 0:
                    nleft = 2
                nright = pair[0] + 1
                if nright == psize + 1:
                    nright = psize - 1
                ncurv.append([nleft, pair[1]])
                ncurv.append([nright, pair[1]])
            curv = ncurv
        for entry in curv:
            numer += entry[1]
    denom = (3 ** len(fstring)) * (2 ** (len(fstring) - 1)) * psize
    return frac_disp(numer, denom)


def problem329():
    """
    Wrapper for specific call.
    """
    return problem329inner(500, 'PPPPNNPPPNPPNPN')


if __name__ == "__main__":
    STRT = datetime.now()
    print problem329()
    print datetime.now() - STRT
