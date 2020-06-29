# test_SAX_Parser.py
# Author: Aditya Bhargava (abhargava@g.hmc.edu)
# Date: Summer 2020
# Organization: RIT REU Cultivating New Generation Software
# Function: Tests SAX_Parser.py where "Java.xml" is: 
# <class><specifier>public</specifier> class <name>MyPublicClass</name> <block>{
# <class><specifier>private</specifier> class <name>Helper</name>
# <block>{
# }</block></class>
# }</block></class>
from SAX_Parser import*
import unittest
class Test(unittest.TestCase):
    def test_SAX_Parser(self):
        parser = xml.sax.make_parser() # Create an XMLReader
        parser.setFeature(xml.sax.handler.feature_namespaces, 0) # Turn off namepsaces
        Handler = JavaHandler() # Override the default ContextHandler
        parser.setContentHandler(Handler)
        parser.parse("Java.xml") # Parses an xml file 
        self.assertEqual(Handler.listName, ['MyPublicClass', 'Helper']) 
        self.assertEqual(Handler.dictName, {'MyPublicClass': 'class', 'Helper': 'class'})
        self.assertEqual(Handler.dictPOS, {'MyPublicClass': [('My', 'PRP$'), ('Public', 'JJ'), ('Class', 'NN')], 'Helper': [('Helper', 'NN')]})
if __name__ == '__main__':
    unittest.main()
