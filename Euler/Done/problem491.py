#!/usr/bin/python
"""
Copyright (C) 2017  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Divisibility Streaks -- Project Euler Problem 491
"""
from datetime import datetime


def problem491():
    """
    If a number is divisible by 11, then the differences between the odd
    digits and the even digits must be divisible by 11.  In this problem,
    in order to be divisible by 11 the sum of the odd digits have to be
    23, 34, 45, 56, or 67 in order for there to be a solution.
    This program loops through all distributions (0, 1, or 2) of each digit,
    and finds the sets that are correct for numbers that are divisible by 11.
    The number of permutations of these numbers, and the corresponding even
    numbers, are then calculated.
    """
    tenfact = 1
    for i in range(2, 11):
        tenfact *= i
    answer = 0
    for i in range(0, 3**10):
        isum = 0
        idv = i
        vals = []
        for j in range(0, 10):
            isum += idv % 3
            vals.append(idv % 3)
            idv //= 3
        if isum == 10:
            tot = 0
            twocnt = 0
            for j in range(0, 10):
                tot += j * vals[j]
                if vals[j] == 2:
                    twocnt += 1
            if tot % 11 == 1:
                combs = tenfact / (2 ** twocnt)
                answer += combs * combs
    answer *= 9
    answer //= 10
    return answer

if __name__ == "__main__":
    STRT = datetime.now()
    print problem491()
    print datetime.now() - STRT
