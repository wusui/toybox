"""
Handle all the date related stuff.

get_current_week is the externally called routine in this file.
It returns the current week number.

config.cfg is read to initialize the starting date (which is used
to derive the current week number).
"""
from datetime import datetime
from datetime import timedelta
import ConfigParser

CONFIG = ConfigParser.RawConfigParser()
CONFIG.read('config.cfg')

CONF_DATA = CONFIG.get('YahooFootball', 'start_of_season')
DATE_DATA = datetime.strptime(CONF_DATA, '%m-%d-%Y')
START_OF_SEASON = DATE_DATA.timetuple().tm_yday
THIS_SEASON = DATE_DATA.year
SEASON_LENGTH = 16
DAYS_IN_WEEK = 7

def _get_week_given_date(in_date):
    """
    Given the date (in datetime format) return the NFL week number.
    """
    val = in_date.timetuple().tm_yday - START_OF_SEASON
    if val < 0:
        return 0
    return val / DAYS_IN_WEEK + 1


def get_current_week():
    """
    Return: The current week number during the fantasy season
            (this value is in the range of 1 to 16).
    """
    return _get_week_given_date(datetime.now())


def unit_test():
    """
    Unit tester for _get_week_given_date.
    Test boundary conditions around the first day of the season,
    and then make sure that all weeks thereafter are numbered
    in order and all have seven days in them.
    """
    assert _get_week_given_date(DATE_DATA) == 1
    yesterday = DATE_DATA - timedelta(1)
    assert _get_week_given_date(yesterday) == 0
    assert DATE_DATA.strftime("%A") == 'Tuesday'
    test_buffer = []
    for day in range(1, 367):
        day_str = "%d %03d" % (THIS_SEASON, day)
        day_of_year = datetime.strptime(day_str, "%Y %j")
        week = _get_week_given_date(day_of_year)
        if week > SEASON_LENGTH:
            break
        test_buffer.append(week)
    hist = {}
    prev = -1
    for tst in test_buffer:
        assert tst >= prev
        prev = tst
        if tst in hist:
            hist[tst] += 1
        else:
            hist[tst] = 1
    for week in range(1, SEASON_LENGTH + 1):
        assert hist[week] == 7


if __name__ == '__main__':
    unit_test()
