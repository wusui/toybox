#!/usr/bin/env python
from get_players import log_team
from initialize import initialize

def extrapolate(number, numer, denom):
    retv = number * numer * 1000
    retv /= denom
    retv += 500
    retv /= 1000
    return retv

def get_extrap(data, numer, denom):
    retv = {}
    for keyv in data.keys():
        retv[keyv] = extrapolate(data[keyv], numer, denom)
    return retv

class teams_score():
    def __init__(self, league):
        startv = initialize('roto.ini')
        self.batters = []
        self.pitchers = []
        for tmno in range(0,12):
            tmdata = log_team(league, tmno+1)
            self.batters.append(get_extrap(tmdata[0], startv['totalg'], startv['sofar']))
            self.pitchers.append(get_extrap(tmdata[1], startv['totalg'], startv['sofar']))
    def comp_data(self, myteam, other, swtch):
        score = 0
        larray = [self.batters, self.pitchers][swtch]
        stat_tab = [['rbis', 'runs', 'sb', 'homers', ['hits', 'at-bats']], ['wins', 'saves', 'ks', ['outs','earned-runs'], ['outs', 'wh']]]
        for stat in stat_tab[swtch]:
            if type(stat) is list:
                fnum = larray[myteam][stat[0]] * larray[other][stat[1]]
                snum = larray[other][stat[0]] * larray[myteam][stat[1]]
            else:
                fnum = larray[myteam][stat]
                snum = larray[other][stat]
            if fnum > snum:
                score += 2
            if fnum == snum:
                score += 1
        return score
    def comp_score(self, myteam, swtch):
        score = 0
        inttm = myteam - 1
        for tmno in range(0,12):
            if inttm == tmno:
                continue
            score += self.comp_data(inttm, tmno, swtch)
        return score
    def adjust_score(self, myteam, swtch, stats_down, stats_up):
        larray = [self.batters, self.pitchers][swtch]
        inttm = myteam - 1
        for stat in larray[inttm]:
            larray[inttm][stat] -= stats_down[stat]
            larray[inttm][stat] += stats_up[stat]
if __name__ == "__main__":
    teams = teams_score(99866)
    print teams.comp_score(9,0)
    print teams.comp_score(9,1)
