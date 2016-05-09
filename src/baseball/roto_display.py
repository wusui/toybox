#!/usr/bin/env python
import operator
from datetime import datetime
from eval_others import eval_loop
from make_table import make_table
from make_table import make_page

def merge_tables(tlist, gpos):
    table = "<table><tr>"
    for tbl in tlist:
        table += "<td>%s</td>" % tbl
    table += "</tr><table>"
    page = make_page(table, gpos)
    with open("%s.html" % gpos, 'w') as ofile:
        ofile.write(page)

def build_tables(all_info):
    for gpos in ['Batter', 'Pitcher']:
        tlist = []
        for period in ['7','14','30',str(datetime.now().year)]:
            skey = "%s-%s" % (period, gpos)
            title = "%s day" % period
            if len(period) > 3:
                title = 'Season'
            tlist.append(make_table(title, all_info[skey], ['name', 'team', 'pos', 'pts'], ['left', 'center', 'center', 'center']))
        merge_tables(tlist, gpos)


def arrange():
    sortie = {}
    all_data = eval_loop()
    for period in ['7','14','30',str(datetime.now().year)]:
        for ptype in ['Batter','Pitcher']:
            skey = "%s-%s" % (period, ptype)
            sortie[skey] = sorted(all_data[skey].items(), key=operator.itemgetter(1))[::-1]
    all_info = {}
    for nkey in sortie.keys():
        llist = []
        for entry in sortie[nkey][0:25]:
            newline = {}
            first_part = entry[0].split(':')
            newline['name'] = first_part[0]
            newline['team'] = first_part[1]
            newline['pos'] = first_part[2]
            newline['pts'] = str(entry[1])
            llist.append(newline)
        all_info[nkey] = llist
    build_tables(all_info)

if __name__ == "__main__":
    arrange()
