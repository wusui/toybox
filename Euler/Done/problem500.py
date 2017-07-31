#!/usr/bin/python
"""
Copyright (C) 2016  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Problem 500! -- Project Euler Problem 500
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


def problem500inner(limitv, modv):
    """
    The lowest number with limitv divisors is the product lowest limitv numbers
    in the set of prime numbers raised to the power of 2**n where n is a
    non-negative integer.
    """
    insize = 8*(10**6)
    primes = []
    for i in bigsieve(insize):
        primes.append(i)
    sqz = []
    for i in primes:
        if i**2 > insize:
            break
        factor = 2
        numb = i ** factor
        while numb < insize:
            sqz.append(numb)
            factor *= 2
            numb = i ** factor
    primes.extend(sqz)
    prods = sorted(primes)
    ans = 1
    for k in prods[:limitv]:
        ans *= k
        ans %= modv
    return ans


def problem500():
    """
    Wrapper for specific call
    """
    return problem500inner(500500, 500500507)


if __name__ == "__main__":
    STRT = datetime.now()
    print problem500()
    print datetime.now() - STRT
