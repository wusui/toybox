"""
Created on May 11, 2014

@author: Warren Usui
"""

import Tkinter

import tkFont
import ttk
from Tkinter import Button
from tkMessageBox import showwarning
from tkMessageBox import showinfo
from llsimilarity.llama import Llama
from llsimilarity.llops import CompareLlamas
from llsimilarity.utilities import make_tempdir
from llsimilarity.rundle import get_rundle_list
from llsimilarity.cli import report_vs_rundle


class LleagueGui(object):
    """
    classdocs
    """

    def __init__(self, root):
        """
        Constructor
        """
        make_tempdir()
        self.root = root
        self.font = tkFont.Font(family='Arial', size=24, weight='bold')
        root.title('Llama Similarity Matcher')
        root.geometry('750x250+100+100')
        bottomframe = Tkinter.Frame(root)
        bottomframe.pack(side=Tkinter.BOTTOM)
        topframe = Tkinter.Frame(root)
        topframe.pack(side=Tkinter.TOP)
        self.fields = [{}, {}]
        loc_text = ['Llama', 'Versus']
        for cnt, field in enumerate(self.fields):
            field['var'] = Tkinter.StringVar()
            field['area'] = Tkinter.LabelFrame(topframe, text=loc_text[cnt],
                                               font=self.font)
            field['area'].pack()
            field['msg'] = Tkinter.Label(field['area'],
                                         textvariable=field['var'],
                                         font=self.font, fg='red')
            field['msg'].pack()
            field['llama'] = None
            field['rundle'] = None
        self.button = {}
        for name, command in (('Set Player', self.player_set),
                              ('Set Opponent', self.opponent_set),
                              ('Set Rundle', self.rundle_set),
                              ('Clear Fields', self.clear),
                              ('Get Rating(s)', self.get_rating),
                              ('QUIT', self.quit)):
            self.button[name] = Button(bottomframe, text=name, command=command)
            self.button[name].pack(side=Tkinter.LEFT, expand=False,
                                   padx=10, pady=10)
        self.progbar = ttk.Progressbar(self.root, length=200,
                                       mode='determinate')

    def player_set(self):
        """
        Set a player
        """
        save(self.fields[0])

    def opponent_set(self):
        """
        Set a player
        """
        save(self.fields[1])

    def rundle_set(self):
        """
        Set a rundle
        """
        rundlepick(self.fields[1])

    def clear(self):
        """
        Clear all the fields

        """
        for indx in range(0, 2):
            self.fields[indx]['var'].set('')
            self.fields[indx]['llama'] = None
            self.fields[indx]['rundle'] = None
        self.root.update_idletasks()

    def get_rating(self):
        """
        Find the rating and display it on a dialog page
        """
        if not self.fields[0]['llama']:
            return
        if self.fields[1]['llama']:
            ratio = CompareLlamas(self.fields[0]['llama'],
                                  self.fields[1]['llama']).get_display_ratio()
            msg = "{} has a ratio of {} versus {}".format(
                    self.fields[0]['var'].get(), ratio,
                    self.fields[1]['var'].get())
            showinfo('Learned league similarity', msg)
        else:
            self.progbar.pack(side="bottom")
            self.progbar.start(10000)
            report_vs_rundle(self.fields[0]['var'].get().lower(),
                             self.fields[1]['rundle'].replace(' ', '_'),
                             self.updatebar)
            self.progbar.stop()
            self.progbar.pack_forget()

    def quit(self):
        """
        Provide an alternate way of exiting.
        """
        self.root.quit()

    def updatebar(self, player):
        """
        Move status bar (slightly less than 4%)
        """
        if len(player) % 2 == 0:
            self.progbar.step(3.9)
        else:
            self.progbar.step(3.8)
        self.progbar.update_idletasks()


def save(field_info):
    """
    Handle the save key on the main window.
    """
    def save_button_hit():
        """
        Save key (on local window) was hit.
        """
        text_in = save_entry.get().strip()
        this_llama = Llama(text_in.lower())
        field_info['var'].set(text_in)
        if len(this_llama.get_dunno()) + len(this_llama.get_know()) == 0:
            showwarning('Error', 'Invalid or inactive Llama entered.')
            return
        field_info['llama'] = this_llama
        field_info['rundle'] = None
        top.quit()
        top.destroy()
    font = tkFont.Font(family='Arial', size=24, weight='bold')
    top = Tkinter.Toplevel(bd=10)
    top.geometry('480x160+800+200')
    top.title('Enter a Llama')
    label1 = Tkinter.Label(top, text='Llama name', font=font)
    label1.pack()
    save_entry = Tkinter.Entry(top, font=font)
    save_entry.pack()
    save_button = Button(top, text='SAVE', command=save_button_hit, font=font)
    save_button.pack()
    top.mainloop()


def rundlepick(field_info):
    """
    Handle the rundle selection
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
    fname = []
    rlist = get_rundle_list()
    olist = []
    for rund in rlist:
        if rund.startswith('R'):
            continue
        olist.append(rund.replace('_', ' '))
    if not olist:
        showwarning('Error', 'No Rundles Found')
        return
    font = tkFont.Font(family='Arial', size=24, weight='bold')
    top = Tkinter.Toplevel(bd=10)
    top.geometry('600x800+800+200')
    top.title('Rundle Selector')
    tpart = Tkinter.Frame(top)
    tpart.pack(side=Tkinter.TOP)
    bpart = Tkinter.Frame(top)
    bpart.pack(side=Tkinter.BOTTOM)
    scrollbar = Tkinter.Scrollbar(tpart)
    scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
    mylist = Tkinter.Listbox(tpart, yscrollcommand=scrollbar.set,
                             height=18, font=font)
    for line in olist:
        mylist.insert(Tkinter.END, line)
    mylist.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
    scrollbar.config(command=mylist.yview)
    picker = Button(bpart, text='SELECT', command=save_select, font=font)
    picker.pack()
    top.mainloop()
    if fname:
        top.destroy()
        field_info['var'].set(fname[0].replace('_', ' '))
        field_info['llama'] = None
        field_info['rundle'] = fname[0]


def ll_loop():
    """
    Wrapper supporting League Gui
    """
    root = Tkinter.Tk()
    LleagueGui(root)
    root.mainloop()


if __name__ == '__main__':
    ll_loop()
