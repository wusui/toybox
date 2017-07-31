#!/usr/bin/python
"""
Copyright (C) 2016  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Counting Digits -- Project Euler Problem 156
"""
from datetime import datetime


def checkout(numbr, digit):
    """
    Solve f(n,d) as defined in the problem definition
    """
    dval = 1
    ans = 0
    while dval <= numbr:
        nval = dval * 10
        lftnumb = (numbr // nval) * dval
        rgtnumb = numbr % dval
        odigit = (numbr // dval) % 10
        ans += lftnumb
        if odigit > digit:
            ans += dval
        if odigit == digit:
            ans += rgtnumb+1
        dval = nval
    return ans


class NumbData(object):
    """
    Object for storing information while extracting a solution for parameter d.
    """
    def __init__(self, value):
        self.value = value
        self.upper = value * (10**10)
        self.lower = 0
        self.solution = []
        self.checked = []

    def solve(self, lower, upper):
        """
        Binary search between two bounds.  Returns a new set of bounds
        where all points between those numbers are not solutions.  Endpoint
        values can be checked later.
        """
        mid = (lower + upper) / 2
        prev = 0
        mpt = mid
        while prev != mpt:
            prev = mpt
            mpt = checkout(prev, self.value)
            if mpt > self.upper:
                return [mid, self.upper]
        if mpt > mid:
            return [mid, mpt]
        return [mpt, mid]

    def notdone(self):
        """
        Returns False only when there is one entry left in self.checked that
        indicates the range of all possible answers has been checked.
        """
        if len(self.checked) != 1:
            return True
        if self.checked[0][0] != 0:
            return True
        if self.checked[0][1] != self.upper:
            return True
        return False


def problem156_inner(iparm):
    """
    Main loop for this problem.

    NumbData.checked is used to hold regions of the number line that have
    been tested.  NumbData.solution holds points found along the way.  In
    general, we find gaps between NumbData.checked fields and try solving
    for those, terminating when the entire range of possible solutions has
    been verified.
    """
    nrep = NumbData(iparm)
    minv = 0
    maxv = nrep.upper
    nrange = []

    def do_search():
        """
        search for a number that matches it's position
        """
        nadded = False
        for i in range(0, len(nrep.checked)):
            if nrange[0] <= nrep.checked[i][0]:
                if nrange[1] >= nrep.checked[i][1]:
                    nrep.checked[i] = nrange
                    nadded = True
                    break
                elif nrange[1] >= nrep.checked[i][0]:
                    nrep.checked[i][0] = nrange[0]
                    nadded = True
            else:
                if nrange[0] <= nrep.checked[i][1] and \
                        nrange[1] >= nrep.checked[i][1]:
                    nrep.checked[i][1] = nrange[1]
                    nadded = True
        return nadded

    def found_match():
        """
        Update nrep if matching values are found
        """
        skip = False
        for i in range(0, len(cpy)):
            if skip:
                skip = False
                continue
            if i+1 < len(cpy) and cpy[i][1] >= cpy[i+1][0]-1:
                cpy[i][1] = cpy[i+1][1]
                skip = True
            nrep.checked.append(cpy[i])

    def none_continue():
        """
        Update nrep if no matching values are found
        """
        last = -1
        for i in range(0, len(cpy)):
            if nrange[0] > last and nrange[1] < cpy[i][0]:
                nrep.checked.append(nrange)
            nrep.checked.append(cpy[i])
            last = cpy[i][1]
        if nrange[0] > last:
            nrep.checked.append(nrange)

    while nrep.notdone():
        nrange = nrep.solve(minv, maxv)
        for i in range(0, 2):
            if checkout(nrange[i], iparm) == nrange[i]:
                nrep.solution.append(nrange[i])
        if not nrep.checked:
            nrep.checked = [nrange]
        else:
            added = do_search()
            cpy = nrep.checked[:]
            nrep.checked = []
            if added:
                found_match()
            else:
                none_continue()
            if nrep.checked[0][0] > 0:
                minv = 0
                maxv = nrep.checked[0][0]
            else:
                minv = nrep.checked[0][1]
                if len(nrep.checked) > 1:
                    maxv = nrep.checked[1][0]
                else:
                    maxv = nrep.upper
    return sum(set(nrep.solution))


def problem156():
    """
    Top-level loop for all numbers.
    """
    answer = 0
    for i in range(1, 10):
        answer += problem156_inner(i)
    return answer

if __name__ == "__main__":
    STRT = datetime.now()
    print problem156()
    print datetime.now() - STRT
