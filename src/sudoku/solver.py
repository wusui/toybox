#    Copyright (C) 2014, 2015  Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license. 
"""
Methods and objects used to support the solver method.  Solver is
called by both the Tkinter based code and from the sudoku.py cgi script.
"""

BIG_SQ_DIM = 3
SQ_NUMB = 9


def get_row(numb):
    """
    list of square numbers in a row.
    """
    ret = []
    for ival in range(0, SQ_NUMB):
        ret.append((numb, ival))
    return 'row', ret


def get_col(numb):
    """
    list of square numbers in a column.
    """
    ret = []
    for ival in range(0, SQ_NUMB):
        ret.append((ival, numb))
    return 'column', ret


def get_box(ynumb, xnumb):
    """
    list of square numbers in a box.
    """
    ret = []
    ybase = (ynumb // BIG_SQ_DIM) * BIG_SQ_DIM
    xbase = (xnumb // BIG_SQ_DIM) * BIG_SQ_DIM
    for yind in range(0, BIG_SQ_DIM):
        for xind in range(0, BIG_SQ_DIM):
            ret.append((ybase + yind, xbase + xind))
    return 'box', ret


def box_facade(numb):
    """
    Get_box wrapper to convert from one parameter (box number)
    to x and y coordinates.
    """
    xval = (numb % BIG_SQ_DIM) * BIG_SQ_DIM
    yval = (numb // BIG_SQ_DIM) * BIG_SQ_DIM
    return get_box(yval, xval)


def get_hist(flist, grid):
    """
    get a histogram of all set squares within flist.
    """
    retv = [0] * SQ_NUMB
    for coord in flist:
        entry = grid[coord[0]][coord[1]]
        if not entry == '0':
            retv['123456789'.find(entry)] += 1
    return retv


def addv(vec1, vec2):
    """
    Add histogram vector 2 to histogram vector 1.
    """
    for ind in range(0, SQ_NUMB):
        vec1[ind] += vec2[ind]


def chk_badvals(local):
    """
    Make sure that there are no duplicate numbers in any group.
    """
    for rowcl in range(0, SQ_NUMB):
        for group_type, func_array in [get_row(rowcl), get_col(rowcl),
                                       box_facade(rowcl)]:
            if max(get_hist(func_array, local)) > 1:
                return ('Error: Duplicate values in %s %d' % \
                        (group_type, rowcl + 1), local)


def chk_unsolvable(local):
    """
    Return true if it is known that the puzzle cannot be solved.
    """
    big_pat = []
    for row in range(0, SQ_NUMB):
        big_pat.append([])
        for col in range(0, SQ_NUMB):
            big_pat[row].append([])
            set_info_arr(big_pat, row, col, local)
    for rowcl in range(0, SQ_NUMB):
        for _, func_array in [get_row(rowcl), get_col(rowcl),
                                       box_facade(rowcl)]:
            hist1 = get_hist(func_array, local)
            for coord in func_array:
                if not local[coord[0]][coord[1]] == '0':
                    continue
                for numb in big_pat[coord[0]][coord[1]]:    
                    hist1[numb - 1] += 1
            if min(hist1) == 0:
                return True
    return False


def chk_solved(local):
    """
    Return 'Solved' string and grid if solved.
    """
    for row in range(0, SQ_NUMB):
        for col in range(0, SQ_NUMB):
            if local[row][col] == '0':
                return
    return ('Solved', local)


def set_info_arr(info_arr, row, col, local):
    """
    Set the info_arr info from data on the grid.
    """
    usvec = [0] * SQ_NUMB
    for _, func_array in [get_row(row), get_col(col),
                          get_box(row, col)]:
        addv(usvec, get_hist(func_array, local))
    for ind in range(0, SQ_NUMB):
        if usvec[ind] == 0:
            info_arr[row][col].append(ind + 1)


class GuessData(object):
    """
    Object used to hold guess information
    """
    def __init__(self):
        self.row = -1
        self.col = -1
        self.vals = []
        self.limit = SQ_NUMB

    def get_row(self):
        """
        Return row
        """
        return self.row

    def get_col(self):
        """
        Return col
        """
        return self.col


def find_uniq(flist, info, local):
    """
    Find a square that needs to be set, due to the fact that it is the
    only square that can have that value within the set of squares indicated
    by flist.
    """
    chkv = [0] * SQ_NUMB
    for coord in flist:
        for entry in info[coord[0]][coord[1]]:
            chkv[entry - 1] += 1
    nmb = -1
    for cnt, val in enumerate(chkv):
        if val == 1:
            nmb = cnt + 1
            break
    if nmb >= 0:
        for coord in flist:
            if nmb in info[coord[0]][coord[1]]:
                local[coord[0]][coord[1]] = '0123456789'[nmb]
                return True
    return


def find_only_in_grp(info_arr, local):
    """
    Find the only square left for a number within a group
    """
    for rowcl in range(0, SQ_NUMB):
        for _, func_array in [get_row(rowcl), get_col(rowcl),
                              box_facade(rowcl)]:
            if find_uniq(func_array, info_arr, local):
                return True


def solver(layout):
    """
    Loop finding obvious squares to fill in.
    If none left, loop through a square's possible values, recursively calling
    solver.
    """
    local = []
    for row in range(0, SQ_NUMB):
        local.append(layout[row][:])
    if chk_unsolvable(local): 
        return 'failure', local
    retv = chk_badvals(local)
    if retv:
        return retv
    loop_flg = True
    guess = GuessData()
    while loop_flg:
        loop_flg = False
        info_arr = []
        for row in range(0, SQ_NUMB):
            info_arr.append([])
            for col in range(0, SQ_NUMB):
                info_arr[row].append([])
                if not local[row][col] == '0':
                    continue
                set_info_arr(info_arr, row, col, local)
                len_this = len(info_arr[row][col])
                if len_this == 1:
                    value = '0123456789'[info_arr[row][col][0]]
                    local[row][col] = value
                    loop_flg = True
                    continue
                if len_this < guess.limit:
                    guess.row = row
                    guess.col = col
                    guess.vals = info_arr[row][col]
        loop_flg = find_only_in_grp(info_arr, local)
    retv = chk_solved(local)
    if retv:
        return retv
    for entry in guess.vals:
        local[guess.get_row()][guess.get_col()] = '0123456789'[entry]
        retv = solver(local)
        if retv[0] == 'Solved':
            return retv
    return ('partial solution', local)
