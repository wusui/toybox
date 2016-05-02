def get_pool(period, pos, league):
    """Get available players (as dictionary keys)

    Input:
        period: length of time, in days or year number (7, 14, 30, 2016)
        pos: position of the players being found
        league: league number

    Returns:
        A dictionary whose values are a players stats.  The keys are a
        colon separated string consisting of the player's name, the player's
        team, and a comma separated list of positions played.
    """
    pool = {}
    statlist = B_STATS
    if pos.endswith('P'):
        statlist = P_STATS
    for stat in statlist:
        for count in range(0,4):
            data = available(period, pos, stat, league, count)
            for plr in data:
                key = ":".join([plr['name'], plr['team'], plr['pos']])
                pool[key] = plr['stats']
    return pool
