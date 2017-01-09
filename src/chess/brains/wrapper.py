#!/usr/bin/python
#    Copyright (C) 2017 Warren Usui (warrenusui@eartlink.net)
#    Licensed under the GPL 3 license.
from board import board

def solver_filter(in_data, pfunc):
    """
    Generate a board from in_data. Send an error message if appropriate
    """
    cboard = board(in_data, pfunc)
    if len(cboard.msg_type) > 0:
        return make_emesg(cboard)
    cboard.pfunc('Sample use of pfunc (not permanent)')
    # TO DO: add check check here
    return "ATTENTION|Chess solver not yet implemented|120|360"

def make_emesg(cboard):
    """
    Format the text of the error message in cboard
    """
    lilen = len(cboard.error_list) * 30 + 90
    limax = 0
    for msg in cboard.error_list:
        if len(msg) > limax:
            limax = len(msg)
    limax = limax * 12 + 60
    internal_list = "</li><li>".join(cboard.error_list)
    bmsg = "<ul><li>%s</li></ul>" % internal_list
    return "|".join([cboard.msg_type, bmsg, "%d" % lilen, "%d" % limax])
