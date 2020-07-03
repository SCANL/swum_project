# Author: Aditya Bhargava (abhargava@g.hmc.edu)
# Date: Summer 2020
# Organization: RIT REU Cultivating New Generation Software
# Function: Takes an XML file and analyzes it based on identifier name and function using a SAX parser. Prints the results in a XML format.
import xml.sax
import nltk
from xml.etree import ElementTree
from xml.dom import minidom
from lxml import etree 
from spiral import ronin
from nltk.tokenize import sent_tokenize, word_tokenize


class JavaHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.currentTag = ""
        self.currentContent = ""
        self.dictTag = {"decl": 0, "decl_stmt": 0, "type": 0, "name": 0, "class": 0, "function": 0, "function_decl": 0,
                        "expr": 0, "expr_stmt": 0, "parameter": 0, "parameter_list": 0, "operator": 0, "specifier": 0, "constructor": 0, "interface": 0, "interface_decl": 0}
        self.dictPOS = {}  # Stores the part of speech of every identifier
        self.sentence = ""  # Used for Part of Speech (POS) tagging
        self.xml = etree.Element('swum_identifiers')
        

    def startElement(self, tag, attributes):  # Call when an element starts
        for x in self.dictTag:
            if tag == x:
                self.dictTag[tag] += 1

    def endElement(self, tag):  # Call when an elements ends
        self.sentence = ""
        if tag == "name":
            # Eliminates the expression statments since variable names are already declared
            if not (self.dictTag["expr"] or self.dictTag["expr_stmt"]):
                # Differentiates between type and name
                if not (self.dictTag["type"]):
                    if self.dictTag["class"] and not (self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"] or self.dictTag["constructor"]):
                        # Stores the class name and assigns the key a "class" value
                        print("Class Name: ", self.currentContent)
                        #classTag = etree.SubElement(self.xml, 'class') # Defines class tag
                        swumIdentifierTag = etree.SubElement( # Defines swum_identifier tag
                            self.xml, 'swum_identifier')
                        locationTag = etree.SubElement( # Defines location tag
                            swumIdentifierTag, 'location')
                        locationTag.text = 'class'
                        identifier = etree.SubElement( # Defines identifier tag
                            swumIdentifierTag, 'identifier')
                        tempList = ronin.split(self.currentContent) # Splits the current identifer into the respective words 
                        for word in tempList: # Part of Speech Tagger 
                            self.sentence = self.sentence + word + " " # Part of Speech Tagger functions when a sentence is used as a parameter
                            self.text = word_tokenize(self.sentence)
                            self.dictPOS[self.currentContent] = nltk.pos_tag(
                                self.text)
                        for splitWord in self.dictPOS[self.currentContent]: # Asserting each word to a wordTag and part of speech to a POS tag
                            wordTag = etree.SubElement(identifier, 'word')
                            wordTag.text = splitWord[0]
                            partOfSpeechTag = etree.SubElement(wordTag, 'pos')
                            partOfSpeechTag.text = splitWord[1]
                    elif self.dictTag["constructor"]:
                        print("Constructor Name: ", self.currentContent)
                        swumIdentifierTag = etree.SubElement(
                            self.xml, 'swum_identifier')
                        location = etree.SubElement(swumIdentifierTag, 'location')
                        location.text = 'constructor'
                        identifier = etree.SubElement(swumIdentifierTag, 'identifier')
                        tempList = ronin.split(self.currentContent)
                        for word in tempList:
                            self.sentence = self.sentence + word + " "
                            self.text = word_tokenize(self.sentence)
                            self.dictPOS[self.currentContent] = nltk.pos_tag(
                                self.text)
                        for splitWord in self.dictPOS[self.currentContent]:
                            wordTag = etree.SubElement(identifier, 'word')
                            wordTag.text = splitWord[0]
                            partOfSpeechTag = etree.SubElement(wordTag, 'pos')
                            partOfSpeechTag.text = splitWord[1]
                    elif self.dictTag["parameter"] or self.dictTag["parameter_list"] and not (self.dictTag["class"]):
                        print("Parameter Name: ", self.currentContent)
                        #parameterTag = etree.SubElement(self.xml, 'parameter')
                        swumIdentifierTag = etree.SubElement(
                            self.xml, 'swum_identifier')
                        location = etree.SubElement(
                            swumIdentifierTag, 'location')
                        location.text = 'parameter'
                        identifier = etree.SubElement(
                            swumIdentifierTag, 'identifier')
                        tempList = ronin.split(self.currentContent)
                        for word in tempList:
                            self.sentence = self.sentence + word + " "
                            self.text = word_tokenize(self.sentence)
                            self.dictPOS[self.currentContent] = nltk.pos_tag(
                                self.text)
                        for splitWord in self.dictPOS[self.currentContent]:
                            wordTag = etree.SubElement(identifier, 'word')
                            wordTag.text = splitWord[0]
                            partOfSpeechTag = etree.SubElement(wordTag, 'pos')
                            partOfSpeechTag.text = splitWord[1]
                    elif self.dictTag["function"] or self.dictTag["function_decl"] and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                        print("Function Name: ", self.currentContent)
                        #functionTag = etree.SubElement(self.xml, 'function')
                        swumIdentifierTag = etree.SubElement(
                            self.xml, 'swum_identifier')
                        location = etree.SubElement(
                            swumIdentifierTag, 'location')
                        location.text = 'function'
                        identifier = etree.SubElement(
                            swumIdentifierTag, 'identifier')
                        tempList = ronin.split(self.currentContent)
                        for word in tempList:
                            self.sentence = self.sentence + word + " "
                            self.text = word_tokenize(self.sentence)
                            self.dictPOS[self.currentContent] = nltk.pos_tag(
                                self.text)
                        for splitWord in self.dictPOS[self.currentContent]:
                            wordTag = etree.SubElement(identifier, 'word')
                            wordTag.text = splitWord[0]
                            partOfSpeechTag = etree.SubElement(wordTag, 'pos')
                            partOfSpeechTag.text = splitWord[1]
                    elif self.dictTag["interface"] or self.dictTag["interface_decl"] and not(self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                        print("Interface Name: ", self.currentContent)
                        swumIdentifierTag = etree.SubElement(
                            self.xml, 'swum_identifier')
                        location = etree.SubElement(
                            swumIdentifierTag, 'location')
                        location.text = 'interface'
                        identifier = etree.SubElement(
                            swumIdentifierTag, 'identifier')
                        tempList = ronin.split(self.currentContent)
                        for word in tempList:
                            self.sentence = self.sentence + word + " "
                            self.text = word_tokenize(self.sentence)
                            self.dictPOS[self.currentContent] = nltk.pos_tag(
                                self.text)
                        for splitWord in self.dictPOS[self.currentContent]:
                            wordTag = etree.SubElement(identifier, 'word')
                            wordTag.text = splitWord[0]
                            partOfSpeechTag = etree.SubElement(wordTag, 'pos')
                            partOfSpeechTag.text = splitWord[1]
                    elif self.dictTag["decl_stmt"] or self.dictTag["decl"] and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                        print("Variable Name: ", self.currentContent)
                        #variableTag = etree.SubElement(self.xml, 'variable')
                        swumIdentifierTag = etree.SubElement(
                            self.xml, 'swum_identifier')
                        location = etree.SubElement(
                            swumIdentifierTag, 'location')
                        location.text = 'variable'
                        identifier = etree.SubElement(
                            swumIdentifierTag, 'identifier')
                        tempList = ronin.split(self.currentContent)
                        for word in tempList:
                            self.sentence = self.sentence + word + " "
                            self.text = word_tokenize(self.sentence)
                            self.dictPOS[self.currentContent] = nltk.pos_tag(
                                self.text)
                        for splitWord in self.dictPOS[self.currentContent]:
                            wordTag = etree.SubElement(identifier, 'word')
                            wordTag.text = splitWord[0]
                            partOfSpeechTag = etree.SubElement(wordTag, 'pos')
                            partOfSpeechTag.text = splitWord[1]
                elif(self.dictTag["type"] and not(self.currentContent == 'int' or self.currentContent == 'void' or self.currentContent == 'boolean' or self.currentContent == 'double' or self.currentContent == 'float' or self.currentContent == 'char' or self.currentContent == 'String' or '[]' in self.currentContent)): # Filters out the primitive data types and arrays. 
                    print("Type: ", self.currentContent)
                    #typeTag = etree.SubElement(self.xml, 'type')
                    swumIdentifierTag = etree.SubElement(
                        self.xml, 'swum_identifier')
                    location = etree.SubElement(swumIdentifierTag, 'location')
                    location.text = 'type'
                    identifier = etree.SubElement(
                        swumIdentifierTag, 'identifier')
                    tempList = ronin.split(self.currentContent)
                    for word in tempList:
                        self.sentence = self.sentence + word + " "
                        self.text = word_tokenize(self.sentence)
                        self.dictPOS[self.currentContent] = nltk.pos_tag(
                            self.text)
                    for splitWord in self.dictPOS[self.currentContent]:
                        wordTag = etree.SubElement(identifier, 'word')
                        wordTag.text = splitWord[0]
                        partOfSpeechTag = etree.SubElement(wordTag, 'pos')
                        partOfSpeechTag.text = splitWord[1]
            self.dictTag[tag] -= 1
        elif tag == "specifier":
            print("Specifier: ", self.currentContent)
            self.dictTag[tag] -= 1
        else:
            for x in self.dictTag:
                if tag == x:
                    self.dictTag[tag] -= 1
        if tag == "name":
            tempList = ronin.split(self.currentContent)
            for word in tempList:
                self.sentence = self.sentence + word + " "
                self.text = word_tokenize(self.sentence)
                self.dictPOS[self.currentContent] = nltk.pos_tag(self.text)
        self.currentTag = ""  # Call when a character is read

    def characters(self, content):
        self.currentContent = ""
        self.currentContent += content

# Source: PyMOTW-3 "Building Documents with Element Nodes"
def prettify(elem):  # Prints the XML file into an understandable and comprehensible format
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


if (__name__ == "__main__"):
    parser = xml.sax.make_parser()  # Create an XMLReader
    parser.setFeature(xml.sax.handler.feature_namespaces,0)  # Turn off namepsaces
    Handler = JavaHandler()  # Override the default ContextHandler
    parser.setContentHandler(Handler)
    parser.parse("Java.xml")  # Parses an xml file
    print(prettify(Handler.xml))  # Prints the SAX Parser results as an XML file
