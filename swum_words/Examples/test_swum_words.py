# Author: Aditya Bhargava (abhargava@g.hmc.edu)
# Date: Summer 2020
# Organization: RIT REU Cultivating New Generation Software
# Function: Tests swum_words.py using boundary testing and equivalence class partitioning
from swum_words import *
from xml.etree import ElementTree
import unittest
class Test(unittest.TestCase):
    maxDiff = None
    def test_swum_words(self):
        parser = xml.sax.make_parser() # Create an XMLReader
        parser.setFeature(xml.sax.handler.feature_namespaces, 0) # Turn off namepsaces
        Handler = JavaHandler() # Override the default ContextHandler
        parser.setContentHandler(Handler)
        parser.parse("MyClass.xml") # Parses an xml file
        xmlResultString = xml.etree.ElementTree.tostring(Handler.xmlResult)
        self.assertEqual(xmlResultString,'<swum_identifiers><swum_identifier><location>class</location><name>MyClass</name><identifier><word>My<pos>PRP$</pos></word><word>Class<pos>NN</pos></word></identifier></swum_identifier><swum_identifier><location>constructor</location><class>MyClass</class><name>MyClass</name><identifier><word>My<pos>PRP$</pos></word><word>Class<pos>NN</pos></word></identifier></swum_identifier><swum_identifier><location>function</location><class>MyClass</class><name>getArea</name><type><swum_identifier><location>type</location><name>int</name><identifier><word>int<pos>NN</pos></word></identifier></swum_identifier></type><parameters><swum_identifier><location>parameter</location><name>x</name><type><swum_identifier><location>type</location><name>int</name><identifier><word>int<pos>NN</pos></word></identifier></swum_identifier></type><identifier><word>x<pos>NN</pos></word></identifier></swum_identifier><swum_identifier><location>parameter</location><name>y</name><type><swum_identifier><location>type</location><name>int</name><identifier><word>int<pos>NN</pos></word></identifier></swum_identifier></type><identifier><word>y<pos>NN</pos></word></identifier></swum_identifier></parameters><identifier><word>get<pos>VB</pos></word><word>Area<pos>NNP</pos></word></identifier></swum_identifier><swum_identifier><location>decl</location><name>z</name><type><swum_identifier><location>type</location><name>int</name><identifier><word>int<pos>NN</pos></word></identifier></swum_identifier></type><identifier><word>z<pos>NN</pos></word></identifier></swum_identifier></swum_identifiers>')
if __name__ == '__main__':
    unittest.main()