#!/usr/bin/env python
from datetime import datetime
from initialize import initialize
from get_players import log_team
from get_players import one_team
from get_pool import get_pool
from team_score import teams_score
from team_score import extrapolate
from team_score import get_extrap

def eval_others(pdata, period, ptype, startv):
    retv = {}
    player_type = ['B', 'P']
    our_pool = get_pool(period, player_type[ptype], startv['league'])
    adj_period = period
    if adj_period > 366:
        adj_period = startv['sofar']
    for plyr in our_pool.keys():
        p_stats = get_extrap(our_pool[plyr], startv['daysleft'], adj_period)
        count = 0
        total_points = 0
        for oplyr in pdata['our_plyrs'][ptype]:
            npos = plyr.split(':')[-1].split(',')
            opos = oplyr['pos'].split(',')
            intr = [x for x in npos if x in opos]
            if len(intr) > 0:
                t_stats =  get_extrap(oplyr['stats'], startv['daysleft'], adj_period)
                pdata['tm_scores'].adjust_score(startv['team'], ptype, t_stats, p_stats)
                total_points += pdata['tm_scores'].comp_score(startv['team'], ptype)
                count += 1
                pdata['tm_scores'].adjust_score(startv['team'], ptype, p_stats, t_stats)
        if count > 0:
            retv[plyr] = extrapolate(total_points * 10, 1, count)
    return retv

def eval_loop():
    startv = initialize('roto.ini')
    league = startv['league']
    usno = startv['team']
    player_data = {}
    tm_scores = teams_score(league)
    player_data['std_scores'] = [tm_scores.comp_score(usno,x) for x in range(0,2)]
    player_data['tm_scores'] = tm_scores
    player_data['our_team'] = log_team(league, usno)
    all_data = {}
    for period in [7, 14, 30, datetime.now().year]:
        player_data['our_plyrs'] = one_team(period, league, usno)
        for ptype in  [0, 1]:
            tkey = str(period) + "-" + ['Batter', 'Pitcher'][ptype]
            all_data[tkey] = eval_others(player_data, period, ptype, startv)
    return all_data

if __name__ == "__main__":
    eval_loop()
