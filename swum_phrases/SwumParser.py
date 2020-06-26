# Generated from SwumParser.g4 by ANTLR 4.8
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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\r")
        buf.write("\61\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3")
        buf.write("\2\3\2\5\2\21\n\2\3\3\7\3\24\n\3\f\3\16\3\27\13\3\3\3")
        buf.write("\3\3\3\4\3\4\3\4\3\5\7\5\37\n\5\f\5\16\5\"\13\5\3\5\6")
        buf.write("\5%\n\5\r\5\16\5&\3\5\5\5*\n\5\3\6\3\6\3\6\5\6/\n\6\3")
        buf.write("\6\2\2\7\2\4\6\b\n\2\2\2\63\2\20\3\2\2\2\4\25\3\2\2\2")
        buf.write("\6\32\3\2\2\2\b \3\2\2\2\n+\3\2\2\2\f\21\5\4\3\2\r\21")
        buf.write("\5\n\6\2\16\21\5\6\4\2\17\21\5\b\5\2\20\f\3\2\2\2\20\r")
        buf.write("\3\2\2\2\20\16\3\2\2\2\20\17\3\2\2\2\21\3\3\2\2\2\22\24")
        buf.write("\7\4\2\2\23\22\3\2\2\2\24\27\3\2\2\2\25\23\3\2\2\2\25")
        buf.write("\26\3\2\2\2\26\30\3\2\2\2\27\25\3\2\2\2\30\31\7\5\2\2")
        buf.write("\31\5\3\2\2\2\32\33\7\r\2\2\33\34\5\4\3\2\34\7\3\2\2\2")
        buf.write("\35\37\7\6\2\2\36\35\3\2\2\2\37\"\3\2\2\2 \36\3\2\2\2")
        buf.write(" !\3\2\2\2!$\3\2\2\2\" \3\2\2\2#%\7\b\2\2$#\3\2\2\2%&")
        buf.write("\3\2\2\2&$\3\2\2\2&\'\3\2\2\2\')\3\2\2\2(*\7\7\2\2)(\3")
        buf.write("\2\2\2)*\3\2\2\2*\t\3\2\2\2+,\5\b\5\2,.\5\4\3\2-/\5\6")
        buf.write("\4\2.-\3\2\2\2./\3\2\2\2/\13\3\2\2\2\b\20\25 &).")
        return buf.getvalue()


class SwumParser ( Parser ):

    grammarFileName = "SwumParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'NM'", "'N'", "'VM'", "'VPR'", 
                     "'V'", "'CJ'", "'DT'", "'D'", "'PR'", "'P'" ]

    symbolicNames = [ "<INVALID>", "Whitespace", "Noun_Modifier", "Noun", 
                      "Verb_Modifier", "Verb_Particle", "Verb", "Conjunction", 
                      "Determiner", "Digit", "Pronoun", "Preposition" ]

    RULE_start = 0
    RULE_noun_phrase = 1
    RULE_prepositional_phrase = 2
    RULE_verb_group = 3
    RULE_verb_phrase = 4

    ruleNames =  [ "start", "noun_phrase", "prepositional_phrase", "verb_group", 
                   "verb_phrase" ]

    EOF = Token.EOF
    Whitespace=1
    Noun_Modifier=2
    Noun=3
    Verb_Modifier=4
    Verb_Particle=5
    Verb=6
    Conjunction=7
    Determiner=8
    Digit=9
    Pronoun=10
    Preposition=11

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def noun_phrase(self):
            return self.getTypedRuleContext(SwumParser.Noun_phraseContext,0)


        def verb_phrase(self):
            return self.getTypedRuleContext(SwumParser.Verb_phraseContext,0)


        def prepositional_phrase(self):
            return self.getTypedRuleContext(SwumParser.Prepositional_phraseContext,0)


        def verb_group(self):
            return self.getTypedRuleContext(SwumParser.Verb_groupContext,0)


        def getRuleIndex(self):
            return SwumParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart" ):
                return visitor.visitStart(self)
            else:
                return visitor.visitChildren(self)




    def start(self):

        localctx = SwumParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.state = 14
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 10
                self.noun_phrase()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 11
                self.verb_phrase()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 12
                self.prepositional_phrase()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 13
                self.verb_group()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Noun_phraseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Noun(self):
            return self.getToken(SwumParser.Noun, 0)

        def Noun_Modifier(self, i:int=None):
            if i is None:
                return self.getTokens(SwumParser.Noun_Modifier)
            else:
                return self.getToken(SwumParser.Noun_Modifier, i)

        def getRuleIndex(self):
            return SwumParser.RULE_noun_phrase

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNoun_phrase" ):
                listener.enterNoun_phrase(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNoun_phrase" ):
                listener.exitNoun_phrase(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNoun_phrase" ):
                return visitor.visitNoun_phrase(self)
            else:
                return visitor.visitChildren(self)




    def noun_phrase(self):

        localctx = SwumParser.Noun_phraseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_noun_phrase)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SwumParser.Noun_Modifier:
                self.state = 16
                self.match(SwumParser.Noun_Modifier)
                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 22
            self.match(SwumParser.Noun)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Prepositional_phraseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Preposition(self):
            return self.getToken(SwumParser.Preposition, 0)

        def noun_phrase(self):
            return self.getTypedRuleContext(SwumParser.Noun_phraseContext,0)


        def getRuleIndex(self):
            return SwumParser.RULE_prepositional_phrase

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrepositional_phrase" ):
                listener.enterPrepositional_phrase(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrepositional_phrase" ):
                listener.exitPrepositional_phrase(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrepositional_phrase" ):
                return visitor.visitPrepositional_phrase(self)
            else:
                return visitor.visitChildren(self)




    def prepositional_phrase(self):

        localctx = SwumParser.Prepositional_phraseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_prepositional_phrase)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.match(SwumParser.Preposition)
            self.state = 25
            self.noun_phrase()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Verb_groupContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Verb_Modifier(self, i:int=None):
            if i is None:
                return self.getTokens(SwumParser.Verb_Modifier)
            else:
                return self.getToken(SwumParser.Verb_Modifier, i)

        def Verb(self, i:int=None):
            if i is None:
                return self.getTokens(SwumParser.Verb)
            else:
                return self.getToken(SwumParser.Verb, i)

        def Verb_Particle(self):
            return self.getToken(SwumParser.Verb_Particle, 0)

        def getRuleIndex(self):
            return SwumParser.RULE_verb_group

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVerb_group" ):
                listener.enterVerb_group(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVerb_group" ):
                listener.exitVerb_group(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVerb_group" ):
                return visitor.visitVerb_group(self)
            else:
                return visitor.visitChildren(self)




    def verb_group(self):

        localctx = SwumParser.Verb_groupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_verb_group)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SwumParser.Verb_Modifier:
                self.state = 27
                self.match(SwumParser.Verb_Modifier)
                self.state = 32
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 34 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 33
                self.match(SwumParser.Verb)
                self.state = 36 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==SwumParser.Verb):
                    break

            self.state = 39
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SwumParser.Verb_Particle:
                self.state = 38
                self.match(SwumParser.Verb_Particle)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Verb_phraseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def verb_group(self):
            return self.getTypedRuleContext(SwumParser.Verb_groupContext,0)


        def noun_phrase(self):
            return self.getTypedRuleContext(SwumParser.Noun_phraseContext,0)


        def prepositional_phrase(self):
            return self.getTypedRuleContext(SwumParser.Prepositional_phraseContext,0)


        def getRuleIndex(self):
            return SwumParser.RULE_verb_phrase

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVerb_phrase" ):
                listener.enterVerb_phrase(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVerb_phrase" ):
                listener.exitVerb_phrase(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVerb_phrase" ):
                return visitor.visitVerb_phrase(self)
            else:
                return visitor.visitChildren(self)




    def verb_phrase(self):

        localctx = SwumParser.Verb_phraseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_verb_phrase)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.verb_group()
            self.state = 42
            self.noun_phrase()
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SwumParser.Preposition:
                self.state = 43
                self.prepositional_phrase()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





