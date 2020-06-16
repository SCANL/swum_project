from antlr4 import *
# if __name__ is not None and "." in __name__:
#     from .SwumParser import SwumParser
# else:
from SwumParser import SwumParser
from SwumParserVisitor import SwumParserVisitor
from SwumLexer import SwumLexer

# hide start rule from xml output
SwumParser.ruleNames[0] = None

# This class defines a complete generic visitor for a parse tree produced by SwumParser.

class PrintVisitor(SwumParserVisitor):

    def __init__(self, tokens):
        self.tokens = tokens
        self.str_output = ''
        self.ds = None
    
    # Visit a parse tree produced by SwumParser#noun_phrase.
    def visitNoun_phrase(self, ctx:SwumParser.Noun_phraseContext):
        pass

    # Visit a parse tree produced by SwumParser#prepositional_phrase.
    def visitPrepositional_phrase(self, ctx:SwumParser.Prepositional_phraseContext):
        pass


    # Visit a parse tree produced by SwumParser#verb_group.
    def visitVerb_group(self, ctx:SwumParser.Verb_groupContext):
        pass


    # Visit a parse tree produced by SwumParser#verb_phrase.
    def visitVerb_phrase(self, ctx:SwumParser.Verb_phraseContext):
        pass


    # Visit a parse tree produced by SwumParser#equivalence.
    def visitEquivalence(self, ctx:SwumParser.EquivalenceContext):
        pass


    # Visit a parse tree produced by SwumParser#equivalence_np.
    def visitEquivalence_np(self, ctx:SwumParser.Equivalence_npContext):
        pass


    # Visit a parse tree produced by SwumParser#equivalence_vg.
    def visitEquivalence_vg(self, ctx:SwumParser.Equivalence_vgContext):
        pass

    # Visit a parse tree produced by SwumParser#phrase.
    def visitPhrase(self, ctx:SwumParser.PhraseContext):
        self.ds = CustomNodeType(ctx, self.tokens)

    # def printParseSubTree(self, ctx):
    #     new_node = CustomNodeType(ctx)

    #     stop_token_index = ctx.stop.tokenIndex
    #     new_metadata = self.tokens.getHiddenTokensToLeft(stop_token_index, SwumLexer.METADATA)
    #     num_metadata = len(new_metadata)
    #     assert num_metadata % 2 == 0   # imperfect guard against empty XML tags (TODO: improve this)
    #     i = 0
    #     while i < num_metadata - 1:
    #         new_node.metadata[new_metadata[i].text] = new_metadata[i+1].text
    #         i += 2

    #     self.ds.insert(new_node)

    #     self.str_output += '{}('.format(new_node.nodeType)
    #     for index, child in enumerate(ctx.getChildren()):
    #         if index != 0:
    #             self.str_output += ' '
    #         if child.getChildCount() == 0:    # terminal node
    #             self.str_output += child.getText()
    #         else:
    #             self.visit(child)
    #     self.str_output += ')'


# custom data structure to use internally after reading in antlr tree
class CustomNodeType():
    def __init__(self, antlrCtx, tokens):
        self.antlrCtx = antlrCtx
        self.tokens = tokens
        if self.antlrCtx.getChildCount() > 0:   # nonterminal node
            self.nodeType = SwumParser.ruleNames[self.antlrCtx.getRuleIndex()]
        else:   # terminal node
            self.nodeType = SwumLexer.symbolicNames[self.antlrCtx.symbol.type]

        self.metadata = {}
        self.children = []

        if self.antlrCtx.getChildCount() > 0:   # nonterminal node
            self.buildSubtrees()
        
        self.buildMetadata()    # do on traversal up the tree to support synthesized attributes (e.g. NP identifier being concatenation of NM and N words)

    def buildSubtrees(self):
        for childCtx in self.antlrCtx.getChildren():
            newNode = CustomNodeType(childCtx, self.tokens)
            self.children.append(newNode)

    def buildMetadata(self):
        token_index = self.antlrCtx.start.tokenIndex if self.antlrCtx.getChildCount() > 0 else self.antlrCtx.symbol.tokenIndex
        new_metadata = self.tokens.getHiddenTokensToLeft(token_index, SwumLexer.METADATA)
        num_metadata = len(new_metadata)
        assert num_metadata % 2 == 0   # imperfect guard against empty XML tags (TODO: improve this)
        i = 0
        while i < num_metadata - 1:
            self.metadata[new_metadata[i].text] = new_metadata[i+1].text
            i += 2

    def __str__(self):
        str_repr = ''
        if self.nodeType is not None:
            str_repr += '<{}>'.format(self.nodeType)
            if self.antlrCtx.getChildCount() > 0:
                for key, value in self.metadata.items():
                    if key == 'name':   # TODO: consider synthesizing names for nonterminals instead of omitting them
                        continue
                    str_repr += '<{key}>{val}</{key}>'.format(key=key, val=value)
            else:
                str_repr += self.metadata['name']
        
        for child in self.children:                
            str_repr += '{}'.format(str(child))

        if self.nodeType is not None:
            str_repr += '</{}>'.format(self.nodeType)
        return str_repr


# del SwumParser