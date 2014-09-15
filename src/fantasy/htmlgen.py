"""
Html text handling routines.

Tblz, a parameter passed to many of these routines, is a list of
four lists.  When displayed in html, each list is converted into
a table and is displayed inside another table, resulting in the
output being four tables in a row.  
"""

import webbrowser
from datetime import datetime
from fantasy.dateutils import get_current_week
TEMP_FILE = "temporary.html"


def wrapper(tblz, title):
    """
    Wrap the html header, style, and body blocks around some html data.
    Title is the page header to be displayed.
    """
    with open("header.html") as fdesc:
        data = fdesc.read()
    data = data % title
    retv = "%s\n%s</body></html>" % (data, tblz)
    return retv


def fmt_score(score):
    """
    Given an integer score, return a 1/100's unit value as a string.
    """
    lpart = score // 100
    rpart = score % 100
    return "%d.%02d" % (lpart, rpart)


def one_score(entry):
    """
    Extract total score early for comparison later.  Used to determine
    winner in last week's page.
    """
    tscore = 0
    for indx in range(0, 9):
        person = entry[1][indx]
        tscore += person.get_score()
    return tscore


def one_table(entry, rev_ind):
    """
    Return an html string representation of one of the tables to be displayed.
    If Rev_ind is set, display the total points in a different color.
    """
    retv = ['<td><table>']
    retv.append('<tr><th colspan="4">%s</th></tr>' % entry[0])
    retv.append('<tr><th>Position</th><th>Player</th><th>Team</th>')
    retv.append('<th>Score</th></tr>')
    posa = ['QB', 'WR', 'WR', 'WR', 'RB', 'RB', 'TE', 'K', 'DEF']
    tscore = 0
    for indx, position in enumerate(posa):
        person = entry[1][indx]
        line = []
        line.append('<tr class="%s"><td>' % person.get_color())
        line.append(position)
        line.append('</td><td>%s' % person.get_name())
        line.append('</td><td>%s' % person.get_team())
        line.append('</td><td class="alnright">%s</td></tr>' %
                    fmt_score(person.get_score()))
        retv.append(''.join(line))
        tscore += person.get_score()
    if rev_ind:
        rev_txt = ' class="revgreen"'
    else:
        rev_txt = ''
    retv.append('<tr%s><th colspan="4">Total Points: %s</th></tr>' %
                 (rev_txt, fmt_score(tscore)))
    retv.append('</table></td>')
    return '\n'.join(retv)


def gen_html_table(wno, tblz, last_week):
    """
    Generate a table for a week.  That table contains subtables displayed
    horizontally on the page.  Wno is the week number value displayed at the
    top of the page.  If Last_week is set, determine who the winner was and
    set the indicator in rev_ind list.
    """
    title = '<br>\n<h1>WEEK %s</h1>\n<br>\n<table cellspacing="10">' % wno
    retv = [title]
    rev_ind = [False] * 4
    cmp_vec = []
    if last_week:
        for entry1 in tblz[0:2]:
            cmp_vec.append(one_score(entry1))
        rev_ind = [cmp_vec[0] > cmp_vec[1], cmp_vec[0] < cmp_vec[1],
                   False, False]
    for indx, entry in enumerate(tblz):
        retv.append(one_table(entry, rev_ind[indx]))
    retv.append('</table>')
    return '\n'.join(retv)


def create_new_page(last_week, tblz, spec_file):
    """
    If spec_file is set, write new html page to that file.  Otherwise,
    store the html page in TEMP_FILE.  Return the name of the file created.
    """
    out_file = TEMP_FILE
    if spec_file:
        out_file = spec_file
    wno = get_current_week()
    if last_week:
        wno -= 1
    data = gen_html_table(wno, tblz, last_week)
    if out_file == TEMP_FILE:
        datenow = datetime.now().strftime("%b %d, %Y")
        data = wrapper(data, "Fantasy -- %s" % datenow)
    with open(out_file, 'w') as fdesc:
        fdesc.write(data)
    return out_file


def display_new_page(last_week, tblz, spec_file=''):
    """
    Display page created by create_new_page
    """
    out_file = create_new_page(last_week, tblz, spec_file)
    webbrowser.open(out_file)
