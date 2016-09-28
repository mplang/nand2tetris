# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:26:24 2016

@author: mlang
"""

from enum import Enum


class HackToken(Enum):
    """Enumeration of all valid Hack assembly language tokens
    """
    IDENTIFIER = 1
    NUMBER = 2
    OPERATOR = 3
    EOF = 4
    ERROR = 5