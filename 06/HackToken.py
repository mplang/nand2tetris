# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:26:24 2016

@author: mlang
"""

from enum import Enum, unique

@unique
class HackToken(Enum):
    """Enumeration of all valid Hack assembly language tokens
    """
    IDENTIFIER = 1
    NUMBER = 2
    OP_LPAREN = 3
    OP_RPAREN = 4
    OP_ADDR = 5
    OP_ASSIGN = 6
    OP_PLUS = 7
    OP_MINUS = 8
    OP_NOT = 9
    OP_AND = 10
    OP_OR = 11
    OP_SEMICOLON = 12
    EOF = 13
    ERROR = 14