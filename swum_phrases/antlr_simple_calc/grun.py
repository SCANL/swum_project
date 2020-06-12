import sys
from antlr4 import *
from CalcLexer import CalcLexer
from CalcParser import CalcParser
# from MyListener import ExpressionPrinter
from MyVisitor import *

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CalcLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CalcParser(stream)
    tree = parser.expression()
    # printer = ExpressionPrinter()
    # walker = ParseTreeWalker()
    # walker.walk(printer, tree)

    visitor = MyVisitor()
    ret = visitor.visit(tree)
    print(ret)

if __name__ == '__main__':
    main(sys.argv)
