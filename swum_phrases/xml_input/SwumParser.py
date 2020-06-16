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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\22")
        buf.write("H\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\3\2\3\2\3\2\3\2\3\2\5\2\30\n\2\3\3\7\3\33")
        buf.write("\n\3\f\3\16\3\36\13\3\3\3\3\3\3\4\3\4\3\4\3\5\7\5&\n\5")
        buf.write("\f\5\16\5)\13\5\3\5\3\5\5\5-\n\5\3\6\3\6\5\6\61\n\6\3")
        buf.write("\6\3\6\5\6\65\n\6\3\6\5\68\n\6\3\7\3\7\5\7<\n\7\3\b\6")
        buf.write("\b?\n\b\r\b\16\b@\3\t\6\tD\n\t\r\t\16\tE\3\t\2\2\n\2\4")
        buf.write("\6\b\n\f\16\20\2\2\2L\2\27\3\2\2\2\4\34\3\2\2\2\6!\3\2")
        buf.write("\2\2\b\'\3\2\2\2\n\60\3\2\2\2\f;\3\2\2\2\16>\3\2\2\2\20")
        buf.write("C\3\2\2\2\22\30\5\4\3\2\23\30\5\n\6\2\24\30\5\6\4\2\25")
        buf.write("\30\5\b\5\2\26\30\5\f\7\2\27\22\3\2\2\2\27\23\3\2\2\2")
        buf.write("\27\24\3\2\2\2\27\25\3\2\2\2\27\26\3\2\2\2\30\3\3\2\2")
        buf.write("\2\31\33\7\b\2\2\32\31\3\2\2\2\33\36\3\2\2\2\34\32\3\2")
        buf.write("\2\2\34\35\3\2\2\2\35\37\3\2\2\2\36\34\3\2\2\2\37 \7\t")
        buf.write("\2\2 \5\3\2\2\2!\"\7\21\2\2\"#\5\4\3\2#\7\3\2\2\2$&\7")
        buf.write("\n\2\2%$\3\2\2\2&)\3\2\2\2\'%\3\2\2\2\'(\3\2\2\2(*\3\2")
        buf.write("\2\2)\'\3\2\2\2*,\7\f\2\2+-\7\13\2\2,+\3\2\2\2,-\3\2\2")
        buf.write("\2-\t\3\2\2\2.\61\5\b\5\2/\61\5\20\t\2\60.\3\2\2\2\60")
        buf.write("/\3\2\2\2\61\64\3\2\2\2\62\65\5\4\3\2\63\65\5\16\b\2\64")
        buf.write("\62\3\2\2\2\64\63\3\2\2\2\65\67\3\2\2\2\668\5\6\4\2\67")
        buf.write("\66\3\2\2\2\678\3\2\2\28\13\3\2\2\29<\5\16\b\2:<\5\20")
        buf.write("\t\2;9\3\2\2\2;:\3\2\2\2<\r\3\2\2\2=?\5\4\3\2>=\3\2\2")
        buf.write("\2?@\3\2\2\2@>\3\2\2\2@A\3\2\2\2A\17\3\2\2\2BD\5\b\5\2")
        buf.write("CB\3\2\2\2DE\3\2\2\2EC\3\2\2\2EF\3\2\2\2F\21\3\2\2\2\f")
        buf.write("\27\34\',\60\64\67;@E")
        return buf.getvalue()


class SwumParser ( Parser ):

    grammarFileName = "SwumParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'<POS>'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'NM'", "'N'", "'VM'", "'VPR'", "'V'", 
                     "'CJ'", "'DT'", "'D'", "'PR'", "'P'", "'</POS>'" ]

    symbolicNames = [ "<INVALID>", "POS_Tag", "End_Tag", "Bracket", "Metadata", 
                      "Whitespace", "Noun_Modifier", "Noun", "Verb_Modifier", 
                      "Verb_Particle", "Verb", "Conjunction", "Determiner", 
                      "Digit", "Pronoun", "Preposition", "End_POS_Tag" ]

    RULE_phrase = 0
    RULE_noun_phrase = 1
    RULE_prepositional_phrase = 2
    RULE_verb_group = 3
    RULE_verb_phrase = 4
    RULE_equivalence = 5
    RULE_equivalence_np = 6
    RULE_equivalence_vg = 7

    ruleNames =  [ "phrase", "noun_phrase", "prepositional_phrase", "verb_group", 
                   "verb_phrase", "equivalence", "equivalence_np", "equivalence_vg" ]

    EOF = Token.EOF
    POS_Tag=1
    End_Tag=2
    Bracket=3
    Metadata=4
    Whitespace=5
    Noun_Modifier=6
    Noun=7
    Verb_Modifier=8
    Verb_Particle=9
    Verb=10
    Conjunction=11
    Determiner=12
    Digit=13
    Pronoun=14
    Preposition=15
    End_POS_Tag=16

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class PhraseContext(ParserRuleContext):

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


        def equivalence(self):
            return self.getTypedRuleContext(SwumParser.EquivalenceContext,0)


        def getRuleIndex(self):
            return SwumParser.RULE_phrase

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPhrase" ):
                listener.enterPhrase(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPhrase" ):
                listener.exitPhrase(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPhrase" ):
                return visitor.visitPhrase(self)
            else:
                return visitor.visitChildren(self)




    def phrase(self):

        localctx = SwumParser.PhraseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_phrase)
        try:
            self.state = 21
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 16
                self.noun_phrase()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 17
                self.verb_phrase()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 18
                self.prepositional_phrase()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 19
                self.verb_group()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 20
                self.equivalence()
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
            self.state = 26
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SwumParser.Noun_Modifier:
                self.state = 23
                self.match(SwumParser.Noun_Modifier)
                self.state = 28
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 29
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
            self.state = 31
            self.match(SwumParser.Preposition)
            self.state = 32
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

        def Verb(self):
            return self.getToken(SwumParser.Verb, 0)

        def Verb_Modifier(self, i:int=None):
            if i is None:
                return self.getTokens(SwumParser.Verb_Modifier)
            else:
                return self.getToken(SwumParser.Verb_Modifier, i)

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
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SwumParser.Verb_Modifier:
                self.state = 34
                self.match(SwumParser.Verb_Modifier)
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 40
            self.match(SwumParser.Verb)
            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SwumParser.Verb_Particle:
                self.state = 41
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


        def equivalence_vg(self):
            return self.getTypedRuleContext(SwumParser.Equivalence_vgContext,0)


        def noun_phrase(self):
            return self.getTypedRuleContext(SwumParser.Noun_phraseContext,0)


        def equivalence_np(self):
            return self.getTypedRuleContext(SwumParser.Equivalence_npContext,0)


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
            self.state = 46
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.state = 44
                self.verb_group()
                pass

            elif la_ == 2:
                self.state = 45
                self.equivalence_vg()
                pass


            self.state = 50
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.state = 48
                self.noun_phrase()
                pass

            elif la_ == 2:
                self.state = 49
                self.equivalence_np()
                pass


            self.state = 53
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SwumParser.Preposition:
                self.state = 52
                self.prepositional_phrase()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EquivalenceContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def equivalence_np(self):
            return self.getTypedRuleContext(SwumParser.Equivalence_npContext,0)


        def equivalence_vg(self):
            return self.getTypedRuleContext(SwumParser.Equivalence_vgContext,0)


        def getRuleIndex(self):
            return SwumParser.RULE_equivalence

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEquivalence" ):
                listener.enterEquivalence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEquivalence" ):
                listener.exitEquivalence(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEquivalence" ):
                return visitor.visitEquivalence(self)
            else:
                return visitor.visitChildren(self)




    def equivalence(self):

        localctx = SwumParser.EquivalenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_equivalence)
        try:
            self.state = 57
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [SwumParser.Noun_Modifier, SwumParser.Noun]:
                self.enterOuterAlt(localctx, 1)
                self.state = 55
                self.equivalence_np()
                pass
            elif token in [SwumParser.Verb_Modifier, SwumParser.Verb]:
                self.enterOuterAlt(localctx, 2)
                self.state = 56
                self.equivalence_vg()
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


    class Equivalence_npContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def noun_phrase(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SwumParser.Noun_phraseContext)
            else:
                return self.getTypedRuleContext(SwumParser.Noun_phraseContext,i)


        def getRuleIndex(self):
            return SwumParser.RULE_equivalence_np

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEquivalence_np" ):
                listener.enterEquivalence_np(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEquivalence_np" ):
                listener.exitEquivalence_np(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEquivalence_np" ):
                return visitor.visitEquivalence_np(self)
            else:
                return visitor.visitChildren(self)




    def equivalence_np(self):

        localctx = SwumParser.Equivalence_npContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_equivalence_np)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 59
                self.noun_phrase()
                self.state = 62 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==SwumParser.Noun_Modifier or _la==SwumParser.Noun):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Equivalence_vgContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def verb_group(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SwumParser.Verb_groupContext)
            else:
                return self.getTypedRuleContext(SwumParser.Verb_groupContext,i)


        def getRuleIndex(self):
            return SwumParser.RULE_equivalence_vg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEquivalence_vg" ):
                listener.enterEquivalence_vg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEquivalence_vg" ):
                listener.exitEquivalence_vg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEquivalence_vg" ):
                return visitor.visitEquivalence_vg(self)
            else:
                return visitor.visitChildren(self)




    def equivalence_vg(self):

        localctx = SwumParser.Equivalence_vgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_equivalence_vg)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 64
                self.verb_group()
                self.state = 67 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==SwumParser.Verb_Modifier or _la==SwumParser.Verb):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





