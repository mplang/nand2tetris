# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 16:10:17 2016

@author: mlang
"""
import argparse, os.path
from glob import glob
from Parser import Parser
from CodeWriter import CodeWriter
from VmToken import VmToken

class VMtranslator(object):
    def __init__(self, source):
        self._set_inputs(source)
    
    def _set_inputs(self, source):
        self._file_list = None
        basename = None
        if os.path.isdir(source):
            basename = os.path.normpath(os.path.basename(source))
            self._file_list = glob(os.path.join(source, '*.vm'))
        else:
            basename, ext = os.path.splitext(source)
            if ext.lower() != ".vm":
                raise Exception("Invalid input file type!")
            self._file_list = [source]
        if basename != None:
            self._out_filename = "{}.asm".format(basename)
    
    def translate(self):
        if (self._file_list is None) or (len(self._file_list) == 0):
            raise Exception("No valid files to translate.")
        with CodeWriter(self._out_filename) as writer:
            for infile in self._file_list:
                p = Parser(infile)
                while p.has_more_commands():
                    p.advance()
                    if p.command_type == VmToken.ARITHMETIC:
                        writer.write_arithmetic(p.arg1)
                    elif p.command_type == VmToken.POP or p.command_type == VmToken.PUSH:
                        writer.write_push_pop(p.command_type, p.arg1, p.arg2)
                    else:
                        raise Exception('Unknown command type "{}".'.format(p.command_type))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="path to the file or files to translate")
    args = parser.parse_args()
    translator = VMtranslator(args.source)
    translator.translate()