from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SwumParser import SwumParser
else:
    from SwumParser import SwumParser
from SwumVisitor import SwumVisitor

# This class defines a complete generic visitor for a parse tree produced by SwumParser.

class PrintVisitor(SwumVisitor):

    def __init__(self):
        self.str_output = ''
        self.ds = None
    
    # Visit a parse tree produced by SwumParser#noun_phrase.
    def visitNoun_phrase(self, ctx:SwumParser.Noun_phraseContext):
        self.printParseSubTree('NP', ctx)

    # Visit a parse tree produced by SwumParser#prepositional_phrase.
    def visitPrepositional_phrase(self, ctx:SwumParser.Prepositional_phraseContext):
        self.printParseSubTree('PP', ctx)


    # Visit a parse tree produced by SwumParser#verb_group.
    def visitVerb_group(self, ctx:SwumParser.Verb_groupContext):
        self.printParseSubTree('VG', ctx)


    # Visit a parse tree produced by SwumParser#verb_phrase.
    def visitVerb_phrase(self, ctx:SwumParser.Verb_phraseContext):
        self.printParseSubTree('VP', ctx)


    # Visit a parse tree produced by SwumParser#equivalence.
    def visitEquivalence(self, ctx:SwumParser.EquivalenceContext):
        self.printParseSubTree('EQ', ctx)


    # Visit a parse tree produced by SwumParser#equivalence_np.
    def visitEquivalence_np(self, ctx:SwumParser.Equivalence_npContext):
        self.printParseSubTree('EQ_np', ctx)


    # Visit a parse tree produced by SwumParser#equivalence_vg.
    def visitEquivalence_vg(self, ctx:SwumParser.Equivalence_vgContext):
        self.printParseSubTree('EQ_vg', ctx)


    # Visit a parse tree produced by SwumParser#phrase.
    def visitPhrase(self, ctx:SwumParser.PhraseContext):
        self.ds = CustomTree(ctx, 'Phrase')
        return self.visitChildren(ctx)

    def printParseSubTree(self, string:str, ctx):
        self.ds.insert(ctx, ctx.parentCtx, string)
        self.str_output += '{}('.format(string)
        for index, child in enumerate(ctx.getChildren()):
            if index != 0:
                self.str_output += ' '
            if child.getChildCount() == 0:    # terminal node
                self.str_output += child.getText()
            else:
                self.visit(child)
        self.str_output += ')'


# custom data structure to use internally after reading in antlr tree
class CustomTree():
    def __init__(self, antlr_ctx=None, str_repr=''):
        self.antlr_ctx = antlr_ctx # useful for finding parent node to insert under
        self.str_repr = str_repr
        self.children = []
        # TODO: add more fields (like POS tag)

    def insert(self, ctx, parent_ctx, string):
        if parent_ctx == self.antlr_ctx:
            self.children.append(CustomTree(ctx, string))
        else:
            for child in self.children:
                child.insert(ctx, parent_ctx, string)

    def __str__(self):
        str_repr = self.str_repr
        for child in self.children:
            str_repr += ' ' + str(child)
        return str_repr


del SwumParser