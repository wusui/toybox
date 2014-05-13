"""
Created on May 10, 2014

@author: Warren Usui
"""
from operator import itemgetter
from llsimilarity.llama import Llama


class CompareLlamas(object):
    """
    Compare two llamas
    """

    def __init__(self, llama1, llama2):
        self.match = 0
        self.nomatch = 0
        for qind in llama1.get_know():
            if qind in llama2.get_know():
                self.match += 1
            if qind in llama2.get_dunno():
                self.nomatch += 1
        for qind in llama1.get_dunno():
            if qind in llama2.get_dunno():
                self.match += 1
            if qind in llama2.get_know():
                self.nomatch += 1
        self.total = self.match + self.nomatch
        if self.total == 0:
            self.total = 1

    def get_ratio(self):
        """
        Return the similarity ratio as a real number.
        """
        return (self.match + 0.0) / self.total

    def get_display_ratio(self):
        """
        Return the similarity ratio as a display-able string.
        """
        if self.match > 0:
            if self.nomatch == 0:
                return '1.0000'
        mval = self.match * 100000
        result = int(mval / self.total)
        result += 5
        result = int(result / 10)
        answer = "0.{0:04d}".format(result)
        return answer


def comp_two_players(player1, player2):
    """
    Compare the two players whose names are passed as parameters.
    Return a string representation of the similarity ratio.
    """
    return CompareLlamas(Llama(player1), Llama(player2)).get_display_ratio()


def comp_with_rundle(player, rundle_list, call_back):
    """
    Compare the player with all players in the rundle.  Returns a list of
    tuples, where each tuple contains the name of a player in the rundle and
    that player's similarity ratio.  The list is sorted from highest ratio to
    lowest.
    """
    result = {}
    for opp in rundle_list:
        if opp == player.name:
            continue
        call_back(opp)
        res = CompareLlamas(player, Llama(opp))
        rating = res.get_display_ratio()
        result[opp] = rating
    return sorted(result.items(), key=itemgetter(1), reverse=True)
