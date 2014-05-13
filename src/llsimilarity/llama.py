"""
Created on May 9, 2014

@author: Warren Usui
"""
from HTMLParser import HTMLParser
from llsimilarity.utilities import get_url_info
from llsimilarity.utilities import get_ll_url


class Llama(object):
    """
    Container of a person's knowledge.
    """

    def __init__(self, name):
        """
        Given a llama id, find that person's question history
        and save correct answers and misses.
        """
        self.correct = []
        self.incorrect = []
        self.name = name
        self.url_head = "{}/profiles/qhist.php?".format(get_ll_url())
        self.my_qhist = ''.join([self.url_head, name])
        self.llama = get_url_info(self.my_qhist, LlamaParser())
        self.correct = self.llama.correct
        self.incorrect = self.llama.incorrect

    def get_know(self):
        """
        Return a list of question numbers that this llama got right.
        """
        return self.correct

    def get_dunno(self):
        """
        Return a list of question numbers that this llama missed.
        """
        return self.incorrect


# pylint: disable=R0904
class LlamaParser(HTMLParser, object):
    """
    Extract the person's data from the question history
    """
    def  __init__(self):
        self.last_q = ''
        self.look_for = '/question.php?'
        self.correct = []
        self.incorrect = []
        super(LlamaParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        """
        Scan for each question number.  After the question is found,
        the dot image indicates whether that question was missed or
        not.  Add the question to the appropriate list.
        """
        if tag == 'a':
            if attrs:
                if attrs[0][0] == 'href':
                    if attrs[0][1].startswith(self.look_for):
                        tmp = attrs[0][1]
                        self.last_q = tmp[len(self.look_for):]
        if tag == 'img':
            if attrs:
                if attrs[0][0] == 'src':
                    tmp = attrs[0][1]
                    if tmp.find('greendot.gif') > 0:
                        self.correct.append(self.last_q[:])
                    else:
                        self.incorrect.append(self.last_q[:])
