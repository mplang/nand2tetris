# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:02:26 2016

@author: mlang
"""
import argparse
import os.path
from glob import glob
from JackTokenizer import JackTokenizer
from JackToken import JackToken
from JackKeyword import JackKeyword

class JackAnalyzer(object):
    def __init__(self, source):
        self._set_inputs(source)

    def _set_inputs(self, source):
        source = os.path.normpath(source)
        self._file_list = None
        if os.path.isdir(source):
            # For a folder, get a list of all .jack files
            self._file_list = glob(os.path.join(source, '*.jack'))
        else:
            _, ext = os.path.splitext(source)
            if ext.lower() != ".jack":
                raise Exception("Invalid input file type!")
            self._file_list = [source]

    def _gen_xml(self, token):
        tok = token.Token
        lex = token.Lexeme
        if tok == JackToken.KEYWORD:
            # Special handling for keyword lexeme
            tag = "keyword"
            value = lex.name.lower()
        elif tok == JackToken.SYMBOL:
            # Special handling to convert certain symbols to valid XML
            tag = "symbol"
            if lex == '<':
                value = "&lt;"
            elif lex == '>':
                value = "&gt;"
            elif lex == '"':
                value = "&quot;"
            elif lex == '&':
                value = "&amp;"
            else:
                value = lex
        else:
            # No special handling to lexemes of other tokens
            if tok == JackToken.IDENTIFIER:
                tag = "identifier"
            elif tok == JackToken.INT_CONST:
                tag = "integerConstant"
            elif tok == JackToken.STRING_CONST:
                tag = "stringConstant"
            else:
                raise Exception("Invalid or unknown token!")
            value = lex
        
        line = "<{0}> {1} </{0}>\n".format(tag, value)
        return line


    def analyze(self):
        print("Starting analyzer...")
        if (self._file_list is None) or (len(self._file_list) == 0):
            raise Exception("No valid files to analyze.")
        for infile in self._file_list:
            print("Processing file '{}' ...".format(infile))
            # We know the filenames end in .jack, so we can do a simple replace
            outfile = '{}xml'.format(infile[:-4])
            with open(outfile, 'w') as f:
                tokenizer = JackTokenizer(infile)
                tokenizer.tokenize()
                f.write("<tokens>\n")
                while tokenizer.has_more_tokens():
                    t = tokenizer.advance()
                    f.write(self._gen_xml(t))
                f.write("</tokens>\n")
            print("Analysis complete.\nOutput is '{}'".format(outfile))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="path to the file or folder to translate")
    args = parser.parse_args()
    analyzer = JackAnalyzer(args.source)
    analyzer.analyze()
