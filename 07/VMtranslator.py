# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 16:10:17 2016

@author: mlang
"""
from Parser import Parser
from CodeWriter import CodeWriter
from VmToken import VmToken

class VMtranslator(object):
    def __init__(self, infile):
        self._infile = infile
        self._writer = CodeWriter(infile)
    
    def translate(self):
        p = Parser(self._infile)
        while p.has_more_commands():
            p.advance()
            if p.command_type == VmToken.ARITHMETIC:
                self._writer.write_arithmetic(p.arg1)
            elif p.command_type == VmToken.POP or p.command_type == VmToken.PUSH:
                self._writer.write_push_pop(p.command_type, p.arg1, p.arg2)
            else:
                raise Exception('Unknown command type "{}".'.format(p.command_type))

if __name__ == "__main__":
    translator = VMtranslator(r"C:\Users\mlang\Desktop\programming\nand2tetris\07\StackArithmetic\SimpleAdd\SimpleSub.vm")
    translator.translate()