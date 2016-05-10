#!/usr/bin/env python
from get_players import log_team
from initialize import initialize

def extrapolate(number, numer, denom):
    """
    Perform extrapolation of a statistic to another number (basically do long
    division and adjust back to an integer value.

    Input:
        number -- statistic (integer)
        numer -- numerator of fraction number is multiplied by.
        denom -- denominator of fraction number is multiplied by.

    Returns:
        Extrapolated number.
    """
    retv = number * numer * 1000
    retv /= denom
    retv += 500
    retv /= 1000
    return retv

def get_extrap(data, numer, denom):
    """
    Perform the above extrapolation on all the values in a dictionary.

    Returns the same dictionary keys with adjusted values.
    """
    retv = {}
    for keyv in data.keys():
        retv[keyv] = extrapolate(data[keyv], numer, denom)
    return retv

class teams_score():
    """
    Object used to keep track of the adjusted scoring stats for all teams in
    the league.
    """

    def __init__(self, league):
        """
        Create self.batters and self.pitchers, lists where every entry
        represnts a fantasy team.  These are ordered by league team number.
        Each entry is a dictionary of statistics for that team.
        """
        startv = initialize('roto.ini')
        self.batters = []
        self.pitchers = []
        for tmno in range(0,12):
            tmdata = log_team(league, tmno+1)
            self.batters.append(get_extrap(tmdata[0], startv['totalg'], startv['sofar']))
            self.pitchers.append(get_extrap(tmdata[1], startv['totalg'], startv['sofar']))

    def comp_data(self, myteam, other, swtch):
        """
        Score my team againsta another team in our league. +2 if my stat
        beats them, +1 if we tie.

        Input:
            myteam -- my team number
            other -- my opponents team number
            swtch -- 0 == Batting stats, 1 == Pitching stats

        Returns:
            integer used to calculate rating.
        """
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
        """
        Perform the above comp_data calculation against all teams in the league.

        Input:
            myteam -- my team number
            swtch -- 0 == Batting stats, 1 == Pitching stats

        Returns:
            Sum of the comp_data calls
        """
        score = 0
        inttm = myteam - 1
        for tmno in range(0,12):
            if inttm == tmno:
                continue
            score += self.comp_data(inttm, tmno, swtch)
        return score

    def adjust_score(self, myteam, swtch, stats_down, stats_up):
        """
        Used to readjust the stats of our team by replacing a player.

        Input:
            myteam -- our team number
            swtch -- 0 == Batting stats, 1 == Pitching stats
            stats_down -- Stats of player being hypothetically replaced
            stats_up -- Stats of player being hypothetically added

        Results: Updates local self.batters or self.pitchers value.
                 Switching the down and up parameterst can be used to
                 reverse the action of this call.
        """
        larray = [self.batters, self.pitchers][swtch]
        inttm = myteam - 1
        for stat in larray[inttm]:
            larray[inttm][stat] -= stats_down[stat]
            larray[inttm][stat] += stats_up[stat]

if __name__ == "__main__":
    teams = teams_score(99866)
    print teams.comp_score(9,0)
    print teams.comp_score(9,1)
