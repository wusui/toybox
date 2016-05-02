#!/usr/bin/env python
from read_parse import read_parse
from html_strings import get_avail
from html_strings import get_team
from html_strings import get_team_log

def bstats(lstr):
    """ Extract batter stats from string

    Input:
        lstr: Colon seperate batting statistics
    Returns:
        dictionary of batting statistics
    """
    retd = {}
    lstats = lstr.split(":")
    first_no = lstats[0].split('/')
    retd['hits'] = int(first_no[0])
    retd['at-bats'] = int(first_no[1])
    retd['runs'] = int(lstats[1])
    retd['homers'] = int(lstats[2])
    retd['rbis'] = int(lstats[3])
    retd['sb'] = int(lstats[4])
    return retd

def derivep(outs, factor, value):
    """Extract integer numerator from pitching stat ratios.

    ERA and WHIP pitching stats are manipulated in order to extract
    earned runs and walks + hits values.

    Input:
        outs: outs (more granular than IP)
        factor: number to ajdust ERA or WHIP ratios.
        value: ERA or WHIP used to extract numerator.
    Returns:
        Int value extracted from pitching ratio and outs.
    """
    first_no = value.split(".")
    ratio = int(first_no[0])*100 + int(first_no[1])
    ratio *= 10 * outs
    ratio //= factor * 100
    ratio += 5
    ratio //= 10
    return ratio

def pstats(lstr):
    """ Extract pitcher stats from string

    Input:
        lstr: Colon seperate pitching statistics
    Returns:
        dictionary of pitching statistics
    """
    retd = {}
    lstats = lstr.split(":")
    first_no = lstats[0].split('.')
    retd['outs'] = int(first_no[0])*3 + int(first_no[1])
    retd['wins'] = int(lstats[1])
    retd['saves'] = int(lstats[2])
    retd['ks'] = int(lstats[3])
    retd['earned-runs'] = derivep(retd['outs'], 27, lstats[4])
    retd['wh'] = derivep(retd['outs'], 3, lstats[5])
    return retd

def relist(table):
    """Return a list of player records.

    Input: Table containing player data
    Returns:
        List of Dictionaries of player information.  Each player
        entry contains name, team, position, and stat information.  Each
        set of stats is another dictionary of statistics appropriate for this
        player's position.
    """
    retv = []
    for record in table:
        sp = 5
        if record[3] ==  'Video Playlist':
            sp += 1
        name = record[sp]+record[sp+1]
        team_info = record[sp+2]+record[sp+3]
        lstr = ":".join(record)
        lstr = lstr[lstr.find('%')+2:]
        team_pos = team_info.split('-')
        team = team_pos[0].strip()
        pos = team_pos[1].strip()
        lstr = lstr.replace('-','0')
        if pos.endswith('P'):
            stats = pstats(lstr)
        else:
            stats = bstats(lstr)
        retv.append({'name': name, 'team': team, 'pos': pos, 'stats': stats})
    return retv

def available(period, position, stat, league, count):
    """Return html text to find available players

    Input:
        period: length of time stats are collected (7, 14, 30, this year)
        position: player position being searched
        stat: Stat being searched for best available players. This should
           be one of the elements in B_STATS or P_STATS
        league: League number
        count: Number of pages of players to check.
    Returns:
        List of relist dictonary entries, one for each availableplayer
    """
    data = read_parse(get_avail(period, position, stat, league, count))
    return relist(data[1][2:])

def one_team(period, league, team):
    """Get team statistics.

    Input:
        period: length of time stats are collected
        league: league number
        team: team number
    Returns:
        List of relist dictonary entries, one for each player on the team
    """
    data = read_parse(get_team(period, league, team))
    return relist(data[1][2:]), relist(data[2][2:])

def log_team(league, team):
    """Get team log (stats for a team).

    Input:
        league: league number
        team: team number
    Returns:
        Dictionary of player stats and a dictionary of pitcher stats
    """
    data = read_parse(get_team_log(league,team))
    return bstats(":".join(data[1][-1][2:])), pstats(":".join(data[2][-1][2:]))
