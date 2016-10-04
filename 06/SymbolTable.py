# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 14:55:11 2016

@author: mlang
"""

class SymbolTable(object):
    """A symbol table that keeps a correspondence between symbolic labels
       and numeric addresses
    """
    _symbol_table = {'R0':0, 'R1':1, 'R2':2, 'R3':3,
                     'R4':4, 'R5':5, 'R6':6, 'R7':7,
                     'R8':8, 'R9':9, 'R10':10, 'R11':11,
                     'R12':12, 'R13':13, 'R14':14, 'R15':15,
                     'SCREEN':16384, 'KBD':24576,
                     'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4}

    def add_entry(self, symbol, address):
        """Adds or updates the symbol in the table
        """
        self._symbol_table[symbol] = address

    def contains(self, symbol):
        """Returns True if the given symbol exists in the symbol table
        """
        # This method is more-or-less unnecessary, but it conforms to the
        # documented API
        return symbol in self._symbol_table

    def get_address(self, symbol):
        """Returns the address of the given symbol, or None if not found
        """
        return self._symbol_table.get(symbol, None)