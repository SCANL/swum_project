from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SwumParser import SwumParser
else:
    from SwumParser import SwumParser
from SwumListener import SwumListener

class MyParseTreePrinter(SwumListener):
    def __init__(self):
        self.str_output = ''
    
    # Enter a parse tree produced by SwumParser#noun_phrase.
    def enterNoun_phrase(self, ctx:SwumParser.Noun_phraseContext):
        self.print_enter('NP')
        # self.str_output += '('
        num_children = ctx.getChildCount()
        for index, child in enumerate(ctx.getChildren()):
            self.str_output += child.getText()
            if index != num_children - 1:
                self.str_output += ' '
        # self.print_exit()

    # Exit a parse tree produced by SwumParser#noun_phrase.
    def exitNoun_phrase(self, ctx:SwumParser.Noun_phraseContext):
        self.print_exit()


    # Enter a parse tree produced by SwumParser#prepositional_phrase.
    def enterPrepositional_phrase(self, ctx:SwumParser.Prepositional_phraseContext):
        self.print_enter('PP')
        # self.str_output += '(' + ctx.getChild(0).getText()
        self.str_output += ctx.getChild(0).getText()
        
    # Exit a parse tree produced by SwumParser#prepositional_phrase.
    def exitPrepositional_phrase(self, ctx:SwumParser.Prepositional_phraseContext):
        # self.print_exit()   # close open paren from preposition
        self.print_exit()

    # Enter a parse tree produced by SwumParser#verb_group.
    def enterVerb_group(self, ctx:SwumParser.Verb_groupContext):
        self.print_enter('VG')
        # self.str_output += '('
        num_children = ctx.getChildCount()
        for index, child in enumerate(ctx.getChildren()):
            print(dir(child))
            self.str_output += child.getText()
            if index != num_children - 1:
                self.str_output += ' '
        # self.print_exit()

    # Exit a parse tree produced by SwumParser#verb_group.
    def exitVerb_group(self, ctx:SwumParser.Verb_groupContext):
        self.print_exit()


    # Enter a parse tree produced by SwumParser#verb_phrase.
    def enterVerb_phrase(self, ctx:SwumParser.Verb_phraseContext):
        self.print_enter('VP')

    # Exit a parse tree produced by SwumParser#verb_phrase.
    def exitVerb_phrase(self, ctx:SwumParser.Verb_phraseContext):
        self.print_exit()


    # Enter a parse tree produced by SwumParser#equivalence.
    def enterEquivalence(self, ctx:SwumParser.EquivalenceContext):
        self.print_enter('EQ')

    # Exit a parse tree produced by SwumParser#equivalence.
    def exitEquivalence(self, ctx:SwumParser.EquivalenceContext):
        self.print_exit()


    # Enter a parse tree produced by SwumParser#equivalence_np.
    def enterEquivalence_np(self, ctx:SwumParser.Equivalence_npContext):
        self.print_enter('EQ_np')

    # Exit a parse tree produced by SwumParser#equivalence_np.
    def exitEquivalence_np(self, ctx:SwumParser.Equivalence_npContext):
        self.print_exit()


    # Enter a parse tree produced by SwumParser#equivalence_vg.
    def enterEquivalence_vg(self, ctx:SwumParser.Equivalence_vgContext):
        self.print_enter('EQ_vg')

    # Exit a parse tree produced by SwumParser#equivalence_vg.
    def exitEquivalence_vg(self, ctx:SwumParser.Equivalence_vgContext):
        self.print_exit()

    def print_enter(self, string:str):
        # print('({}'.format(string), end='')
        self.str_output += ' {}('.format(string)

    def print_exit(self):
        # print(')', end='')
        self.str_output += ')'

del SwumParser