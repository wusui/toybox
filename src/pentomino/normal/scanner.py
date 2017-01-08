#!/usr/bin/env python
"""
The portion of the pentomino program that actually computes the layouts.
"""
import id_figs
import copy
#
# Print utilities.
#
def printr(strng, bsize):
    print strng
    with open(''.join(['output.',str(bsize),'.txt']), 'a') as f:
        f.write(strng+'\n')
    return False
display = lambda board, cnt : \
    printr(''.join([''.join([{331: 'p', 2311: 'n', 323: 'u',
                              1311: 'y', 3111: 'l', 711: 'v',
                              11111: 'i', 227: 't', 623: 'z',
                              271: 'f', 631: 'w', 1: 'x'
                              }[square] for square in row] + ['\n'])
            for row in board]), len(board)) or cnt + 1
#
# Recursive search and fill routines
#
lcomp_it = lambda board, tree, pnts, figs, extras, cnt : \
    sum(filter(lambda x : x > 0, [do_comp(board, tree, pnts, figs, extras,
                                          cnt, val) for val in tree]))
negative = lambda points : any(y < 0 for _,y in points)
odd_front = lambda points : sum([x[0] == 0 and 1 or 0 for x in points]) % 2 == 1
do_comp = lambda board, tree, pnts, figs, extras, cnt, val : \
    val[1] in figs and -1 or (extras[0]*2 + 1) == len(board) and \
    val[1] == 2311 and negative(val[0]) and -1 or \
    (extras[1]*2 + 1) == len(board[0]) and val[1] == 331 and odd_front(val[0]) \
    and -1 or overlaps(board, tree, pnts, figs, extras, cnt, val)
overlaps = lambda board, tree, pnts, figs, extras, cnt, val : \
    scan_desc([check_over([sum(x) for x in zip(fpt,pnts)], board,
                    tree, figs, extras, cnt) for fpt in val[0]], \
                    board, tree, figs, extras, cnt, val)
check_over = lambda plist, board, tree, figs, extras, cnt : \
    plist[0] >= 0 and plist[1] >= 0 \
    and plist[0] < len(board[0]) and plist[1] < len(board) and \
    board[plist[1]][plist[0]] == 0 and plist
scan_desc = lambda slist, board, tree, figs, extras, cnt, val: all(slist) \
            and partial(slist, board, tree, figs, extras, cnt, val)
#
# Heart of the recursive search routine
#
scan_for_blank = lambda board : \
    [[xcoord, ycoord] for xcoord in range(0, len(board[0])) for ycoord in \
     range(0, len(board)) if board[ycoord][xcoord] == 0] or [[]]
partial = lambda slist, board, tree, figs, extras, cnt, val : \
    partial1(add_fig(copy.deepcopy(board), slist, val[1]), tree,
             figs, extras, cnt, val)
partial1 = lambda iboard, tree, figs, extras, cnt, val : \
    partial2(scan_for_blank(iboard)[0], iboard, tree, figs, extras, cnt, val)
partial2 = lambda newspt, iboard, tree, figs, extras, cnt, val : \
    newspt == [] and display(iboard,cnt) or \
    lcomp_it(iboard, tree, newspt, figs + [val[1]], extras, cnt)     
#
# Wrapper used to layout X-pentomino locations and call the main
# calculation routines
#
set_sq = lambda row, rcnt, pnt, value : not rcnt == pnt[1] and row or \
        row[0:pnt[0]] + [value] + row[pnt[0]+1:]                     
set_square = lambda board, pnt, value : [set_sq(row,rcnt,pnt,value) for rcnt,row \
                                         in enumerate(board)]
add_fig = lambda board, pnts, value : not pnts and board or \
                                      set_square(add_fig(board,pnts[1:],value
                                      ),pnts[0],value)
boardify = lambda pnts, dims, value : add_fig([[0]*dims[0] for _ in range(0,
                                       dims[1])], pnts, value)
gen_board = lambda xx, yy, dims : boardify(
                    [[sum(x) for x in zip([xx,yy],z)] for z in                      
                    [[0,0],[1,0],[-1,0],[0,1],[0,-1]]], dims, 1)
comp_part = lambda point, dims: lcomp_it(gen_board(point[0], point[1], dims),
                                   id_figs.id_no_x(), [0,0], [], [point[1],
                                   point[0]], 0)
do_scan = lambda xpoints, dims: sum([comp_part(x, dims) for x in xpoints])
scan_box = lambda height, width : do_scan([[x,y] for y in range(1,(height+1)/2)
                                          for x in range(1,(width+1)/2)][1:],
                                          [width, height])
#
# Entry point to computation -- the only routine that needs to be known
# by outside callers.
#
looper = lambda : [scan_box(i, 60//i) for i in range(3,7)]

#
# Docstrings
#
looper.__doc__ = \
"""
Main entry point to pentomino calculator.
Returns a list of the number of solutions generated for each size
(3x20, 4x15, 5x12, 6x10).  The solutions are printed out and also
stored in output.[3-6].txt files.
"""

scan_box.__doc__ = \
"""
Given the height and width of the rectangle to tile, find the center
points for all X-pentomino solutions in the upper-left quadrant
of the rectangle.  This accounts for most rotation/reflection cases.
Pass the X-pentomino center points to do_scan.
"""

do_scan.__doc__ = \
"""
Call comp_part with all possible center points of the X-pentomino
for this specific shape.  Add up the counts of solutions and return.
"""

comp_part.__doc__ = \
"""
Wrapper around the call to the main routine that actually
recursively finds solutions.  Parameters passed (and
generated by this call) include a board representation
of the rectangle to be filled with the x-pentomino
pre-placed, a list of possible figures and their
orientations generated by id_figs, and the original
starting location for scans.
"""

gen_board.__doc__ = \
"""
Called from comp_part to generate a board.  Generate the blank spaces
on the board by calling boardify.  Expand the center of the
x-pentomino location to fill all squares in the x-pentomino.
"""

boardify.__doc__ = \
"""
Call add_fig with a full empty rectangle, the locations of all
x-pentomino squares, and a value used to represent the
x-pentomino.
"""

add_fig.__doc__ = \
"""
Call set_square to set a square in the figure.  Recursively called from
set_square to can the entire list of points in the pnts list.
"""

set_square.__doc__ = \
"""
Return a list of what are essentially rows in the solution. Calls set_sq
to add the square into the board rows.
"""

set_sq.__doc__ = \
"""
If the point is not in this row, do not change it.  Otherwise, add this
point into the board row.
"""

printr.__doc__ = \
"""
Monad used to write pentomino solutions to files.
"""

display.__doc__ = \
"""
Wrapper for printr function.  Takes the board data and formats squares
into unique characters for each figure.  Produces a sting of rows
separated by newline chacraters.
"""

lcomp_it.__doc__ = \
"""
Main solver routine.  Loops through all figures and tries each
unique figure layout as a solution.  This routine is eventually
recursively called to add the next level of figures into the
rectangle.
"""

negative.__doc__ = \
"""
Tests if there are any negatively indexed vertical squares in a
pentomino.  Used in the cases where there are an odd number of
rows and the x-pentomino's center is in the middle row.  This function
called on the y-pentomino removes duplicate reflections
"""

odd_front.__doc__ = \
"""
Tests if there are an odd number of squares in the first column of
a solution.  Used in the cases where there are an odd number of
columns and the x-pentomino's center is in the middle column.  This
function called on the p-pentomino removes duplicate reflections
"""

do_comp.__doc__ = \
"""
Check to make sure that a pentomino is valid (no
previous use of this pentomino, reflections eliminated if needed).
Calls overlaps if valid.
"""

overlaps.__doc__ = \
"""
Calls scan_desc passing check_over data to it.
"""

check_over.__doc__ = \
"""
Makes sure a square is valid (inside grid and empty).
"""

scan_desc.__doc__ = \
"""
Call partial -- returns combined slist value
"""

scan_for_blank.__doc__ = \
"""
Scan for the next available blank square in the rectangle.
"""

partial.__doc__ = \
"""
Call partial1, passing it add_fig which used a copy of the rectangle as
a parameter.
"""

partial1.__doc__ = \
"""
Call partial2 passing it an available blank square returned from
scan_for_blank
"""

partial2.__doc__ = \
"""
Deepest point in the scan.   If the figure is all filled in,
print the output.  If not filled all the way in  recursively
call lcomp_it to add the next pentomino.
"""
#
# Unit test call
#
if __name__ == '__main__':
    print looper()

