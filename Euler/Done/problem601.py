#!/usr/bin/python
"""
Copyright (C) 2017  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Divisibility Streaks -- Project Euler Problem 601
"""
from datetime import datetime


def get_primes(size):
    """
    Simple sieve used to generate list of primes
    """
    primes = []
    numbers = size * [True]
    numbers[0] = False
    numbers[1] = False
    cnt = 2
    while True:
        if numbers[cnt] is False:
            cnt += 1
            continue
        nextv = cnt * cnt
        if nextv > size:
            cnt += 1
            break
        while nextv < size:
            numbers[nextv] = False
            nextv += cnt
        cnt += 1
    for count, value in enumerate(numbers):
        if value:
            primes.append(count)
    return primes


def problem_inner(size):
    """
    In order to get a streak of n, k+1 must be divisible by 2,
    k+2 must be divisible by 3 ...  Also the streak number must
    not be divisble by n+1a

    So a streak exists for a number x where x-1 is factorable by every number
    in that streak.  The minimum possible value x-1 is a product of the minimum
    number of prime factors needed for all integers from 1 to the length of
    the streak.

    A streak also can not have the number after the streak be factorable
    by x-1.  Therefore that number must either be a new prime factor,
    or one more power in a previous number formed by raising the power
    of one prime.
    """
    primlst = get_primes(size+1)
    answer = 6
    for ivalue in range(3, size+1):
        nfactors = []
        nval = ivalue + 1
        for nfact in primlst:
            while nval % nfact == 0:
                if nfact not in nfactors:
                    nfactors.append(nfact)
                nval //= nfact
            if nfact == 1:
                break
        if len(nfactors) == 1:
            basef = 1
            for pnum in primlst:
                if pnum > ivalue:
                    break
                lnumb = 1
                while lnumb <= ivalue:
                    lnumb *= pnum
                lnumb //= pnum
                basef *= lnumb
            tval = (4 ** ivalue) // basef
            dontuse = tval // nfactors[0]
            tval -= dontuse
            answer += tval
    return answer


def problem601():
    """
    Wrapper to pass the right size for this problem
    """
    return problem_inner(31)

if __name__ == "__main__":
    STRT = datetime.now()
    print problem601()
    print datetime.now() - STRT
