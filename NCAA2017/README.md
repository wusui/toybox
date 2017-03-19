2017 March Madness Tracker
==========================

Introduction
------------
This directory contains the code necessary to create the NCAA tournament tracking pages linked to from the 'Mad as a March Aardvark' page for 2017.  All instructions in this guide will assume that you are in the same directory where you downloaded the source.

Definitions
-----------
* a bracket is an indvidual ladder grid filled out by an entrant.  Entry can be used as a synonym for bracket.
* a group is an ESPN defined set of brackets that are competing against each other.  In this document, the following words may be used as synonyms for group: pool, league, rundle

Set-up
------
Due to the nature of how EPSN groups and bracket information is saved, I was unable to extract the data from the web pages for which they are displayed.  In order to follow an ESPN group, the following files need to be created:
* a directory named data
* a directory with the name of the pool in data (data/XXX for the XXX pool)
* data/XXX/groupno.txt -- a file containing the corresponding EPSN group number for the group (go to the webpage for the group, and look at the number after "group?groupID=" text in the address field
* data/XXX/peeps.txt -- a line by line list of entrant names.  This is listed in the bracket column for the results on the group's web page.
* data/XXX/numbs.txt -- the bracket number corresponding to each entrant name.  This can be extracted from the bracket name by placing the cursor over the bracket name and looking at the text that the browser displays.  The text contains a link to an entry page and the bracket number is the number following the "entry?entryID=" text in the address field

There must be a one to one correspondence between each line in the numbs.txt file and the peeps.txt file.  In other words, the first number in numbs.txt must be the entry number that corresponds to the first name in peeps.txt, and the thirty-seventh number in numbs.txt must be the entry number that corresponds to the thrity-seventh name in peeps.txt.  Run 'python check_data.py' to look for errors.

Multiple ESPN groups can be added to the data directory, and the scripts here should be able to handle them.  If a group name contains blanks, use underscore (_) characters in the directory name to indicate blanks.  If you want to have group directory not be checked or used by these scripts, make sure that there is no groupno.txt file in that directory.

If you are running this script for the Sweet Sixteen`, create a directory named sweet16.  If you are running this script for the Elite Eight, create a directory named elite8. If you are running this script for the Final Four, create a  directory named Final4.

Running the code / Creating the pages
-------------------------------------
'python get_picks.py' can be run to collect pick data into the data/XXX/picks.json file.  This contains each bracket's picks and player name.  Once run for an ESPN group, this script need not be run again.

'python computencaa.py' should be run to collect data for all possible future combinations of wins and losses.  It first creates a file named reality.json in data if that file does not exist.  It contains the information from the previous tournament games.  If you do not want to collect this data and use another source, put that file data into data/reality.json.  Delete data/reality.json and run this script if you want to collect the latest data.  This should only be done during the period of time between rounds.

The 'python computencaa.py' run also creates two files in the directory for this ESPN group.  One file, scores.txt, tabulates the teams scores so far.  This can be compared with the scores listed on the website for double checking purposes. The second file, results.json, contains lists of all possible outcomes for all future scenarios for all brackets.

'python gen_tables.py' can then be run create the pages.

