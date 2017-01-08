#!/usr/bin/env python
"""
Interface between get_layouts and the tree builder routine. 
The only externally called definition here is id_figs which
generates a list of pentomino layout points and a figure id.
"""
import get_layouts

#
# Utilities used to generate alternative figure orientations
# prior to identifying the pentomino that corresponds to a
# layout
#
sqmult = lambda x, y : [a*b for a,b in zip(x,y)]
figmult = lambda pent : [[sqmult(x,y) for x in pent] for y in \
                         [[1,1],[-1,1],[1,-1],[-1,-1]]]
flip = lambda pent : [x[::-1] for x in pent]
get_all_orientations = lambda pent : figmult(pent) + figmult(flip(pent))

#
# Routines to find the size of a figure and to find the [0,0] point of the
# figure.
#
min_x = lambda x : min([a[0] for a in x])
max_x = lambda x : max([a[0] for a in x])
min_y = lambda x : min([a[1] for a in x])
max_y = lambda x : max([a[1] for a in x])
min_left_corner = lambda x : min([a[1] for a in x if a[0] == 0])

#
# Given a layout, make surte that it is legal, oriented vertically, and
# then calculate an int value to represent it.
#
get_uniq_pent = lambda fixed : sum([(2**x[0]) * 10**x[1] for x in fixed])
uniq_wrap = lambda x : ((min_y(x) < 0) and 1) or ((max_x(x) > max_y(x)) and 1) \
                     or get_uniq_pent(x)

#
# Shift a pentomino to the right or down in order to either check it's
# validity or to generate an id.
#
fixx = lambda layt : [[x[0]-min_x(layt), x[1]] for x in layt]
fixy = lambda fix1 : [[x[0], x[1]-min_left_corner(fix1)] for x in fix1]

#
# Given a layout, assign an id to it.
#
add_fig_id = lambda pat : (pat, max([uniq_wrap(fixy(fixx(layt))) \
                          for layt in get_all_orientations(pat)]))

#
# Main entry points of function used to add id's to layouts
#
id_figs = lambda : [add_fig_id(x) for x in get_layouts.get_layouts()]
id_no_x = lambda : [(x,y) for x,y in id_figs() if y > 1]

#
# Docstrings
#
sqmult.__doc__ = \
"""
Elementwise product of the two elements in a list

input: x -- first list
       y -- second list
       
Returns a list whose elements are: [x[0]*y[0], x[1]*y[1], x[2]*y[2], ...] 
"""

figmult.__doc__ = \
"""
Multiply a figure with values that cause different orientations of a
pentomino to be generated.

input: pent -- list of point in a pentomino

return: list of pentomino point lists.  Each list of points represents
a unique orientation of the pentomino figure
"""

flip.__doc__ = \
"""
Return a flipping of a pentomino layout, where every point has its
x and y values reversed.

input: pent -- list of points in a pentomino.

Returns a list of points in a pentomino where every point has its
x and y values reversed from the pent list.
"""

get_all_orientations.__doc__ = \
"""
Given a list of point return a list of eight lists where each
list returned is a representation of the original list of points
rotated and/or flipped into a new set (oriented differently).

input: pent -- list of points in a pentomino.

Returns all possible orientations of the figure.
"""

min_x.__doc__ = \
"""
Find the minimum x-coordinate in a list of points.

input: x -- point list

Returns: integer value of the lowest x-coordinate in the list
"""

max_x.__doc__ = \
"""
Find the largest x-coordinate in a list of points.

input: x -- point list

Returns: integer value of the largest x-coordinate in the list
"""

min_y.__doc__ = \
"""
Find the minimum y-coordinate in a list of points.

input: x -- point list

Returns: integer value of the lowest y-coordinate in the list
"""

max_y.__doc__ = \
"""
Find the maximum y-coordinate in a list of points.

input: x -- point list

Returns: integer value of the largest y-coordinate in the list
"""

min_left_corner.__doc__ = \
"""
Find the lowest value of y (in an [x,y] point description where
x is 0.

Input:  x -- point list

Returns the y-coordinate for the figure where the uper left corner
of the figure is [0,0]
"""

get_uniq_pent.__doc__ = \
"""
Calculate a figure's representation number.

Input:  fixed -- point list

Returns a numeric representation of this figure.
"""

uniq_wrap.__doc__ = \
"""
Get_uniq_pent wrapper which checks for non-computable orientations.

Inputs: x -- point list

Returns 1 if there are negative x values in the figure or if the figure is
wider than it is tall.   Otherwise, a get_uniq_pent vaule is calculated
and returned.
"""

fixx.__doc__ = \
"""
Adjust a figure to the right.

Input: layt -- point list

Returns a list of points adjusted such that the minimum x value is 0.
"""

fixy.__doc__ = \
"""
Adjust a figure up/down.

Input: fix1 -- point list

Returns a list of points adjusted such that the minimum y value on row 0 is 0.
"""

add_fig_id.__doc__ = \
"""
Given a pattern or layout representing points in a figure, return the figure
and its numeric representation.

Input: pat -- point list

Returns: a list whose first entry is pat and whose second entry is a number
uniquely identifying the type of pentomino this is.
"""

id_figs.__doc__ = \
"""
Generate a list of layout representations.  Each entry consists of a list of
points in a figure, and a numeric value representing the pentomino
corresponding to this figure.
"""

id_no_x.__doc__ = \
"""
Remove the X-pentomino from id_figs.
"""

#
# Unit test non-functional calls
#
if __name__ == '__main__':
    for yy,xx in enumerate(id_no_x()): 
        print xx
    print yy
