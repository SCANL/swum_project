
# import sys
# sys.path.append('/home/brian/reu/swum_project/swum_phrases')    # allow import of modules outside of test directory
# from antlr4 import *
# from SwumLexer import SwumLexer
# from SwumParser import SwumParser
# from MyVisitor import PrintVisitor

# def parse_string(string):
#     input_stream = InputStream(string)
#     lexer = SwumLexer(input_stream)
#     stream = CommonTokenStream(lexer)
#     parser = SwumParser(stream)
#     tree = parser.phrase()

#     visitor = PrintVisitor()
#     visitor.visit(tree)
#     return visitor.str_output

# def test_parse_basic_phrases():
#     # noun phrase
#     assert parse_string('NM N') == 'NP(NM N)'
#     # prepositional phrase
#     assert parse_string('P NM N') == 'PP(P NP(NM N))'
#     # verb phrase simple
#     assert parse_string('VM V N P NM N') == 'VP(VG(VM V) NP(N) PP(P NP(NM N)))'
#     # verb phrase complex
#     assert parse_string('VM VM VM V VPR V NM NM N NM N P NM NM NM N') == 'VP(EQ_vg(VG(VM VM VM V VPR) VG(V)) EQ_np(NP(NM NM N) NP(NM N)) PP(P NP(NM NM NM N)))'

# def test_rule_example_phrases():
#     # commit
#     assert parse_string('V') == 'VG(V)'
#     # parseStringForDateInformation
#     assert parse_string('V N P NM N') == 'VP(VG(V) NP(N) PP(P NP(NM N)))'
#     # onFailure
#     assert parse_string('P N') == 'PP(P NP(N))'
#     # factorial
#     assert parse_string('N') == 'NP(N)'
#     # onDestroy
#     assert parse_string('P N') == 'PP(P NP(N))'
#     # fromBytes
#     assert parse_string('P N') == 'PP(P NP(N))'
#     # asSet
#     assert parse_string('P N') == 'PP(P NP(N))'
#     # errorOutput
#     assert parse_string('NM N') == 'NP(NM N)'
#     # messageReceived
#     assert parse_string('VM V') == 'VG(VM V)'
#     # StoryTest
#     assert parse_string('NM N') == 'NP(NM N)'

# def test_improved_grammar():
#     # convertToMinCardinalityRestriction
#     assert parse_string('V P NM NM N') == 'VG(V) PP(P NP(NM NM N))'  # (VG PP) not supported by grammar as presented in paper

# def test_preamble_support():
#     # jj_3R_188
#     # ICStart
#     # ejbCreate
#     pass
