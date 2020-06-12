# Generated from CalcParser.g4 by ANTLR 4.8
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\13")
        buf.write("*\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\5\3\26\n\3\3\4\3\4\3\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\4\5\4!\n\4\3\5\3\5\3\5\3\5\3\5\5\5(\n")
        buf.write("\5\3\5\2\2\6\2\4\6\b\2\2\2*\2\n\3\2\2\2\4\25\3\2\2\2\6")
        buf.write(" \3\2\2\2\b\'\3\2\2\2\n\13\5\4\3\2\13\3\3\2\2\2\f\26\5")
        buf.write("\6\4\2\r\16\5\6\4\2\16\17\7\6\2\2\17\20\5\6\4\2\20\26")
        buf.write("\3\2\2\2\21\22\5\6\4\2\22\23\7\7\2\2\23\24\5\6\4\2\24")
        buf.write("\26\3\2\2\2\25\f\3\2\2\2\25\r\3\2\2\2\25\21\3\2\2\2\26")
        buf.write("\5\3\2\2\2\27!\5\b\5\2\30\31\5\b\5\2\31\32\7\b\2\2\32")
        buf.write("\33\5\b\5\2\33!\3\2\2\2\34\35\5\b\5\2\35\36\7\t\2\2\36")
        buf.write("\37\5\b\5\2\37!\3\2\2\2 \27\3\2\2\2 \30\3\2\2\2 \34\3")
        buf.write("\2\2\2!\7\3\2\2\2\"(\7\3\2\2#$\7\n\2\2$%\5\2\2\2%&\7\13")
        buf.write("\2\2&(\3\2\2\2\'\"\3\2\2\2\'#\3\2\2\2(\t\3\2\2\2\5\25")
        buf.write(" \'")
        return buf.getvalue()


class CalcParser ( Parser ):

    grammarFileName = "CalcParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'+'", "'-'", "'*'", "'/'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "Number", "Whitespace", "Comment", "Add", 
                      "Subtract", "Multiply", "Divide", "OpenParen", "CloseParen" ]

    RULE_expression = 0
    RULE_addop = 1
    RULE_mulop = 2
    RULE_term = 3

    ruleNames =  [ "expression", "addop", "mulop", "term" ]

    EOF = Token.EOF
    Number=1
    Whitespace=2
    Comment=3
    Add=4
    Subtract=5
    Multiply=6
    Divide=7
    OpenParen=8
    CloseParen=9

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addop(self):
            return self.getTypedRuleContext(CalcParser.AddopContext,0)


        def getRuleIndex(self):
            return CalcParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = CalcParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.addop()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddopContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CalcParser.RULE_addop

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ADDContext(AddopContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CalcParser.AddopContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mulop(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CalcParser.MulopContext)
            else:
                return self.getTypedRuleContext(CalcParser.MulopContext,i)

        def Add(self):
            return self.getToken(CalcParser.Add, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitADD" ):
                return visitor.visitADD(self)
            else:
                return visitor.visitChildren(self)


    class SUBContext(AddopContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CalcParser.AddopContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mulop(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CalcParser.MulopContext)
            else:
                return self.getTypedRuleContext(CalcParser.MulopContext,i)

        def Subtract(self):
            return self.getToken(CalcParser.Subtract, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSUB" ):
                return visitor.visitSUB(self)
            else:
                return visitor.visitChildren(self)


    class ADD_ATOMContext(AddopContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CalcParser.AddopContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mulop(self):
            return self.getTypedRuleContext(CalcParser.MulopContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitADD_ATOM" ):
                return visitor.visitADD_ATOM(self)
            else:
                return visitor.visitChildren(self)



    def addop(self):

        localctx = CalcParser.AddopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_addop)
        try:
            self.state = 19
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                localctx = CalcParser.ADD_ATOMContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 10
                self.mulop()
                pass

            elif la_ == 2:
                localctx = CalcParser.ADDContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 11
                self.mulop()
                self.state = 12
                self.match(CalcParser.Add)
                self.state = 13
                self.mulop()
                pass

            elif la_ == 3:
                localctx = CalcParser.SUBContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 15
                self.mulop()
                self.state = 16
                self.match(CalcParser.Subtract)
                self.state = 17
                self.mulop()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MulopContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CalcParser.RULE_mulop

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DIVContext(MulopContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CalcParser.MulopContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CalcParser.TermContext)
            else:
                return self.getTypedRuleContext(CalcParser.TermContext,i)

        def Divide(self):
            return self.getToken(CalcParser.Divide, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDIV" ):
                return visitor.visitDIV(self)
            else:
                return visitor.visitChildren(self)


    class MULContext(MulopContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CalcParser.MulopContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CalcParser.TermContext)
            else:
                return self.getTypedRuleContext(CalcParser.TermContext,i)

        def Multiply(self):
            return self.getToken(CalcParser.Multiply, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMUL" ):
                return visitor.visitMUL(self)
            else:
                return visitor.visitChildren(self)


    class MUL_ATOMContext(MulopContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CalcParser.MulopContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self):
            return self.getTypedRuleContext(CalcParser.TermContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMUL_ATOM" ):
                return visitor.visitMUL_ATOM(self)
            else:
                return visitor.visitChildren(self)



    def mulop(self):

        localctx = CalcParser.MulopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_mulop)
        try:
            self.state = 30
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = CalcParser.MUL_ATOMContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 21
                self.term()
                pass

            elif la_ == 2:
                localctx = CalcParser.MULContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 22
                self.term()
                self.state = 23
                self.match(CalcParser.Multiply)
                self.state = 24
                self.term()
                pass

            elif la_ == 3:
                localctx = CalcParser.DIVContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 26
                self.term()
                self.state = 27
                self.match(CalcParser.Divide)
                self.state = 28
                self.term()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CalcParser.RULE_term

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class NUMBERContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CalcParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Number(self):
            return self.getToken(CalcParser.Number, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNUMBER" ):
                return visitor.visitNUMBER(self)
            else:
                return visitor.visitChildren(self)


    class NESTED_EXPRContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CalcParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def OpenParen(self):
            return self.getToken(CalcParser.OpenParen, 0)
        def expression(self):
            return self.getTypedRuleContext(CalcParser.ExpressionContext,0)

        def CloseParen(self):
            return self.getToken(CalcParser.CloseParen, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNESTED_EXPR" ):
                return visitor.visitNESTED_EXPR(self)
            else:
                return visitor.visitChildren(self)



    def term(self):

        localctx = CalcParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_term)
        try:
            self.state = 37
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [CalcParser.Number]:
                localctx = CalcParser.NUMBERContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 32
                self.match(CalcParser.Number)
                pass
            elif token in [CalcParser.OpenParen]:
                localctx = CalcParser.NESTED_EXPRContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 33
                self.match(CalcParser.OpenParen)
                self.state = 34
                self.expression()
                self.state = 35
                self.match(CalcParser.CloseParen)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





