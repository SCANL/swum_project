# Generated from SwumLexer.g4 by ANTLR 4.8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\r")
        buf.write(";\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\3\2\3\2")
        buf.write("\3\3\3\3\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\6\3\6\3\7\3\7\3")
        buf.write("\7\3\b\3\b\3\b\3\t\3\t\3\n\3\n\3\n\3\13\3\13\3\f\6\f\66")
        buf.write("\n\f\r\f\16\f\67\3\f\3\f\2\2\r\3\3\5\4\7\5\t\6\13\7\r")
        buf.write("\b\17\t\21\n\23\13\25\f\27\r\3\2\3\5\2\13\f\17\17\"\"")
        buf.write("\2;\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2")
        buf.write("\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23")
        buf.write("\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\3\31\3\2\2\2\5\34\3")
        buf.write("\2\2\2\7\36\3\2\2\2\t!\3\2\2\2\13%\3\2\2\2\r\'\3\2\2\2")
        buf.write("\17*\3\2\2\2\21-\3\2\2\2\23/\3\2\2\2\25\62\3\2\2\2\27")
        buf.write("\65\3\2\2\2\31\32\7P\2\2\32\33\7O\2\2\33\4\3\2\2\2\34")
        buf.write("\35\7P\2\2\35\6\3\2\2\2\36\37\7X\2\2\37 \7O\2\2 \b\3\2")
        buf.write("\2\2!\"\7X\2\2\"#\7R\2\2#$\7T\2\2$\n\3\2\2\2%&\7X\2\2")
        buf.write("&\f\3\2\2\2\'(\7E\2\2()\7L\2\2)\16\3\2\2\2*+\7F\2\2+,")
        buf.write("\7V\2\2,\20\3\2\2\2-.\7F\2\2.\22\3\2\2\2/\60\7R\2\2\60")
        buf.write("\61\7T\2\2\61\24\3\2\2\2\62\63\7R\2\2\63\26\3\2\2\2\64")
        buf.write("\66\t\2\2\2\65\64\3\2\2\2\66\67\3\2\2\2\67\65\3\2\2\2")
        buf.write("\678\3\2\2\289\3\2\2\29:\b\f\2\2:\30\3\2\2\2\4\2\67\3")
        buf.write("\b\2\2")
        return buf.getvalue()


class SwumLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    Noun_Modifier = 1
    Noun = 2
    Verb_Modifier = 3
    Verb_Particle = 4
    Verb = 5
    Conjunction = 6
    Determiner = 7
    Digit = 8
    Pronoun = 9
    Preposition = 10
    Whitespace = 11

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'NM'", "'N'", "'VM'", "'VPR'", "'V'", "'CJ'", "'DT'", "'D'", 
            "'PR'", "'P'" ]

    symbolicNames = [ "<INVALID>",
            "Noun_Modifier", "Noun", "Verb_Modifier", "Verb_Particle", "Verb", 
            "Conjunction", "Determiner", "Digit", "Pronoun", "Preposition", 
            "Whitespace" ]

    ruleNames = [ "Noun_Modifier", "Noun", "Verb_Modifier", "Verb_Particle", 
                  "Verb", "Conjunction", "Determiner", "Digit", "Pronoun", 
                  "Preposition", "Whitespace" ]

    grammarFileName = "SwumLexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


