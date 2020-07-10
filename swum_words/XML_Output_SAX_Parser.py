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
        self.dictTag = {"decl": 0, "decl_stmt": 0, "type": 0, "name": 0, "class": 0, "function": 0, "function_decl": 0,
                        "expr": 0, "expr_stmt": 0, "parameter": 0, "parameter_list": 0, "operator": 0, "specifier": 0, "constructor": 0, "interface": 0, "interface_decl": 0}
        self.xml = etree.Element('swum_identifiers')
        # Used to define attributes
        self.interface = ""
        self.variable = ""
        self.function = ""
        self.constructor = ""
        self.type = ""
        self.className = ""
        self.currentContent = ""
        # Used for parameters in functions and constructors
        self.parameterList = []
        self.parameterType = []
        self.parameterDict = {}
        # Used for Part of Speech (POS) tagging
        self.dictPOS = {}  
        self.sentence = ""  
    # Call when an element starts
    def startElement(self, tag, attributes):  
        for x in self.dictTag:
            if tag == x:
                self.dictTag[tag] += 1
    # Part Of Speech (POS) Tagging
    def PartOfSpeechTag(self,currentContent, tree):
        self.sentence = ""
        tempList = ronin.split(currentContent)
        for word in tempList:
            self.sentence = self.sentence + word + " "
            self.text = word_tokenize(self.sentence)
            self.dictPOS[currentContent] = nltk.pos_tag(self.text)
        for splitWord in self.dictPOS[currentContent]:
            wordTag = etree.SubElement(tree, 'word')
            wordTag.text = splitWord[0]
            partOfSpeechTag = etree.SubElement(wordTag, 'pos')
            partOfSpeechTag.text = splitWord[1]
    # XML writer for class names, parameters, variable names, and interface names
    def XMLWriter(self,locationTagText,tree,currentContent, parameterType): 
        swumIdentifierTag = etree.SubElement(tree, 'swum_identifier')
        locationTag = etree.SubElement(swumIdentifierTag, 'location')
        locationTag.text = locationTagText
        nameTag = etree.SubElement(swumIdentifierTag, 'name')
        nameTag.text = currentContent
        identifierTag = etree.SubElement(swumIdentifierTag, 'identifier')
        self.PartOfSpeechTag(currentContent, identifierTag)
        # Recursive call for parameters and types
        if parameterType and self.parameterList:
            typeTag = etree.SubElement(swumIdentifierTag, 'type')
            self.XMLWriter("type", typeTag, self.type, '')
    # XML writer for functions and constructor names
    def functionAndConstructorXMLWriter(self):
        swumIdentifierTag = etree.SubElement(self.xml, 'swum_identifier')
        locationTag = etree.SubElement(swumIdentifierTag, 'location')
        if self.constructor:
            name = self.constructor
            locationTag.text = "constructor"
        else:
            name = self.function
            locationTag.text = "function"
        classTag = etree.SubElement(swumIdentifierTag, 'class')
        classTag.text = self.className
        nameTag = etree.SubElement(swumIdentifierTag, 'name')
        nameTag.text = name
        if self.type:
            typeTag = etree.SubElement(swumIdentifierTag, 'type')
            self.XMLWriter("type", typeTag, self.type, '')
        if self.parameterList:
            parameterTag = etree.SubElement(swumIdentifierTag, 'parameters')
            for key in self.parameterDict:
                self.XMLWriter("parameter", parameterTag, key, self.parameterDict[key])
        identifierTag = etree.SubElement(swumIdentifierTag, 'identifier')
        self.PartOfSpeechTag(name, identifierTag)
        # Resetting the function, constructor, and parameter attributes
        self.function = ""
        self.constructor = ""
        self.parameterList = []
        self.parameterType = []
        self.type = ""
        self.parameterDict.clear()
    # Call when an elements ends
    def endElement(self, tag):
        # The function and constructor information is complete and therefore sent to their XML writer
        if tag == "parameter_list":
            for tempNum in range(0,len(self.parameterList)):
                self.parameterDict[self.parameterList[tempNum]] = self.parameterType[tempNum]
            self.functionAndConstructorXMLWriter()
        # Determining self.currentContent's location
        if tag == "name":
            if not (self.dictTag["expr"] or self.dictTag["expr_stmt"]):
                if not (self.dictTag["type"]) or self.dictTag["parameter_list"]:
                    if self.dictTag["class"] and not (self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"] or self.dictTag["constructor"]):
                        print("Class Name: ", self.currentContent)
                        self.className = self.currentContent
                        self.XMLWriter("class", self.xml, self.currentContent, '')
                    elif self.dictTag["constructor"] and not(self.dictTag["parameter"]):
                        print("Constructor Name: ", self.currentContent)  
                        self.constructor = self.currentContent            
                    elif self.dictTag["parameter_list"]:
                        if self.dictTag["name"] and self.dictTag["parameter"]and self.dictTag["type"]:
                            print("Parameter Type: ", self.currentContent)
                            self.parameterType.append(self.currentContent)
                        elif self.dictTag["name"] and self.dictTag["parameter"]:
                            print("Parameter Name: ", self.currentContent)
                            self.parameterList.append(self.currentContent)
                    elif self.dictTag["decl_stmt"] or self.dictTag["decl"] and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                        print("Variable Name: ", self.currentContent)
                        self.variable = self.currentContent
                        self.XMLWriter("decl", self.xml, self.currentContent, '')
                    elif self.dictTag["function"] or self.dictTag["function_decl"] and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                        print("Function Name: ", self.currentContent)
                        self.function = self.currentContent
                    elif self.dictTag["interface"] or self.dictTag["interface_decl"] and not(self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                        print("Interface Name: ", self.currentContent)
                        self.interface = self.currentContent 
                        self.XMLWriter("interface", self.xml, self.currentContent, '')
                elif(self.dictTag["type"]):
                    print("Type: ", self.currentContent)
                    self.type = self.currentContent
            self.dictTag[tag] -= 1
        elif tag == "specifier":
            print("Specifier: ", self.currentContent)
            self.dictTag[tag] -= 1
        else:
            for x in self.dictTag:
                if tag == x:
                    self.dictTag[tag] -= 1
    # Called when a character is called 
    def characters(self, content):
        self.currentContent = ""
        self.currentContent += content

# Source: PyMOTW-3 "Building Documents with Element Nodes"
# Prints the XML file into an understandable and comprehensible format
def prettify(elem):  
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


if (__name__ == "__main__"):
    # Create an XMLReader
    parser = xml.sax.make_parser()
    # Turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces,0)  
    # Override the default ContextHandler
    Handler = JavaHandler()  
    parser.setContentHandler(Handler)
     # Parses an xml file
    parser.parse("Java.xml")
    # Prints the SAX Parser result as a "pretty" XML file
    print(prettify(Handler.xml))  