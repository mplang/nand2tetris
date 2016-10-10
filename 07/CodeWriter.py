# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:45:24 2016

@author: mlang
"""
import os.path
from VmToken import VmToken
from enum import Enum, unique

class CodeWriter(object):
    @unique
    class SegmentType(Enum):
        argument = 1
        local = 2
        static = 3
        constant = 4
        this = 5
        that = 6
        pointer = 7
        temp = 8

    def __init__(self, infile):
        # create the output filename from the input filenam
        base, ext = os.path.splitext(infile)
        if ext.lower() != ".vm":
            base = infile
        self._outfile = "{}.asm".format(base)

    # Arithmetic and logic commands

    def _add(self):
        self._binary("D+A")

    def _sub(self):
        self._binary("A-D")
        #self._binary("D-A")

    def _and(self):
        self._binary("D&A")

    def _or(self):
        self._binary("D|A")
    
    def _neg(self):
        self._unary("-D")
        
    def _unary(self, comp):
        self._stack_to_dest("A")
        self._c_command("D", comp)
        self._comp_to_stack("D")
    
    def _binary(self, comp):
        self._stack_to_dest("D")
        self._unary(comp)
#        self._stack_to_dest("D")
#        self._stack_to_dest("A")
#        self._c_command("D", comp)
#        self._comp_to_stack("D")

    # Stack manipulation

    def _push(self, segment, index):
        if segment == self.SegmentType.constant.name:
            self._push_constant(index)
        else:
            raise Exception('Unknown segment type "{}".'.format(segment))

    def _push_constant(self, value):
        self._a_command(value)      # @value
        self._c_command("D", "A")   # D=A
        self._a_command("SP")       # @SP
        self._c_command("A", "M")   # A=M
        self._c_command("M", "D")   # M=D
        self._inc_sp()              # ++SP

    def _pop(self, segment, index):
        pass

    def _stack_to_dest(self, dest):
        """Pop an item from the stack and put it in the dest register(s)
        """
        self._dec_sp()              # --SP
        self._load_sp()            # A=M[SP]
        self._c_command(dest, "M")  # dest=M[A]

    def _comp_to_stack(self, comp):
        self._load_sp()
        self._c_command("M", comp)
        self._inc_sp()

    def _load_sp(self):
        """Gets the value of the stack pointer and stores it in the A register
        """
        self._a_command("SP")       # @SP
        self._c_command("A", "M")   # A=M[SP]

    def _inc_sp(self):
        """Increment the stack pointer
        """
        self._a_command("SP")       # @SP
        self._c_command("M", "M+1") # M=M+1

    def _dec_sp(self):
        """Decrement the stack pointer
        """
        self._a_command("SP")       # @SP
        self._c_command("M", "M-1") # M=M-1

    # Code generation

    def _a_command(self, value):
        """Generates an a-command for the given value
        """
        self._writeline("@{}".format(value))

    def _c_command(self, dest, comp, jump=None):
        """Generates a c-command given the dest, comp, and jump fields
        """
        if comp == None:
            raise Exception('Invalid value "{}" for comp field.'.format(comp))
        line = ''
        if dest != None:
            line = dest + '='
        line += comp
        if jump != None:
            line += ';' + jump
        self._writeline(line)

    def _writeline(self, line):
        """Writes a line of translated code to the file
        """
        #self._file.write("{}\n".format(line))
        print(line)

    # Public methods

    def write_push_pop(self, command, segment, index):
        """Translates PUSH and POP commands
        """
        if command == VmToken.PUSH:
            self._push(segment, index)
        elif command == VmToken.POP:
            self._pop(segment, index)
        else:
            raise Exception("Invalid command")

    def write_arithmetic(self, command):
        """Translates arithmetic and logic commands
        """
        if command == "add":
            self._add()
        elif command == "sub":
            self._sub()
        elif command == "and":
            self._and()
        elif command == "or":
            self._or()
        elif command == "neg":
            self._neg()
        elif command == "eq":
            pass
        elif command == "gt":
            pass
        elif command == "lt":
            pass
        elif command == "not":
            pass
        else:
            raise Exception('Unknown command "{}".'.format(command))