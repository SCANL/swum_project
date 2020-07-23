"""Implementation of SWUM phrases layer"""

import sys
import subprocess
from typing import *    # for type annotations
from collections import namedtuple
from dataclasses import dataclass, field
import copy

from antlr4 import *
from antlr4.error.ErrorStrategy import BailErrorStrategy
from antlr4.error.Errors import ParseCancellationException
from antlr.SwumParser import SwumParser
from antlr.SwumParserVisitor import SwumParserVisitor
from antlr.SwumLexer import SwumLexer
from enum import Enum, auto

from lxml import etree

# TODO: support special cases for boolean type examples

tag_map = {'CC':"CJ", 'CD':"D", "DT":"DT", "EX":"N", "FW":"N", "IN":"P", "JJ":"NM", "JJR":"NM", "JJS":"NM", "LS":"N", "MD":"V", "NN":"N", "NNS":"N", "NNP":"N", "NNPS":"N", "PDT":"DT", "POS":"N", "PRP":"P", "PRP$":"P", "RB":"VM", "RBR":"VM", "RBS":"VM", "RP":"N", "SYM":"N", "TO":"P", "UH":"N", "VB":"V", "VBD":"V", "VBG":"V", "VBN":"V", "VBP":"V", "VBZ":"V", "WDT":"DT", "WP":"P", "WP,":"P", "WRB":"VM"
}

class SwumException(Exception):
    pass

@dataclass
class SwumToken():
    literal: str = None
    pos_tag: str = None

@dataclass
class SwumMetadata():
    """Program-level and natural language information read from input file per identifier"""
    location: str = None
    name: str = None
    tokens: List[SwumToken] = field(default_factory=list)
    # TODO: consider nested metadata for class and type info (since generic classes and generic types each have parameter of their own)
    class_m: 'SwumMetadata' = None
    type_m: 'SwumMetadata' = None
    parameter_m: List['SwumMetadata'] = field(default_factory=list) # parameterized types, methods, classes
    formal_parameter_m: List['SwumMetadata'] = field(default_factory=list)

    def is_void(self) -> bool:
        if self.location != 'function':
            raise SwumException('Checking if non-function identifier is void')
        return len(self.type_m.tokens) == 1 and self.type_m.tokens[0].literal == 'void'

    def is_method(self) -> bool:
        return self.location == 'function' and self.class_m is not None
    
    def to_xml_elements(self) -> List[etree._Element]:
        xml_elements: List[etree._Element] = []

        def append_xml(tag: str, text: str) -> None:
            node = etree.Element(tag)
            node.text = text
            xml_elements.append(node)
        
        append_xml('name', self.name)
        append_xml('location', self.location)
        if self.class_m is not None:
            append_xml('class', self.class_m.name)
        if self.type_m is not None:
            append_xml('type', self.type_m.name)
        if len(self.parameter_m) > 0:
            parameters_node = etree.Element('parameters')
            for param_metadata in self.parameter_m:
                etree.SubElement(parameters_node, 'parameter').text = param_metadata.name
            xml_elements.append(parameters_node)
        if len(self.formal_parameter_m) > 0:
            formal_parameters_node = etree.Element('formal_parameters')
            for formal_param_metadata in self.formal_parameter_m:
                etree.SubElement(formal_parameters_node, 'formal_parameter').text = formal_param_metadata.name
            xml_elements.append(formal_parameters_node)

        return xml_elements

# classname mapped to its metadata
class_dict: Dict[str, SwumMetadata] = {}

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

class SwumPhrasesNode():
    """Node on phrasal tree"""
    def __init__(self, antlr_ctx):
        self.node_type: str = None
        self.edges: List[SwumPhrasesEdge] = []
        self.token: SwumToken = None

        if antlr_ctx is None:
            return

        if antlr_ctx.getChildCount() == 0:
            self.node_type = SwumLexer.symbolicNames[antlr_ctx.symbol.type].lower()
        else:
            self.node_type = SwumParser.ruleNames[antlr_ctx.getRuleIndex()].lower()
            for child_ctx in antlr_ctx.getChildren():
                child_node = SwumPhrasesNode(child_ctx)
                if child_node.node_type != 'stop_code':
                    self.add_edge(child_node)
    
    def add_edge(self, node, label: str = None):
        # TODO: remove experimental guard against phrases that don't parse with SWUM grammar
        if node is None:
            raise SwumException('Tried to add a NoneType node as child on phrase tree')
        new_edge = SwumPhrasesEdge(child=node, label=label)
        self.edges.append(new_edge)
        
    def associate_words(self, tokens: List[SwumToken], head=True):
        """Recursively associates each token from tokens with the appropriate leaf node on this phrasal tree
        
        Preserves the input token list"""
        
        # make copy to preserve initial input tokens
        if head:
            tokens = list(tokens)
        
        if len(self.edges) == 0:
            self.token = tokens.pop(0)
        else:
            for edge in self.edges:
                edge.child.associate_words(tokens, False)

    def get_child(self, index):
        """Returns the indexth direct child of this phrasal node"""
        return self.edges[index].child

    def contains_node(self, node_type: str):
        """Returns true if and only if phrasal subtree contains a node x where x.node_type == node_type"""
        if self.node_type == node_type:
            return True

        for edge in self.edges:
            if edge.child.contains_node(node_type):
                return True

        return False

    def subtree_nodes(self):
        """left to right traversal of phrasal tree"""
        yield self
        for edge in self.edges:
            yield from edge.child.subtree_nodes()

    def to_xml(self) -> etree._Element:
        root = etree.Element(self.node_type)

        if self.token is not None:
            root.text = self.token.literal
        else:
            for edge in self.edges:
                if edge.label:
                    child_node = edge.child.to_xml()
                    child_node.set('swum_attr', edge.label)
                    root.append(child_node)
                else:
                    root.append(edge.child.to_xml())

        return root


class SwumPhrasesRoot(SwumPhrasesNode):
    """Mapped to unique code identifier"""
    def __init__(self, antlr_ctx=None, tokens: List[SwumToken] = None, metadata: SwumMetadata = None):
        self.metadata = metadata
        super().__init__(antlr_ctx)
        self.node_type = 'swum_phrase'

        if antlr_ctx:
            self.associate_words(tokens)
            self.annotate()
    
    def annotate(self):
        """Returns a copy of self annotated according to the rule determined by this node's metadata"""
        # head noun
        for node in self.subtree_nodes():
            if node.node_type == 'noun_phrase':
                for edge in node.edges:
                    if edge.child.node_type == 'noun':
                        edge.label = 'head_noun'
                        break

        # ignorable verbs
        for node in self.subtree_nodes():
            if node.node_type == 'verb_phrase':
                for index, edge in enumerate(node.edges):
                    if edge.child.node_type == 'verb' and index > 0 and node.edges[index-1].child.node_type == 'verb':
                        node.edges[index-1].label = 'ignorable_verb'

        
        attr_rule = self.get_attr_rule()

        if attr_rule is None:
            return

        swum_phrase = SwumPhrasesRoot(metadata=self.metadata)

        if attr_rule == SwumAttrRule.verb_default:
            # starts with VG
            first_child = self.get_child(0)
            class_is_theme: bool = False

            # identify action and theme
            if first_child.node_type == 'verb_phrase':
                # VP -> VG NP PP?
                swum_phrase.add_edge(first_child.get_child(0), 'action')
                swum_phrase.add_edge(first_child.get_child(1), 'theme')
            else:
                # VG -> VM* V+ VPR?
                swum_phrase.add_edge(first_child, 'action')
                
                if len(self.edges) > 1:
                    swum_phrase.add_edge(self.get_child(1), 'theme')
                elif len(self.metadata.formal_parameter_metadata) > 0:
                    swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.formal_parameter_metadata.pop(0)), 'theme')
                else:
                    swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.class_m), 'theme')
                    class_is_theme = True

            # identify aux args
            # formal parameters
            for formal_parameter_metadata in self.metadata.formal_parameter_m:
                swum_phrase.add_edge(get_swum_phrase(metadata=formal_parameter_metadata), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.type_m), 'aux_arg')
            # class
            if not class_is_theme:
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.class_m), 'aux_arg')
        elif attr_rule == SwumAttrRule.verb_preposition:
            # starts with VG, contains PP

            # identify action and theme
            first_child = self.get_child(0)
            if first_child.node_type == 'verb_phrase':
                # VP -> VG NP PP?
                swum_phrase.add_edge(first_child.get_child(0), 'action')
                swum_phrase.add_edge(first_child.get_child(1), 'theme')

                # secondary args
                if len(first_child.edges) == 3:
                    # VP -> VG NP PP
                    swum_phrase.add_edge(first_child.get_child(2), 'secondary_arg')
                else:
                    # VP -> VG NP
                    # look for preposition in remainder of identifier
                    for edge in self.edges:
                        if edge.child.node_type == 'prepositional_phrase':
                            swum_phrase.add_edge(edge.child, 'secondary_arg')
                            break
            else:
                # VG -> VM* V+ VPR?
                swum_phrase.add_edge(first_child, 'action')
                
                # look in rest of name prior to preposition
                if len(self.edges) > 1:
                    second_child = self.get_child(1)
                    if second_child.node_type != 'prepositional_phrase':
                        swum_phrase.add_edge(second_child, 'theme')
                else:   # class
                    if self.metadata.class_metadata is not None:
                        swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.class_m), 'theme')

                # secondary args
                for edge in self.edges:
                    if edge.child.node_type == 'prepositional_phrase':
                        swum_phrase.add_edge(edge.child, 'secondary_arg')
                        break


            # identify aux args
            # formal parameters
            for formal_parameter_metadata in self.metadata.formal_parameter_metadata:
                swum_phrase.add_edge(get_swum_phrase(metadata=formal_parameter_metadata), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.type_m), 'aux_arg')
            # class
            if self.metadata.class_metadata is not None:
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.class_m), 'aux_arg')
        elif attr_rule == SwumAttrRule.verb_checker:
            # starts with VG

            first_child = self.get_child(0)
            # identify action and theme
            if first_child.node_type == 'verb_phrase':
                # VP -> VG NP PP?
                swum_phrase.add_edge(first_child.get_child(0), 'condition')
                swum_phrase.add_edge(first_child.get_child(1), 'condition')
            else:
                # VG -> VM* V+ VPR?
                swum_phrase.add_edge(first_child, 'condition')

                if len(self.edges) > 1:
                    swum_phrase.add_edge(self.get_child(1), 'condition')
                elif len(self.metadata.parameter_tokens) > 0:
                    swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.parameter_m.pop(0)), 'condition')
                else:
                    swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.class_m), 'condition')
                
            # identify secondary args
            # class
            if self.metadata.is_method():
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.class_m), 'subject')

            # identify aux args
            # formal parameters
            for formal_parameter_metadata in self.metadata.formal_parameter_m:
                swum_phrase.add_edge(get_swum_phrase(metadata=formal_parameter_metadata), 'subject')
        elif attr_rule in [SwumAttrRule.general, SwumAttrRule.event_handler, SwumAttrRule.starts_with_prep0, SwumAttrRule.noun_phrase_void]:
            swum_phrase.add_edge(get_swum_phrase(tokens=[SwumToken(literal='handle', pos_tag='VBZ')]), 'action')
            # if identifier parses into multiple phrases, have multiple themes
            for edge in self.edges:
                swum_phrase.add_edge(edge.child, 'theme')
            
            # identify aux args
            # formal parameters
            for formal_parameter_metadata in self.metadata.formal_parameter_m:
                swum_phrase.add_edge(get_swum_phrase(metadata=formal_parameter_metadata), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.type_m), 'aux_arg')
            # class
            if self.metadata.is_method():
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.class_m), 'aux_arg')
        elif attr_rule in [SwumAttrRule.starts_with_prep1, SwumAttrRule.starts_with_prep_default]:
            swum_phrase.add_edge(get_swum_phrase(tokens=[SwumToken(literal='convert', pos_tag='VBZ')]), 'action')
            # if identifier parses into multiple phrases, have multiple secondary args
            for edge in self.edges:
                swum_phrase.add_edge(edge.child, 'secondary_arg')
            
            # identify aux args
            # formal parameters
            for formal_parameter_metadata in self.metadata.formal_parameter_m:
                swum_phrase.add_edge(get_swum_phrase(metadata=formal_parameter_metadata), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.type_m), 'aux_arg')
            # class
            if self.metadata.is_method():
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.class_m), 'aux_arg')
        elif attr_rule == SwumAttrRule.noun_phrase_non_void:
            swum_phrase.add_edge(get_swum_phrase(tokens=[SwumToken(literal='get', pos_tag='VBZ')]), 'action')
            # if identifier parses into multiple phrases, have multiple themes
            for edge in self.edges:
                swum_phrase.add_edge(edge.child, 'theme')
            
            # identify aux args
            # formal parameters
            for formal_parameter_metadata in self.metadata.formal_parameter_m:
                swum_phrase.add_edge(get_swum_phrase(metadata=formal_parameter_metadata), 'aux_arg')
            # return type
            if not self.metadata.is_void():
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.type_m), 'aux_arg')
            # class
            if self.metadata.is_method():
                swum_phrase.add_edge(get_swum_phrase(metadata=self.metadata.class_m), 'aux_arg')
        elif attr_rule == SwumAttrRule.constructor:
            swum_phrase.add_edge(get_swum_phrase(tokens=[SwumToken(literal='create', pos_tag='VBZ')]), 'action')
            swum_phrase.add_edge(get_swum_phrase(tokens=[SwumToken(literal='construct', pos_tag='VBZ')]), 'action')
            # if identifier parses into multiple phrases, have multiple themes
            for edge in self.edges:
                swum_phrase.add_edge(edge.child, 'theme')
            
            # identify aux args
            # formal parameters
            for formal_parameter_metadata in self.metadata.formal_parameter_m:
                swum_phrase.add_edge(get_swum_phrase(metadata=formal_parameter_metadata), 'aux_arg')
        elif attr_rule == SwumAttrRule.all_preamble:
            fail('Error: preambles are not yet supported')
        else:
            fail('Error: did not recognize annotation rule ' + str(attr_rule))

        # copy newly constructed tree into self (metadata is already shared, token not applicable for root)
        self.node_type = copy.deepcopy(swum_phrase.node_type)
        self.edges = copy.deepcopy(swum_phrase.edges)

    def get_attr_rule(self):
        """Returns the appropriate rule for annotating this phrasal node based on its metadata"""
        if self.metadata.location == 'constructor':
            return SwumAttrRule.constructor
        elif self.metadata.location == 'function':
            last_pos = self.metadata.tokens[-1].pos_tag
            if self.metadata.name.lower() in ['main', 'run'] or last_pos in ['VBD', 'VBG']:
                return SwumAttrRule.general

            # TODO: detect event handlers by looking at parameter types

            first_child = self.get_child(0)
            
            if first_child.node_type in ['verb_phrase', 'verb_group']:
                if self.contains_node('prepositional_phrase'):
                    return SwumAttrRule.verb_preposition
                elif self.metadata.tokens[0].pos_tag in ['VBZ', 'MD']:
                    return SwumAttrRule.verb_checker
                else:
                    return SwumAttrRule.verb_default

            if first_child.node_type == 'noun_phrase':
                if self.metadata.is_void():
                    return SwumAttrRule.noun_phrase_void
                else:
                    return SwumAttrRule.noun_phrase_non_void

            if first_child.node_type == 'prepositional_phrase':
                leading_prep = self.metadata.tokens[0].literal.lower()
                if leading_prep in ['on', 'before', 'after']:
                    return SwumAttrRule.starts_with_prep0
                elif leading_prep in ['to', 'from']:
                    return SwumAttrRule.starts_with_prep1
                else:
                    return SwumAttrRule.starts_with_prep_default

        return None

    def to_xml(self) -> etree._Element:
        root = etree.Element('swum_identifier')
        for xml_element in self.metadata.to_xml_elements():
            root.append(xml_element)
            
        for edge in self.edges:
            child_node = edge.child.to_xml()
            if edge.label is not None:
                child_node.set('swum_attr', edge.label)
            root.append(child_node)
        
        return root


@dataclass
class SwumPhrasesEdge():
    """Edge on phrasal tree. May be annotated with a label"""
    child: SwumPhrasesNode = None
    label: str = None


def main(argv):    
    input_filename = argv[1]
    output_filename = argv[2]
    with open(output_filename, 'wb') as output_f:
        with open(input_filename, 'rb') as input_f:
            output_f.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<swum_identifiers>\n'.encode('utf-8'))

            try:
                for _, element in etree.iterparse(input_f, tag='swum_identifier', remove_blank_text=True):
                    if element.getparent().tag != 'swum_identifiers': # only process nested identifiers recursively
                        continue
                    
                    metadata = get_metadata(element)
                    if metadata.location == 'class':
                        # add to class dict to resolve later
                        class_dict[metadata.name] = metadata

                    swum_phrase = get_swum_phrase(metadata=metadata)
                    
                    if swum_phrase is not None:
                        output_f.write(etree.tostring(swum_phrase.to_xml(), encoding='utf-8', pretty_print=True))
                    
                    element.clear(keep_tail=True) 
            except Exception as e:
                print(str(e))
                raise e
                fail('Error: Either {} is not a valid input file, or an internal error occurred.'.format(input_filename))

        output_f.write('</swum_identifiers>'.encode('utf-8'))     

def fail(error: str, err_code: int = 1):
    print(error, file=sys.stderr)
    sys.exit(err_code)


def get_swum_phrase(*, tokens: List[SwumToken] = None, metadata: SwumMetadata = None):
    """Returns a phrasal tree based on the input tokens and identifier metadata
    
    Keyword arguments:
    tokens -- list of consituent tokens for identifier
    metadata -- program-level and NL metadata for identifier; if not None, metadata tokens override tokens argument
    """
    if tokens is not None and metadata is not None:
        raise SwumException('Call to get_swum_phrase sets both tokens and metadata')

    if metadata is not None:
        tokens = metadata.tokens
    swum_pos_tokens = penn_tags_to_swum([swum_token.pos_tag for swum_token in tokens])
    tree = get_parse_tree(swum_pos_tokens + ['STOP'])
    visitor = SwumVisitor()

    if metadata is None:
        if tree is None:
            return None
        else:
            node = SwumPhrasesNode(visitor.visit(tree))
            node.associate_words(tokens)
            return node
    else:
        if tree is None:
            return SwumPhrasesRoot(metadata=metadata)
        else:
            return SwumPhrasesRoot(visitor.visit(tree), tokens, metadata)

def get_parse_tree(swum_pos_tokens : List[str]):
    """Returns the raw ANTLR parse tree for swum_pos_tokens based on SWUM grammar.
    
    If the POS tokens do not parse into valid phrase, returns None"""
    lexer = SwumLexer(InputStream(' '.join(swum_pos_tokens)))
    stream = CommonTokenStream(lexer)
    parser = SwumParser(stream)
    parser._errHandler = BailErrorStrategy()

    # TODO: force antlr to match entire input else throw an exception
    try:
        tree = parser.start_rule()
        return tree
    except ParseCancellationException as e:
        return None
    
def penn_tags_to_swum(pos_tokens:List[str]):
    """Converts POS tags from Penn tagset to SWUM's simplified tagset"""
    # assume nouns preceding nouns are noun-modifiers
    try:
        swum_tags = [tag_map[penn_tag] for penn_tag in pos_tokens]
    except KeyError as e:
        fail('Unrecognized POS tag {} in input file'.format(str(e)))
    last_tag = None
    for index, tag in enumerate(swum_tags):
        if last_tag == 'N' and tag == 'N':
            swum_tags[index-1] = 'NM'
        last_tag = tag
    
    return swum_tags

def get_metadata(element: etree._Element) -> SwumMetadata:
    """Returns the extracted metadata object from a <swum_identifier> XML node in input"""
    metadata: SwumMetadata = SwumMetadata()
    for child in element:
        if child.tag == 'location':
            metadata.location = child.text.strip()
        elif child.tag == 'name':
            metadata.name = child.text.strip()
        elif child.tag == 'class':
            metadata.class_m = class_dict[child.text.strip()]
        elif child.tag == 'type':
            metadata.type_m = get_metadata(child[0])
        elif child.tag == 'parameters':
            for parameter_node in child:
                metadata.parameter_m.append(get_metadata(parameter_node))
        elif child.tag == 'formal_parameters':
            for formal_parameter_node in child:
                metadata.formal_parameter_m.append(get_metadata(formal_parameter_node))
        elif child.tag == 'identifier':
            for word_node in child:
                pos_node = word_node[0]
                new_token = SwumToken(word_node.text.strip(), pos_node.text.strip())
                metadata.tokens.append(new_token)
    
    if metadata.name is None:
        fail('a swum identifier is missing name')
    elif len(metadata.tokens) == 0:
        fail('{} is missing tokens'.format(metadata.name))
    elif metadata.location is None:
        fail('{} is missing location'.format(metadata.name))
    elif metadata.location == 'function' and metadata.type_m is None:
        fail('{} is missing type'.format(metadata.name))
    
    return metadata


class SwumVisitor(SwumParserVisitor):
    """Override ANTLR's default traversal of parse tree to support custom phrasal tree"""
    def visitStart_rule(self, ctx:SwumParser.Start_ruleContext):
        return ctx

if __name__ == '__main__':
    main(sys.argv)
