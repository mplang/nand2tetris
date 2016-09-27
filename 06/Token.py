from enum import Enum

class Token(Enum):
    """Provides Token values for the Hack assembly language
    """
    IDENTIFIER = 1
    NUMBER = 2
    OPERATOR = 3
    ERROR = 4
    EOF = 5
