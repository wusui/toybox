"""
Created on May 11, 2014

@author: Warren Usui
"""
from sys import argv
from getopt import getopt
from getopt import GetoptError
from operator import itemgetter
from llsimilarity.llama import Llama
from llsimilarity.llops import comp_with_rundle
from llsimilarity.rundle import get_rundle_list
from llsimilarity.rundle import get_rundle_players
from llsimilarity.report import html_report
from llsimilarity.report import ascii_report
from llsimilarity.utilities import make_tempdir


def rprint(info):
    """
    Callback used to print player name
    """
    print info


def rate_against_all_llamas(person):
    """
    Get a list of an individual's ratings vs. all active non-rookies.
    Prints out the Top 100. Takes forever to run.
    """
    my_alter_ego = Llama(person)
    rlist = get_rundle_list()
    answer = []
    for rund in rlist:
        print rund
        if rund.startswith('R'):
            continue
        vsme = comp_with_rundle(my_alter_ego, get_rundle_players(rund),
                                rprint)
        print vsme
        answer.extend(vsme)
    big_list = sorted(answer, key=itemgetter(1), reverse=True)[:100]
    ascii_report("top100.txt", big_list)
    print "See top100.txt for results"


def report_vs_rundle(player, rundle, callback=rprint):
    """
    Compare a player with a rundle, and generate a report that
    is displayed on a browser. The generated page is saved in
    the local data directory with the name <player>_vs_<rundle>.
    """
    rep_data = comp_with_rundle(Llama(player), get_rundle_players(rundle),
                                callback)
    title = '{} vs. Rundle {}'.format(player, rundle.replace('_', ' '))
    out_file = "{}_vs_{}".format(player, rundle)
    html_report(rep_data, title, out_file)


def cli_main(arguments):
    """
    Cli interface
    """
    name = 'usuiw'
    rundle = 'B_Pacific'
    vflag = False
    try:
        opts, _ = getopt(arguments, "vl:r:")
    except GetoptError:
        print 'cli.py [-v] [-l <user-name>] [-r <rundle>]'
        exit(2)
    for opt, arg in opts:
        if opt == '-l':
            name = arg
        if opt == '-r':
            rundle = arg
        if opt == '-v':
            vflag = True
    make_tempdir()
    if vflag:
        rate_against_all_llamas(name)
    else:
        report_vs_rundle(name, rundle)


if __name__ == "__main__":
    cli_main(argv[1:])
