# Generated from CalcLexer.g4 by ANTLR 4.8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\13")
        buf.write("Y\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\3\2\6\2\27\n\2\r\2\16\2\30\3")
        buf.write("\2\3\2\6\2\35\n\2\r\2\16\2\36\5\2!\n\2\3\2\3\2\6\2%\n")
        buf.write("\2\r\2\16\2&\5\2)\n\2\3\3\6\3,\n\3\r\3\16\3-\3\3\3\3\3")
        buf.write("\4\3\4\3\4\3\4\7\4\66\n\4\f\4\16\49\13\4\3\4\5\4<\n\4")
        buf.write("\3\4\3\4\3\4\3\4\3\4\7\4C\n\4\f\4\16\4F\13\4\3\4\3\4\5")
        buf.write("\4J\n\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3")
        buf.write("\t\3\n\3\n\3D\2\13\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n")
        buf.write("\23\13\3\2\4\5\2\13\f\17\17\"\"\4\2\f\f\17\17\2b\2\3\3")
        buf.write("\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2")
        buf.write("\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2")
        buf.write("\3(\3\2\2\2\5+\3\2\2\2\7I\3\2\2\2\tM\3\2\2\2\13O\3\2\2")
        buf.write("\2\rQ\3\2\2\2\17S\3\2\2\2\21U\3\2\2\2\23W\3\2\2\2\25\27")
        buf.write("\4\62;\2\26\25\3\2\2\2\27\30\3\2\2\2\30\26\3\2\2\2\30")
        buf.write("\31\3\2\2\2\31 \3\2\2\2\32\34\7\60\2\2\33\35\4\62;\2\34")
        buf.write("\33\3\2\2\2\35\36\3\2\2\2\36\34\3\2\2\2\36\37\3\2\2\2")
        buf.write("\37!\3\2\2\2 \32\3\2\2\2 !\3\2\2\2!)\3\2\2\2\"$\7\60\2")
        buf.write("\2#%\4\62;\2$#\3\2\2\2%&\3\2\2\2&$\3\2\2\2&\'\3\2\2\2")
        buf.write("\')\3\2\2\2(\26\3\2\2\2(\"\3\2\2\2)\4\3\2\2\2*,\t\2\2")
        buf.write("\2+*\3\2\2\2,-\3\2\2\2-+\3\2\2\2-.\3\2\2\2./\3\2\2\2/")
        buf.write("\60\b\3\2\2\60\6\3\2\2\2\61\62\7\61\2\2\62\63\7\61\2\2")
        buf.write("\63\67\3\2\2\2\64\66\n\3\2\2\65\64\3\2\2\2\669\3\2\2\2")
        buf.write("\67\65\3\2\2\2\678\3\2\2\28;\3\2\2\29\67\3\2\2\2:<\7\17")
        buf.write("\2\2;:\3\2\2\2;<\3\2\2\2<=\3\2\2\2=J\7\f\2\2>?\7\61\2")
        buf.write("\2?@\7,\2\2@D\3\2\2\2AC\13\2\2\2BA\3\2\2\2CF\3\2\2\2D")
        buf.write("E\3\2\2\2DB\3\2\2\2EG\3\2\2\2FD\3\2\2\2GH\7,\2\2HJ\7\61")
        buf.write("\2\2I\61\3\2\2\2I>\3\2\2\2JK\3\2\2\2KL\b\4\2\2L\b\3\2")
        buf.write("\2\2MN\7-\2\2N\n\3\2\2\2OP\7/\2\2P\f\3\2\2\2QR\7,\2\2")
        buf.write("R\16\3\2\2\2ST\7\61\2\2T\20\3\2\2\2UV\7*\2\2V\22\3\2\2")
        buf.write("\2WX\7+\2\2X\24\3\2\2\2\r\2\30\36 &(-\67;DI\3\b\2\2")
        return buf.getvalue()


class CalcLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    Number = 1
    Whitespace = 2
    Comment = 3
    Add = 4
    Subtract = 5
    Multiply = 6
    Divide = 7
    OpenParen = 8
    CloseParen = 9

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'+'", "'-'", "'*'", "'/'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "Number", "Whitespace", "Comment", "Add", "Subtract", "Multiply", 
            "Divide", "OpenParen", "CloseParen" ]

    ruleNames = [ "Number", "Whitespace", "Comment", "Add", "Subtract", 
                  "Multiply", "Divide", "OpenParen", "CloseParen" ]

    grammarFileName = "CalcLexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


