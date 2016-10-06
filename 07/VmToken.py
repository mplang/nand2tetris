# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:26:24 2016

@author: mlang
"""

from enum import Enum, unique

@unique
class VmToken(Enum):
    """Enumeration of all valid VM IL tokens
    """
    IDENTIFIER = 1
    NUMBER = 2
    EOF = 3
    ERROR = 4