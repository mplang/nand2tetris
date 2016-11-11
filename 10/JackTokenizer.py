# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 12:40:24 2016

@author: mlang
"""
from collections import deque, namedtuple
from enum import Enum, unique
from JackToken import JackToken
from JackKeyword import JackKeyword

Token = namedtuple("Token", ["Token", "Lexeme"])

_symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';',
            '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

@unique
class CharacterClass(Enum):
    """Represents the general kinds of characters in the input
    """
    LETTER = 1
    DIGIT = 2
    WHITESPACE = 3
    MISC_CHAR = 4
    OTHER = 5
    EOF = 6

class JackTokenizer(object):
    """Lexical analyzer for the Jack Language
    """
    def __init__(self, filename):
        self.filename = filename
        self._iter = self._file_iter()
        self.next_char = None
        self._skip_line = False
        self.tokens = deque()

    def has_more_tokens(self):
        """Returns True if there are more tokens in the input
        """
        return (len(self.tokens) > 0
                and self.peek_next_token().Token != JackToken.EOF)

    def advance(self):
        """Returns the next token in the input
        """
        try:
            # Return the token at the front of the queue and add it back
            # to the end of the queue
            token = self.tokens.popleft()
            self.tokens.append(token)
            return token
        except:
            return None

    def peek_next_token(self):
        """Returns the next token in the input,
           but does not remove it from the queue
        """
        try:
            return self.tokens[0]
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
            if c.isalpha() or c == '_':
                self.char_class = CharacterClass.LETTER
            elif c.isdecimal():
                self.char_class = CharacterClass.DIGIT
            elif c.isspace():
                self.char_class = CharacterClass.WHITESPACE
            else:
                self.char_class = CharacterClass.OTHER
        except StopIteration:
            self.next_char = None
            self.char_class = CharacterClass.EOF

    def _get_non_blank(self):
        while self.char_class == CharacterClass.WHITESPACE:
            self._get_char()

    def _lookup_keyword(self, lexeme):
        """If a given lexeme is a valid keyword, return that keyword,
           else return None
       """
        for k in JackKeyword.__members__:
            if lexeme == k.lower():
                return JackKeyword[k]
        return None

    def _lex(self):
        self._get_non_blank()
        lexeme = self.next_char
        if self.char_class == CharacterClass.LETTER:
            # parse identifiers
            self._get_char()
            while (self.char_class == CharacterClass.LETTER
                   or self.char_class == CharacterClass.DIGIT):
                lexeme += self.next_char
                self._get_char()
            keyword = self._lookup_keyword(lexeme)
            if keyword:
                return Token(JackToken.KEYWORD, keyword)
            else:
                return Token(JackToken.IDENTIFIER, lexeme)
        elif self.char_class == CharacterClass.DIGIT:
            # parse integer literals
            self._get_char()
            while self.char_class == CharacterClass.DIGIT:
                lexeme += self.next_char
                self._get_char()
            return Token(JackToken.INT_CONST, lexeme)
        elif self.char_class == CharacterClass.OTHER:
            # TODO: Handle multi-line comments
            if self.next_char == '/':
                self._get_char()
                if self.next_char == '/':
                    # Single-line comment; Skip the rest of the line
                    self._skip_line = True
                    self._get_char()
                    return None
                elif self.next_char == '*':
                    # Multi-line comment
                    self._get_char()
                    in_comment = True
                    while in_comment:
                        while self.next_char != '*':
                            self._get_char()
                        self._get_char()
                        if self.next_char == '/':
                            in_comment = False
                    self._get_char()
                    return None
                else:
                    # Not a comment, just a regular forward slash
                    self._get_char()
                    return Token(JackToken.SYMBOL, '/')
            elif self.next_char == '"':
                # parse string literal
                lexeme = ""
                self._get_char()
                while self.next_char != '"':
                    lexeme += self.next_char
                    self._get_char()
                self._get_char()
                return Token(JackToken.STRING_CONST, lexeme)
            elif self.next_char in _symbols:
                self._get_char()
                return Token(JackToken.SYMBOL, lexeme)
            else:
                # There are no other valid characters
                return Token(JackToken.ERROR, lexeme)
        elif self.char_class == CharacterClass.EOF:
            return Token(JackToken.EOF, None)
        else:
            return Token(JackToken.ERROR, None)

    def display_symbols(self):
        for t in self.tokens:
            print("{}, {}".format(t.Token.name, t.Lexeme))

    def tokenize(self):
        """Begins the lexical analysis of the VM IL source file
        """
        self._get_char()
        while True:
            next_symbol = self._lex()
            if next_symbol is None:
                continue
            if next_symbol.Token == JackToken.ERROR:
                raise Exception("Bad token!", next_symbol.Lexeme)
            self.tokens.append(next_symbol)
            if next_symbol.Token == JackToken.EOF:
                break

if __name__ == "__main__":
    l = JackTokenizer(r"C:\Users\mlang\Desktop\programming\nand2tetris\09\Fraction\Fraction.jack")
    l.tokenize()
    l.display_symbols()
