"""
Created on May 10, 2014

@author: Warren Usui
"""
import unittest
from llsimilarity.league import get_league_number
from llsimilarity.llama import Llama
from llsimilarity.rundle import get_rundle_players
from llsimilarity.rundle import get_rundle_list
from llsimilarity.llops import CompareLlamas
from llsimilarity.llops import comp_with_rundle
from llsimilarity.llops import comp_two_players
from llsimilarity.cli import report_vs_rundle
from llsimilarity.cli import rprint
from llsimilarity.utilities import make_tempdir


# pylint: disable=R0904
class Test(unittest.TestCase):
    """
    Unit-tester.  This code runs as an Eclipse unit-test program.
    """

    # pylint: disable=W0201
    def testllama(self):
        """
        Test league number code and test Llama initialization code
        """
        make_tempdir()
        self.tmp = get_league_number()
        assert self.tmp == '61', 'Bad league number'
        llama = Llama('veredj')
        print llama.correct
        print llama.incorrect
        assert len(llama.correct) >= 0, 'got negative number correct'

    def test2llamas(self):
        """
        Test llama comparison code
        """
        self.comp = CompareLlamas(Llama('usuiw'), Llama('foderab'))
        print self.comp.match
        print self.comp.nomatch
        print self.comp.get_ratio()
        print self.comp.get_display_ratio()
        print comp_two_players('usuiw', 'veredj')
        assert self.comp.match >= 0, 'do not match on some number'

    def testrundle(self):
        """
        Test rundle generation code and rundle comparison code
        """
        self.rundle = get_rundle_players('B_Pacific')
        print self.rundle
        assert len(self.rundle) > 0, 'rundle missing players'
        print comp_with_rundle(Llama('usuiw'), self.rundle, rprint)

    def testrundlelist(self):
        """
        test get_rundle_list and report_vs_rundle
        """
        self.dummy = 0
        print get_rundle_list()
        report_vs_rundle('usuiw', 'B_Pacific')


if __name__ == "__main__":
    import sys
    sys.argv = ['', 'Test.testName']
    unittest.main()
