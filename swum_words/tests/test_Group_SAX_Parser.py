# Author: Aditya Bhargava (abhargava@g.hmc.edu)
# Date: Summer 2020
# Organization: RIT REU Cultivating New Generation Software
# Function: Tests Group_SAX_Parser.py where "Group.xml" is uploaded in the test folder
from Group_SAX_Parser import*
import unittest
class Test(unittest.TestCase):
    def test_SAX_Parser(self):
        parser = xml.sax.make_parser() # Create an XMLReader
        parser.setFeature(xml.sax.handler.feature_namespaces, 0) # Turn off namepsaces
        Handler = GroupHandler() # Override the default ContextHandler
        parser.setContentHandler(Handler)
        parser.parse("Group.xml") # Parses an xml file 
        self.assertEqual(Handler.nameList, [' Adi ', ' Tom ', ' Chad ']) 
        self.assertEqual(Handler.ageList, [' 18', ' 18', ' 18'])
        self.assertEqual(Handler.weightList, [' 170 ', ' 170 ', ' 170 '])
        self.assertEqual(Handler.heighList, [[' 74 ', ' 74 ', ' 74 ']]) 
if __name__ == '__main__':
    unittest.main()
