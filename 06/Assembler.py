# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 19:57:43 2016

@author: michael
"""
import os.path
from Parser import Parser, CommandType
from SymbolTable import SymbolTable
import Code

class Assembler(object):
    _BASE_VAR_ADDR = 16  # The first available memory address for variables

    def __init__(self, infile):
        self._parser = Parser(infile)
        self._symbol_table = SymbolTable()
        self._var_addr = self._BASE_VAR_ADDR
        
        # create the output filename from the input filenam
        base, ext = os.path.splitext(infile)
        if ext.lower() != ".asm":
            base = infile
        self._outfile = "{}.hack".format(base)

    def _first_pass(self):
        instr_count = 0
        while self._parser.has_more_commands():
            self._parser.advance()
            cmd_type = self._parser.command_type
            if (cmd_type == CommandType.A_COMMAND
                or cmd_type == CommandType.C_COMMAND):
                instr_count += 1
            elif cmd_type == CommandType.L_COMMAND:
                self._symbol_table.add_entry(self._parser.symbol, instr_count)
            else:
                # TODO: Error handling
                raise Exception("Something went wrong!")
        # Consume the EOF token to "reset" the token queue
        self._parser.advance()

    def _second_pass(self):
        with open(self._outfile, 'w') as f:
            while self._parser.has_more_commands():
                self._parser.advance()
                cmd_type = self._parser.command_type
                symbol = self._parser.symbol
                if cmd_type == CommandType.L_COMMAND:
                    # Skip labels -- they are already in the symbol table
                    continue
                elif cmd_type == CommandType.A_COMMAND:
                    addr = self._get_address(symbol)
                    f.write(Code.gen_a_command(addr) + '\n')
                elif cmd_type == CommandType.C_COMMAND:
                    f.write(Code.gen_c_command(
                        self._parser.dest,
                        self._parser.comp,
                        self._parser.jump) + '\n')

    def _get_address(self, symbol):
        try:
            # If the symbol is a number, convert to an int and return it
            addr = int(symbol)
            return addr
        except:
            # If the conversion failed, we'll consult the symbol table
            if not self._symbol_table.contains(symbol):
                # Add a new entry and increment the next available address
                self._symbol_table.add_entry(symbol, self._var_addr)
                self._var_addr += 1
            return self._symbol_table.get_address(symbol)

    def assemble(self):
        self._first_pass()
        self._second_pass()

if __name__ == "__main__":
    a = Assembler(r"C:\Users\mlang\Desktop\programming\nand2tetris\06\pong\Pong.asm")
    a.assemble()