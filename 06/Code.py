# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 14:55:54 2016

@author: mlang
"""

def gen_a_command(self, address):
    """Returns the binary representation of the a-command for the given address
    """
    # 1. Convert the decimal address to a binary string representation
    # 2. Strip the "0b" prefix
    # 3. Retain the least-significan 15 bits
    # 4. Left-fill to 16 zeros
    return bin(address)[2:][-15:].zfill(16)

def gen_c_command(self, dest, comp, jump):
    pass

def _dest():
    pass

def _comp():
    pass

def _jump():
    pass
