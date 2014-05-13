"""
Created on May 9, 2014

@author: Warren Usui
"""
import os
import inspect
import contextlib
import urllib2


def get_tempdir():
    """
    Returns a path to the directory/folder where we will store temporary data.
    """
    src_file = inspect.getfile(get_tempdir)
    src_dir = src_file[0:len(src_file) - len('utilities.py')]
    path_data = os.path.join(src_dir, 'data')
    return path_data


def make_tempdir():
    """
    Make sure that data directory exists
    """
    fname = get_tempdir()
    if not os.path.isdir(fname):
        os.mkdir(fname)


def get_url_info(http_page, parser):
    """
    Run the parser specified on the http data specified.

    input: http_page -- page to be parsed
    input: parser -- HTMLParser object (League or Llama)

    returns: parsed information
    """
    with contextlib.closing(urllib2.urlopen(
            urllib2.Request(http_page))) as response:
        parser.feed(response.read())
    return parser


def get_ll_url():
    """
    Get root of all urls scanned.
    """
    return "http://www.learnedleague.com"
