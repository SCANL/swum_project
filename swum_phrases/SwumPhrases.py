import sys
from typing import *    # for type annotations
from collections import namedtuple

from antlr4 import *
from SwumParser import SwumParser
from SwumParserVisitor import SwumParserVisitor
from SwumLexer import SwumLexer
from enum import Enum, auto

def main(argv):
    # do example
    method_pos_tokens = ['V']
    method_tokens = ['do']
    class_pos_tokens = ['NM', 'N']
    class_tokens = ['my', 'class']
    type_pos_tokens = ['N']
    type_tokens = ['void']
    parameter_pos_tokens = []
    parameter_tokens = []

    # # doThing example
    # method_pos_tokens = ['V', 'N']
    # method_tokens = ['do', 'thing']
    # class_pos_tokens = ['NM', 'N']
    # class_tokens = ['my', 'class']
    # type_pos_tokens = ['N']
    # type_tokens = ['void']
    # parameter_pos_tokens = []
    # parameter_tokens = []


    method_pos_stream = ' '.join(method_pos_tokens)
    swum_phrase = getSwumPhrase(InputStream(method_pos_stream), method_tokens)

    # identify rule
    attr_rule = SwumAttrRule.verb_default

    # label attributes (and modify phrase tree as necessary)
    if attr_rule == SwumAttrRule.verb_default:
        # starts with VG

        # identify action and theme
        if len(swum_phrase.edges) > 1:
            # VP -> VG NP PP?
            swum_phrase.edges[0].label = 'action'
            swum_phrase.edges[1].label = 'theme'
        else:
            # VG
            # construct VP node, add VG under it
            vp = SwumPhrasesNode()
            vp.nodeType = 'verb_phrase'
            vp.addEdge(swum_phrase, 'action')
            swum_phrase = vp

            if len(parameter_tokens) > 0:
                node = getSwumPhrase(InputStream(' '.join(parameter_pos_tokens.pop(0))), parameter_tokens.pop(0))
                swum_phrase.addEdge(node, 'theme')
            else:
                # copy class tokens to new list in order to preserve them for 
                node = getSwumPhrase(InputStream(' '.join(class_pos_tokens)), class_tokens)
                swum_phrase.addEdge(node, 'theme')
            
        # identify secondary args
        # none for verb_default

        # identify aux args
        # formal parameters
        for index, pos_tokens in enumerate(parameter_pos_tokens):
            node = getSwumPhrase(InputStream(' '.join(pos_tokens)), parameter_tokens[index])
            swum_phrase.addEdge(node, 'aux_arg')
        # return type
        if len(type_tokens) == 1 and type_tokens[0] == 'void':
            pass
        else:
            node = getSwumPhrase(InputStream(' '.join(type_pos_tokens)), type_tokens)
            swum_phrase.addEdge(node, 'aux_arg')
        # class
        node = getSwumPhrase(InputStream(' '.join(class_pos_tokens)), class_tokens)
        swum_phrase.addEdge(node, 'aux_arg')

    print(swum_phrase)

class SwumAttrRule(Enum):
    verb_default = auto()
    verb_preposition = auto()
    verb_checker = auto()
    general = auto()
    starts_with_prep = auto()
    noun_phrase_non_void = auto()
    constructor = auto()
    all_preamble = auto()

def getSwumPhrase(input_stream, tokens: List[str]):
    tree = getParseTree(input_stream)
    visitor = SwumVisitor()
    swum_phrase = visitor.visit(tree)
    swum_phrase.associateWords(tokens)

    return swum_phrase

def getParseTree(input_stream):
    lexer = SwumLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SwumParser(stream)
    tree = parser.start()

    return tree

# custom data structure to use internally after reading in antlr tree
class SwumPhrasesNode():
    def __init__(self, antlrCtx = None):
        self.antlrCtx = None
        self.isTerminal = None
        self.word = None
        self.nodeType = None
        self.edges = None

        if antlrCtx:
            self.configFromAntlrCtx(antlrCtx)

    def configFromAntlrCtx(self, antlrCtx):
        self.antlrCtx = antlrCtx
        self.isTerminal = antlrCtx.getChildCount() == 0
        self.word = None

        if self.isTerminal:
            self.nodeType = SwumLexer.symbolicNames[self.antlrCtx.symbol.type]
        else:
            self.nodeType = SwumParser.ruleNames[self.antlrCtx.getRuleIndex()]

        self.edges: List[SwumPhrasesEdge] = []

        if not self.isTerminal:
            self.buildSubtrees()
    
    def addEdge(self, node, label: str = None):
        new_edge = SwumPhrasesEdge(node)
        if label:
            new_edge.label = label

        if self.edges is None:
            self.edges: List[SwumPhrasesEdge] = []
        self.edges.append(new_edge)
    
    def buildSubtrees(self):
        for child_ctx in self.antlrCtx.getChildren():
            new_node = SwumPhrasesNode(child_ctx)
            self.edges.append(SwumPhrasesEdge(new_node))

    def associateWords(self, tokens: List[str], head=True):
        # make copy to preserve initial input tokens
        if head:
            tokens = list(tokens)
        
        if self.isTerminal:
            self.word = tokens.pop(0)
        else:
            for edge in self.edges:
                child = edge.child
                child.associateWords(tokens, False)


    def __str__(self):
        str_repr = ''

        str_repr += '<{}>'.format(self.nodeType)

        if self.isTerminal:
            str_repr += self.word
        else:
            for swum_phrases_edge in self.edges:                
                if swum_phrases_edge.label:
                    str_repr += '<{}>'.format(swum_phrases_edge.label)
                str_repr += '{}'.format(str(swum_phrases_edge.child))
                if swum_phrases_edge.label:
                    str_repr += '</{}>'.format(swum_phrases_edge.label)

        str_repr += '</{}>'.format(self.nodeType)

        return str_repr

class SwumPhrasesEdge():
    def __init__(self, child=None, label=None):
        self.child = child
        self.label = label

class SwumVisitor(SwumParserVisitor):
    # Visit a parse tree produced by SwumParser#start.
    def visitStart(self, ctx:SwumParser.StartContext):
        return SwumPhrasesNode(ctx.getChild(0))


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

if __name__ == '__main__':
    main(sys.argv)
