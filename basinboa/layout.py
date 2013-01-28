#!/usr/bin/env python
"""
message layout.
"""

def align_right(client, msg_right, msg_left=None):
    """docstring for align_right"""
    msg_left = '' if not msg_left else msg_left
    columns = client.columns
    space = ' ' * (columns - len(str(msg_left)) - len(str(msg_right))) 
    return "%s%s%s" % (msg_left, space, msg_right)

