#!/usr/bin/python
"""
Copyright (C) 2017  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Connectivity of a network -- Project Euler Problem 186
"""
from datetime import datetime


def number_gen():
    """
    Implement the lagged Fibonacci function as a generator.
    """
    past_numb = []
    for notk in range(0, 55):
        k = notk + 1
        numb = 100003 - 200003 * k + 300007 * k * k * k
        numb %= 1000000
        past_numb.append(numb)
    for notk in range(0, 55):
        yield past_numb[notk]
    while True:
        for notk in range(0, 55):
            nxt = (notk + 31) % 55
            numb = past_numb[notk] + past_numb[nxt]
            numb %= 1000000
            past_numb[notk] = numb
            yield numb


def problem186():
    """
    Main problem loop.  Save lists of related entries until PM's number is
    called.  Then form a table whose positive entries are numbers that are
    friends with the PM.  Then keep adding entries to that table until the
    threshold is exceeded.
    """
    pm_numbert = 524287
    million = 1000000
    g_array = [[] for _ in range(0, million)]
    found_map = [0] * million
    call_cnt = 0
    fnum = 0
    first_time_through = True
    gsize = 0

    def add2map(number):
        """
        Add an entry to the map.  Make sure that all friends are also
        added to the map.
        """
        addcnt = 0
        thislist = [number]
        nextlist = []
        while thislist:
            for entry in thislist:
                if found_map[entry] == 0:
                    found_map[entry] = 1
                    addcnt += 1
                    for nxt in g_array[entry]:
                        if found_map[nxt] == 0:
                            nextlist.append(nxt)
            thislist = nextlist
            nextlist = []
        return addcnt

    def cnt_new_branch(num1, num2):
        """
        Check entries and call add2map. Parameterized so that
        the values can be called in different orders.
        """
        if found_map[num1] == 1:
            if found_map[num2] == 0:
                return add2map(num2)
        return 0

    for cnt, i in enumerate(number_gen()):
        if cnt > 10**7:
            return 'done'
        if cnt % 2 == 0:
            fnum = i
        else:
            snum = i
            if snum == fnum:
                continue
            g_array[fnum].append(snum)
            g_array[snum].append(fnum)
            call_cnt += 1
            if not first_time_through:
                gsize += cnt_new_branch(fnum, snum)
                gsize += cnt_new_branch(snum, fnum)
                if gsize >= 990000:
                    break
            if fnum == pm_numbert or snum == pm_numbert:
                if first_time_through:
                    gsize = add2map(pm_numbert)
                    if gsize >= 990000:
                        break
                    first_time_through = False
    return call_cnt

if __name__ == "__main__":
    STRT = datetime.now()
    print problem186()
    print datetime.now() - STRT
