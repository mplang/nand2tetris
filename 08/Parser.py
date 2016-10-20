# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 14:27:59 2016

@author: mlang
"""
from Lexer import Lexer
from VmToken import VmToken

class Parser(object):
    def __init__(self, filename):
        self._lexer = Lexer(filename)   # Lexical analyzer instance
        self._lexer.analyze()           # Let the lexer do it's thing
        self._command_type = None       # The type of command we're parsing now
        self._arg1 = None               # The first arg of the current command
        self._arg2 = None               # The second arg of the current command
        self._token = None
        self._lexeme = None

        # VM IL command dispatch table
        # Commands can have an arity of 0, 1, or 2
        self._commands = {k:self._nullary for k 
                          in ('add', 'sub', 'neg', 'eq', 'gt', 'lt',
                              'and', 'or', 'not', 'return')}
        self._commands.update({k:self._unary for k 
                               in ('label', 'goto', 'if-goto')})
        self._commands.update({k:self._binary for k 
                               in ('push', 'pop', 'function', 'call')})

    def _get_next_token(self):
        """Populates the current token and lexeme with the next from the lexer
        """
        self._token, self._lexeme = self._lexer.get_next_token()

    def _peek_next_token(self):
        """Returns the next token without removing it from the input
        """
        return self._lexer.peek_next_token()

    def has_more_commands(self):
        """Returns True is there are more tokens in the input
        """
        return self._lexer.has_more_tokens()

    def _parse_command(self, func):
        """Simple helper method for the command dispatch table
        """
        func()

    def _nullary(self):
        self._command_type = self._token
        if self._command_type == VmToken.ARITHMETIC:
            self._arg1 = self._lexeme

    def _unary(self):
        self._command_type = self._token
        self._get_next_token()
        self._arg1 = self._lexeme

    def _binary(self):
        self._unary()
        self._get_next_token()
        self._arg2 = self._lexeme

    def advance(self):
        """Gets the next command
        """
        try:
            self._arg1 = None
            self._arg2 = None
            self._get_next_token()
            self._parse_command(self._commands[self._lexeme])
        except Exception as ex:
            self._command_type = VmToken.ERROR
            self._symbol = None
            print(str(ex))

    @property
    def command_type(self):
        """Returns the current command type as a VmToken
        """
        return self._command_type

    @property
    def arg1(self):
        """Returns the first argument of the current command, or the operator
           in the case of arithmetic commands
        """
        return self._arg1

    @property
    def arg2(self):
        """Returns the second argument of the current command
        """
        return self._arg2


if __name__ == "__main__":
    p = Parser("nand2tetris\07\StackArithmetic\SimpleAdd\SimpleAdd.vm")
    while p.has_more_commands():
        p.advance()
        print(p.command_type, p.arg1, p.arg2)