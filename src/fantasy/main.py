"""
Fantasy football data collector

The behavior of of this program depends on when it runs.
If there are active games or completed games this week
that were played by members of my team or this week's
opponent's team, then the statistics for the current week
are accumulated and displayed on a browser.  If not,
then last week's statistics are accumulated in a week##.html
file in the data directory, and a new diary.html
file is generated.

Since there is a game on Monday night, weeks start on
Tuesday.
"""
import os
from fantasy.tables import generate_tables
from fantasy.dateutils import get_current_week
from fantasy.htmlgen import wrapper

WEEK_XX = 'week%02d.html'

def fantasy_football():
    """
    Generate the path for last week.  Then generate the tables.
    If last week's data ends up getting collected, write out a new
    diary file based on all the saved week data.  
    """
    src_file = os.path.realpath(__file__)
    path_data = os.path.join(src_file, '..', '..', '..', 'data', 'fantasy')
    pth = os.path.normpath(path_data)
    lastweek = get_current_week() - 1
    week_file = WEEK_XX % lastweek
    ofile = os.path.join(pth, week_file)
    last_week = generate_tables(ofile)
    if last_week:
        wpages = []
        for week in range(1, get_current_week()):
            tweek = WEEK_XX % week
            dfile = os.path.join(pth, tweek)
            if not os.path.isfile(dfile):
                break
            with open(dfile, 'r') as fdesc:
                wdata = fdesc.read()
                wpages.append(wdata)
        bdata = '\n'.join(wpages)
        bdata = wrapper(bdata, "Yahoo Fantasy Football")
        fpath = os.path.join(pth, 'diary.html')
        with open(fpath, 'w') as fdesc:
            fdesc.write(bdata)

if __name__ == '__main__':
    fantasy_football()
