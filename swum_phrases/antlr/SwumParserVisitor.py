# Generated from SwumParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SwumParser import SwumParser
else:
    from SwumParser import SwumParser

# This class defines a complete generic visitor for a parse tree produced by SwumParser.

class SwumParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SwumParser#start.
    def visitStart(self, ctx:SwumParser.StartContext):
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



del SwumParser