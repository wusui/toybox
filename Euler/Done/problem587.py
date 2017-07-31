#!/usr/bin/python
"""
Copyright (C) 2017  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Concave Triangles. --  Project Euler Problem 587
"""

from math import sqrt
from math import hypot
from math import pi
from math import sin
from math import asin
from datetime import datetime


def sec_area_find(sec_len):
    """
    Given the length of a chord, find the area of the secant
    """
    ang1 = 2 * asin(sec_len / 2.)
    return (ang1 - sin(ang1)) / 2.0


def xtra_find(xpt_1, ypt_1):
    """
    Find the area of L-section to the right of the right-most point
    """
    rrect = 2.0 * (1.0 - xpt_1)
    sec2_area = sec_area_find(-ypt_1 * 2.0)
    return (rrect - sec2_area) / 2.0


def quadratic_and_more(qdv_a, qdv_b, qdv_c):
    """
    Solve the quadratic passed to determine the points on the line segment
    that intersects the circle, and then continue doing computations to find
    the ratio we are looking for.
    """
    disc = sqrt(qdv_b**2 - 4*qdv_a*qdv_c)
    xpt_1 = (-qdv_b + disc)/(2*qdv_a)
    xpt_2 = (-qdv_b - disc)/(2*qdv_a)
    ypt_1 = -sqrt(1.0 - xpt_1**2)
    ypt_2 = -sqrt(1.0 - xpt_2**2)
    sec_area = sec_area_find(hypot(xpt_1-xpt_2, ypt_1-ypt_2))
    tri_area = (1.0 + xpt_1) * (1.0 + ypt_1) / 2.0
    lsec_area = (4.0 - pi) / 4.0
    rt_sec = lsec_area - xtra_find(xpt_1, ypt_1)
    concave_area = tri_area - sec_area - rt_sec
    return concave_area / lsec_area


def find_area_ratio(circ_numb):
    """
    Given a number of circles, find the slope of the line and derive the
    quadratic equation values where this line intersects the circle.  Return
    the ratio computed.
    """
    yint = 1. - float(circ_numb)
    yint /= float(circ_numb)
    slope = yint + 1.
    qdv_a = 1 + slope**2
    qdv_b = 2 * yint * slope
    qdv_c = yint**2 - 1
    return quadratic_and_more(qdv_a, qdv_b, qdv_c)


def problem587():
    """
    Binary search for the solution
    """
    low_bound = 0
    upper_bound = 4
    while find_area_ratio(upper_bound) >= .001:
        upper_bound *= 2
    while upper_bound - low_bound > 1:
        midpoint = (low_bound + upper_bound) / 2
        if find_area_ratio(midpoint) > .001:
            low_bound = midpoint
        else:
            upper_bound = midpoint
    return upper_bound


if __name__ == "__main__":
    STRT = datetime.now()
    print problem587()
    print datetime.now() - STRT
