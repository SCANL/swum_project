# Generated from CalcParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CalcParser import CalcParser
else:
    from CalcParser import CalcParser

# This class defines a complete listener for a parse tree produced by CalcParser.
class CalcParserListener(ParseTreeListener):

    # Enter a parse tree produced by CalcParser#expression.
    def enterExpression(self, ctx:CalcParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CalcParser#expression.
    def exitExpression(self, ctx:CalcParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CalcParser#ADD_ATOM.
    def enterADD_ATOM(self, ctx:CalcParser.ADD_ATOMContext):
        pass

    # Exit a parse tree produced by CalcParser#ADD_ATOM.
    def exitADD_ATOM(self, ctx:CalcParser.ADD_ATOMContext):
        pass


    # Enter a parse tree produced by CalcParser#ADD.
    def enterADD(self, ctx:CalcParser.ADDContext):
        pass

    # Exit a parse tree produced by CalcParser#ADD.
    def exitADD(self, ctx:CalcParser.ADDContext):
        pass


    # Enter a parse tree produced by CalcParser#SUB.
    def enterSUB(self, ctx:CalcParser.SUBContext):
        pass

    # Exit a parse tree produced by CalcParser#SUB.
    def exitSUB(self, ctx:CalcParser.SUBContext):
        pass


    # Enter a parse tree produced by CalcParser#MUL_ATOM.
    def enterMUL_ATOM(self, ctx:CalcParser.MUL_ATOMContext):
        pass

    # Exit a parse tree produced by CalcParser#MUL_ATOM.
    def exitMUL_ATOM(self, ctx:CalcParser.MUL_ATOMContext):
        pass


    # Enter a parse tree produced by CalcParser#MUL.
    def enterMUL(self, ctx:CalcParser.MULContext):
        pass

    # Exit a parse tree produced by CalcParser#MUL.
    def exitMUL(self, ctx:CalcParser.MULContext):
        pass


    # Enter a parse tree produced by CalcParser#DIV.
    def enterDIV(self, ctx:CalcParser.DIVContext):
        pass

    # Exit a parse tree produced by CalcParser#DIV.
    def exitDIV(self, ctx:CalcParser.DIVContext):
        pass


    # Enter a parse tree produced by CalcParser#NUMBER.
    def enterNUMBER(self, ctx:CalcParser.NUMBERContext):
        pass

    # Exit a parse tree produced by CalcParser#NUMBER.
    def exitNUMBER(self, ctx:CalcParser.NUMBERContext):
        pass


    # Enter a parse tree produced by CalcParser#NESTED_EXPR.
    def enterNESTED_EXPR(self, ctx:CalcParser.NESTED_EXPRContext):
        pass

    # Exit a parse tree produced by CalcParser#NESTED_EXPR.
    def exitNESTED_EXPR(self, ctx:CalcParser.NESTED_EXPRContext):
        pass



del CalcParser