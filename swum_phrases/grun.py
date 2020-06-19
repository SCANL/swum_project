import sys
from antlr4 import *
from SwumLexer import SwumLexer
from SwumParser import SwumParser
# from MyListener import MyParseTreePrinter
from MyVisitor import PrintVisitor

def main(argv):
    # input_stream = FileStream(argv[1])
    input_stream = InputStream(input('Enter text to parse: '))
    lexer = SwumLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SwumParser(stream)
    tree = parser.phrase()

    visitor = PrintVisitor(stream)
    visitor.visit(tree)
    print(visitor.ds)


if __name__ == '__main__':
    main(sys.argv)
