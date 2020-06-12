# Generated from CalcParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CalcParser import CalcParser
else:
    from CalcParser import CalcParser

# This class defines a complete generic visitor for a parse tree produced by CalcParser.

class CalcParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CalcParser#expression.
    def visitExpression(self, ctx:CalcParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalcParser#ADD_ATOM.
    def visitADD_ATOM(self, ctx:CalcParser.ADD_ATOMContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalcParser#ADD.
    def visitADD(self, ctx:CalcParser.ADDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalcParser#SUB.
    def visitSUB(self, ctx:CalcParser.SUBContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalcParser#MUL_ATOM.
    def visitMUL_ATOM(self, ctx:CalcParser.MUL_ATOMContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalcParser#MUL.
    def visitMUL(self, ctx:CalcParser.MULContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalcParser#DIV.
    def visitDIV(self, ctx:CalcParser.DIVContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalcParser#NUMBER.
    def visitNUMBER(self, ctx:CalcParser.NUMBERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalcParser#NESTED_EXPR.
    def visitNESTED_EXPR(self, ctx:CalcParser.NESTED_EXPRContext):
        return self.visitChildren(ctx)



del CalcParser