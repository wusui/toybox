#!/usr/bin/env python
from datetime import datetime
BATTERS = ['B', 'C', '1B', '2B', '3B', 'SS', 'OF']
PITCHERS = ['P', 'SP', 'RP']
PERIODS = [7, 14, 30, datetime.now().year]
B_STATS = {'H/AB': [60, 1], 'R': [7, 1], 'HR': [12, 1],
           'RBI': [13, 1], 'SB': [14, 1]}
P_STATS = {'IP': [50, 1], 'W': [28, 1], 'SV': [32, 1],
           'K': [42, 1], 'ERA': [26, 0], 'WHIP': [27, 0]}

COMMON_TXT = "http://baseball.fantasysports.yahoo.com/b1/%s/"
REST = "players?status=A&pos=%s&cut_type=33&stat1=S_%s&myteam=0&sort=%d&sdir=%d"

def set_period(period):
    """Get string representation of period.

    Input: period (integer, possible values are 7, 14, 30, or a year)
    Output: String representation of this field used in http paths.
    """
    if not period in PERIODS:
        return 'ERROR'
    if period < 366:
        return "L%d" % period
    return "S_%d" % period

def get_avail(period, position, stat, league, count):
    """Return html text to find available players

    Input:
        period: length of time stats are collected (7, 14, 30, this year)
        position: player position being searched
        stat: Stat being searched for best available players. This should
           be one of the elements in B_STATS or P_STATS
        league: League number
        count: Number of pages of players to check.
    Returns:
        Text of available player query
    """
    htmlv = COMMON_TXT % league
    stval = [0, 0]
    if position in BATTERS:
        stval = B_STATS[stat]
    if position in PITCHERS:
        stval = P_STATS[stat]
    htmlv += REST % (position, set_period(period), stval[0], stval[1])
    if count > 0:
        count *= 25
        htmlv += "&count=%s" % count
    return htmlv

def get_team(period, league, team):
    """Get team statistics.

    Input:
        period: length of time stats are collected
        league: league number
        team: team number
    Returns:
        Html text to find the player stats for the team
    """
    return "".join([COMMON_TXT % league, "%s" % team,
            "?stat1=S&stat2=%s" % set_period(period)])

def get_team_log(league, team):
    """Get team log (stats for a team).

    Input:
        league: league number
        team: team number
    Returns:
        Html text to find the team log
    """
    return "".join([COMMON_TXT % league, "%s/teamlog" % team])
