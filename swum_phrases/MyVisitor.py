from antlr4 import *
from SwumParser import SwumParser
from SwumParserVisitor import SwumParserVisitor
from SwumLexer import SwumLexer

# This class defines a complete generic visitor for a parse tree produced by SwumParser.

class PrintVisitor(SwumParserVisitor):

    def __init__(self, tokens):
        self.tokens = tokens
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
        # self.ds = CustomNodeType(ctx, self.tokens, visible=False)   # set root to be invisible (want to output graph, not tree)
        self.ds = CustomNodeType(ctx.getChild(0), self.tokens)

# custom data structure to use internally after reading in antlr tree
class CustomNodeType():
    def __init__(self, antlrCtx, tokens, visible=True):
        self.antlrCtx = antlrCtx
        self.tokens = tokens
        self.visible = visible

        self.isTerminal = antlrCtx.getChildCount() == 0
        self.isRoot = SwumParser.ruleNames[antlrCtx.parentCtx.getRuleIndex()] == 'phrase'

        if self.visible:
            if self.isTerminal:
                self.nodeType = SwumLexer.symbolicNames[self.antlrCtx.symbol.type]
            else:
                self.nodeType = SwumParser.ruleNames[self.antlrCtx.getRuleIndex()]
            
        self.metadata = {}
        self.children = []

        if not self.isTerminal:
            self.buildSubtrees()
        
        self.buildMetadata()    # do on traversal up the tree to support synthesized attributes (e.g. NP identifier being concatenation of NM and N words)

    def buildSubtrees(self):
        for childCtx in self.antlrCtx.getChildren():
            newNode = CustomNodeType(childCtx, self.tokens)
            self.children.append(newNode)

    def buildMetadata(self):
        # assumes input is well-formed XML with a "name" field containing the word literal for each POS tag
        token_index = self.antlrCtx.start.tokenIndex if self.antlrCtx.getChildCount() > 0 else self.antlrCtx.symbol.tokenIndex
        new_metadata = self.tokens.getHiddenTokensToLeft(token_index, SwumLexer.METADATA)
        i = 0
        while i < len(new_metadata) - 1:
            if self.isRoot or new_metadata[i].text == 'name':
                self.metadata[new_metadata[i].text] = new_metadata[i+1].text
            i += 2

        # synthesize identifier names for nonterminal nodes
        if not self.isTerminal:
            self.metadata['name'] = ''
            for child in self.children:
                self.metadata['name'] += child.metadata['name']

    def __str__(self):
        str_repr = ''
        if self.visible:
            str_repr += '<{}>'.format(self.nodeType)
            if self.isTerminal:
                str_repr += self.metadata['name']
            else:
                for key, value in self.metadata.items():
                    str_repr += '<{key}>{val}</{key}>'.format(key=key, val=value)
            
        
        for child in self.children:                
            str_repr += '{}'.format(str(child))

        if self.visible:
            str_repr += '</{}>'.format(self.nodeType)
        return str_repr
