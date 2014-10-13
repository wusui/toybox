"""
Utilities -- read the configuration, do url reads, general http parser.
"""
import ConfigParser
from datetime import datetime
import urllib2
from contextlib import closing

DAYS_IN_WEEK = 7
COMMON_URL = 'http://football.fantasysports.yahoo.com/f1/%s%s'
MY_BEST_TEAM = (11, 'My Best Team')
BEST_FREE_AGENTS = (12, 'Best Free Agents')

def get_configuration(config_file, config_section):
    """
    Read configuration information

    Input:
        config_file -- Name of the cfg file.
        config_section --Section in config_file we are extracting data from

    return a dictionary containing:
            league (string)
            current_week (int)
            my_team (string)
            year (int)
    """
    conf = ConfigParser.RawConfigParser()
    conf.read(config_file)
    conf_data = dict(conf.items(config_section))
    date_data = datetime.strptime(conf_data['start_of_season'], '%m-%d-%Y')
    first_day = date_data.timetuple().tm_yday
    val = datetime.now().timetuple().tm_yday - first_day
    conf_data['current_week'] = val / DAYS_IN_WEEK + 1
    conf_data['year'] = date_data.year
    return conf_data


def read_url(league, in_url):
    """
    Read a url.

    Input:
        league -- league name
        in_url -- full name of the http entry to read.

    Returns the text read in utf-8 format.
    """
    real_url = COMMON_URL % (league, in_url)
    with closing(urllib2.urlopen(real_url)) as page:
        data = page.read()
    return unicode(data, 'utf-8')


def parse_url(league, in_url, parser):
    """
    Parse a url.

    Input:
        league -- league name
        in_url -- full name of the http entry to read.
        parser -- parser object.  See parsers.py for examples.

    Returns data extracted from the webpage.  The parser results are set
    by the individual parsers.
    """
    in_data = read_url(league, in_url)
    in_data = in_data.replace(u'&#8211;', u'-')
    parser.feed(in_data)
    return parser.results
