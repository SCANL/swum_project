# Generated from SwumParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SwumParser import SwumParser
else:
    from SwumParser import SwumParser

# This class defines a complete listener for a parse tree produced by SwumParser.
class SwumParserListener(ParseTreeListener):

    # Enter a parse tree produced by SwumParser#phrase.
    def enterPhrase(self, ctx:SwumParser.PhraseContext):
        pass

    # Exit a parse tree produced by SwumParser#phrase.
    def exitPhrase(self, ctx:SwumParser.PhraseContext):
        pass


    # Enter a parse tree produced by SwumParser#noun_phrase.
    def enterNoun_phrase(self, ctx:SwumParser.Noun_phraseContext):
        pass

    # Exit a parse tree produced by SwumParser#noun_phrase.
    def exitNoun_phrase(self, ctx:SwumParser.Noun_phraseContext):
        pass


    # Enter a parse tree produced by SwumParser#prepositional_phrase.
    def enterPrepositional_phrase(self, ctx:SwumParser.Prepositional_phraseContext):
        pass

    # Exit a parse tree produced by SwumParser#prepositional_phrase.
    def exitPrepositional_phrase(self, ctx:SwumParser.Prepositional_phraseContext):
        pass


    # Enter a parse tree produced by SwumParser#verb_group.
    def enterVerb_group(self, ctx:SwumParser.Verb_groupContext):
        pass

    # Exit a parse tree produced by SwumParser#verb_group.
    def exitVerb_group(self, ctx:SwumParser.Verb_groupContext):
        pass


    # Enter a parse tree produced by SwumParser#verb_phrase.
    def enterVerb_phrase(self, ctx:SwumParser.Verb_phraseContext):
        pass

    # Exit a parse tree produced by SwumParser#verb_phrase.
    def exitVerb_phrase(self, ctx:SwumParser.Verb_phraseContext):
        pass


    # Enter a parse tree produced by SwumParser#equivalence.
    def enterEquivalence(self, ctx:SwumParser.EquivalenceContext):
        pass

    # Exit a parse tree produced by SwumParser#equivalence.
    def exitEquivalence(self, ctx:SwumParser.EquivalenceContext):
        pass


    # Enter a parse tree produced by SwumParser#equivalence_np.
    def enterEquivalence_np(self, ctx:SwumParser.Equivalence_npContext):
        pass

    # Exit a parse tree produced by SwumParser#equivalence_np.
    def exitEquivalence_np(self, ctx:SwumParser.Equivalence_npContext):
        pass


    # Enter a parse tree produced by SwumParser#equivalence_vg.
    def enterEquivalence_vg(self, ctx:SwumParser.Equivalence_vgContext):
        pass

    # Exit a parse tree produced by SwumParser#equivalence_vg.
    def exitEquivalence_vg(self, ctx:SwumParser.Equivalence_vgContext):
        pass



del SwumParser