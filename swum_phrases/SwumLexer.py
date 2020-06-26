# Generated from SwumLexer.g4 by ANTLR 4.8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\r")
        buf.write(";\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\6\2\33")
        buf.write("\n\2\r\2\16\2\34\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3")
        buf.write("\5\3\6\3\6\3\6\3\6\3\7\3\7\3\b\3\b\3\b\3\t\3\t\3\t\3\n")
        buf.write("\3\n\3\13\3\13\3\13\3\f\3\f\2\2\r\3\3\5\4\7\5\t\6\13\7")
        buf.write("\r\b\17\t\21\n\23\13\25\f\27\r\3\2\3\5\2\13\f\17\17\"")
        buf.write("\"\2;\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2")
        buf.write("\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2")
        buf.write("\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\3\32\3\2\2\2\5 ")
        buf.write("\3\2\2\2\7#\3\2\2\2\t%\3\2\2\2\13(\3\2\2\2\r,\3\2\2\2")
        buf.write("\17.\3\2\2\2\21\61\3\2\2\2\23\64\3\2\2\2\25\66\3\2\2\2")
        buf.write("\279\3\2\2\2\31\33\t\2\2\2\32\31\3\2\2\2\33\34\3\2\2\2")
        buf.write("\34\32\3\2\2\2\34\35\3\2\2\2\35\36\3\2\2\2\36\37\b\2\2")
        buf.write("\2\37\4\3\2\2\2 !\7P\2\2!\"\7O\2\2\"\6\3\2\2\2#$\7P\2")
        buf.write("\2$\b\3\2\2\2%&\7X\2\2&\'\7O\2\2\'\n\3\2\2\2()\7X\2\2")
        buf.write(")*\7R\2\2*+\7T\2\2+\f\3\2\2\2,-\7X\2\2-\16\3\2\2\2./\7")
        buf.write("E\2\2/\60\7L\2\2\60\20\3\2\2\2\61\62\7F\2\2\62\63\7V\2")
        buf.write("\2\63\22\3\2\2\2\64\65\7F\2\2\65\24\3\2\2\2\66\67\7R\2")
        buf.write("\2\678\7T\2\28\26\3\2\2\29:\7R\2\2:\30\3\2\2\2\4\2\34")
        buf.write("\3\b\2\2")
        return buf.getvalue()


class SwumLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    Whitespace = 1
    Noun_Modifier = 2
    Noun = 3
    Verb_Modifier = 4
    Verb_Particle = 5
    Verb = 6
    Conjunction = 7
    Determiner = 8
    Digit = 9
    Pronoun = 10
    Preposition = 11

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'NM'", "'N'", "'VM'", "'VPR'", "'V'", "'CJ'", "'DT'", "'D'", 
            "'PR'", "'P'" ]

    symbolicNames = [ "<INVALID>",
            "Whitespace", "Noun_Modifier", "Noun", "Verb_Modifier", "Verb_Particle", 
            "Verb", "Conjunction", "Determiner", "Digit", "Pronoun", "Preposition" ]

    ruleNames = [ "Whitespace", "Noun_Modifier", "Noun", "Verb_Modifier", 
                  "Verb_Particle", "Verb", "Conjunction", "Determiner", 
                  "Digit", "Pronoun", "Preposition" ]

    grammarFileName = "SwumLexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


