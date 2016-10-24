# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:45:24 2016

@author: mlang
"""
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

    # map of segment types to assembler register labels
    _seg_reg_map = {
                SegmentType.argument: "ARG",
                SegmentType.local: "LCL",
                SegmentType.this: "THIS",
                SegmentType.that: "THAT"}

    def __init__(self, out_filename):
        self._out_filename = out_filename
        self._label_count = 0
    
    def __enter__(self):
        self._file = open(self._out_filename, 'w')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()

    # Arithmetic and logic commands

    def _unary(self, comp):
        """Handle unary arithmetic commands

        :param comp: The c-command comp field for the operation (!D, -D)
        """
        self._pop_to_dest("A")
        self._c_command("D", comp)
        self._push_comp("D")

    def _binary(self, comp):
        """Handle binary arithmetic commands

        :param comp: The c-command comp field for the operation (D+A, A-D, etc)
        """
        self._pop_to_dest("D")
        self._unary(comp)

    # Comparison/jump commands

    def _comparison(self, jump):
        """Handle EQ, LT, and GT

        :param jump: The jump value for the comparison (JEQ, JLT, JGT)
        """
        self._pop_to_dest("D")    # pop Op2
        self._pop_to_dest("A")    # pop Op1
        self._c_command("D", "A-D") # Op1-Op2
        eq_label = self._get_label()
        # if the comparison is true, jump to (eq_label)
        self._jump(eq_label, None, "D", jump)   # @eq_label # D;JUMP
        # else, push false (0) on the stack...
        self._push_comp("0")
        # ...and jump to (neq_label)
        neq_label = self._get_label()
        self._jump(neq_label, None, "0", "JMP")
        # (eq_label) here, push true (-1) on the stack
        self._l_command(eq_label)
        self._push_comp("-1")
        # (neq_label)
        self._l_command(neq_label)

    def _jump(self, label, dest, comp, jump):
        """Generates a pair of commands to jump to the given label
        """
        self._a_command(label)
        self._c_command(dest, comp, jump)

    # Stack manipulation

    def _push(self, segment, index):
        if segment == self.SegmentType.constant.name:
            self._push_value(index)
        elif (segment == self.SegmentType.argument.name
              or segment == self.SegmentType.local.name
              or segment == self.SegmentType.this.name
              or segment == self.SegmentType.that.name):
            self._push_mem(self._seg_reg_map[self.SegmentType[segment]], index)
        elif segment == self.SegmentType.pointer.name:
            if index != "0" or index != "1":
                raise Exception('Segment index out of range.')
            else:
                self._push_reg("THIS" if index == "0" else "THAT")
        elif segment == self.SegmentType.temp.name:
            try:
                idx = int(index)
            except:
                raise Exception('Invalid segment index value.')
            if idx < 0 or idx > 7:
                raise Exception('Segment index out of range.')
            else:
                self._push_reg("R{}".format(5+idx))
        elif segment == self.SegmentType.static.name:
            self._push_reg("{}.{}".format(self._basename, index))
        else:
            raise Exception('Unknown segment type "{}".'.format(segment))

    def _push_value(self, value):
        """Pushes the given immediate value on the stack
        """
        self._a_command(value)
        self._c_command("D", "A")
        self._push_comp("D")
    
    def _push_comp(self, comp):
        """Pushes the value of the given comp field on the stack
        """
        self._load_sp()
        self._c_command("M", comp)
        self._inc_sp()
    
    def _push_mem(self, reg, offset):
        """Pushes the value at M[*reg+offset] on the stack
        """
        self._a_command(offset)
        self._c_command("D", "A")
        self._a_command(reg)
        self._c_command("A", "M")
        self._c_command("A", "D+A")
        self._c_command("D", "M")
        self._load_sp()
        self._c_command("M", "D")
        self._inc_sp()
    
    def _push_reg(self, reg):
        """Pushes the register value on the stack
        """
        self._a_command(reg)
        self._c_command("D", "M")
        self._push_comp("D")

    def _pop(self, segment, index):
        pass

    def _pop_to_dest(self, dest):
        """Pop an item from the stack and put it in the dest register(s)
        """
        self._dec_sp()              # --SP
        self._load_sp()            # A=M[SP]
        self._c_command(dest, "M")  # dest=M[A]

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
    
    def write_init(self):
        """Generates the VM bootstrap code
        """
        self._a_command(256)
        self._c_command("D", "A")
        self._a_command("SP")
        self._c_command("M", "D")
    
    def write_label(self, label):
        """Translates the LABEL command
        """
        self._l_command(label)
    
    def write_goto(self, label):
        """Translates the GOTO command
        """
        self._a_command(label)
        self._c_command(None, "0", "JMP")
    
    def write_if(self, label):
        """Translates the IF_GOTO command
        """
        self._pop_to_dest("D")
        self._a_command(label)
        self._c_command(None, "D", "JNE")
    
    def write_call(self, function_name, num_args):
        """Translates the CALL command
        """
        return_label = self._get_label()
        self._push_value(return_label)  # push return address
        self._push_reg("LCL")
        self._push_reg("ARG")   
        self._push_reg("THIS")
        self._push_reg("THAT")
        self._a_command(num_args + 5)   # @num_args+5
        self._c_command("D", "A")       # D=A
        self._a_command("SP")           # @SP
        self._c_command("A", "M")       # A=M
        self._c_command("D", "A-D")     # D=A-D
        self._a_command("ARG")          # @ARG
        self._c_command("M", "D")       # M=D
        self._a_command("SP")           # @SP
        self._c_command("D", "M")       # D=M
        self._a_command("LCL")          # @LCL
        self._c_command("M", "D")       # M=D
        self._a_command(function_name)  # @function_name
        self._c_command(None, 0, "JMP") # 0;JMP
        self._l_command(return_label)   # (return_label)
    
    def write_return(self):
        """Translates the RETURN command
        """
        self._a_command("LCL")      # @LCL
        self._c_command("D", "M")   # D=M
        self._a_command("FRAME")    # @FRAME
        self._c_command("M", "D")   # M=D
        # *(LCL-5) == return_address
        # @5
        # D=D-A
        # @RET
        # M=D
        # TODO: Finish me! Also, _pop()!
        
        
    
    def write_function(self, function_name, num_locals):
        """Translates the FUNCTION command
        """
        self._l_command(function_name)
        # foreach i in [0..num_locals]: push 0
        for i in range(num_locals):
            self._push_value(0)

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
