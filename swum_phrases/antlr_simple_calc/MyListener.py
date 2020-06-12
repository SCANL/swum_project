from antlr4 import *
from CalcParserListener import CalcParserListener
if __name__ is not None and "." in __name__:
    from .CalcParser import CalcParser
else:
    from CalcParser import CalcParser

class ExpressionPrinter(CalcParserListener):
    def enterExpression(self, ctx:CalcParser.ExpressionContext):
        print('Expression(', end='')
    def exitExpression(self, ctx:CalcParser.ExpressionContext):
        print(')', end='')
        