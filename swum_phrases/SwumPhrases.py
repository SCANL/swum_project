import sys
import subprocess
from typing import *    # for type annotations
from collections import namedtuple
from dataclasses import dataclass, field

from antlr4 import *
from antlr.SwumParser import SwumParser
from antlr.SwumParserVisitor import SwumParserVisitor
from antlr.SwumLexer import SwumLexer
from enum import Enum, auto

from lxml import etree

# TODO: support special cases for boolean type examples

# key is classname, value is metadata for that class
class_dict = {}

SwumToken = namedtuple('SwumToken', 'literal pos_tag')

class SwumAttrRule(Enum):
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
    location: str = None
    name: str = None
    tokens: List[SwumToken] = field(default_factory=list)
    class_tokens: List[SwumToken] = field(default_factory=list)
    type_tokens: List[SwumToken] = field(default_factory=list)
    parameter_tokens: List[List[SwumToken]] = field(default_factory=list)

    def is_void(self) -> bool:
        return len(self.type_tokens) == 1 and self.type_tokens[0].literal == 'void'

# custom data structure to use internally after reading in antlr tree
class SwumPhrasesNode():
    def __init__(self, antlr_ctx=None, literal=None, token: SwumToken = None, tokens: List[SwumToken] = None):
        self.antlrCtx = None
        self.literal = literal
        self.isTerminal = None
        self.token = token
        self.tokens = tokens
        self.nodeType = None
        self.edges = None

        if antlr_ctx:
            self.configFromAntlrCtx(antlr_ctx)

    def configFromAntlrCtx(self, antlrCtx):
        self.antlrCtx = antlrCtx
        self.isTerminal = antlrCtx.getChildCount() == 0
        self.literal = None

        if self.isTerminal:
            self.nodeType = SwumLexer.symbolicNames[self.antlrCtx.symbol.type].lower()
        else:
            self.nodeType = SwumParser.ruleNames[self.antlrCtx.getRuleIndex()].lower()

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
            new_node = SwumPhrasesNode(antlr_ctx=child_ctx)
            self.edges.append(SwumPhrasesEdge(new_node))

    def get_attr_rule(self, metadata: SwumMetadata):
        if metadata.location == 'constructor':
            return SwumAttrRule.constructor

        last_pos = self.tokens[-1].pos_tag
        if self.literal and self.literal.lower() in ['main', 'run'] or last_pos in ['VBD', 'VBG']:
            return SwumAttrRule.general

        # TODO: detect event handlers by looking at parameter types

        first_child = self.getChild(0)
        
        if first_child.nodeType in ['verb_phrase', 'verb_group']:
            if self.containsNode('prepositional_phrase'):
                return SwumAttrRule.verb_preposition
            elif self.tokens[0].pos_tag in ['VBZ', 'MD']:
                return SwumAttrRule.verb_checker
            else:
                return SwumAttrRule.verb_default

        if first_child.nodeType == 'noun_phrase':
            if metadata.is_void():
                return SwumAttrRule.noun_phrase_void
            else:
                return SwumAttrRule.noun_phrase_non_void

        if first_child.nodeType == 'prepositional_phrase':
            leading_prep = self.tokens[0].literal.lower()
            if leading_prep in ['on', 'before', 'after']:
                return SwumAttrRule.starts_with_prep0
            elif leading_prep in ['to', 'from']:
                return SwumAttrRule.starts_with_prep1
            else:
                return SwumAttrRule.starts_with_prep_default

        return None


    def associateWords(self, tokens: List[SwumToken], head=True):
        # make copy to preserve initial input tokens
        if head:
            tokens = list(tokens)
            self.tokens = list(tokens)
        
        if self.isTerminal:
            self.token = tokens.pop(0)
        else:
            for edge in self.edges:
                child = edge.child
                child.associateWords(tokens, False)

    def getChild(self, index):
        if (index > len(self.edges)):
            fail('Index {} is out of bounds')
        for idx, edge in enumerate(self.edges):
            if idx == index:
                return edge.child

    # Returns true if phrase subtree contains a node of type NodeType
    def containsNode(self, nodeType: str):
        if self.nodeType == nodeType:
            return True

        for edge in self.edges:
            child = edge.child
            if child.containsNode(nodeType):
                return True

        return False

    def __str__(self):
        str_repr = ''

        if self.nodeType != 'swum_phrase':
            str_repr += '<{}>'.format(self.nodeType)

        if self.isTerminal:
            str_repr += self.token.literal
        else:
            for swum_phrases_edge in self.edges:                
                if swum_phrases_edge.label:
                    str_repr += '<{}>'.format(swum_phrases_edge.label)
                str_repr += '{}'.format(str(swum_phrases_edge.child))
                if swum_phrases_edge.label:
                    str_repr += '</{}>'.format(swum_phrases_edge.label)

        if self.nodeType != 'swum_phrase':
            str_repr += '</{}>'.format(self.nodeType)

        return str_repr

@dataclass
class SwumPhrasesEdge():
    child: SwumPhrasesNode = None
    label: str = None


def main(argv):    
    filename = argv[1]
    with open(filename, 'rb') as f:
        for _, element in etree.iterparse(f, tag='swum_identifier', remove_blank_text=True):
            if element.getparent().tag != 'swum_identifiers':
                continue
            
            metadata = get_metadata(element)
            if metadata.location == 'class':
                # add to class dict to resolve later
                class_dict[metadata.name] = metadata
            elif metadata.location == 'function':
                # annotate
                swum_phrase = get_swum_phrase(metadata.tokens)
                swum_phrase = annotate(swum_phrase, metadata)
                print(swum_phrase)

            element.clear(keep_tail=True)        

def fail(error: str):
    print(error, file=sys.stderr)
    sys.exit(1)


def get_swum_phrase(tokens: List[SwumToken]):
    swum_pos_tokens = penn_tags_to_swum([swum_token.pos_tag for swum_token in tokens])
    tree = get_parse_tree(InputStream(' '.join(swum_pos_tokens)))
    visitor = SwumVisitor()
    swum_phrase = visitor.visit(tree)
    swum_phrase.associateWords(tokens)
    
    return swum_phrase

def get_parse_tree(input_stream):
    lexer = SwumLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SwumParser(stream)
    tree = parser.swum_phrase()

    return tree

def penn_tags_to_swum(pos_tokens:List[str]):
    tag_map = {'CC':"CJ", 'CD':"D", "DT":"DT", "EX":"N", "FW":"N", "IN":"P", "JJ":"NM", "JJR":"NM", "JJS":"NM", "LS":"N", "MD":"V", "NN":"N", "NNS":"NPL", "NNP":"N", "NNPS":"NPL", "PDT":"DT", "POS":"N", "PRP":"P", "PRP$":"P", "RB":"VM", "RBR":"VM", "RBS":"VM", "RP":"N", "SYM":"N", "TO":"P", "UH":"N", "VB":"V", "VBD":"V", "VBG":"V", "VBN":"V", "VBP":"V", "VBZ":"V", "WDT":"DT", "WP":"P", "WP,":"P", "WRB":"VM"
    }
    
    swum_tags = []
    for pos_token in pos_tokens:
        swum_tags.append(tag_map[pos_token])
    return swum_tags

# for <swum_identifier> xml node
def get_metadata(element) -> SwumMetadata:
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
    
    return metadata

def annotate(parsed_identifier: SwumPhrasesNode, metadata: SwumMetadata) -> SwumPhrasesNode:
    attr_rule = parsed_identifier.get_attr_rule(metadata)

    swum_phrase = SwumPhrasesNode(literal=metadata.name)

    # label attributes (and modify phrase tree as necessary)
    if attr_rule == SwumAttrRule.verb_default:
        # starts with VG
        swum_phrase.nodeType = 'verb_phrase'
        first_child = parsed_identifier.getChild(0)

        # identify action and theme
        if first_child.nodeType == 'verb_phrase':
            # VP -> VG NP PP?
            swum_phrase.addEdge(first_child.getChild(0), 'action')
            swum_phrase.addEdge(first_child.getChild(1), 'theme')
        else:
            # VG -> VM* V+ VPR?
            swum_phrase.addEdge(first_child, 'action')
            
            if len(parsed_identifier.edges) > 1:
                swum_phrase.addEdge(parsed_identifier.getChild(1), 'theme')
            elif len(metadata.parameter_tokens) > 0:
                swum_phrase.addEdge(get_swum_phrase(metadata.parameter_tokens.pop(0)), 'theme')
            else:
                swum_phrase.addEdge(get_swum_phrase(metadata.class_tokens), 'theme')
            
        # identify aux args
        # formal parameters
        for parameter_tokens in metadata.parameter_tokens:
            swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
        # return type
        if not metadata.is_void():
            swum_phrase.addEdge(get_swum_phrase(metadata.type_tokens), 'aux_arg')
        # class
        if len(metadata.class_tokens) > 0:
            swum_phrase.addEdge(get_swum_phrase(metadata.class_tokens), 'aux_arg')
    elif attr_rule == SwumAttrRule.verb_preposition:
        # starts with VG, contains PP
        swum_phrase.nodeType = 'verb_phrase'

        # identify action and theme
        first_child = parsed_identifier.getChild(0)
        if first_child.nodeType == 'verb_phrase':
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
                for edge in parsed_identifier.edges:
                    if edge.child.nodeType == 'prepositional_phrase':
                        swum_phrase.addEdge(edge.child, 'secondary_arg')
                        break
        else:
            # VG -> VM* V+ VPR?
            swum_phrase.addEdge(first_child, 'action')
            
            # look in rest of name prior to preposition
            if len(parsed_identifier.edges) > 1:
                second_child = parsed_identifier.getChild(1)
                if second_child.nodeType != 'prepositional_phrase':
                    swum_phrase.addEdge(second_child, 'theme')
            else:   # class
                if len(metadata.class_tokens) > 0:
                    swum_phrase.addEdge(get_swum_phrase(metadata.class_tokens), 'theme')

            # secondary args
            for edge in parsed_identifier.edges:
                if edge.child.nodeType == 'prepositional_phrase':
                    swum_phrase.addEdge(edge.child, 'secondary_arg')
                    break


        # identify aux args
        # formal parameters
        for parameter_tokens in metadata.parameter_tokens:
            swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
        # return type
        if not metadata.is_void():
            swum_phrase.addEdge(get_swum_phrase(metadata.type_tokens), 'aux_arg')
        # class
        if len(metadata.class_tokens) > 0:
            swum_phrase.addEdge(get_swum_phrase(metadata.class_tokens), 'aux_arg')
    elif attr_rule == SwumAttrRule.verb_checker:
        # starts with VG
        swum_phrase.nodeType = 'verb_phrase'

        first_child = parsed_identifier.getChild(0)
        # identify action and theme
        if first_child.nodeType == 'verb_phrase':
            # VP -> VG NP PP?
            swum_phrase.addEdge(first_child.getChild(0), 'condition')
            swum_phrase.addEdge(first_child.getChild(1), 'condition')
        else:
            # VG -> VM* V+ VPR?
            swum_phrase.addEdge(first_child, 'condition')

            if len(parsed_identifier.edges) > 1:
                swum_phrase.addEdge(parsed_identifier.getChild(1), 'condition')
            elif len(metadata.parameter_tokens) > 0:
                swum_phrase.addEdge(get_swum_phrase(metadata.parameter_tokens.pop(0)), 'condition')
            else:
                swum_phrase.addEdge(get_swum_phrase(metadata.class_tokens), 'condition')
            
        # identify secondary args
        # class
        if len(metadata.class_tokens) > 0:
            swum_phrase.addEdge(get_swum_phrase(metadata.class_tokens), 'subject')

        # identify aux args
        # formal parameters
        for parameter_tokens in metadata.parameter_tokens:
            swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'subject')
    elif attr_rule in [SwumAttrRule.general, SwumAttrRule.event_handler, SwumAttrRule.starts_with_prep0, SwumAttrRule.noun_phrase_void]:
        swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='handle', pos_tag='VBZ')]), 'action')
        # if identifier parses into multiple phrases, have multiple themes
        for edge in parsed_identifier.edges:
            swum_phrase.addEdge(edge.child, 'theme')
        
        # identify aux args
        # formal parameters
        for parameter_tokens in metadata.parameter_tokens:
            swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
        # return type
        if not metadata.is_void():
            swum_phrase.addEdge(get_swum_phrase(metadata.type_tokens), 'aux_arg')
        # class
        if len(metadata.class_tokens) > 0:
            swum_phrase.addEdge(get_swum_phrase(metadata.class_tokens), 'aux_arg')
    elif attr_rule in [SwumAttrRule.starts_with_prep1, SwumAttrRule.starts_with_prep_default]:
        swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='convert', pos_tag='VBZ')]), 'action')
        # if identifier parses into multiple phrases, have multiple secondary args
        for edge in parsed_identifier.edges:
            swum_phrase.addEdge(edge.child, 'secondary_arg')
        
        # identify aux args
        # formal parameters
        for parameter_tokens in metadata.parameter_tokens:
            swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
        # return type
        if not metadata.is_void():
            swum_phrase.addEdge(get_swum_phrase(metadata.type_tokens), 'aux_arg')
        # class
        if len(metadata.class_tokens > 0):
            swum_phrase.addEdge(get_swum_phrase(metadata.class_tokens), 'aux_arg')
    elif attr_rule == SwumAttrRule.noun_phrase_non_void:
        swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='get', pos_tag='VBZ')]), 'action')
        # if identifier parses into multiple phrases, have multiple themes
        for edge in parsed_identifier.edges:
            swum_phrase.addEdge(edge.child, 'theme')
        
        # identify aux args
        # formal parameters
        for parameter_tokens in metadata.parameter_tokens:
            swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
        # return type
        if not metadata.is_void():
            swum_phrase.addEdge(get_swum_phrase(metadata.type_tokens), 'aux_arg')
        # class
        if len(metadata.class_tokens) > 0:
            swum_phrase.addEdge(get_swum_phrase(metadata.class_tokens), 'aux_arg')
    elif attr_rule == SwumAttrRule.constructor:
        swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='create', pos_tag='VBZ')]), 'action')
        swum_phrase.addEdge(get_swum_phrase([SwumToken(literal='construct', pos_tag='VBZ')]), 'action')
        # if identifier parses into multiple phrases, have multiple themes
        for edge in parsed_identifier.edges:
            swum_phrase.addEdge(edge.child, 'theme')
        
        # identify aux args
        # formal parameters
        for parameter_tokens in metadata.parameter_tokens:
            swum_phrase.addEdge(get_swum_phrase(parameter_tokens), 'aux_arg')
    elif attr_rule == SwumAttrRule.all_preamble:
        fail('Error: preambles are not yet supported')
    else:
        fail('Error: did not recognize rule for phrase tree')

    return swum_phrase

class SwumVisitor(SwumParserVisitor):
    def visitSwum_phrase(self, ctx:SwumParser.Swum_phraseContext):
        return SwumPhrasesNode(antlr_ctx=ctx)

if __name__ == '__main__':
    main(sys.argv)
