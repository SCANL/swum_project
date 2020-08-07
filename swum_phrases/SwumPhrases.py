"""Implementation of SWUM phrases layer"""

import sys
from typing import *    # type annotations
from collections import namedtuple
from dataclasses import dataclass, field
from copy import deepcopy
from enum import Enum, auto

from antlr4 import *
from antlr.SwumParser import SwumParser
from antlr.SwumParserVisitor import SwumParserVisitor
from antlr.SwumLexer import SwumLexer

from lxml import etree

# map from Penn tagset to SWUM grammar
swum_tag_map = {'CC':"CJ", 'CD':"D", "DT":"DT", "EX":"N", "FW":"N", "IN":"P", "JJ":"NM", "JJR":"NM", "JJS":"NM", "LS":"N", "MD":"V", "NN":"N", "NNS":"N", "NNP":"N", "NNPS":"N", "PDT":"DT", "POS":"N", "PRP":"P", "PRP$":"P", "RB":"VM", "RBR":"VM", "RBS":"VM", "RP":"N", "SYM":"N", "TO":"P", "UH":"N", "VB":"V", "VBD":"V", "VBG":"V", "VBN":"V", "VBP":"V", "VBZ":"V", "WDT":"DT", "WP":"P", "WP,":"P", "WRB":"VM"}

class SwumException(Exception):
    """A SWUM logical error"""
    pass

@dataclass
class SwumToken():
    """Word literal and Penn POS tag, grouped for processing by SWUM"""
    literal: str = None
    pos_tag: str = None

@dataclass
class SwumMetadata():
    """Program-level and natural language information read from input file per identifier"""
    id_num: str = None
    location: str = None
    name: str = None
    tokens: List[SwumToken] = field(default_factory=list)
    class_m: 'SwumMetadata' = None
    type_m: 'SwumMetadata' = None
    parameter_m: List['SwumMetadata'] = field(default_factory=list) # parameterized types, methods, classes
    formal_parameter_m: List['SwumMetadata'] = field(default_factory=list) # e.g. for functions and methods

    def is_void(self) -> bool:
        if self.location != 'function':
            raise SwumException('Checking if non-function identifier is void')
        return len(self.type_m.tokens) == 1 and self.type_m.tokens[0].literal == 'void'

    def is_method(self) -> bool:
        return self.location == 'function' and self.class_m is not None
    
    def to_xml_elements(self) -> List[etree._Element]:
        """Converts metadata to list of xml elements"""
        xml_elements: List[etree._Element] = []

        def append_xml(tag: str, text: str) -> None:
            node = etree.Element(tag)
            node.text = text
            xml_elements.append(node)
        
        if self.id_num is not None:
            append_xml('id', self.id_num)
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
# This is an optimization to save space in XML I/O files - for methods, class metadata does not need to be repeated (only the class name)
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
    """Node on phrase tree - does not necessarily correspond with code identifier"""
    def __init__(self, antlr_ctx):
        self.node_type: str = None
        self.edges: List[SwumPhrasesEdge] = []
        self.token: SwumToken = None

        if antlr_ctx is None:
            return

        # Recursively build phrase tree from antlr context
        if antlr_ctx.getChildCount() == 0:
            self.node_type = SwumLexer.symbolicNames[antlr_ctx.symbol.type].lower()
        else:
            self.node_type = SwumParser.ruleNames[antlr_ctx.getRuleIndex()].lower()
            for child_ctx in antlr_ctx.getChildren():
                child_node = SwumPhrasesNode(child_ctx)
                # ignore the stop code which is an artifact of parsing
                if child_node.node_type != 'stop_rule':
                    self.add_edge(child_node)
                # self.add_edge(child_node)
    
    def add_edge(self, node, label: str = None):
        """Adds node as a child to self and labels the added edge as label"""
        if node is None:
            raise SwumException('Tried to add a NoneType node as child on phrase tree')
        new_edge = SwumPhrasesEdge(child=node, label=label)
        self.edges.append(new_edge)
        
    def associate_words(self, tokens: List[SwumToken]):
        """Associates each token from tokens with the next leaf node on this phrase tree"""
        def _associate_words_rec(self, tokens: List[SwumToken]):
            if len(self.edges) == 0:
                self.token = tokens.pop(0)
            else:
                for edge in self.edges:
                    _associate_words_rec(edge.child, tokens)

        # make copy to preserve initial input tokens
        tokens = list(tokens)

        _associate_words_rec(self, tokens)

    def get_child(self, index):
        """Returns the indexth direct child of this phrase node"""
        return self.edges[index].child

    def contains_node_type(self, node_type: str):
        """Returns true if and only if phrase subtree contains a node x with matching node type"""
        for node in self.subtree_nodes():
            if node.node_type == node_type:
                return True

        return False

    def subtree_nodes(self):
        """left to right traversal of phrase tree"""
        yield self
        for edge in self.edges:
            yield from edge.child.subtree_nodes()

    def to_xml(self) -> etree._Element:
        "Converts phrase tree to single xml element"
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
    """Corresponds with a unique code identifier"""
    def __init__(self, antlr_ctx=None, metadata: SwumMetadata = None):
        self.metadata = metadata
        super().__init__(antlr_ctx)

        if antlr_ctx:
            self.associate_words(metadata.tokens)
            self.annotate()
    
    def annotate(self):
        """Annotates self for head nouns, ignorable verbs, and generics. Does additional annotations according to the rule determined by self's metadata"""
        # parameterized identifiers
        self._annotate_parameterized_identifiers()
        
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

        # annotate based on rule
        if attr_rule == SwumAttrRule.verb_default:
            SwumAnnotations.annotate_verb_default(self, swum_phrase)
        elif attr_rule == SwumAttrRule.verb_preposition:
            SwumAnnotations.annotate_verb_preposition(self, swum_phrase)
        elif attr_rule == SwumAttrRule.verb_checker:
            self.annotate_verb_checker(self, swum_phrase) 
        elif attr_rule in [SwumAttrRule.general, SwumAttrRule.event_handler, SwumAttrRule.starts_with_prep0, SwumAttrRule.noun_phrase_void]:
            SwumAnnotations.annotate_general(self, swum_phrase)
        elif attr_rule in [SwumAttrRule.starts_with_prep1, SwumAttrRule.starts_with_prep_default]:
            SwumAnnotations.annotate_starts_with_prep1(self, swum_phrase)
        elif attr_rule == SwumAttrRule.noun_phrase_non_void:
            SwumAnnotations.annotate_noun_phrase_non_void(self, swum_phrase)
        elif attr_rule == SwumAttrRule.constructor:
            SwumAnnotations.annotate_constructor(self, swum_phrase)
        elif attr_rule == SwumAttrRule.all_preamble:
            SwumAnnotations.annotate_all_preamble(self, swum_phrase)
        else:
            fail('Error: annotation rule {} is not yet implemented'.format(str(attr_rule)))

        # copy newly constructed tree into self (metadata is already shared)
        self.node_type = deepcopy(swum_phrase.node_type)
        self.edges = deepcopy(swum_phrase.edges)

        # equivalences between similar phrases in different attributes
        self._make_equivalences()

    def _annotate_parameterized_identifiers(self):
        """Annotates parameterized identifiers in the phrase subtree rooted at self. Attempts to parse parameters and identifier name into single phrase, if possible."""
        for node in self.subtree_nodes():
            if isinstance(node, SwumPhrasesRoot) and len(node.metadata.parameter_m) > 0:
                # try and parse (param1, param2, ..., identifier) into single phrase
                param_tokens: List[SwumToken] = []
                for param_metadata in node.metadata.parameter_m:
                    param_tokens += param_metadata.tokens
                tokens = param_tokens + node.metadata.tokens
                
                # will copy into SwumPhrasesRoot, so don't collapse root
                combined_swum_phrase = get_swum_phrase_from_tokens(tokens, collapse_root=False)
                
                if combined_swum_phrase.node_type == 'unknown_phrase':
                    # add params as attributes
                    for param_metadata in node.metadata.parameter_m:
                        node.add_edge(get_swum_phrase_from_metadata(param_metadata), 'param')
                else:
                    # label param edges within the single combined phrase
                    param_token_literals = [token.literal for token in param_tokens] 
                    for parent_node in combined_swum_phrase.subtree_nodes():
                        for edge in parent_node.edges:
                            if len(edge.child.edges) == 0 and edge.child.token.literal in param_token_literals:
                                edge.label = 'param'
                                # keep track of which params have been marked already
                                param_token_literals.remove(edge.child.token.literal)
                        
                    # replace original node with combined phrase
                    node.node_type = deepcopy(combined_swum_phrase.node_type)
                    node.edges = deepcopy(combined_swum_phrase.edges)

    def _make_equivalences(self):        
        """Creates equivalences between noun phrases which share a head noun, and verb phrases which share a base verb. Equivalences are grouped under "major" attributes."""
        np_list: List[(str, SwumPhrasesEdge)] = [] # head noun, edge
        vp_list: List[(str, SwumPhrasesEdge)] = [] # verb, edge
        major_attrs = ['action', 'theme']

        # gather noun phrases and verb phrases into lists
        for edge in self.edges:
            child = edge.child.edges[0].child if isinstance(edge.child, SwumPhrasesRoot) else edge.child
            if child.node_type == 'noun_phrase':
                for child_edge in child.edges:
                    if child_edge.label == 'head_noun':
                        head_noun = child_edge.child.token.literal.lower()
                        np_list.append((head_noun, edge))
                        break
            elif child.node_type == 'verb_phrase':
                for child_edge in child.edges:
                    if child_edge.child.node_type == 'verb' and child_edge.label != 'ignorable_verb':
                        verb = child_edge.child.token.literal.lower()
                        vp_list.append((verb, edge))
                        break

        # separate phrases based on attribute - merge into major attrs from minor attrs
        np_majors = [pair for pair in np_list if pair[1].label in major_attrs]
        np_minors = [pair for pair in np_list if pair[1].label not in major_attrs]
        vp_majors = [pair for pair in vp_list if pair[1].label in major_attrs]
        vp_minors = [pair for pair in vp_list if pair[1].label not in major_attrs]

        def construct_equivalences(majors, minors, node_type: str):
            for major_pair in majors:
                attr = major_pair[1].label
                equiv = SwumPhrasesNode(antlr_ctx=None)
                equiv.node_type = node_type
                equiv.add_edge(major_pair[1].child)
                for minor_pair in minors:
                    if minor_pair[0] == major_pair[0]:
                        equiv.add_edge(minor_pair[1].child)
                        self.edges.remove(minor_pair[1])
                        minors.remove(minor_pair)
                
                if len(equiv.edges) > 1:
                    self.edges.remove(major_pair[1])
                    self.add_edge(equiv, label=attr)

        construct_equivalences(np_majors, np_minors, 'noun_phrase_equivalence')
        construct_equivalences(vp_majors, vp_minors, 'verb_phrase_equivalence')
            
    def get_attr_rule(self):
        """Returns the appropriate rule for annotating this phrase node based on its metadata"""
        if self.metadata.location == 'constructor':
            return SwumAttrRule.constructor
        elif self.metadata.location == 'function':
            # check for general methods
            last_pos = self.metadata.tokens[-1].pos_tag
            if self.metadata.name.lower() in ['main', 'run'] or last_pos in ['VBD', 'VBG']:
                return SwumAttrRule.general

            first_child = self.get_child(0)
            
            if first_child.node_type in ['verb_phrase', 'verb_group']:
                if self.contains_node_type('prepositional_phrase'):
                    return SwumAttrRule.verb_preposition
                elif self.metadata.tokens[0].pos_tag in ['VBZ', 'MD']:
                    return SwumAttrRule.verb_checker
                else:
                    return SwumAttrRule.verb_default
            elif first_child.node_type == 'noun_phrase':
                if self.metadata.is_void():
                    return SwumAttrRule.noun_phrase_void
                else:
                    return SwumAttrRule.noun_phrase_non_void
            elif first_child.node_type == 'prepositional_phrase':
                leading_prep = self.metadata.tokens[0].literal.lower()
                if leading_prep in ['on', 'before', 'after']:
                    return SwumAttrRule.starts_with_prep0
                elif leading_prep in ['to', 'from']:
                    return SwumAttrRule.starts_with_prep1
                else:
                    return SwumAttrRule.starts_with_prep_default

        return None

    def to_xml(self) -> etree._Element:
        """Converts phrase tree to single xml element"""
        #  The root of the tree is replaced with 'swum_identifier' in the output, and the first child of the tree becomes the head of the actual SWUM phrase. This enables the grammar to support SWUM phrases which have more than one top-level element, if desired. 
        root = etree.Element('swum_identifier')
        for xml_element in self.metadata.to_xml_elements():
            root.append(xml_element)
            
        if len(self.edges) > 0:
            phrase_root = etree.Element('swum_phrase')
            for edge in self.edges:
                child_node = edge.child.to_xml()
                if edge.label is not None:
                    child_node.set('swum_attr', edge.label)
                phrase_root.append(child_node)
            root.append(phrase_root)
        
        return root

class SwumAnnotations():
    """Annotation logic based on an identifier's metadata and grammar structure"""
    @staticmethod
    def annotate_verb_default(root: SwumPhrasesRoot, swum_phrase: SwumPhrasesRoot):
        # starts with VG
        first_child = root.get_child(0)
        class_is_theme: bool = False

        # identify action and theme
        if first_child.node_type == 'verb_phrase':
            # VP -> VG NP PP?
            swum_phrase.add_edge(first_child.get_child(0), 'action')
            swum_phrase.add_edge(first_child.get_child(1), 'theme')
        else:
            # VG -> VM* V+ VPR?
            swum_phrase.add_edge(first_child, 'action')
            
            if len(root.edges) > 1:
                swum_phrase.add_edge(root.get_child(1), 'theme')
            elif len(root.metadata.formal_parameter_m) > 0:
                swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.formal_parameter_m.pop(0)), 'theme')
            else:
                swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.class_m), 'theme')
                class_is_theme = True

        # identify aux args
        # formal parameters
        for formal_parameter_metadata in root.metadata.formal_parameter_m:
            swum_phrase.add_edge(get_swum_phrase_from_metadata(formal_parameter_metadata), 'aux_arg')
        # return type
        if not root.metadata.is_void():
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.type_m), 'aux_arg')
        # class
        if not class_is_theme:
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.class_m), 'aux_arg')

    @staticmethod
    def annotate_verb_preposition(root: SwumPhrasesRoot, swum_phrase: SwumPhrasesRoot):
        # starts with VG, contains PP

        # identify action and theme
        first_child = root.get_child(0)
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
                for edge in root.edges:
                    if edge.child.node_type == 'prepositional_phrase':
                        swum_phrase.add_edge(edge.child, 'secondary_arg')
                        break
        else:
            # VG -> VM* V+ VPR?
            swum_phrase.add_edge(first_child, 'action')
            
            # look in rest of name prior to preposition
            if len(root.edges) > 1:
                second_child = root.get_child(1)
                if second_child.node_type != 'prepositional_phrase':
                    swum_phrase.add_edge(second_child, 'theme')
            else:   # class
                if root.metadata.class_metadata is not None:
                    swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.class_m), 'theme')

            # secondary args
            for edge in root.edges:
                if edge.child.node_type == 'prepositional_phrase':
                    swum_phrase.add_edge(edge.child, 'secondary_arg')
                    break


        # identify aux args
        # formal parameters
        for formal_parameter_metadata in root.metadata.formal_parameter_m:
            swum_phrase.add_edge(get_swum_phrase_from_metadata(formal_parameter_metadata), 'aux_arg')
        # return type
        if not root.metadata.is_void():
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.type_m), 'aux_arg')
        # class
        if root.metadata.class_metadata is not None:
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.class_m), 'aux_arg')

    @staticmethod
    def annotate_verb_checker(root: SwumPhrasesRoot, swum_phrase: SwumPhrasesRoot):
        # starts with VG

        first_child = root.get_child(0)
        # identify action and theme
        if first_child.node_type == 'verb_phrase':
            # VP -> VG NP PP?
            swum_phrase.add_edge(first_child.get_child(0), 'condition')
            swum_phrase.add_edge(first_child.get_child(1), 'condition')
        else:
            # VG -> VM* V+ VPR?
            swum_phrase.add_edge(first_child, 'condition')

            if len(root.edges) > 1:
                swum_phrase.add_edge(root.get_child(1), 'condition')
            elif len(root.metadata.parameter_tokens) > 0:
                swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.parameter_m.pop(0)), 'condition')
            else:
                swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.class_m), 'condition')
            
        # identify secondary args
        # class
        if root.metadata.is_method():
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.class_m), 'subject')

        # identify aux args
        # formal parameters
        for formal_parameter_metadata in root.metadata.formal_parameter_m:
            swum_phrase.add_edge(get_swum_phrase_from_metadata(formal_parameter_metadata), 'subject')

    @staticmethod
    def annotate_general(root: SwumPhrasesRoot, swum_phrase: SwumPhrasesRoot):
        swum_phrase.add_edge(get_swum_phrase_from_tokens([SwumToken(literal='handle', pos_tag='VBZ')]), 'action')
        # if identifier parses into multiple phrases, have multiple themes
        for edge in root.edges:
            swum_phrase.add_edge(edge.child, 'theme')
        
        # identify aux args
        # formal parameters
        for formal_parameter_metadata in root.metadata.formal_parameter_m:
            swum_phrase.add_edge(get_swum_phrase_from_metadata(formal_parameter_metadata), 'aux_arg')
        # return type
        if not root.metadata.is_void():
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.type_m), 'aux_arg')
        # class
        if root.metadata.is_method():
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.class_m), 'aux_arg')

    @staticmethod
    def annotate_starts_with_prep1(root: SwumPhrasesRoot, swum_phrase: SwumPhrasesRoot):
        swum_phrase.add_edge(get_swum_phrase_from_tokens([SwumToken(literal='convert', pos_tag='VBZ')]), 'action')
        # if identifier parses into multiple phrases, have multiple secondary args
        for edge in root.edges:
            swum_phrase.add_edge(edge.child, 'secondary_arg')
        
        # identify aux args
        # formal parameters
        for formal_parameter_metadata in root.metadata.formal_parameter_m:
            swum_phrase.add_edge(get_swum_phrase_from_metadata(formal_parameter_metadata), 'aux_arg')
        # return type
        if not root.metadata.is_void():
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.type_m), 'aux_arg')
        # class
        if root.metadata.is_method():
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.class_m), 'aux_arg')

    @staticmethod
    def annotate_noun_phrase_non_void(root: SwumPhrasesRoot, swum_phrase: SwumPhrasesRoot):
        swum_phrase.add_edge(get_swum_phrase_from_tokens([SwumToken(literal='get', pos_tag='VBZ')]), 'action')
        # if identifier parses into multiple phrases, have multiple themes
        for edge in root.edges:
            swum_phrase.add_edge(edge.child, 'theme')
        
        # identify aux args
        # formal parameters
        for formal_parameter_metadata in root.metadata.formal_parameter_m:
            swum_phrase.add_edge(get_swum_phrase_from_metadata(formal_parameter_metadata), 'aux_arg')
        # return type
        if not root.metadata.is_void():
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.type_m), 'aux_arg')
        # class
        if root.metadata.is_method():
            swum_phrase.add_edge(get_swum_phrase_from_metadata(root.metadata.class_m), 'aux_arg')

    @staticmethod
    def annotate_constructor(root: SwumPhrasesRoot, swum_phrase: SwumPhrasesRoot):
        swum_phrase.add_edge(get_swum_phrase_from_tokens([SwumToken(literal='create', pos_tag='VBZ')]), 'action')
        swum_phrase.add_edge(get_swum_phrase_from_tokens([SwumToken(literal='construct', pos_tag='VBZ')]), 'action')
        # if identifier parses into multiple phrases, have multiple themes
        for edge in root.edges:
            swum_phrase.add_edge(edge.child, 'theme')
        
        # identify aux args
        # formal parameters
        for formal_parameter_metadata in root.metadata.formal_parameter_m:
            swum_phrase.add_edge(get_swum_phrase_from_metadata(formal_parameter_metadata), 'aux_arg')

    @staticmethod
    def annotate_all_preamble(root: SwumPhrasesRoot, swum_phrase: SwumPhrasesRoot):
        fail('Error: preambles are not yet supported')

@dataclass
class SwumPhrasesEdge():
    """Edge on phrase tree. May be annotated with a label"""
    child: SwumPhrasesNode = None
    label: str = None


def main(argv):    
    input_filename = argv[1]
    output_filename = argv[2]
    with open(output_filename, 'wb') as output_f:
        with open(input_filename, 'rb') as input_f:
            # write XML output one identifier at a time to avoid having to load entire XML input into memory all at once
            output_f.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<swum_identifiers>\n'.encode('utf-8'))

            try:
                for _, element in etree.iterparse(input_f, tag='swum_identifier', remove_blank_text=True):
                    # nested identifiers are processed recursively
                    if element.getparent().tag != 'swum_identifiers':
                        continue
                    
                    metadata = get_metadata(element)
                    swum_phrase = get_swum_phrase_from_metadata(metadata)
                    
                    if swum_phrase is not None:
                        output_f.write(etree.tostring(swum_phrase.to_xml(), encoding='utf-8', pretty_print=True))

                    if metadata.location == 'class':
                        # add to class dict to resolve later
                        metadata.id_num = None  # only top level identifiers should have an id num
                        class_dict[metadata.name] = metadata
                    
                    element.clear(keep_tail=True) 
            except Exception as e:
                print('Error: Either {} is not a valid input file, or an internal error occurred.'.format(input_filename))
                raise e

        output_f.write('</swum_identifiers>'.encode('utf-8'))     

def fail(error: str, err_code: int = 1):
    print(error, file=sys.stderr)
    sys.exit(err_code)

def get_swum_phrase_from_tokens(tokens: List[SwumToken] = None, collapse_root: bool = True):
    """Returns a phrase tree based on the input tokens
    
    Keyword arguments:
    tokens -- list of consituent tokens for identifier
    collapse_root -- If true and tokens parse into phrase with single top-level grammar symbol, make this symbol the root. Otherwise, the top-most grammar rule is the root of the phrase tree. Meant to help prevent parser artifacts from creeping into SWUM output.
    """
    swum_pos_tokens = penn_tags_to_swum([swum_token.pos_tag for swum_token in tokens])
    tree = get_parse_tree(swum_pos_tokens + ['STOP'])

    if tree is not None:
        if collapse_root:
            is_collapsable: bool = tree.getChildCount() == 1 or (tree.getChildCount() > 1 and isinstance(list(tree.getChildren())[1], SwumParser.Stop_ruleContext))
            if is_collapsable:
                tree = tree.getChild(0)
        node = SwumPhrasesNode(tree)
        node.associate_words(tokens)
        return node
    else:
        print('could not parse {}, {}'.format([swum_token.literal for swum_token in tokens], [swum_token.pos_tag for swum_token in tokens]))
        raise SwumException('Failed to recover from bad parse of {}'.format(tokens))

def get_swum_phrase_from_metadata(metadata: SwumMetadata = None):
    """Returns a phrase tree based on identifier metadata
    
    Keyword arguments:
    metadata -- program-level and NL metadata for identifier
    """
    swum_pos_tokens = penn_tags_to_swum([swum_token.pos_tag for swum_token in metadata.tokens])
    tree = get_parse_tree(swum_pos_tokens + ['STOP'])

    if tree is not None:
        return SwumPhrasesRoot(tree, metadata)
    else:
        print('could not parse {}, {}'.format([swum_token.literal for swum_token in metadata.tokens], [swum_token.pos_tag for swum_token in metadata.tokens]))
        raise SwumException('Failed to recover from bad parse of {}'.format(metadata.tokens))


def get_parse_tree(swum_pos_tokens : List[str]):
    """Returns the raw ANTLR parse tree for swum_pos_tokens based on SWUM grammar.
    
    If the POS tokens do not parse into valid phrase, greedily parses non-terminals then terminals from front of token list until stop code is reached"""    
    lexer = SwumLexer(InputStream(' '.join(swum_pos_tokens)))
    stream = CommonTokenStream(lexer)
    parser = SwumParser(stream)
    parser._errHandler = error.ErrorStrategy.BailErrorStrategy()
    parser.removeErrorListeners()

    try:
        tree = parser.start_rule()
        return tree
    except error.Errors.ParseCancellationException as e:
        tree = ParserRuleContext()
        first_child = SwumParser.Unknown_phraseContext(parser)
        tree.addChild(first_child)
        swum_tokens_copy = deepcopy(swum_pos_tokens)
        finished_parsing = False
        while finished_parsing == False:
            lexer = SwumLexer(InputStream(' '.join(swum_tokens_copy)))
            stream = CommonTokenStream(lexer)
            parser = SwumParser(stream)
            parser._errHandler = error.ErrorStrategy.BailErrorStrategy()
            parser.removeErrorListeners()
            
            try:
                # parse nonterminal from head of input
                partial_tree = parser.fail_rule1().getChild(0)
                first_child.addChild(partial_tree)
                swum_tokens_copy = swum_tokens_copy[num_leaves(partial_tree):]
            except error.Errors.ParseCancellationException as e:
                parser.reset()
                try:
                    # parse terminal from head of input
                    partial_tree = parser.fail_rule2().getChild(0)
                    first_child.addChild(partial_tree)
                    swum_tokens_copy = swum_tokens_copy[num_leaves(partial_tree):]
                except error.Errors.ParseCancellationException as e:
                    parser.reset()
                    try:
                        # find stop code
                        parser.stop_rule()
                        finished_parsing = True
                    except error.Errors.ParseCancellationException as e:
                        raise SwumException('Error parsing remaining SWUM tokens: {}'.format(swum_tokens_copy))

        return tree

    
def penn_tags_to_swum(pos_tokens:List[str]):
    """Converts POS tags from Penn tagset to SWUM's simplified tagset"""
    # assume nouns preceding nouns are noun-modifiers
    try:
        swum_tags = [swum_tag_map[penn_tag] for penn_tag in pos_tokens]
    except KeyError as e:
        raise SwumException('Unrecognized POS tag {} in input file'.format(str(e)))
    
    # assume rightmost noun is described by any consecutive nouns to the left
    last_tag = None
    for index, tag in enumerate(swum_tags):
        if last_tag == 'N' and tag == 'N':
            swum_tags[index-1] = 'NM'
        last_tag = tag
    
    return swum_tags

def num_leaves(antlr_ctx) -> int:
    """Returns the number of leaf nodes in the subtree rooted at antlr_ctx"""
    count = 0
    if antlr_ctx.getChildCount() > 0:
        for child in antlr_ctx.getChildren():
            count += num_leaves(child)
    else:
        count = 1
    
    return count

def get_metadata(element: etree._Element) -> SwumMetadata:
    """Returns the extracted metadata object from a <swum_identifier> XML node in input"""
    metadata: SwumMetadata = SwumMetadata()
    for child in element:
        if child.tag == 'swum_ID':
            metadata.id_num = child.text.strip()
        elif child.tag == 'location':
            metadata.location = child.text.strip()
        elif child.tag == 'name':
            metadata.name = child.text.strip()
        elif child.tag == 'class':
            metadata.class_m = class_dict[child.text.strip()]
        elif child.tag == 'type':
            metadata.type_m = get_metadata(child[0])
        elif child.tag == 'parameters':
            for parameter_node in child:
                metadata.parameter_m.append(get_metadata(parameter_node[0]))
        elif child.tag == 'formal_parameters':
            for formal_parameter_node in child:
                metadata.formal_parameter_m.append(get_metadata(formal_parameter_node[0]))
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
    elif metadata.location in ['function', 'formal_parameter'] and metadata.type_m is None:
        fail('{} is missing type'.format(metadata.name))
    
    return metadata

if __name__ == '__main__':
    main(sys.argv)
