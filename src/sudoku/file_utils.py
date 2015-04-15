#    Copyright (C) 2014, 2015  Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license. 
"""
Methods used to support the tkinter based sudoku sover gui.
"""

import inspect
import os
import Tkinter
from Tkinter import Toplevel
from Tkinter import Entry
from Tkinter import Button
from Tkinter import Label
from Tkinter import Frame
from Tkinter import Scrollbar
from Tkinter import Listbox
from tkMessageBox import showwarning


def getdir():
    """
    Returns a path to the directory/folder where we will store saved
    Sudoku configurations
    """
    src_file = inspect.getfile(getdir)
    src_dir = src_file[0:len(src_file) - len('file_utils.py')]
    path_data = os.path.join(src_dir, '..', '..', 'data')
    return path_data


def load():
    """
    Handle the load key on the main window.
    """
    def save_select():
        """
        Select key hit.  Set fname and exit if a field is high-lighted.
        """
        sel = mylist.curselection()
        if not sel:
            return
        fname.append(olist[int(sel[0])])
        top.quit()
    olist = sorted(os.listdir(getdir()))
    if len(olist) == 0:
        showwarning('Error', 'No files to load')
        return
    top = Toplevel()
    top.geometry('200x180+800+200')
    fname = []
    top.title('Sudoku Loader')
    tpart = Frame(top)
    tpart.pack(side=Tkinter.TOP)
    bpart = Frame(top)
    bpart.pack(side=Tkinter.BOTTOM)
    scrollbar = Scrollbar(tpart)
    scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
    mylist = Listbox(tpart, yscrollcommand=scrollbar.set)
    for line in olist:
        mylist.insert(Tkinter.END, line)
    mylist.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
    scrollbar.config(command=mylist.yview)
    picker = Button(bpart, text='SELECT', command=save_select)
    picker.pack(pady=5)
    top.mainloop()
    if fname:
        retvec = []
        fyle = '%s%s%s' % (getdir(), os.path.sep, fname[0])
        top.destroy()
        with open(fyle, 'r') as infile:
            inline = infile.readline()
            while inline:
                retvec.append(inline.split(':'))
                inline = infile.readline()
            return retvec


def save(squares):
    """
    Handle the save key on the main window.
    """
    def save_button_hit():
        """
        Save key (on local window) was hit.  Save the file name entered.
        """
        text_in = save_entry.get().strip()
        if len(text_in) == 0:
            showwarning('Error', 'File name specified is empty.')
            return
        outfile = os.path.join(savedir, text_in)
        with open(outfile, 'w') as fyle:
            for sqr_info in save_squares:
                fyle.write('%d:%d:%s\n' % tuple(save_squares[sqr_info]))
        top.destroy()
    top = Toplevel()
    top.geometry('180x80+800+200')
    top.title('Save a layout')
    save_squares = squares
    savedir = getdir()
    label1 = Label(top, text='File name')
    save_entry = Entry(top)
    label1.grid(row=0)
    save_entry.grid(row=0, column=1, columnspan=2)
    save_entry.focus_set()
    save_button = Button(top, text='SAVE', pady=3,
            command=save_button_hit)
    sspace = Label(top)
    sspace.grid(row=1)
    save_button.grid(row=2, column=1)
    top.mainloop()
