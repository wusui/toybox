#!/usr/bin/python
#    Copyright (C) 2015  Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license. 
from wordlist import WordList
"""
Find all the solutions for a word rummy board.

This module consists of solver, and support functions for solver (score_it,
ptval, and find_sol).  When a solution is found, it calls gen_html to
produce the html table, which in turn calls a succession of nested routines
to format the tables.

"""
def solver(inlist):
    """
    Generate all solutions to the word rummy board.

    Col4 is a list of sorted letter values for each column.
    Col3 is a list of 4 item lists, where each entry is a possible 3 letter
    combination in a column.

    Loop through all 3 and 4 letter runs, and see how the fit on the front
    and on the back of each word combination.
    """
    NROWS = 4
    MINRUNL = 3
    MAXRUNL = 4
    wlist = WordList()
    ncol = len(inlist)/NROWS
    board = []
    inpt = iter(inlist)
    for row in range(0, NROWS):
        board.append([])
        for col in range(0, ncol):
            board[row].append(inpt.next())
    col4 = []
    col3 = []
    for col in range(0, ncol):
        cval = []
        for row in range(0, NROWS):
            cval.append(board[row][col])
        cstr = ''.join(sorted(cval))
        col4.append(cstr)
        tarr3 = []
        tarr3.append(''.join(cstr[0:3]))
        tarr3.append(''.join([cstr[0],cstr[2:]]))
        tarr3.append(''.join([cstr[0:2],cstr[3]]))
        tarr3.append(''.join(cstr[1:]))
        col3.append(tarr3)
    lines = []
    for row in range(0, NROWS):
        lines.append(''.join(board[row]))
    ans_dict = {}
    for row in range(0, NROWS):
        for indx in range(0, ncol - MINRUNL + 1):
            for rlen in [MINRUNL, MAXRUNL]:
                if rlen + indx > ncol:
                    continue
                runv = lines[row][indx:indx + rlen]
                tailv = wlist.findStart(runv)
                headv = wlist.findEnd(runv)
                for entry in tailv:
                    mval = find_sol(entry, runv, col3, col4, indx)
                    if mval >= 0:
                        score_it(ans_dict, [0, entry, runv, indx, mval])
                for entry in headv:
                    mval = find_sol(entry, runv, col3, col4, indx)
                    if mval >= 0:
                        score_it(ans_dict, [1, entry, runv, indx, mval])
    olist = []
    for entry in ans_dict:
        olist.append([entry, ans_dict[entry], ptval(ans_dict[entry])])
    return gen_html(olist);

def score_it(ans_dict, info):
    """
    Find the best point total score for a word
    
    Store that value in a dictionary indexed by each word (ans_dict)
    """
    cardz = 'A23456789TJQK'
    runst = ''
    for i in range(info[3], info[3]+len(info[2])):
        runst += cardz[i]
    rank = ''
    for i in range(0, len(info[1])):
        rank += cardz[info[4]]
    if info[0] == 1:
        key = "%s%s" % (info[1], info[2])
        cvals = "%s%s" % (rank, runst)
    else:
        key = "%s%s" % (info[2], info[1])
        cvals = "%s%s" % (runst, rank)
    if key not in ans_dict:
        ans_dict[key] = cvals
    else:
        if ptval(ans_dict[key]) < ptval(cvals):
            ans_dict[key] = cvals

def ptval(strng):
    """
    Convert a string of card values to the corresponding point total.
    """
    cardz = 'A23456789TJQK'
    pts = 0
    for letr in strng:
        lpt = cardz.find(letr)
        lpt += 1
        if lpt > 10:
            lpt = 10
        pts += lpt
    return pts

def find_sol(entry, runv, col3, col4, indx):
    """
    Given a word, and a string representing the run portion of that word
    (runv starting at index), return the highest scoring column number
    that can be used to complete that word (-1 if none found)
    """
    cmpval = ''.join(sorted(entry))
    bestcol = -1
    for cind in range(0,13):
        if len(runv) == 3:
            if (cind >= indx) & (cind < indx+3):
                continue
            if col4[cind] == cmpval:
                bestcol = cind
        else:
            mgclet = ' '
            if (cind >= indx) & (cind < indx+4):
                mgclet = runv[cind - indx]
            fokcnt = 4
            patrn = ''
            for each3 in col3[cind]:
                if mgclet == ' ':
                    if each3 == cmpval:
                        bestcol = cind
                        break
                else:
                     lcnt = each3.count(mgclet)
                     if lcnt == 0:
                         patrn = each3
                         break
                     if lcnt < fokcnt:
                         fokcnt = lcnt
                         patrn = each3 
            if len(patrn) > 0:
                if patrn == cmpval:
                    bestcol = cind
    return bestcol

def gen_html(ansl):
    """
    Generate html table solution.

    Wrap the <div> portion around the tables.
    """
    cnt = len(ansl)
    tblcnt = 1
    if cnt >= 6:
        tblcnt = 2
    if cnt >= 12:
        tblcnt = 3
    return "<b><br><br><div id=content%d>\n%s</div></b>" % (tblcnt, ptables(tblcnt, ansl))

def ptables(tblcnt, ansl):
    """
    Generate a list of table entries
    """
    tblstr = []
    for i in range(0, tblcnt):
        tblstr.append(wrap_table(tblcnt, i, ansl));
    return ''.join(tblstr)

def wrap_table(cnt, i, ansl):
    """
    Wrap the table html around a table.
    """
    return '<table border=1>\n%s\n</table>\n' % gen_table(cnt, i, ansl);

def gen_table(cnt, i, ansl):
    """
    Calculate the layout of a column (expressed as a table entry).
    """
    tind = cnt - 1
    numb = len(ansl)
    cstrt =[0]
    if tind == 1:
        cstrt = [0, 4]
        xtra = numb - 6
        cstrt[1] += (xtra // 2)
    if tind == 2:
        cstrt = [0, 5, 10]
        xtra = numb - 12
        incr = xtra // 3
        cstrt[1] += incr
        cstrt[2] += 2 * incr
        if xtra % 3 == 2:
            cstrt[2] += 1
    cstrt.append(numb)
    return gen_lines(cstrt, i, ansl)

def gen_lines(cstrt, i, ansl):
    """
    Generate the actual table entries (2 lines each, one row spanned score)
    Also handle the totals on the end of each column.
    """
    retv = []
    newind = True
    for j in range(cstrt[i],cstrt[i+1]):
        if newind:
            hdr = '<td style="width:20px">'
        else:
            hdr = '<td>'
        str1 = gen_boxes(ansl[j][0], hdr)
        str2 = gen_boxes(ansl[j][1], hdr)
        str1 = '<b>%s<td style="width:40px" rowspan="2">%d</td></b>\n' % (str1, ansl[j][2])
        retv.append('<tr>%s</tr>\n<tr>%s</tr>\n' % (str1, str2))
    pts = addemup (cstrt, i, ansl)
    if len(ansl) >= 6:
        retv.append('<tr><td colspan="7" style="height:46px">COLUMN %d TOTAL</td><td>%d</td></tr>' % (i+1, pts))
    if cstrt[i+1] == len(ansl):
        total = pts
        for j in range(0,i):
            xpts = addemup(cstrt, j, ansl)
            retv.append('<tr><td colspan="7" style="height:46px">COLUMN %d TOTAL</td><td>%d</td></tr>' % (j+1, xpts))
            total += xpts
        if total > 0:
            retv.append('<tr><td colspan="7" style="height:46px">TOTAL SCORE</td><td>%d</td></tr>' % total)
        else:
            retv.append('<tr><td>NO SOLUTIONS FOUND</td></tr>')
    return ''.join(retv)

def addemup(cstr, i, ansl):
    """
    Add a column in the display
    """
    numb = 0
    for j in range(cstr[i],cstr[i+1]):
        numb += ansl[j][2]
    return numb

def gen_boxes(word, hdr):
    """
    Generate the cells around individual letters
    """
    retv = []
    for letter in word:
        retv.append("%s%s</td>\n" % (hdr,letter))
    return ''.join(retv)

if __name__ == "__main__":
    print solver("HANGLISTACORUISHETTWEYSQUESBCARDYNTHEARUNUSEFKHSMULB")
