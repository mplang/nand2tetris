# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 12:40:24 2016

@author: mlang
"""

from enum import Enum, unique

@unique
class JackKeyword(Enum):
    """Enumeration of all valid Jack keywords
    """
    CLASS = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    INT = 5
    BOOLEAN = 6
    CHAR = 7
    VOID = 8
    VAR = 9
    STATIC = 10
    FIELD = 11
    LET = 12
    DO = 13
    IF = 14
    ELSE = 15
    WHILE = 16
    RETURN = 17
    TRUE = 18
    FALSE = 19
    NULL = 20
    THIS = 21
