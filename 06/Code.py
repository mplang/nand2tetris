# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 14:55:54 2016

@author: mlang
"""
from enum import IntEnum, unique

@unique
class Dest(IntEnum):
    null = 0
    M = 1
    D = 2
    MD = 3
    A = 4
    AM = 5
    AD = 6
    AMD = 7

@unique
class Jump(IntEnum):
    null = 0
    JGT = 1
    JEQ = 2
    JGE = 3
    JLT = 4
    JNE = 5
    JLE = 6
    JMP = 7

# Decimal representation of comp values
comp_table = {"0": 42, "1": 63, "-1": 58,
              "D": 12, "A": 48, "!D": 13, "!A": 49, "-D": 15, "-A": 51,
              "D+1": 31, "A+1": 55, "D-1": 14, "A-1": 50,
              "D+A": 2, "D-A": 19, "A-D": 7, "D&A": 0, "D|A": 21,
              "M": 112, "!M": 77, "-M": 115,
              "M+1": 119, "M-1": 114,
              "D+M": 66, "D-M": 83, "M-D": 71,
              "D&M": 64, "D|M": 85}

def _get_bin(address, fill=0):
    """Converts the decimal address to a binary string representation,
        strips the "0b" prefix, and left-pads with the specified number of '0's
    """
    return bin(address)[2:].zfill(fill)

def gen_a_command(address):
    """Returns the binary representation of the a-command for the given address
    """
    # Retain the least-significan 15 bits and left-fill to 16 zeros
    return _get_bin(address)[-15:].zfill(16)

def gen_c_command(dest, comp, jump):
    return "111{}{}{}".format(_comp(comp), _dest(dest), _jump(jump))

def _dest(dest):
    return _get_bin(Dest[dest], 3)

def _comp(comp):
    return _get_bin(comp_table[comp], 7)

def _jump(jump):
    return _get_bin(Jump[jump], 3)
