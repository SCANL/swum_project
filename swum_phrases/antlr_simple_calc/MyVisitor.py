from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CalcParser import CalcParser
else:
    from CalcParser import CalcParser
from CalcParserVisitor import *

class MyVisitor(CalcParserVisitor):
    # Visit a parse tree produced by CalcParser#expression.
    def visitExpression(self, ctx:CalcParser.ExpressionContext):
        return self.visit(ctx.addop())


    # Visit a parse tree produced by CalcParser#ADD_ATOM.
    def visitADD_ATOM(self, ctx:CalcParser.ADD_ATOMContext):
        return self.visit(ctx.mulop())


    # Visit a parse tree produced by CalcParser#ADD.
    def visitADD(self, ctx:CalcParser.ADDContext):
        lhs = self.visit(ctx.mulop(0))
        rhs = self.visit(ctx.mulop(1))
        return lhs + rhs

    # Visit a parse tree produced by CalcParser#SUB.
    def visitSUB(self, ctx:CalcParser.SUBContext):
        lhs = self.visit(ctx.mulop(0))
        rhs = self.visit(ctx.mulop(1))
        return lhs - rhs


    # Visit a parse tree produced by CalcParser#MUL_ATOM.
    def visitMUL_ATOM(self, ctx:CalcParser.MUL_ATOMContext):
        return self.visit(ctx.term())


    # Visit a parse tree produced by CalcParser#MUL.
    def visitMUL(self, ctx:CalcParser.MULContext):
        lhs = self.visit(ctx.term(0))
        rhs = self.visit(ctx.term(1))
        return lhs * rhs


    # Visit a parse tree produced by CalcParser#DIV.
    def visitDIV(self, ctx:CalcParser.DIVContext):
        lhs = self.visit(ctx.term(0))
        rhs = self.visit(ctx.term(1))
        return lhs / rhs


    # Visit a parse tree produced by CalcParser#NUMBER.
    def visitNUMBER(self, ctx:CalcParser.NUMBERContext):
        numStr = ctx.Number().getText()
        if '.' in numStr:
            return float(numStr)

        return int(numStr)


    # Visit a parse tree produced by CalcParser#NESTED_EXPR.
    def visitNESTED_EXPR(self, ctx:CalcParser.NESTED_EXPRContext):
        return self.visit(ctx.expression())