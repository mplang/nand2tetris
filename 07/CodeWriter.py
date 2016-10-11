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
        self._label_count = 0
        self._file = open(self._outfile, 'w')
    
    def done(self):
        self._file.close()

    # Arithmetic and logic commands

    def _unary(self, comp):
        """Handle unary arithmetic commands
        
        :param comp: The c-command comp field for the operation (!D, -D)
        """
        self._stack_to_dest("A")
        self._c_command("D", comp)
        self._comp_to_stack("D")

    def _binary(self, comp):
        """Handle binary arithmetic commands
        
        :param comp: The c-command comp field for the operation (D+A, A-D, etc)
        """
        self._stack_to_dest("D")
        self._unary(comp)

    # Comparison/jump commands

    def _comparison(self, jump):
        """Handle EQ, LT, and GT
        
        :param jump: The jump value for the comparison (JEQ, JLT, JGT)
        """
        self._stack_to_dest("D")    # pop Op2
        self._stack_to_dest("A")    # pop Op1
        self._c_command("D", "A-D") # Op1-Op2
        eq_label = self._get_label()
        # if the comparison is true, jump to (eq_label)
        self._jump(eq_label, None, "D", jump)   # @eq_label # D;JUMP
        # else, push false (0) on the stack...
        self._comp_to_stack("0")
        # ...and jump to (neq_label)
        neq_label = self._get_label()
        self._jump(neq_label, None, "0", "JMP")
        # (eq_label) here, push true (-1) on the stack
        self._l_command(eq_label)
        self._comp_to_stack("-1")
        # (neq_label)
        self._l_command(neq_label)

    def _jump(self, label, dest, comp, jump):
        self._a_command(label)
        self._c_command(dest, comp, jump)

    # Stack manipulation

    def _push(self, segment, index):
        if segment == self.SegmentType.constant.name:
            self._push_value(index)
        else:
            raise Exception('Unknown segment type "{}".'.format(segment))

    def _push_value(self, value):
        self._a_command(value)
        self._c_command("D", "A")
        self._comp_to_stack("D")

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

    def _l_command(self, label):
        """Generates an l-command from the given label
        """
        line = "({})".format(label)
        self._writeline(line)

    def _writeline(self, line):
        """Writes a line of translated code to the file
        """
        self._file.write("{}\n".format(line))
        #print(line)

    def _get_label(self):
        """Returns the next sequential label
        """
        label = "LABEL{}".format(self._label_count)
        self._label_count += 1
        return label

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
            self._binary("D+A")
        elif command == "sub":
            self._binary("A-D")
        elif command == "and":
            self._binary("D&A")
        elif command == "or":
            self._binary("D|A")
        elif command == "neg":
            self._unary("-D")
        elif command == "not":
            self._unary("!D")
        elif command == "eq":
            self._comparison("JEQ")
        elif command == "gt":
            self._comparison("JGT")
        elif command == "lt":
            self._comparison("JLT")
        else:
            raise Exception('Unknown command "{}".'.format(command))