#!/usr/bin/env python
from ConfigParser import RawConfigParser
from datetime import datetime
from read_parse import get_team_names

def initialize(ini_file):
    """Extract starting ini file information.

    Input: ini file name.
    Returns: dictionary with the following values:
        league: Yahoo league number
        team: our team number in the league
        start: integer day of the year for the start of the season
        end: integer day of the year for the end of the season
        today: today's day of the year

    The ini file passed should contain two sections, DATES and TEAM

    DATE fields:
        start: Date the season starts in dd mmm yyyy format
        end: Date the season ends in dd mmm yyyy format
    TEAM fields:
        league: league number
        name: name of the team that we are tracking

    The dates are converted into integer day of the year values.
    get_team_names is called to extract the team number
    """
    retv = {}
    config = RawConfigParser()
    config.read(ini_file)
    dinfo = config.items('DATES')
    dates = dict(dinfo)
    tinfo = config.items('TEAM')
    ini_data = dict(tinfo)
    retv['league'] = int(ini_data['league'])
    strt = datetime.strptime(dates['start'], '%d %b %Y')
    retv['start'] = strt.timetuple().tm_yday
    endd = datetime.strptime(dates['end'], '%d %b %Y')
    retv['end'] = endd.timetuple().tm_yday
    #tm_html_data = get_team_names(retv['league'])[ini_data['name']]
    #retv['team'] = int(tm_html_data.split('/')[-1])
    retv['team'] = get_team_names(retv['league'])[ini_data['name']]
    retv['today'] = datetime.now().timetuple().tm_yday
    retv['totalg'] = retv['end'] - retv['start']
    retv['sofar'] = retv['today'] - retv['start']
    retv['daysleft'] = retv['end'] - retv['today']
    return retv
