# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 14:27:59 2016

@author: mlang
"""
from Lexer import Lexer, Token
from HackToken import HackToken
from enum import Enum

class CommandType(Enum):
    """Enumeration of command types
    """
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3
    ERROR = 4

class Parser(object):
    def __init__(self, filename):
        self._lexer = Lexer(filename)   # Lexical analyzer instance
        self._lexer.analyze()           # Let the lexer do it's thing
        self._command_type = None       # The type of command we're parsing now
        self._symbol = None             # The current a- or l-command symbol
        self._dest = None               # The current c-command dest field
        self._comp = None               # The current c-command comp field
        self._jump = None               # The current c-command jump field

    @property
    def _next_token(self):
        return self._lexer.get_next_token()

    def _peek_next_token(self):
        return self._lexer.peek_next_token()

    def _parse_a_command(self):
        """Parses commands of the form @symbol or @number
        """
        token, lexeme = self._next_token
        if token == HackToken.IDENTIFIER or token == HackToken.NUMBER:
            self._command_type = CommandType.A_COMMAND
            self._symbol = lexeme
            # Consume and ignore the next token
            # Well, mostly ignore -- it's useful for error checking
            token, lexeme = self._next_token
            if token != HackToken.OP_RPAREN:
                raise Exception("Invalid input '{}'; expected ')'.".format(lexeme))
        else:
            raise Exception("Invalid input '{}'; expected ')'.".format(lexeme))

    def _parse_l_command(self):
        """Parses label commands of the form (symbol)
        """
        token, lexeme = self._next_token
        if token == HackToken.IDENTIFIER or token == HackToken.NUMBER:
            self._command_type = CommandType.L_COMMAND
            self._symbol = lexeme
        else:
            raise Exception("Invalid input '{}'; expected ')'.".format(lexeme))

    def _parse_dest(self, token, lexeme):
        """Sets the dest part of the c-command, if there is one
        """
        t, _ = self._peek_next_token()
        if t == HackToken.OP_ASSIGN:
            # This token is the dest; consume the '=' and return the next token
            self._next_token
            self._dest = lexeme
            return self._next_token
        else:
            # This is not the dest; return it back to the caller
            return Token(token, lexeme)
    
    def _parse_comp(self, token, lexeme):
        """Sets the comp part of the c-command; this is required
        """
        self._comp = lexeme
        if token == HackToken.OP_NOT or token == HackToken.OP_MINUS:
            # Unary not or negation
            _, l = self._next_token
            self._comp += l     # concatenate the two lexemes
        elif token == HackToken.NUMBER or token == HackToken.IDENTIFIER:
            t, l = self._peek_next_token()
            if t != HackToken.OP_SEMICOLON:
                # We've got a binary operator
                # Or, we hope we do
                # TODO: Add error checking here
                _, ll = self._next_token
                self._comp += ll
        else:
            raise Exception("Invalid input '{}'.".format(lexeme))

    def _parse_jump(self):
        """Sets the jump part of the c-command, if it exists
        """
        t, _ = self._next_token
        if t == HackToken.OP_SEMICOLON:
            # Found a semicolon; next token should be the jump value
            # TODO: Add error checking here
            _, l = self._next_token
            self._jump = l

    def _parse_c_command(self, token, lexeme):
        """Parses commands of the following forms:
            dest=comp;jump
            dest=comp
            comp;jump
            comp
        """
        self.command_type = CommandType.C_COMMAND
        comp_tok, comp_val = self._parse_dest(token, lexeme)
        self._parse_comp(comp_tok, comp_val)
        self._parse_jump()

    def has_more_commands(self):
        return self._lexer.has_more_tokens()

    def advance(self):
        try:
            token, lexeme = self._next_token
            if token == HackToken.OP_ADDR:
                self._parse_a_command()
            elif token == HackToken.OP_LPAREN:
                self._parse_l_command()
            else:
                self._parse_c_command(token, lexeme)
        except Exception as ex:
            self._command_type = CommandType.ERROR
            self._symbol = None
            print(str(ex))

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