#!/usr/bin/python
#    Copyright (C) 2014, 2015  Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license. (See ./COPYING)
"""
Main entry point for thte Tkinter based interface for the sudoku solver.
"""

import Tkinter
import tkFont
import tkMessageBox
from Tkinter import Button

from solver import solver
from file_utils import load as file_load
from file_utils import save as file_save

SQ_SIZE = 40
SQ_NUMB = 9
BIG_SQ_DIM = 3


class Sudoku(object):
    """
    Representation of a Sudoku Board.

    The top half is a canvas which can handle mouse click events and keyboard
    input.  The bottom half is a row of control buttons.
    """
    def __init__(self, root):
        self.squares = {}
        self.last_rect = []
        self.ext_grid = []
        self.root = root
        self.font = tkFont.Font(family='Arial', size=32, weight='bold')
        root.title('Sudoku Solver')
        root.geometry('500x500+100+100')
        bottomframe = Tkinter.Frame(root)
        bottomframe.pack(side=Tkinter.BOTTOM)
        temp = SQ_SIZE * (SQ_NUMB + 2)
        lcanv = Tkinter.Canvas(root, width=temp, height=temp, bg='white')
        lcanv.bind('<Key>', self.keyboard)
        lcanv.bind('<Button-1>', self.mouse_button)
        lcanv.focus_set()
        lcanv.pack(side=Tkinter.TOP)
        draw_lim = SQ_NUMB + 1
        for row in range(0, draw_lim):
            width = 1
            if row % BIG_SQ_DIM == 0:
                width = 2
            lcanv.create_line(SQ_SIZE, SQ_SIZE + SQ_SIZE * row,
                              SQ_SIZE * draw_lim, SQ_SIZE + SQ_SIZE * row,
                              width=width)
            lcanv.create_line(SQ_SIZE + SQ_SIZE * row, SQ_SIZE,
                              SQ_SIZE + SQ_SIZE * row, SQ_SIZE * draw_lim,
                              width=width)
        self.canvas = lcanv
        self.button = {}
        for name, command in (('SAVE', self.save), ('LOAD', self.load),
                              ('RESET', self.reset), ('CLEAR', self.clear),
                              ('SOLVE', self.solve), ('QUIT', self.quit)):
            self.button[name] = Button(bottomframe, text=name, command=command)
            self.button[name].pack(side=Tkinter.LEFT, expand=False,
                                   padx=10, pady=10)

    def color_square(self, color, xparm, yparm):
        """
        Fill in a square with a color (used to mark clicked-squarea and to
        return blank white ones.
        """
        localx = xparm * SQ_SIZE
        localy = yparm * SQ_SIZE
        xsize = SQ_SIZE
        ysize = SQ_SIZE
        if xparm % BIG_SQ_DIM == 0:
            xsize -= 1
        if yparm % BIG_SQ_DIM == 0:
            ysize -= 1
        self.canvas.create_rectangle(localx, localy, localx + xsize,
                                     localy + ysize, fill=color)

    def check_square(self, xloc, yloc):
        """
        See if this square can be found in self.squares.
        Return the key if it does.
        """
        for key in self.squares:
            if self.squares[key][0] == xloc and self.squares[key][1] == yloc:
                return key
        return False

    def set_char(self, xloc, yloc, color, value):
        """
        Write a character on the page.
        """
        one_and_half = SQ_SIZE + SQ_SIZE // 2
        knumb = self.canvas.create_text(one_and_half + SQ_SIZE * (xloc - 1),
                                       one_and_half + SQ_SIZE * (yloc - 1) + 1,
                                       font=self.font, fill=color, text=value)
        return knumb

    def keyboard(self, event):
        """
        If the mouse is on a square, the value of the key hit is entered onto
        the board if it is in the range of 1 to 9.
        """
        if not '123456789'.find(event.char) in range(0, SQ_NUMB):
            return
        if not self.last_rect:
            return
        self.color_square('white', self.last_rect[0], self.last_rect[1])
        key = self.check_square(self.last_rect[0], self.last_rect[1])
        if key:
            del self.squares[key]
        knumb = self.set_char(self.last_rect[0], self.last_rect[1],
                'black', event.char)
        self.squares[knumb] = [self.last_rect[0], self.last_rect[1],
                               event.char]

    def mouse_button(self, event):
        """
        If the click is on a square, highlight that square.  The next
        keyboard input will go in that square.
        """
        off_yellow = '#FFFF60'
        xloc = event.x // SQ_SIZE
        yloc = event.y // SQ_SIZE
        if self.last_rect and self.last_rect[0] in range(1, SQ_NUMB + 1) and \
                self.last_rect[1] in range(1, SQ_NUMB + 1):
            found = self.check_square(self.last_rect[0], self.last_rect[1])
            if self.last_rect:
                if not found:
                    self.color_square('white', self.last_rect[0],
                            self.last_rect[1])
        self.last_rect = []
        if not (xloc in range(1, SQ_NUMB + 1) and \
                yloc in range(1, SQ_NUMB + 1)):
            return
        key = self.check_square(xloc, yloc)
        if key:
            self.canvas.delete(key)
            del self.squares[key]
        self.last_rect = [xloc, yloc]
        self.color_square(off_yellow, xloc, yloc)

    def set_ext_grid(self):
        """
        Set self.ext_grid value with data from self.squares
        """
        self.ext_grid = []
        for _ in range(0, SQ_NUMB):
            temp = ['0'] * SQ_NUMB
            self.ext_grid.append(temp)
        for ent in self.squares:
            lst = self.squares[ent]
            self.ext_grid[lst[1] - 1][lst[0] - 1] = lst[2]

    def erase(self):
        """
        Clear all board entries
        """
        for xval in range(1, SQ_NUMB + 1):
            for yval in range(1, SQ_NUMB + 1):
                self.color_square('white', xval, yval)

    def restore_entered_data(self):
        """
        Restore user input on board.
        """
        for entry in self.squares:
            tmp = self.squares[entry]
            self.set_char(tmp[0], tmp[1], 'black', tmp[2])

    def save(self):
        """
        Save the current board to a file.
        """
        file_save(self.squares)

    def load(self):
        """
        Load a board from a local file.
        """
        recvec = file_load()
        if recvec:
            self.squares = {}
            for pts in recvec:
                ind1 = int(pts[0])
                ind2 = int(pts[1])
                strng = pts[2].strip()
                key = self.set_char(ind1, ind2, 'black', strng)
                self.squares[key] = [ind1, ind2, strng]
            self.reset()

    def reset(self):
        """
        Clear all squares generated by the solve key.
        """
        self.erase()
        self.restore_entered_data()

    def clear(self):
        """
        Clear all squares.
        """
        self.erase()
        self.squares = {}

    def solve(self):
        """
        Solve the puzzle.
        """
        olive_green = '#00A000'
        eflag = 'Error: '
        self.set_ext_grid()
        (info, solution) = solver(self.ext_grid)
        if not info.startswith('Error: '):
            for yval in range(0, SQ_NUMB):
                for xval in range(0, SQ_NUMB):
                    if solution[yval][xval] == '0':
                        continue
                    self.set_char(xval + 1, yval + 1, olive_green,
                                  solution[yval][xval])
            self.restore_entered_data()
        else:
            tkMessageBox.showwarning('Error', '%s' % info[len(eflag):])

    def quit(self):
        """
        Provide an alternate way of exiting.
        """
        self.root.quit()


def sudloop():
    """
    Wrapper supporting Sudoku
    """
    root = Tkinter.Tk()
    Sudoku(root)
    root.mainloop()

if __name__ == '__main__':
    sudloop()
