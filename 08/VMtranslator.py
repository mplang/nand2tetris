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
        source = os.path.normpath(source)
        self._file_list = None
        basename = None
        dirname = None
        if os.path.isdir(source):
            dirname = source
            basename = os.path.basename(dirname)
            self._file_list = glob(os.path.join(dirname, '*.vm'))
        else:
            basename, ext = os.path.splitext(source)
            if ext.lower() != ".vm":
                raise Exception("Invalid input file type!")
            self._file_list = [source]
            dirname = os.path.dirname(source)
        if basename != None:
            self._out_filename = os.path.join(dirname, "{}.asm".format(basename))
    
    def translate(self):
        print("Starting translation...")
        if (self._file_list is None) or (len(self._file_list) == 0):
            raise Exception("No valid files to translate.")
        with CodeWriter(self._out_filename) as writer:
            writer.write_init()
            for infile in self._file_list:
                print("Processing file '{}' ...".format(infile))
                p = Parser(infile)
                while p.has_more_commands():
                    p.advance()
                    if p.command_type == VmToken.ARITHMETIC:
                        writer.write_arithmetic(p.arg1)
                    elif p.command_type == VmToken.POP or p.command_type == VmToken.PUSH:
                        writer.write_push_pop(p.command_type, p.arg1, p.arg2)
                    elif p.command_type == VmToken.LABEL:
                        writer.write_label(p.arg1)
                    elif p.command_type == VmToken.IF:
                        writer.write_if(p.arg1)
                    elif p.command_type == VmToken.GOTO:
                        writer.write_goto(p.arg1)
                    elif p.command_type == VmToken.FUNCTION:
                        writer.write_function(p.arg1, p.arg2)
                    elif p.command_type == VmToken.CALL:
                        writer.write_call(p.arg1, p.arg2)
                    elif p.command_type == VmToken.RETURN:
                        writer.write_return()
                    else:
                        raise Exception('Unknown command type "{}".'.format(p.command_type))
        print("Translation complete.\nOutput is '{}'".format(self._out_filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="path to the file or files to translate")
    args = parser.parse_args()
    translator = VMtranslator(args.source)
    translator.translate()