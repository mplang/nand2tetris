# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:26:24 2016

@author: mlang
"""

from enum import Enum, unique

@unique
class VmToken(Enum):
    """Enumeration of all valid VM IL tokens;
       these tokens also serve as the VM CommandTypes
    """
    IDENTIFIER = 1
    NUMBER = 2
    ARITHMETIC = 3
    PUSH = 4
    POP = 5
    LABEL = 6
    GOTO = 7
    IF = 8
    FUNCTION = 9
    CALL = 10
    RETURN = 11
    EOF = 12
    ERROR = 13
