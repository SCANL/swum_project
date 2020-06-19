
import sys
sys.path.append('/home/brian/reu/swum_project/swum_phrases')    # allow import of modules outside of test directory
from antlr4 import *
from SwumLexer import SwumLexer
from SwumParser import SwumParser
from MyVisitor import PrintVisitor

def parse_xml(string):
    input_stream = InputStream(string)
    lexer = SwumLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SwumParser(stream)
    tree = parser.phrase()

    visitor = PrintVisitor(stream)
    visitor.visit(tree)
    return str(visitor.ds)

def test_noun_phrase():
    # NM N
    assert parse_xml('<location>parameter</location><type>int</type><name>perfect</name><POS>NM</POS><name>ID</name><POS>N</POS>') == '<noun_phrase><location>parameter</location><type>int</type><name>perfectID</name><Noun_Modifier>perfect</Noun_Modifier><Noun>ID</Noun></noun_phrase>'

def test_prepositional_phrase():
    # P NM N
    assert parse_xml('<location>function</location><type>int</type><name>to</name><POS>P</POS><name>Perfect</name><POS>NM</POS><name>ID</name><POS>N</POS>') == '<prepositional_phrase><location>function</location><type>int</type><name>toPerfectID</name><Preposition>to</Preposition><noun_phrase><name>PerfectID</name><Noun_Modifier>Perfect</Noun_Modifier><Noun>ID</Noun></noun_phrase></prepositional_phrase>'

def test_verb_phrase():
    # VM V N P NM N
    assert parse_xml('<location>function</location><type>int</type><name>quickly></name><POS>VM</POS><name>Convert</name><POS>V</POS><name>ID</name><POS>N</POS><name>To</name><POS>P</POS><name>Perfect</name><POS>NM</POS><name>ID</name><POS>N</POS>') == '<verb_phrase><location>function</location><type>int</type><name>quicklyConvertIDToPerfectID</name><verb_group><name>quicklyConvert</name><Verb_Modifier>quickly</Verb_Modifier><Verb>Convert</Verb></verb_group><noun_phrase><name>ID</name><Noun>ID</Noun></noun_phrase><prepositional_phrase><name>ToPerfectID</name><Preposition>To</Preposition><noun_phrase><name>PerfectID</name><Noun_Modifier>Perfect</Noun_Modifier><Noun>ID</Noun></noun_phrase></prepositional_phrase></verb_phrase>'
