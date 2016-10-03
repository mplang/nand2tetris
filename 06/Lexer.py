# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:26:01 2016

@author: mlang
"""

from enum import Enum
from collections import deque, namedtuple
from HackToken import HackToken

Symbol = namedtuple("Symbol", ["Token", "Lexeme"])

class CharacterClass(Enum):
    """Represents the general kinds of characters in the input
    """
    LETTER = 1
    DIGIT = 2
    WHITESPACE = 3
    MISC_CHAR = 4
    OTHER = 5
    EOF = 6

class Lexer(object):
    """Lexical analyzer for the Hack assembly language
    """
    def __init__(self, filename):
        self.filename = filename
        self._iter = self._file_iter()
        self.next_char = None
        self.char_class = CharacterClass.EOF
        self._skip_line = False
        self.symbols = deque()

    def has_more_symbols(self):
        """Returns True if there are more symbols in the input
        """
        return len(self.symbols) > 0

    def get_next_symbol(self):
        """Returns the next symbol in the input, None if no symbols left
        """
        try:
            return self.symbols.popleft()
        except:
            return None

    def _file_iter(self):
        """Generator function to yield one character at a time from the input
        """
        with open(self.filename, 'r') as f:
            for line in f:
                for char in line:
                    if self._skip_line:
                        break
                    yield char
                self._skip_line = False

    def _get_char(self):
        try:
            c = next(self._iter)
            self.next_char = c
            if c.isalpha():
                self.char_class = CharacterClass.LETTER
            elif c.isdecimal():
                self.char_class = CharacterClass.DIGIT
            elif c.isspace():
                self.char_class = CharacterClass.WHITESPACE
            elif c in ['_', '.', '$', ':']:
                self.char_class = CharacterClass.MISC_CHAR
            else:
                self.char_class = CharacterClass.OTHER
        except StopIteration:
            self.next_char = None
            self.char_class = CharacterClass.EOF

    def _get_non_blank(self):
        while self.char_class == CharacterClass.WHITESPACE:
            self._get_char()

    def _lex(self):
        self._get_non_blank()
        lexeme = self.next_char
        if (self.char_class == CharacterClass.LETTER
            or self.char_class == CharacterClass.MISC_CHAR):
            # parse identifiers
            self._get_char()
            while (self.char_class == CharacterClass.LETTER
                   or self.char_class == CharacterClass.DIGIT
                   or self.char_class == CharacterClass.MISC_CHAR):
                lexeme += self.next_char
                self._get_char()
            return Symbol(HackToken.IDENTIFIER, lexeme)
        elif self.char_class == CharacterClass.DIGIT:
            # parse integer literals
            self._get_char()
            while self.char_class == CharacterClass.DIGIT:
                lexeme += self.next_char
                self._get_char()
            return Symbol(HackToken.NUMBER, lexeme)
        elif self.char_class == CharacterClass.OTHER:
            # parse operators and comments
            if self.next_char == '/':
                # We should be reading a comment
                self._get_char()
                if self.next_char == '/':
                    # We found a comment! Skip the rest of the line
                    self._skip_line = True
                    self._get_char()
                    return None
                else:
                    # Not a comment; a single forward slash is invalid
                    return Symbol(HackToken.ERROR, lexeme)
            else:
                self._get_char()
                return Symbol(self._get_oper_token(lexeme), lexeme)
        elif self.char_class == CharacterClass.EOF:
            return Symbol(HackToken.EOF, None)
        else:
            return Symbol(HackToken.ERROR, None)

    def _get_oper_token(self, lexeme):
        if lexeme == '(':
            return HackToken.OP_LPAREN
        elif lexeme == ')':
            return HackToken.OP_RPAREN
        elif lexeme == '@':
            return HackToken.OP_ADDR
        elif lexeme == '=':
            return HackToken.OP_ASSIGN
        elif lexeme == '+':
            return HackToken.OP_PLUS
        elif lexeme == '-':
            return HackToken.OP_MINUS
        elif lexeme == '!':
            return HackToken.OP_NOT
        elif lexeme == '&':
            return HackToken.OP_AND
        elif lexeme == '|':
            return HackToken.OP_OR
        elif lexeme == ';':
            return HackToken.OP_SEMICOLON
        else:
            return HackToken.ERROR

    def display_symbols(self):
        for s in self.symbols:
            print("{}, {}".format(s.Token.name, s.Lexeme))

    def analyze(self):
        """Begins the lexical analysis of the Hack assembly source file
        """
        self._get_char()
        while True:
            next_symbol = self._lex()
            if next_symbol is None:
                continue
            if next_symbol.Token == HackToken.ERROR:
                raise Exception("Bad token!", next_symbol.Lexeme)
            self.symbols.append(next_symbol)
            if next_symbol.Token == HackToken.EOF:
                break

if __name__ == "__main__":
    l = Lexer('Pong.asm')
    l.analyze()
    l.display_symbols()
