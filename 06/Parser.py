# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 14:27:59 2016

@author: mlang
"""
from Lexer import Lexer
from HackToken import HackToken
from enum import Enum

class CommandTypes(Enum):
    """Enumeration of command types
    """
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3

class Parser(object):
    def __init__(self, filename):
        self._lexer = Lexer(filename)
        self._lexer.analyze()
        self._command_type = None
        self._symbol = None
    
    def _parse_a_command(self):
        token, lexeme = self._lexer.get_next_symbol()
        if token == HackToken.IDENTIFIER or token == HackToken.NUMBER:
            self._command_type = CommandTypes.A_COMMAND
            self._symbol = lexeme
        else:
            raise Exception("Error!")

    def has_more_commands(self):
        return self._lexer.has_more_symbols()

    def advance(self):
        token, lexeme = self._lexer.get_next_symbol()
        if token == HackToken.OPERATOR:
            if lexeme == "@":
                self._parse_a_command()
            elif lexeme == "(":
                self._command_type = CommandTypes.L_COMMAND
            else:
                raise Exception("Error!")
        else:
            self._command_type = CommandTypes.C_COMMAND

    @property
    def command_type(self):
        return self._command_type

    @property
    def symbol(self):
        return self._symbol

    def dest(self):
        pass

    def comp(self):
        pass

    def jump(self):
        pass

if __name__ == "__main__":
    p = Parser("Pong.asm")
    while p.has_more_commands():
        p.advance()
        print(p._next_command)