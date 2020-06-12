# Generated from SwumParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SwumParser import SwumParser
else:
    from SwumParser import SwumParser

# This class defines a complete generic visitor for a parse tree produced by SwumParser.

class SwumParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SwumParser#phrase.
    def visitPhrase(self, ctx:SwumParser.PhraseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SwumParser#noun_phrase.
    def visitNoun_phrase(self, ctx:SwumParser.Noun_phraseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SwumParser#prepositional_phrase.
    def visitPrepositional_phrase(self, ctx:SwumParser.Prepositional_phraseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SwumParser#verb_group.
    def visitVerb_group(self, ctx:SwumParser.Verb_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SwumParser#verb_phrase.
    def visitVerb_phrase(self, ctx:SwumParser.Verb_phraseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SwumParser#equivalence.
    def visitEquivalence(self, ctx:SwumParser.EquivalenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SwumParser#equivalence_np.
    def visitEquivalence_np(self, ctx:SwumParser.Equivalence_npContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SwumParser#equivalence_vg.
    def visitEquivalence_vg(self, ctx:SwumParser.Equivalence_vgContext):
        return self.visitChildren(ctx)



del SwumParser