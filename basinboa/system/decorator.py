#!/usr/bin/env python
"""
decorator.
"""

def command(func):
    """docstring for is_command"""
    func.is_command = True
    return func
