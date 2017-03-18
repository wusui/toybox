import json
from os import sep
from check_data import HandleEspnGroup

def get_page_info(rundle):
    with open(sep.join(['data', rundle, 'results.json']), 'r') as f:
        saved_data = json.load(f)
    return saved_data

def get_denom(in_data):
    sumr = 0
    for plr in in_data:
        sumr += plr['score']
    return sumr

def get_pct(numer, denom):
    if numer == denom:
        return '1.00000'
    xnum = 1000000 * numer
    onum = xnum / denom
    onum += 5
    onum /= 10
    retval = ".%05d" % onum
    return retval

def comp_col(red, green):
    return '#%s%s00' % (format(red,'02x'), format(green,'02x'))

def bgcolor(denom, numer):
    if numer * 2 ==  denom:
        return "#ffffff"
    color = numer * 1024 / denom - 512
    if color == 512:
        return "#000000;color:#ffffff"
    if color < 256:
        return comp_col(color, 255)
    return comp_col(255, 511 - color)

def game_headers(pattern):
    ostrm = ''
    for tindx in range(0, len(pattern), 2):
        ostrm += '<th> <div>%s</div><div>%s</div> </th>' % (pattern[tindx], pattern[tindx+1])
    return ostrm

def add_plr_col(otable, field):
    otable += '<td>' + field + '</td>'
    return otable

def gen_tbl_line(otable, plr, sdisp):
    for field in [plr['name'], "%d" % plr['score'], plr['pct']]:
        otable = add_plr_col(otable, field)
    for entry in sdisp:
        otable += '<td style="background-color:' + entry[1] + '">'
        otable += entry[0] + '</td>'
    return otable

def gen_display(rundle):
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
    bround = {16:'sweet16', 8:'elite8', 4:'Final4'}
    pround = bround[len(wpattern)]
    with open(sep.join(['%s','%s.html']) % (pround,rundle), 'w') as wf:
        wf.write(htmld)

if __name__ == "__main__":
    HandleEspnGroup().caller(gen_display)
