import json
from operator import attrgetter
from os import sep
from os.path import isfile
from check_data import HandleEspnGroup
from get_picks import get_reality

def score_so_far(nlist, my_picks):
    score = 0
    for round in range(0,len(nlist)):
        factor = 2**round
        for winner in nlist[round]:
            if winner in my_picks['picks'][round]:
                score += factor
    return score

class player(object):
    def __init__(self, name, score, winv):
        self.name = name
        self.score = score
        self.winv = winv

def xlate(pvec):
    rvec = []
    for entry in pvec:
        nval = {}
        nval['name'] = entry.name
        nval['score'] = entry.score
        nval['winv'] = entry.winv
        rvec.append(nval)
    return rvec

def gen_future(nlist, my_picks):
    all_data = []
    myscore = score_so_far(nlist, my_picks)
    ulim = len(nlist[-1]) - 1
    for i in range(0,2**ulim):
        fval = i
        score = myscore
        rnd_ind = len(nlist)
        cntr = 0
        pval = 2**rnd_ind
        curlist =  nlist[rnd_ind-1]
        futurelist = []
        for fctr in range(0,ulim):
            offset = fval % 2
            fval /= 2
            nentry = curlist[cntr*2 + offset]
            if my_picks['picks'][rnd_ind][cntr] == nentry:
                score += pval
            futurelist.append(nentry)
            cntr += 1
            if cntr >= len(my_picks['picks'][rnd_ind]):
                pval *= 2
                cntr = 0
                rnd_ind += 1
                curlist = futurelist
                futurelist = []
        all_data.append(score)
    return all_data

def gen_possible(nlist, stash, names):
    wcombos = {}
    mscores = [0] * len(stash)
    ulim = len(nlist[-1]) - 1
    for i in range(0,2**ulim):
        cmax = 0
        cindx = []
        for j in range(0,len(stash)):
            if stash[j][i] == cmax:
                cindx.append(j)
            if stash[j][i] > cmax:
                cmax = stash[j][i]
                cindx = [j]
        for cval in cindx:
            mscores[cval] += 1
            if cval in wcombos:
                wcombos[cval].append(i)
            else:
                wcombos[cval] = [i]
    tmin = 2**ulim
    minw = -1
    for v in wcombos.keys():
        if len(wcombos[v]) < tmin:
            tmin = len(wcombos[v])
            minw = v
    pvec = []
    for i in range(0, len(mscores)):
        if mscores[i] == 0:
            continue
        npl = player(names[i], mscores[i], wcombos[i])
        pvec.append(npl)
    pvec.sort(key=attrgetter('score'), reverse=True)
    for i in pvec:
        rvec = [0] * ulim
        for nval in i.winv:
            for gm in range(0,ulim):
                i2 = nval % 2
                nval /= 2
                if i2:
                    rvec[gm] += 1
        i.winv = rvec
    return xlate(pvec)

def compute_it(rundle):
    ofname = sep.join(['data', 'reality.json'])
    if not isfile(ofname):
        with open(ofname, 'w') as f:
            json.dump(get_reality(), f)
    with open(sep.join(["data", "reality.json"]), 'r') as f:
        nlist = json.load(f)
    with open(sep.join(["data", rundle, "picks.json"]), 'r') as f:
        pinfo = json.load(f)
    stash = []
    names = []
    ostring = ''
    for apick in pinfo:
        my_picks = {'name': apick[0], 'picks': apick[1]}
        print "Handling %s" % apick[0]
        ostring += "%s === %s\n" % (apick[0], score_so_far(nlist, my_picks))
        stash.append(gen_future(nlist, my_picks))
        names.append(my_picks['name'])
    data1 = gen_possible(nlist, stash, names)
    with open(sep.join(["data", rundle, "results.json"]), 'w') as f:
        json.dump(data1, f)
    with open(sep.join(["data", rundle, "scores.txt"]), 'w') as f:
        f.write(ostring)

if __name__ == "__main__":
    HandleEspnGroup().caller(compute_it)
