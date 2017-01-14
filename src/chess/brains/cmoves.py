#!/usr/bin/python
#    Copyright (C) 2017 Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license.
from board import PAWN
from board import KNIGHT
from board import BISHOP
from board import ROOK
from board import QUEEN
from board import KING
def check_check(cboard, color):
    """
    Find the king, and then find all pieces that can take it.
    """
    kpos = []
    for row in range(0,8):
        for col in range(0,8):
            if cboard.board[row][col] == color + KING:
                kpos = [row, col]
                break
        if kpos:
            break
    return can_move(cboard, kpos, color)

def can_move(cboard, pos_2_chk, color):
    """
    Return a list of of the positions of all of the opponents pieces that
    can move to pos_2_chk
    """
    opp = 10 - color
    prow = pos_2_chk[0] + 1 - color / 5
    can_goto = []
    for row in range(0,8):
        for col in range(0,8):
            if cboard.board[row][col] != 0:
                if cboard.board[row][col] // 10 == opp // 10:
                    attacker = cboard.board[row][col] % 10
                    loc_dif = sorted([abs(row-pos_2_chk[0]), abs(col-pos_2_chk[1])])
                    if attacker == PAWN:
                        if cboard.board[row][col] != 0:
                            if row == prow:
                                if abs(col-pos_2_chk[1]) == 1:
                                    can_goto.append([row, col])
                        else:
                            startpos = 6 - color / 2
                            if col == pos_2_chk[1]:
                                if row == prow:
                                    can_goto.append([row, col]) 
                                else:
                                    if cboard.board[prow, col] == 0:
                                        if row == startpos:
                                            if abs(row-pos_2_chk[0]) == 2:
                                                can_goto.append([row, col])
                        continue
                    if attacker == KING:
                        if loc_dif[1]  == 1:
                            can_goto.append([row, col])
                        continue
                    if attacker == KNIGHT:
                        if loc_dif == [1, 2]:
                            can_goto.append([row, col])
                        continue
                    if attacker == BISHOP or attacker == QUEEN:
                        if loc_dif[0] == loc_dif[1]:
                            if clear_between(cboard, [row, col], pos_2_chk):
                                can_goto.append([row, col])
                                continue
                    if attacker == ROOK or attacker == QUEEN:
                        if loc_dif[0] == 0:
                            if clear_between(cboard, [row, col], pos_2_chk):
                                can_goto.append([row, col])
    return can_goto

get_direction = lambda x, y : 0 if x == y else (y-x)//abs(y-x)

def clear_between(cboard, pt1, pt2):
    """
    Make sure all squares between the two points specified on the
    board are blank.
    """
    xdiff = get_direction(pt1[0], pt2[0])
    ydiff = get_direction(pt1[1], pt2[1])
    xloc = pt1[0] + xdiff
    yloc = pt1[1] + ydiff
    while [xloc, yloc] != pt2:
        if cboard.board[xloc][yloc] != 0:
            return False
        xloc += xdiff
        yloc += ydiff
    return True

