#!/usr/bin/env python
"""
Create the html files from data collected by computencaa.py
"""
import json
from os import sep
from check_data import HandleEspnGroup


def get_page_info(rundle):
    # Read the results.json file for the appropriate group.
    #
    # rundle -- group name
    # returns:  data collected for this group by the computencaa.py script
    with open(sep.join(['data', rundle, 'results.json']), 'r') as f:
        saved_data = json.load(f)
    return saved_data


def get_denom(in_data):
    # Get denominator used to calculate percentages in displays.
    #
    # in_data -- data collected for this group by the computencaa.py script
    # returns:   the sum of all scores for all entries in the group
    sumr = 0
    for plr in in_data:
        sumr += plr['score']
    return sumr


def get_pct(numer, denom):
    # Calculate a ratio using large integer arithmetic.
    #
    # numer -- integer numerator
    # denom -- integer denominator
    # returns: string representation of the ratio in decimal form
    if numer == denom:
        return '1.00000'
    xnum = 1000000 * numer
    onum = xnum / denom
    onum += 5
    onum /= 10
    retval = ".%05d" % onum
    return retval


def comp_col(red, green):
    # Reformat colors on the red/green scale (used in html output).
    #
    # red   -- red rgb value
    # green -- green rgb value
    # returns: String representation of the rgb value
    return '#%s%s00' % (format(red, '02x'), format(green, '02x'))


def bgcolor(denom, numer):
    # Given a ratio, return an rgb value that represents that ratio.  Special
    # case the 1.00 case.
    #
    # denom -- denominator of ratio
    # numer -- numerator of ratio
    # returns: String representation of the rgb value
    if numer * 2 == denom:
        return "#ffffff"
    color = numer * 1024 / denom - 512
    if color == 512:
        return "#000000;color:#ffffff"
    if color < 256:
        return comp_col(color, 255)
    return comp_col(255, 511 - color)


def game_headers(pattern):
    # Return the html text used to display the header columns
    # for upcoming games.
    #
    # pattern -- list of team names
    # returns:   html text that lists the matched teams in two rows.
    ostrm = ''
    for tindx in range(0, len(pattern), 2):
        ostrm += '<th> <div>%s</div><div>%s</div> </th>' % (pattern[tindx],
                                                            pattern[tindx+1])
    return ostrm


def gen_tbl_line(otable, plr, sdisp):
    # Generate an html line for a table display
    #
    # otable -- html text for the table
    #    plr -- entry to be displayed
    #  sdisp -- individual game display information
    # returns: otable with line added.
    for field in [plr['name'], "%d" % plr['score'], plr['pct']]:
        otable += '<td>' + field + '</td>'
    for entry in sdisp:
        otable += '<td style="background-color:' + entry[1] + '">'
        otable += entry[0] + '</td>'
    return otable


def gen_display(rundle):
    """
    Write the html file to display data for each potentially winning entrant.
    First read the template.txt file to get a sample html file.  Next start
    replacing fixed blocks of text with text that is appropriate for the
    table to display.  For each entrant, caclulate the percentage times that
    entry should win and collect a set of 'events to root for next round'.
    After that, write the file to the appropriate subdiretory depending on
    how deep into the tournament we are.

    rundle -- group name
    """
    with open('template.txt', 'r') as f:
        htmld = f.read()
    drundle = ' '.join(rundle.split('_'))
    htmld = htmld.replace('XRUNDLEX', drundle)
    saved_data = get_page_info(rundle)
    denom = get_denom(saved_data)
    for plr in saved_data:
        plr['pct'] = get_pct(plr['score'], denom) 
    with open(sep.join(['data', 'reality.json']), 'r') as f:
        happened = json.load(f)
    wpattern = happened[1]
    game_head = game_headers(wpattern)
    htmld = htmld.replace('XMATCHUPHEADERSX', game_head)
    otable = ''
    for plr in saved_data:
        sdisp = []
        otable += "<tr>"
        for windx in range(0, len(wpattern), 2):
            indx = windx / 2
            opp = plr['score'] - plr['winv'][indx]
            factor = 0
            if opp < plr['winv'][indx]:
                factor = 1
            degree = max(opp, plr['winv'][indx])
            if opp == plr['winv'][indx]:
                school = '*'
            else:
                school = wpattern[windx+factor]
            sdisp.append((school, bgcolor(plr['score'], degree)))
        otable = gen_tbl_line(otable, plr, sdisp)
        otable += "</tr>"
    htmld = htmld.replace('XTABLEDATAX', otable)
    bround = {16: 'sweet16', 8: 'elite8', 4: 'Final4'}
    pround = bround[len(wpattern)]
    with open(sep.join(['%s', '%s.html']) % (pround, rundle), 'w') as wf:
        wf.write(htmld)

if __name__ == "__main__":
    HandleEspnGroup().caller(gen_display)
