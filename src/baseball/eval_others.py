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
    """
    Calculate the value of a player by checking that player against all
    currently players at that player's position.

    Input:
        pdata -- player_data as describ3ed in eval_loop
        period -- length (in days) for a player's stats to be checked
        ptype -- 0==Batter, 1==Pitcher
        startv -- root.ini data.

    Returns a list of values indexed by a player's uniq identifier
    """
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
                t_stats =  get_extrap(oplyr['stats'], startv['daysleft'], adj_riod)
                pdata['tm_scores'].adjust_score(startv['team'], ptype, t_statsp_stats)
                total_points += pdata['tm_scores'].comp_score(startv['team'], ype)
                count += 1
                pdata['tm_scores'].adjust_score(startv['team'], ptype, p_statst_stats)
        if count > 0:
            retv[plyr] = extrapolate(total_points * 10, 1, count)
    return retv

def eval_loop():
    """
    Organize data into a distinct dictionary for use by the eval_others method    The most important dictionary generated is the player_data dictionary,
    whose entries consist of:

    KEY                 DESC
    std_scores          original scores for our team (2 values -- batter and pcher).
    tm_scores           list of team data.  Each team is represented by a
                        dictionary of score values extrapolated to the end
                        of the season.
    our_team            Stats for each individual player on our team.

    Returns a dictionary of rating values keyed by a string representing
    each player.
    """
    startv = initialize('roto.ini')
    league = startv['league']
    usno = startv['team']
    player_data = {}
    tm_scores = teams_score(league)
    player_data['std_scores'] = [tm_scores.comp_score(usno,x) for x in range(0)]
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
