"""Implementation of SWUM phrases layer"""

import sys
import subprocess
from typing import *    # for type annotations
from collections import namedtuple
from dataclasses import dataclass, field
import copy

from antlr4 import *
from antlr.SwumParser import SwumParser
from antlr.SwumParserVisitor import SwumParserVisitor
from antlr.SwumLexer import SwumLexer
from enum import Enum, auto

from lxml import etree

# TODO: support special cases for boolean type examples

# key is classname, value is metadata for that class
class_dict = {}

tag_map = {'CC':"CJ", 'CD':"D", "DT":"DT", "EX":"N", "FW":"N", "IN":"P", "JJ":"NM", "JJR":"NM", "JJS":"NM", "LS":"N", "MD":"V", "NN":"N", "NNS":"NPL", "NNP":"N", "NNPS":"NPL", "PDT":"DT", "POS":"N", "PRP":"P", "PRP$":"P", "RB":"VM", "RBR":"VM", "RBS":"VM", "RP":"N", "SYM":"N", "TO":"P", "UH":"N", "VB":"V", "VBD":"V", "VBG":"V", "VBN":"V", "VBP":"V", "VBZ":"V", "WDT":"DT", "WP":"P", "WP,":"P", "WRB":"VM"
}

SwumToken = namedtuple('SwumToken', 'literal pos_tag')

class SwumAttrRule(Enum):
    """Annotation rule for identifier"""
    verb_default = auto()
    verb_preposition = auto()
    verb_checker = auto()
    general = auto()    # event-driven
    event_handler = auto()
    starts_with_prep0 = auto()  # (on, before, after)
    noun_phrase_void = auto()
    starts_with_prep1 = auto()  # (to, from)
    starts_with_prep_default = auto()
    noun_phrase_non_void = auto()
    constructor = auto()
    all_preamble = auto()

@dataclass
class SwumMetadata():
    """Program-level and natural language information read from input file per identifier"""
    location: str = None
    name: str = None
    tokens: List[SwumToken] = field(default_factory=list)
    class_tokens: List[SwumToken] = field(default_factory=list)
    type_tokens: List[SwumToken] = field(default_factory=list)
    parameter_tokens: List[List[SwumToken]] = field(default_factory=list)

    def is_void(self) -> bool:
        return len(self.type_tokens) == 1 and self.type_tokens[0].literal == 'void'

class SwumPhrasesNode():
    """Node on phrasal tree"""
    def __init__(self, antlr_ctx=None, literal=None, token: SwumToken = None, tokens: List[SwumToken] = None, metadata: SwumMetadata = None):
        self.antlr_ctx = None
        self.literal = literal
        self.metadata = metadata
        self.is_terminal = None
        self.token = token
        self.tokens = tokens
        self.node_type = None
        self.edges: List[SwumPhrasesEdge] = []

        if antlr_ctx:
            self.configFromAntlrCtx(antlr_ctx)

    def configFromAntlrCtx(self, antlr_ctx):
        """Initialize phrasal tree node from ANTLR parse tree"""
        self.antlr_ctx = antlr_ctx
        self.is_terminal = antlr_ctx.getChildCount() == 0

        if self.is_terminal:
            self.node_type = SwumLexer.symbolicNames[self.antlr_ctx.symbol.type].lower()
        else:
            self.node_type = SwumParser.ruleNames[self.antlr_ctx.getRuleIndex()].lower()

        self.edges: List[SwumPhrasesEdge] = []

        if not self.is_terminal:
            self.buildSubtrees()
    
    def addEdge(self, node, label: str = None):
        new_edge = SwumPhrasesEdge(child=node, label=label)
        self.edges.append(new_edge)
    
    def buildSubtrees(self):
        """"Recursively build child nodes using context from the ANTLR parse tree"""
        for child_ctx in self.antlr_ctx.getChildren():
            new_node = SwumPhrasesNode(antlr_ctx=child_ctx)
            self.edges.append(SwumPhrasesEdge(new_node))

    def get_attr_rule(self, metadata: SwumMetadata):
        """Returns the appropriate rule for annotating this phrasal node based on its metadata"""
        if metadata is None:
            return None
        
        if metadata.location == 'constructor':
            return SwumAttrRule.constructor
        elif metadata.location == 'function':
            last_pos = self.tokens[-1].pos_tag
            if self.literal and self.literal.lower() in ['main', 'run'] or last_pos in ['VBD', 'VBG']:
                return SwumAttrRule.general

            # TODO: detect event handlers by looking at parameter types

            first_child = self.getChild(0)
            
            if first_child.node_type in ['verb_phrase', 'verb_group']:
                if self.containsNode('prepositional_phrase'):
                    return SwumAttrRule.verb_preposition
                elif self.tokens[0].pos_tag in ['VBZ', 'MD']:
                    return SwumAttrRule.verb_checker
                else:
                    return SwumAttrRule.verb_default

            if first_child.node_type == 'noun_phrase':
                if metadata.is_void():
                    return SwumAttrRule.noun_phrase_void
                else:
                    return SwumAttrRule.noun_phrase_non_void

            if first_child.node_type == 'prepositional_phrase':
                leading_prep = self.tokens[0].literal.lower()
                if leading_prep in ['on', 'before', 'after']:
                    return SwumAttrRule.starts_with_prep0
                elif leading_prep in ['to', 'from']:
                    return SwumAttrRule.starts_with_prep1
                else:
                    return SwumAttrRule.starts_with_prep_default

        return None

    def associateWords(self, tokens: List[SwumToken], head=True):
        """Recursively associates each token from tokens with the appropriate leaf node on this phrasal tree
        
        Preserves the input token list"""
        
        # make copy to preserve initial input tokens
        if head:
            tokens = list(tokens)
            self.tokens = list(tokens)
        
        if self.is_terminal:
            self.token = tokens.pop(0)
        else:
            for edge in self.edges:
                child = edge.child
                child.associateWords(tokens, False)

    def getChild(self, index):
        """Returns the indexth direct child of this phrasal node"""
        if (index > len(self.edges)):
            fail('Index {} is out of bounds')
        for idx, edge in enumerate(self.edges):
            if idx == index:
                return edge.child

    # Returns true if phrase subtree contains a node of type NodeType
    def containsNode(self, node_type: str):
        """Returns true if and only if phrasal subtree contains a node x where x.node_type == node_type"""
        if self.node_type == node_type:
            return True

        for edge in self.edges:
            child = edge.child
            if child.containsNode(node_type):
                return True

        return False

    def subtreeNodes(self):
        yield self
        for edge in self.edges:
            yield from edge.child.subtreeNodes()

    def annotated(self) -> 'SwumPhrasesNode':
        """Returns a copy of self annotated according to the rule determined by this node's metadata"""
        # head noun
        for node in self.subtreeNodes():
            if node.node_type == 'noun_phrase':
                for edge in node.edges:
                    if edge.child.node_type == 'noun':
                        edge.label = 'head_noun'
                        break

        # ignorable verbs
        for node in self.subtreeNodes():
            if node.node_type == 'verb_phrase':
                last_node = None
                for index, edge in enumerate(node.edges):
                    if edge.child.node_type == 'verb' and last_node is not None and last_node.node_type == 'verb':
                        node.edges[index-1].label = 'ignorable_verb'
                    last_node = edge.child

        
        attr_rule = self.get_attr_rule(self.metadata)

        if attr_rule is None:
            return self

        swum_phrase = SwumPhrasesNode(literal=self.metadata.name, metadata=self.metadata)

        if attr_rule == SwumAttrRule.verb_default:
            # starts with VG
            swum_phrase.node_type = 'verb_phrase'
            first_child = self.getChild(0)

            # identify action and theme
            if first_child.node_type == 'verb_phrase':
                # VP -> VG NP PP?
                swum_phrase.addEdge(first_child.getChild(0), 'action')
                swum_phrase.addEdge(first_child.getChild(1), 'theme')
            else:
                # VG -> VM* V+ VPR?
                swum_phrase.addEdge(first_child, 'action')
                
                if len(self.edges) > 1:
                    swum_phrase.addEdge(self.getChild(1), 'theme')
                elif len(self.metadata.parameter_tokens) > 0:
                    swum_phrase.addEdge(get_swum_phrase(self.metadata.parameter_tokens.pop(0)), 'theme')
                else:
                    swum_phrase.addEdge(get_swum_phrase(self.metadata.class_tokens), 'theme')
                
            # identify aux args
            # formal parameters
            for parameter_tokens in self.metadata.parameter_tokens:
                swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.addEdge(get_swum_phrase(self.metadata.type_tokens), 'aux_arg')
            # class
            if len(self.metadata.class_tokens) > 0:
                swum_phrase.addEdge(get_swum_phrase(self.metadata.class_tokens), 'aux_arg')
        elif attr_rule == SwumAttrRule.verb_preposition:
            # starts with VG, contains PP
            swum_phrase.node_type = 'verb_phrase'

            # identify action and theme
            first_child = self.getChild(0)
            if first_child.node_type == 'verb_phrase':
                # VP -> VG NP PP?
                swum_phrase.addEdge(first_child.getChild(0), 'action')
                swum_phrase.addEdge(first_child.getChild(1), 'theme')

                # secondary args
                if len(first_child.edges) == 3:
                    # VP -> VG NP PP
                    swum_phrase.addEdge(first_child.getChild(2), 'secondary_arg')
                else:
                    # VP -> VG NP
                    # look for preposition in remainder of identifier
                    for edge in self.edges:
                        if edge.child.node_type == 'prepositional_phrase':
                            swum_phrase.addEdge(edge.child, 'secondary_arg')
                            break
            else:
                # VG -> VM* V+ VPR?
                swum_phrase.addEdge(first_child, 'action')
                
                # look in rest of name prior to preposition
                if len(self.edges) > 1:
                    second_child = self.getChild(1)
                    if second_child.node_type != 'prepositional_phrase':
                        swum_phrase.addEdge(second_child, 'theme')
                else:   # class
                    if len(self.metadata.class_tokens) > 0:
                        swum_phrase.addEdge(get_swum_phrase(self.metadata.class_tokens), 'theme')

                # secondary args
                for edge in self.edges:
                    if edge.child.node_type == 'prepositional_phrase':
                        swum_phrase.addEdge(edge.child, 'secondary_arg')
                        break


            # identify aux args
            # formal parameters
            for parameter_tokens in self.metadata.parameter_tokens:
                swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.addEdge(get_swum_phrase(self.metadata.type_tokens), 'aux_arg')
            # class
            if len(self.metadata.class_tokens) > 0:
                swum_phrase.addEdge(get_swum_phrase(self.metadata.class_tokens), 'aux_arg')
        elif attr_rule == SwumAttrRule.verb_checker:
            # starts with VG
            swum_phrase.node_type = 'verb_phrase'

            first_child = self.getChild(0)
            # identify action and theme
            if first_child.node_type == 'verb_phrase':
                # VP -> VG NP PP?
                swum_phrase.addEdge(first_child.getChild(0), 'condition')
                swum_phrase.addEdge(first_child.getChild(1), 'condition')
            else:
                # VG -> VM* V+ VPR?
                swum_phrase.addEdge(first_child, 'condition')

                if len(self.edges) > 1:
                    swum_phrase.addEdge(self.getChild(1), 'condition')
                elif len(self.metadata.parameter_tokens) > 0:
                    swum_phrase.addEdge(get_swum_phrase(self.metadata.parameter_tokens.pop(0)), 'condition')
                else:
                    swum_phrase.addEdge(get_swum_phrase(self.metadata.class_tokens), 'condition')
                
            # identify secondary args
            # class
            if len(self.metadata.class_tokens) > 0:
                swum_phrase.addEdge(get_swum_phrase(self.metadata.class_tokens), 'subject')

            # identify aux args
            # formal parameters
            for parameter_tokens in self.metadata.parameter_tokens:
                swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'subject')
        elif attr_rule in [SwumAttrRule.general, SwumAttrRule.event_handler, SwumAttrRule.starts_with_prep0, SwumAttrRule.noun_phrase_void]:
            swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='handle', pos_tag='VBZ')]), 'action')
            # if identifier parses into multiple phrases, have multiple themes
            for edge in self.edges:
                swum_phrase.addEdge(edge.child, 'theme')
            
            # identify aux args
            # formal parameters
            for parameter_tokens in self.metadata.parameter_tokens:
                swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.addEdge(get_swum_phrase(self.metadata.type_tokens), 'aux_arg')
            # class
            if len(self.metadata.class_tokens) > 0:
                swum_phrase.addEdge(get_swum_phrase(self.metadata.class_tokens), 'aux_arg')
        elif attr_rule in [SwumAttrRule.starts_with_prep1, SwumAttrRule.starts_with_prep_default]:
            swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='convert', pos_tag='VBZ')]), 'action')
            # if identifier parses into multiple phrases, have multiple secondary args
            for edge in self.edges:
                swum_phrase.addEdge(edge.child, 'secondary_arg')
            
            # identify aux args
            # formal parameters
            for parameter_tokens in self.metadata.parameter_tokens:
                swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.addEdge(get_swum_phrase(self.metadata.type_tokens), 'aux_arg')
            # class
            if len(self.metadata.class_tokens > 0):
                swum_phrase.addEdge(get_swum_phrase(self.metadata.class_tokens), 'aux_arg')
        elif attr_rule == SwumAttrRule.noun_phrase_non_void:
            swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='get', pos_tag='VBZ')]), 'action')
            # if identifier parses into multiple phrases, have multiple themes
            for edge in self.edges:
                swum_phrase.addEdge(edge.child, 'theme')
            
            # identify aux args
            # formal parameters
            for parameter_tokens in self.metadata.parameter_tokens:
                swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.addEdge(get_swum_phrase(self.metadata.type_tokens), 'aux_arg')
            # class
            if len(self.metadata.class_tokens) > 0:
                swum_phrase.addEdge(get_swum_phrase(self.metadata.class_tokens), 'aux_arg')
        elif attr_rule == SwumAttrRule.constructor:
            swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='create', pos_tag='VBZ')]), 'action')
            swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='construct', pos_tag='VBZ')]), 'action')
            # if identifier parses into multiple phrases, have multiple themes
            for edge in self.edges:
                swum_phrase.addEdge(edge.child, 'theme')
            
            # identify aux args
            # formal parameters
            for parameter_tokens in self.metadata.parameter_tokens:
                swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
        elif attr_rule == SwumAttrRule.all_preamble:
            fail('Error: preambles are not yet supported')
        else:
            fail('Error: did not recognize rule for phrase tree')

        return swum_phrase


    def __str__(self):
        """Returns output in XML format"""
        str_repr = ''

        if self.node_type != 'swum_phrase':
            str_repr += '<{}>'.format(self.node_type)

        if self.is_terminal:
            str_repr += self.token.literal
        else:
            for swum_phrases_edge in self.edges:                
                if swum_phrases_edge.label:
                    str_repr += '<{}>'.format(swum_phrases_edge.label)
                str_repr += '{}'.format(str(swum_phrases_edge.child))
                if swum_phrases_edge.label:
                    str_repr += '</{}>'.format(swum_phrases_edge.label)

        if self.node_type != 'swum_phrase':
            str_repr += '</{}>'.format(self.node_type)

        return str_repr

@dataclass
class SwumPhrasesEdge():
    """Edge on phrasal tree. May be annotated with a label"""
    child: SwumPhrasesNode = None
    label: str = None


def main(argv):    
    input_filename = argv[1]
    output_filename = argv[2]
    output_f = open(output_filename, 'w')
    with open(input_filename, 'rb') as f:
        for _, element in etree.iterparse(f, tag='swum_identifier', remove_blank_text=True):
            if element.getparent().tag != 'swum_identifiers': # only process nested identifiers recursively
                continue
            
            metadata = get_metadata(element)
            if metadata.location == 'class':
                # add to class dict to resolve later
                class_dict[metadata.name] = metadata
                swum_phrase = get_swum_phrase(metadata.tokens, metadata=metadata)
                print(swum_phrase, file=output_f)
            elif metadata.location == 'function':
                # annotate
                swum_phrase = get_swum_phrase(metadata.tokens, metadata=metadata)
                print(swum_phrase, file=output_f)

            element.clear(keep_tail=True)      

def fail(error: str, err_code: int = 1):
    print(error, file=sys.stderr)
    sys.exit(err_code)


def get_swum_phrase(tokens: List[SwumToken], metadata: SwumMetadata = None):
    """Returns a phrasal tree based on the input tokens and identifier metadata
    
    Keyword arguments:
    tokens -- list of consituent tokens for identifier
    metadata -- program-level and NL metadata for identifier
    annotate -- annotate semantic relationships in phrasal tree if True (default False)
    """
    swum_pos_tokens = penn_tags_to_swum([swum_token.pos_tag for swum_token in tokens])
    tree = get_parse_tree(InputStream(' '.join(swum_pos_tokens)))
    visitor = SwumVisitor()
    swum_phrase = visitor.visit(tree)
    swum_phrase.associateWords(tokens)
    swum_phrase.metadata = metadata

    swum_phrase = swum_phrase.annotated()
    
    return swum_phrase

def get_parse_tree(input_stream):
    """Returns the raw ANTLR parse tree for input_stream based on SWUM grammar"""
    lexer = SwumLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SwumParser(stream)
    tree = parser.swum_phrase()

    return tree

def penn_tags_to_swum(pos_tokens:List[str]):
    """Converts POS tags from Penn tagset to SWUM's simplified tagset"""
    # assume nouns preceding nouns are noun-modifiers
    swum_tags = [tag_map[penn_tag] for penn_tag in pos_tokens]
    last_tag = None
    for index, tag in enumerate(swum_tags):
        if last_tag == 'N' and tag == 'N':
            swum_tags[index-1] = 'NM'
        last_tag = tag
    
    return swum_tags

def get_metadata(element) -> SwumMetadata:
    """Returns the extracted metadata object from a <swum_identifier> XML node in input"""
    metadata = SwumMetadata()
    for child in element:
        if child.tag == 'location':
            metadata.location = child.text.strip()
        elif child.tag == 'name':
            metadata.name = child.text.strip()
        elif child.tag == 'class':
            # resolve class name to class metadata, add to this identifier's metadata
            class_metadata = class_dict[child.text.strip()]
            metadata.class_tokens = class_metadata.tokens
        elif child.tag == 'type':
            type_metadata = get_metadata(child[0])
            metadata.type_tokens = type_metadata.tokens
        elif child.tag == 'parameters':
            for parameter_node in child:
                parameter_metadata = get_metadata(parameter_node)
                metadata.parameter_tokens.append(parameter_metadata.tokens)
        elif child.tag == 'identifier':
            for word_node in child:
                pos_node = word_node[0]
                new_token = SwumToken(word_node.text.strip(), pos_node.text.strip())
                metadata.tokens.append(new_token)

    if metadata.name is None:
        fail('a swum identifier is missing name')
    elif metadata.location is None:
        fail('{} is missing location'.format(metadata.name))
    elif metadata.location == 'function' and len(metadata.type_tokens) == 0:
        fail('{} is missing type'.format(metadata.name))
    
    return metadata


class SwumVisitor(SwumParserVisitor):
    """Override ANTLR's default traversal of parse tree to support custom phrasal tree"""
    def visitSwum_phrase(self, ctx:SwumParser.Swum_phraseContext):
        return SwumPhrasesNode(antlr_ctx=ctx)

if __name__ == '__main__':
    main(sys.argv)
