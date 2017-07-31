#!/usr/bin/python
"""
Copyright (C) 2016  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Finding numbers for which the sum of the squares of the digits is a square --
Project Euler Problem 171
"""
from datetime import datetime


class Memoize(object):
    """
    Memoization class, used to decorate recursive functions.
    """
    def __init__(self, f_attr):
        self.f_attr = f_attr
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.f_attr(*args)
        return self.memo[args]

    def fake_get(self):
        """ Not used -- keeps Lint happy """
        return self.f_attr

    def fake_show(self):
        """ Not used -- keeps Lint happy """
        print self.f_attr


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


@Memoize
def gen_data_rec(parm):
    """
    Recursively generate a tree of numbers in a solution for a given square

    Returns:
        A list of list values and tuple values represent a tree of possible
        numbers whose squares add up to the numb value.
    """
    numb = parm[0]
    amt_left = parm[1]
    maxsq = parm[2]
    combs = parm[3]
    if amt_left * maxsq * maxsq < numb:
        return False
    if maxsq == 1:
        return [(maxsq, numb, combs * combo(amt_left, numb))]
    maxv = 0
    for maxv in range(maxsq, 1, -1):
        if maxv * maxv <= numb:
            break
    maxv += 1
    retv = []
    if maxsq < maxv:
        maxv = maxsq + 1
    for nnumb in range(1, maxv):
        for cnt in range(1, amt_left+1):
            nval = cnt * nnumb * nnumb
            if nval == numb:
                retv.append([(nnumb, cnt, combs * combo(amt_left, cnt))])
                break
            else:
                if nval > numb:
                    break
                rcheck = gen_data_rec((numb-nval, amt_left-cnt, nnumb-1,
                                       combs * combo(amt_left, cnt)))
                if rcheck:
                    retv.append([(nnumb, cnt, combs *
                                  combo(amt_left, cnt)), rcheck])
    return retv


def traverse(tree, sol, aobj):
    """
    Recursively scan through the tree containing possible solutions.

    Input:
        tree -- list of lists representing possible solutions.  Each tuple
                in tree represents a number and the number of times that
                number appears in the solution.  2,2,1 for
                example is represented by [(2,2),[(1,1)]]
        sol --  solution so far.  For example, if 2,2,1 represents the value
                in tree, when this routine is first called, sol would be
                passed as a square number that we are checking (in this case,
                9).  After the (2,2) tree value is processed, this routine
                would be called again with the sol value of 9 - 2^2 * 2.
        aobj -- Permanent object used to store and accumulate the solution.
    """
    dummy = {}
    for fig in tree:
        try:
            dummy[fig] = True
        except TypeError:
            traverse(fig, sol, aobj)
            continue
        aobj.compute(fig, sol)


class AnswerObj(object):
    """
    A persitent storage object that keeps a running total of the number
    we are trying to compute (self.ans), and a list of data collect so
    far to be used to calculate changes to self.ans.
    """
    def __init__(self):
        """
        Set ans and numbs
        """
        self.ans = 0
        self.numbs = 10 * [(0, 0)]

    def reset(self):
        """
        Clear numbs
        """
        self.numbs = 10 * [(0, 0)]

    def get_answer(self):
        """
        Expose ans
        """
        return self.ans

    def compute(self, info, numbw):
        """
        Set ans values
        """
        self.numbs[info[0]] = (info[1], info[2])
        for i in range(0, info[0]):
            self.numbs[i] = (0, 0)
        lans = 0
        maxc = 0
        for i in range(1, 10):
            if self.numbs[i][0] > 0:
                lans += i * i * self.numbs[i][0]
                if self.numbs[i][1] > maxc:
                    maxc = self.numbs[i][1]
        if lans == numbw:
            for i in range(1, 10):
                if self.numbs[i][0] > 0:
                    self.ans += i * maxc * self.numbs[i][0]/20
                    self.ans %= 10**9


def add_up(info):
    """
    info at this point is the expected sum of all the digits for any of the
    digits in the answer.  Since the value wanted is the sum of all the digits,
    this value needs to get added to each of the places in the number.
    """
    carry = 0
    value = info
    answer = 0
    for i in range(0, 9):
        numb = value + carry
        digit = numb % 10
        carry = numb // 10
        answer += digit * (10**i)
    return str(answer).zfill(9)


def problem171():
    """
    Solution description.

    Consider the number 34, a number that should be counted as since
    f(34) == 25.  The same value of 25 would be returned for 304, 3040000,
    43, and 400000000003.  In fact, every number with 3 and 4 and 18 zeros
    in it (including leading zeros) represents the same 25.  So the
     sum of each digit in the 20 digit number, taken alone, would be the same.

    Now there are C(20,1)*C(19,1) possible ways that a number can have one 4,
    one 3, and 18 zeros.  Out of those possible ways, 1/20 can be a 3 and 1/20
    can be a 4.  So each digit in the final solution will have
    3 * C(20.1) * C(19,1) / 20 + 4 * C(20,1) * C(19,1) / 20 added to it to
    handle the case where a number contains one 3, one 4, and nothing else.

    So this program loops through all possible squares (1 through 40, it
    turns out).  gen_data_rec generates all possible solutions to the
    function (for 9, that would be 9 ones, 5 ones and a 2, 1 one and 2 twos,
    and one 3).   Traverse then does the math described in the previous
    paragraph to calculate a running total.

    When this completes, there will be one number that would represent the
    effect of that digit on the final sum.  This needs to get added to a
    corresponding total in order to come up with final answer (In other words,
    if n is the computed number, then the sum would be n + 10*n + 100*n ...
    """
    aobj = AnswerObj()
    for i in range(1, 41):
        aobj.reset()
        ans = gen_data_rec((i*i, 20, 9, 1))
        traverse(ans, i*i, aobj)
    result = aobj.get_answer()
    ans = add_up(result)
    return ans


if __name__ == "__main__":
    STRT = datetime.now()
    print problem171()
    print datetime.now() - STRT
