"""
Handle Yahoo Fantasy Football related page displays.

The main entry point here is fantasy_football() in main.py

The config.cfg file should be all that needs to be changed to run this
for another league, and possibly for another year.

See temporary.html for sample output.

NON-PYTHON FILES USED:
    config.cfg -- Used to set league number, starting date of the season,
                  and my team name.  A season starts on the Tuesday before
                  the first game.
    header.html -- Head of html files used.  Contains CSS style
                   definitions used in the tables generated.

FILES CREATED:
    temporary.html -- Created for currently active week
    ../../data/fantasy/week##.html -- Created for each completed week
    ../../data/fantasy/diary.html -- Summary of all completed weeks.

GENERAL LAYOUT:
    urlutils.py -- reads the data from the URLs
    parseutils.py -- parses the information read by urlutils.py.
    infoutils.py -- uses parseutils.py and urlutils.py to collect data.
    htmlgen.py -- generates the html text to be displayed.
    tables.py -- uses htmlgen.py and infoutils.py to generate tables.
    main.py -- main routine used to call tables do some file writing.
    dateutils.py -- handles week number calculations.

NOTE TO SELF:
For 2014, my league is 133051, I found 920114 as another league to use
for testing.
"""
