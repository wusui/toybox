"""
Html text handling routines.

Most of the output from this set of programs consists of four tables of
stats for a week.  These tables are combined into one table with four
sub-tables.
"""

import webbrowser
TEMP_FILE = "temporary.html"


def wrapper(tblz, title):
    """
    Wrap the html header, style, and body blocks around some html data.

    Input:
        tblz -- String of html text to be wrapped.
        title -- Text of header to be displayed.

    Returns a string with further html headers and trailers wrapped around it.
    Header information is read in from the header.html file.  Once wrapped,
    the text returned should display a valid html page.
    """
    with open("header.html") as fdesc:
        data = fdesc.read()
    data = data % title
    retv = "%s\n%s</body></html>" % (data, tblz)
    return retv


def one_table(entry):
    """
    Return an html string representation of one of the tables to be displayed.

    Input:
        entry -- the representation of a table.  The first item of this
        tuple is the header for the table to be displayed.  The second
        item is a tuple of a list of player pointers and a dictionary of
        player information indexed by the previous pointers.

    The individual player information is formatted into a table to be
    displayed.  By the time this code is reached, the player information
    in the entry passed should be complete and pruned of substitute players.

    This returns a table of stats for different players (either a team, or
    a specially constructed list).
    """
    retv = ['<td><table>']
    retv.append('<tr><th colspan="4">%s</th></tr>' % entry[0])
    retv.append('<tr><th>Position</th><th>Player</th><th>Team</th>')
    retv.append('<th>Score</th></tr>')
    posa = ['QB', 'WR', 'WR', 'WR', 'RB', 'RB', 'TE', 'K', 'DEF']
    tscore = 0
    for indx, position in enumerate(posa):
        key = entry[1][0][indx]
        person = entry[1][1][key]
        line = []
        line.append('<tr class="%s"><td>' % person.get_color())
        line.append(position)
        line.append('</td><td>%s' % person.get_name())
        line.append('</td><td>%s' % person.get_team())
        line.append('</td><td class="alnright">%.2f</td></tr>' %
                    person.get_score())
        retv.append(''.join(line))
        tscore += person.get_score()
    retv.append('<tr class="black"><th colspan="4">Total Points: %.2f</th></tr>'
                % tscore)
    retv.append('</table></td>')
    return '\n'.join(retv)


def gen_html_table(wno, tblz):
    """
    Generate a table for a week.  That table contains subtables displayed
    horizontally on the page.

    Input:
        wno -- Week number
        tblz -- list of four table entries to be displayed.

    The return value is html text that represents a week's worth of tables.
    Code in this routine also determines if the text should be all black (as
    is the case with completed diary records).
    """
    title = '<br>\n<h1>WEEK %s</h1>\n<br>\n<table cellspacing="10">' % wno
    retv = [title]
    for entry in tblz:
        retv.append(one_table(entry))
    retv.append('</table>')
    outstring = '\n'.join(retv)
    rloc = outstring.find('class="red"')
    gloc = outstring.find('class="green"')
    if rloc < 0 and gloc < 0:
        spltr = outstring.split('class="blue"')
        outstring = 'class="black"'.join(spltr)
    return outstring


def create_new_page(wno, out_file, header, tblz, hilitewin=False):
    """
    Create an html page.

    Input:
        wno -- week number
        out_file -- name of the http file we are creating
        header -- text displayed on the header of the page
        tblz -- list of four table entries to be displayed
        hilitewin -- if True, highlight the final total winner between
                     table 1 and table 2.
    """
    data = ''
    for entry in tblz:
        data = '\n'.join([data, gen_html_table(wno, entry)])
        wno += 1
    data = wrapper(data, header)
    if hilitewin:
        data = pick_win(data)
    with open(out_file, 'w') as fdesc:
        fdesc.write(data)
    return out_file

def pick_win(in_text):
    """
    Highlight the winner between the entries in the first two tables]
    (the team being tracked and this week's opponent).

    Input:
        in_text -- Text of tables prior to highlighting.

    The return value of this method is in_text with the winner between the
    first two tables highlighted for every week.
    """
    parts = in_text.split('\n')
    ploc = []
    for indx, field in enumerate(parts):
        pt_ind = field.find('Total Points: ')
        if pt_ind > 0:
            nstart = pt_ind + len('Total Points: ')
            numb = field[nstart:field.find('<', nstart)]
            ploc.append([indx, field, float(numb)])
    challenge = 0
    for indx, field in enumerate(ploc):
        if indx % 4 == 0:
            challenge = field[2]
        if indx % 4 == 1:
            if challenge < field[2]:
                parts[field[0]] = field[1].replace('"black"', '"revgreen"')
            else:
                parts[ploc[indx - 1][0]] = \
                        ploc[indx - 1][1].replace('"black"', '"revgreen"')
    return '\n'.join(parts)


def display_new_page(wno, tblz, parms):
    """
    Display page created by create_new_page.

    Input:
        wno -- week number
        tblz -- table information
        params -- parameters used to change the output file name, specify
                  a new title, or highlight winning totals.

    Unless otherwise specified, this method opens the new page in a
    browser window.
    """
    out_fname = parms.get('out_fname', TEMP_FILE)
    out_head = parms.get('header', "Fantasy Results")
    hilite = parms.get('highlight_win', False)
    out_file = create_new_page(wno, out_fname, out_head, tblz, hilite)
    if 'nobrowse' in parms:
        return
    webbrowser.open(out_file)
