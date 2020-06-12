import sys
from antlr4 import *
from HelloLexer import HelloLexer
from HelloParser import HelloParser
from HelloListener import RPrinter

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = HelloLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.r()
    printer = RPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main(sys.argv)
