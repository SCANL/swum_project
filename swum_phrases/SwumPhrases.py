import sys
import subprocess
from typing import *    # for type annotations
from collections import namedtuple

from antlr4 import *
from antlr.SwumParser import SwumParser
from antlr.SwumParserVisitor import SwumParserVisitor
from antlr.SwumLexer import SwumLexer
from enum import Enum, auto

from lxml import etree

# TODO: support special cases for boolean type examples

# key is classname, value is metadata for that class
class_dict = {}

def main(argv):    
    filename = argv[1]


    with open(filename, 'rb') as f:
        for _, element in etree.iterparse(f, tag='swum_identifier', remove_blank_text=True):
            if element.getparent().tag != 'swum_identifiers':
                continue
            
            metadata = get_metadata(element)
            if metadata['location'] == 'class':
                # add to class dict to resolve later
                class_dict[metadata['name']] = metadata
            elif metadata['location'] == 'function':
                # annotate
                swum_phrase = get_annotated_swum_phrase(metadata)
                print(swum_phrase)

            element.clear(keep_tail=True)        

def fail(error: str):
    print(error, file=sys.stderr)
    sys.exit(1)

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


def get_swum_phrase(pos_tokens: List[str], literal_tokens: List[str]):
    swum_pos_tokens = penn_tags_to_swum(pos_tokens)
    tree = get_parse_tree(InputStream(' '.join(swum_pos_tokens)))
    visitor = SwumVisitor()
    swum_phrase = visitor.visit(tree)
    swum_phrase.associateWords(pos_tokens, literal_tokens)

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



# custom data structure to use internally after reading in antlr tree
class SwumPhrasesNode():
    def __init__(self, antlr_ctx=None, pos=None, literal=None, pos_tokens=None, literal_tokens=None):
        self.antlrCtx = None
        self.isTerminal = None
        self.pos = pos # part of speech tag from Penn tagset
        self.literal = literal
        self.pos_tokens = pos_tokens
        self.literal_tokens = literal_tokens
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

    def get_attr_rule(self, metadata: dict):
        if metadata['location'] == 'constructor':
            return SwumAttrRule.constructor

        last_pos = self.pos_tokens[-1]
        if self.literal and self.literal.lower() in ['main', 'run'] or last_pos in ['VBD', 'VBG']:
            return SwumAttrRule.general

        # TODO: detect event handlers by looking at parameter types

        first_child = self.getChild(0)
        
        if first_child.nodeType in ['verb_phrase', 'verb_group']:
            if self.containsNode('prepositional_phrase'):
                return SwumAttrRule.verb_preposition
            elif self.pos_tokens[0] in ['VBZ', 'MD']:
                return SwumAttrRule.verb_checker
            else:
                return SwumAttrRule.verb_default

        if first_child.nodeType == 'noun_phrase':
            if len(metadata['type_tokens']) == 1 and metadata['type_tokens'][0] == 'void':
                return SwumAttrRule.noun_phrase_void
            else:
                return SwumAttrRule.noun_phrase_non_void

        if first_child.nodeType == 'prepositional_phrase':
            leading_prep = self.literal_tokens[0].lower()
            if leading_prep in ['on', 'before', 'after']:
                return SwumAttrRule.starts_with_prep0
            elif leading_prep in ['to', 'from']:
                return SwumAttrRule.starts_with_prep1
            else:
                return SwumAttrRule.starts_with_prep_default

        return None


    def associateWords(self, pos_tokens:List[str], literal_tokens:List[str], head=True):
        # make copy to preserve initial input tokens
        if head:
            pos_tokens = list(pos_tokens)
            literal_tokens = list(literal_tokens)

            self.pos_tokens = list(pos_tokens)
            self.literal_tokens = list(literal_tokens)
        
        if self.isTerminal:
            self.pos = pos_tokens.pop(0)
            self.literal = literal_tokens.pop(0)
        else:
            for edge in self.edges:
                child = edge.child
                child.associateWords(pos_tokens, literal_tokens, False)

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
            str_repr += self.literal
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

    

# for <swum_identifier> xml node
def get_metadata(element):
    metadata = {'location': None, 'name': None, 'word_tokens': [], 'pos_tokens': [], 'class_tokens': [], 'class_pos_tokens': [], 'type_tokens': [], 'type_pos_tokens': [], 'parameter_tokens': [], 'parameter_pos_tokens': [], }
    for child in element:
        if child.tag == 'location':
            metadata['location'] = child.text.strip()
        elif child.tag == 'name':
            metadata['name'] = child.text.strip()
        elif child.tag == 'class':
            # resolve class name to class metadata, add to this identifier's metadata
            class_metadata = class_dict[child.text.strip()]
            metadata['class_tokens'] = class_metadata['word_tokens']
            metadata['class_pos_tokens'] = class_metadata['pos_tokens']
        elif child.tag == 'type':
            type_metadata = get_metadata(child[0])
            for grand in child[0]:
                print(grand.tag)
            print(etree.tostring(child))
            print(type_metadata)
            metadata['type_tokens'] = type_metadata['word_tokens']
            metadata['type_pos_tokens'] = type_metadata['pos_tokens']
        elif child.tag == 'parameters':
            print('reading parameters')
            print(etree.tostring(child))
            for parameter_node in child:
                # print(parameter_node.tag)
                parameter_metadata = get_metadata(parameter_node)
                # print(parameter_metadata)
                metadata['parameter_tokens'].append(parameter_metadata['word_tokens'])
                metadata['parameter_pos_tokens'].append(parameter_metadata['pos_tokens'])
        elif child.tag == 'identifier':
            for word_node in child:
                metadata['word_tokens'].append(word_node.text.strip())
                pos_node = word_node[0]
                metadata['pos_tokens'].append(pos_node.text.strip())

    
    return metadata

def get_annotated_swum_phrase(metadata: dict) -> SwumPhrasesNode:
    parsed_identifier = get_swum_phrase(metadata['pos_tokens'], metadata['word_tokens'])
    attr_rule = parsed_identifier.get_attr_rule(metadata)

    swum_phrase = SwumPhrasesNode(literal=metadata['name'])

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
            # construct VP node and make it parent of VG
            swum_phrase.addEdge(first_child, 'action')
            
            if len(parsed_identifier.edges) > 1:
                swum_phrase.addEdge(parsed_identifier.edges[1].child, 'theme')
            elif len(metadata['parameter_tokens']) > 0:
                node = get_swum_phrase(metadata['parameter_pos_tokens'].pop(0), metadata['parameter_tokens'].pop(0))
                swum_phrase.addEdge(node, 'theme')
            else:
                node = get_swum_phrase(metadata['class_pos_tokens'], metadata['class_tokens'])
                swum_phrase.addEdge(node, 'theme')
            
        # identify secondary args
        # none for verb_default

        # identify aux args
        # formal parameters
        for index, pos_tokens in enumerate(metadata['parameter_pos_tokens']):
            # print(metadata['parameter_pos_tokens'])
            # print(metadata['parameter_tokens'])
            node = get_swum_phrase(pos_tokens, metadata['parameter_tokens'][index])
            swum_phrase.addEdge(node, 'aux_arg')
        # return type
        if len(metadata['type_tokens']) == 1 and metadata['type_tokens'][0] == 'void':
            pass
        else:
            node = get_swum_phrase(metadata['type_pos_tokens'], metadata['type_tokens'])
            swum_phrase.addEdge(node, 'aux_arg')
        # class
        node = get_swum_phrase(metadata['class_pos_tokens'], metadata['class_tokens'])
        swum_phrase.addEdge(node, 'aux_arg')
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
            else:
                node = get_swum_phrase(metadata['class_pos_tokens'], metadata['class_tokens'])
                swum_phrase.addEdge(node, 'theme')

            # secondary args
            for edge in parsed_identifier.edges:
                if edge.child.nodeType == 'prepositional_phrase':
                    swum_phrase.addEdge(edge.child, 'secondary_arg')
                    break


        # identify aux args
        # formal parameters
        for index, pos_tokens in enumerate(metadata['parameter_pos_tokens']):
            node = get_swum_phrase(pos_tokens, metadata['parameter_tokens'][index])
            swum_phrase.addEdge(node, 'aux_arg')
        # return type
        if len(metadata['type_tokens']) == 1 and metadata['type_tokens'][0] == 'void':
            pass
        else:
            node = get_swum_phrase(metadata['type_pos_tokens'], metadata['type_tokens'])
            swum_phrase.addEdge(node, 'aux_arg')
        # class
        node = get_swum_phrase(metadata['class_pos_tokens'], metadata['class_tokens'])
        swum_phrase.addEdge(node, 'aux_arg')
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
            elif len(metadata['parameter_tokens']) > 0:
                node = get_swum_phrase(metadata['parameter_pos_tokens'].pop(0), metadata['parameter_tokens'].pop(0))
                swum_phrase.addEdge(node, 'condition')
            else:
                node = get_swum_phrase(metadata['class_pos_tokens'], metadata['class_tokens'])
                swum_phrase.addEdge(node, 'condition')
            
        # identify secondary args
        # class
        node = get_swum_phrase(metadata['class_pos_tokens'], metadata['class_tokens'])
        swum_phrase.addEdge(node, 'subject')

        # identify aux args
        # formal parameters
        for index, pos_tokens in enumerate(metadata['parameter_pos_tokens']):
            node = get_swum_phrase(pos_tokens, metadata['parameter_tokens'][index])
            swum_phrase.addEdge(node, 'subject')
    elif attr_rule in [SwumAttrRule.general, SwumAttrRule.event_handler, SwumAttrRule.starts_with_prep0, SwumAttrRule.noun_phrase_void]:
        swum_phrase.addEdge(get_swum_phrase(['VBZ'], ['handle']), 'action')
        # if identifier parses into multiple phrases, have multiple themes
        for edge in parsed_identifier.edges:
            swum_phrase.addEdge(edge.child, 'theme')
        
        # identify aux args
        # formal parameters
        for index, pos_tokens in enumerate(metadata['parameter_pos_tokens']):
            node = get_swum_phrase(pos_tokens, metadata['parameter_tokens'][index])
            swum_phrase.addEdge(node, 'aux_arg')
        # return type
        if len(metadata['type_tokens']) == 1 and metadata['type_tokens'][0] == 'void':
            pass
        else:
            node = get_swum_phrase(metadata['type_pos_tokens'], metadata['type_tokens'])
            swum_phrase.addEdge(node, 'aux_arg')
        # class
        node = get_swum_phrase(metadata['class_pos_tokens'], metadata['class_tokens'])
        swum_phrase.addEdge(node, 'aux_arg')
    elif attr_rule in [SwumAttrRule.starts_with_prep1, SwumAttrRule.starts_with_prep_default]:
        swum_phrase.addEdge(get_swum_phrase(['VBZ'], ['convert']), 'action')
        # if identifier parses into multiple phrases, have multiple secondary args
        for edge in parsed_identifier.edges:
            swum_phrase.addEdge(edge.child, 'secondary_arg')
        
        # identify aux args
        # formal parameters
        for index, pos_tokens in enumerate(metadata['parameter_pos_tokens']):
            node = get_swum_phrase(pos_tokens, metadata['parameter_tokens'][index])
            swum_phrase.addEdge(node, 'aux_arg')
        # return type
        if len(metadata['type_tokens']) == 1 and metadata['type_tokens'][0] == 'void':
            pass
        else:
            node = get_swum_phrase(metadata['type_pos_tokens'], metadata['type_tokens'])
            swum_phrase.addEdge(node, 'aux_arg')
        # class
        node = get_swum_phrase(metadata['class_pos_tokens'], metadata['class_tokens'])
        swum_phrase.addEdge(node, 'aux_arg')
    elif attr_rule == SwumAttrRule.noun_phrase_non_void:
        swum_phrase.addEdge(get_swum_phrase(['VBZ'], ['get']), 'action')
        # if identifier parses into multiple phrases, have multiple themes
        for edge in parsed_identifier.edges:
            swum_phrase.addEdge(edge.child, 'theme')
        
        # identify aux args
        # formal parameters
        for index, pos_tokens in enumerate(metadata['parameter_pos_tokens']):
            node = get_swum_phrase(pos_tokens, metadata['parameter_tokens'][index])
            swum_phrase.addEdge(node, 'aux_arg')
        # return type
        if len(metadata['type_tokens']) == 1 and metadata['type_tokens'][0] == 'void':
            pass
        else:
            node = get_swum_phrase(metadata['type_pos_tokens'], metadata['type_tokens'])
            swum_phrase.addEdge(node, 'aux_arg')
        # class
        node = get_swum_phrase(metadata['class_pos_tokens'], metadata['class_tokens'])
        swum_phrase.addEdge(node, 'aux_arg')
    elif attr_rule == SwumAttrRule.constructor:
        swum_phrase.addEdge(get_swum_phrase(['VBZ'], ['create']), 'action')
        swum_phrase.addEdge(get_swum_phrase(['VBZ'], ['construct']), 'action')
        # if identifier parses into multiple phrases, have multiple themes
        for edge in parsed_identifier.edges:
            swum_phrase.addEdge(edge.child, 'theme')
        
        # identify aux args
        # formal parameters
        for index, pos_tokens in enumerate(metadata['parameter_pos_tokens']):
            node = get_swum_phrase(pos_tokens, metadata['parameter_tokens'][index])
            swum_phrase.addEdge(node, 'aux_arg')
    elif attr_rule == SwumAttrRule.all_preamble:
        fail('Error: preambles are not yet supported')
    else:
        fail('Error: did not recognize rule for phrase tree')

    return swum_phrase

class SwumPhrasesEdge():
    def __init__(self, child=None, label=None):
        self.child = child
        self.label = label

class SwumVisitor(SwumParserVisitor):
    # Visit a parse tree produced by SwumParser#swum_phrase.
    def visitSwum_phrase(self, ctx:SwumParser.Swum_phraseContext):
        return SwumPhrasesNode(antlr_ctx=ctx)


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
