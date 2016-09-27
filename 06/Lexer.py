from collections import deque
from enum import Enum
import Token

class Lexer(object):
    """Lexical analyzer for the hack assembly language
    """
    class CharClass(Enum):
        LETTER = 1
        DIGIT = 2
        OTHER = 3
        EOF = 4

    def __init__(self, filename):
        self.filename = filename
        self.lexeme = []
        self.tokens = deque()
        self.next_char = None
        self.char_class = self.CharClass.EOF

    def analyze(self):
        self._get_char()
        while True:
            self._lex()
            if self.next_token == Token.EOF:
                break

    def _get_char(self):
        with open(self.filename, 'r') as f:
            for line in f:
                for c in line:
                    self.next_char = c
                    if c.isalpha():
                        self.char_class = self.CharClass.LETTER
                    elif c.isdecimal():
                        self.char_class = self.CharClass.DIGIT
                    else:
                        self.char_class = self.CharClass.OTHER
                    yield
            self.char_class = self.CharClass.EOF
            yield

    def _get_non_whitespace(self):
        while self.next_char.isspace():
            self._get_char()

    def _lex(self):
        self._get_non_whitespace()
        if self.char_class == self.CharClass.LETTER:
            print("LETTER")
        elif self.char_class == self.CharClass.DIGIT:
            print("DIGIT")
        elif self.char_class == self.CharClass.OTHER:
            print("OTHER")
        elif self.char_class == self.CharClass.EOF:
            print("EOF")
        else:
            print(self.char_class)
