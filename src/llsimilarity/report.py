"""
Created on May 10, 2014

@author: Warren Usui
"""
import webbrowser

from llsimilarity.utilities import get_tempdir


def html_report(rep_data, title, display):
    """
    Write an html report to display using the user data from
    rep_data and the page title from title.
    """
    header = ['<html><head><title>Learned League Simularity Rankings</title>',
              '</head>',
              '<body style="width:1000px;">',
              '<table class="center" border="1" style="text-align:center;">',
              '<caption style="font-size:x-large;">',
              '{}</caption>'.format(title),
              '<tr><th>Llama Name</th><th>Similarity Rating</th></tr>']
    trailer = "</table></body></html>"
    fname = "{}/{}.html".format(get_tempdir(), display)
    with open(fname, 'w') as ofile:
        for lyne in header:
            ofile.write(lyne)
        for data in rep_data:
            ofile.write('<tr>')
            for field in data:
                ofile.write('<td>')
                ofile.write(field)
                ofile.write('</td>')
            ofile.write('</tr>')
        ofile.write(trailer)
        webbrowser.open(fname)


def ascii_report(file_name, lyst):
    """
    Write an ascii report to file file_name using the data from lyst
    """
    fname = "{}/{}".format(get_tempdir(), file_name)
    with open(fname, 'w') as bfd:
        for entry in lyst:
            bfd.write("{}: {}\n".format(entry[0], entry[1]))
