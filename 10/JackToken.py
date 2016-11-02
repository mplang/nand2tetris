# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 12:40:24 2016

@author: mlang
"""

from enum import Enum, unique

@unique
class JackToken(Enum):
    """Enumeration of all valid Jack tokens
    """
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5
    EOF = 6
    ERROR = 7
