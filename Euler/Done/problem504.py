#!/usr/bin/python
"""
Copyright (C) 2017  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Square on the inside. --  Project Euler Problem 504
"""
from itertools import combinations
from datetime import datetime


def gcd(big, little):
    """
    From a common library.

    Return the gcd of two numbers
    """
    while little > 0:
        remainder = big % little
        big = little
        little = remainder
    return big


def get_sqs(size):
    """
    Return a list of squares of integers between 1 and what is expected
    to be the maximum possible number of points within a figure.
    """
    list_of_squares = []
    counter = 1
    square_value = counter * counter
    max_numb_inside = size * size * 2 + 1
    while square_value < max_numb_inside:
        list_of_squares.append(square_value)
        counter += 1
        square_value = counter * counter
    return list_of_squares


def problem504_inner(size):
    """
    The first part of this function initializes two tables.
    One table is an n x m  table where each entry is the
    greatest common denominator of n and m.  The second table
    is a table indexed by x and y sizes corresponding to the
    distance each vertex is to the origin.  Each entry contains
    the number of points within the figure for the quadrant of
    the quadrilateral that is defined by x and y

    The second part of this function counts the number of
    solutions for quadrilaterals whose ABCD values are all the
    same, added to the number of solutions for quadrilaterals
    whose ABCD values are one of two values, added to the number
    of solutions for quadrilaterals whose ABCD values are one
    of three values, added to the number of solutions for
    quadrilaterals whose ABCD value are all diffent.
    """

    def triangle_area(side1, side2):
        """
        Find the points inside a quadrant that are not on an axis.
        First find the area of the rectangle that contains the line
        in the quadrant.  Next, remove the points that are on the
        line.  The triangle inside the quadrant contains one half
        of the points left.
        """
        hypotneuse = gcd_t[side1][side2] - 1
        sidesq = (side1 - 1) * (side2 - 1)
        sidesq -= hypotneuse
        return sidesq / 2

    list_of_squares = get_sqs(size)
    just_past_upper_limit = size + 1
    gcd_t = [[0]*just_past_upper_limit for _ in range(just_past_upper_limit)]

    def set_tbl_gcd():
        """
        Set a table of gcd values.  Handle both
        orders of parameters so that x,y and y,x
        evaluate to the same number
        """
        for i in range(0, just_past_upper_limit):
            gcd_t[i][i] = i
        for i in range(2, just_past_upper_limit):
            for j in range(1, i):
                tmp = gcd(i, j)
                gcd_t[i][j] = tmp
                gcd_t[j][i] = tmp

    set_tbl_gcd()
    inner_t = [[0]*just_past_upper_limit for _ in range(just_past_upper_limit)]

    def set_tbl_triangle_area():
        """
        Set a table of areas of the quadrant of a triangle. The indices
        to this table are the distance from the center of the endpoints
        of the line segment forming the figure.
        """
        for i in range(1, just_past_upper_limit):
            for j in range(1, i+1):
                tmp = triangle_area(i, j)
                inner_t[i][j] = tmp
                inner_t[j][i] = tmp
    set_tbl_triangle_area()

    def get_pts(alist):
        """
        Calculate the area of the quadrilateral formed by segments between
        the points specified.  First calculate the number of points on the
        x and y axis.  Then add the points in each quadrant.  Return True
        if the number of points is a square, False otherwise
        """
        total = sum(alist) - 3
        total += inner_t[alist[0]][alist[1]] + inner_t[alist[1]][alist[2]] + \
            inner_t[alist[2]][alist[3]] + inner_t[alist[3]][alist[0]]
        if total in list_of_squares:
            return True
        return False

    def find_one_length():
        """
        Solve for all figures that are square (diamond) shaped.
        """
        answer = 0
        for onev in range(1, just_past_upper_limit):
            if get_pts([onev, onev, onev, onev]):
                answer += 1
        return answer

    def find_two_lengths():
        """
        Solve for all figures that have two different numbers on
        the x and y axis.  The first two get_pts calls handle the
        cases where there are three lengths of one value and one
        of another.  The next get_pts call handles the case where
        the values of the same length are next to each other, and
        the last get_pts call handles the case where no values of
        the same length are next to each other.
        """
        answer = 0
        for point in combinations(range(1, just_past_upper_limit), 2):
            if get_pts([point[0], point[0], point[0], point[1]]):
                answer += 4
            if get_pts([point[1], point[1], point[1], point[0]]):
                answer += 4
            if get_pts([point[0], point[0], point[1], point[1]]):
                answer += 4
            if get_pts([point[0], point[1], point[0], point[1]]):
                answer += 2
        return answer

    def find_three_lengths():
        """
        Solve for all figures that have three different numbers
        on the x and y axis.  There are six possible combinations
        here.  Three possible numbers can be a number that is
        used twice, and those two values can either be adjacent to
        each other or not adjacent to each other.
        """
        answer = 0
        for point in combinations(range(1, just_past_upper_limit), 3):
            if get_pts([point[0], point[0], point[1], point[2]]):
                answer += 8
            if get_pts([point[0], point[1], point[0], point[2]]):
                answer += 4
            if get_pts([point[1], point[1], point[0], point[2]]):
                answer += 8
            if get_pts([point[1], point[0], point[1], point[2]]):
                answer += 4
            if get_pts([point[2], point[2], point[0], point[1]]):
                answer += 8
            if get_pts([point[2], point[0], point[2], point[1]]):
                answer += 4
        return answer

    def find_four_lengths():
        """
        Solve for all figures where all x and y axis values are
        different.  There are three class here: one where the shortest
        and second shortest are adjacent, one where the shortest and
        third shortest are adjacent, and one where the shortest and
        the longest are adjacent.
        """
        answer = 0
        for point in combinations(range(1, just_past_upper_limit), 4):
            if get_pts([point[0], point[1], point[2], point[3]]):
                answer += 8
            if get_pts([point[0], point[1], point[3], point[2]]):
                answer += 8
            if get_pts([point[0], point[2], point[1], point[3]]):
                answer += 8
        return answer

    answer = find_one_length()
    answer += find_two_lengths()
    answer += find_three_lengths()
    answer += find_four_lengths()
    return answer


def problem504():
    """
    Wrapper for problem504_inner
    """
    return problem504_inner(100)


if __name__ == "__main__":
    STRT = datetime.now()
    print problem504()
    print datetime.now() - STRT
