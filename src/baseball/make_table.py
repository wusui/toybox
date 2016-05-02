#!/usr/bin/env python
from string import upper

def make_table(header, data, fields, align):
    """Generate an html table

    Input:
        header -- title of the table
        data -- contents of the table (list of list representing rows)
        fields -- header values for the columns
        align -- alignment of each column
    Returns: text of a table
    """
    retv = ""
    if header:
        retv +="<h3>%s</h3>\n" % header
    retv += '<table class="bfmt">\n<tr>'
    for column in fields:
        if column.find(":") > 0:
            column = column.split(":")[-1]
        retv += "<th>%s</th>" % upper(column)
    retv += "</tr>\n"
    for entry in data:
        retv += "<tr>"
        for count,field in enumerate(fields):
            retv += '<td class="%s">' % align[count]
            if field.find(":") > 0:
                parts = field.split(":")
                value = entry[parts[0]][parts[1]]
            else:
                value = entry[field]
            retv += str(value)
            retv += "</td>"
        retv += "</tr>\n"
    retv += "</table>"
    return retv

def make_page(table, header):
    """Create an html page.

    Input:
        table -- Data to be stuck into the middle of the page
        header -- Text to appear on the page tab
    Returns:
        The text of an html page

    Generate a page using the template in htmlpage.txt
    """
    htmlpage = ''
    with open('htmlpage.txt', 'r') as myfile:
        htmlpage=myfile.read()
    return htmlpage % (header, table)
