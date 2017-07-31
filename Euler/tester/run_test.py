#!/usr/bin/python
"""
Copyright (C) 2017  Warren Usui (warrenusui@eartlink.net)
Licensed under the GPL 3 license.

Project Euler tester
"""
from os import listdir
from os.path import sep as separator
from sys import path as spath
from datetime import datetime
from subprocess import Popen
from subprocess import PIPE
import logging

def main_rtn():
    """
    Run all the problems in the real_location directory.  Lint them and pep8
    check them.  Compare results with the values listed in the prob_sol_file file.
    """
    log_file = "test_results.log"
    prob_sol_file = 'testdata.txt'
    real_location = '..%sDone' % separator
    problem_solution = {}
    real_modules = []

    def get_programs(directory):
        """
        Find all the python modules in the directory being checked
        """
        flist = listdir(directory)
        for fname in flist:
            if fname.endswith('.py'):
                real_modules.append(fname)

    def init():
        """
        Setup logging.  Get the information in the prob_sol_file file.
        """
        logging.basicConfig(filename=log_file, level=logging.DEBUG)
        spath.insert(0, real_location)
        get_programs(real_location)
        with open(prob_sol_file, 'r') as file1:
            records = file1.readlines()
        for entry in records:
            pair = entry.split(":")
            try:
                pindx = "problem%s.py" % pair[0]
                problem_solution[pindx] = pair[1].strip()
            except IndexError:
                logging.error('entry %s in %s is invalid', entry, real_location)
        for filen in problem_solution:
            if not filen in real_modules:
                logging.error('%s does not exist', filen)

    def run_check(filen, command):
        """
        Run the command on the file specified (either pylint or pep8).
        Collect error messages in message string.
        """
        pipe_d = Popen([command, filen], stdout=PIPE)
        message = pipe_d.communicate()[0]
        dashloc = message.find('---')
        if dashloc > 0:
            message = message[0:dashloc]
        if message.strip():
            logging.error("While running %s on %s:\n%s", command, filen, message)

    init()
    for pfile in real_modules:
        print pfile
        logging.info('Chceking %s', pfile)
        path_pfile = "%s%s%s" % (real_location, separator, pfile)
        run_check(path_pfile, 'pylint')
        run_check(path_pfile, 'pep8')
        module = __import__(pfile[:-3])
        start = datetime.now()
        test_value = getattr(module, pfile[:-3])()
        elapsed = datetime.now() - start
        if elapsed.total_seconds() >= 60.0:
            logging.error("%s ran in %s seconds", pfile, elapsed.total_seconds())
        if not pfile in problem_solution.keys():
            logging.error('%s is not being tested', pfile)
        else:
            if problem_solution[pfile] != str(test_value):
                logging.error('%s returns an invalid solution')
    logging.info('DONE')

if __name__ == "__main__":
    main_rtn()
