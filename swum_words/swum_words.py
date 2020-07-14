# Author: Aditya Bhargava (abhargava@g.hmc.edu)
# Date: Summer 2020
# Organization: RIT REU Cultivating New Generation Software
# Function: Takes an XML file and analyzes it based on identifier name and function using a SAX parser. Prints the results in a XML format.
import sys
# Part of Speech tagging tools
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from spiral import ronin
# XML Writer
import xml.sax 
from xml.etree import ElementTree
from xml.dom import minidom
from lxml import etree 

class JavaHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.dictTag = {"decl": 0, "decl_stmt": 0, "type": 0, "name": 0, "class": 0, "function": 0, "function_decl": 0,
                        "expr": 0, "expr_stmt": 0, "parameter": 0, "parameter_list": 0, "operator": 0, "specifier": 0, "constructor": 0, "interface": 0, "interface_decl": 0}
        self.xmlResult = etree.Element('swum_identifiers')
        # Used to define attributes
        self.interfaceName = ""
        self.variableName = ""
        self.functionName = ""
        self.constructorName = ""
        self.type = ""
        self.variableType = ""
        self.functionType = ""
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
        tempList = self.dictPOS[currentContent]
        for splitWord in tempList:
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
        if parameterType and self.parameterList:
            typeTag = etree.SubElement(swumIdentifierTag, 'type')
            self.XMLWriter("type", typeTag, parameterType, '')
        identifierTag = etree.SubElement(swumIdentifierTag, 'identifier')
        self.PartOfSpeechTag(currentContent, identifierTag)
    # XML writer for functions and constructor names
    def functionConstructorDeclXMLWriter(self):
        swumIdentifierTag = etree.SubElement(self.xmlResult, 'swum_identifier')
        locationTag = etree.SubElement(swumIdentifierTag, 'location')
        if self.constructorName or self.functionName:
            classTag = etree.SubElement(swumIdentifierTag, 'class')
            classTag.text = self.className
            if self.constructorName:
                name = self.constructorName
                locationTag.text = "constructor"
            else:
                name = self.functionName
                locationTag.text = "function"
        else: 
            name = self.variableName
            locationTag.text = "decl"
        nameTag = etree.SubElement(swumIdentifierTag, 'name')
        nameTag.text = name
        if self.functionType or self.variableType:
            typeTag = etree.SubElement(swumIdentifierTag, 'type')
            if self.functionType:
                self.XMLWriter("type", typeTag, self.functionType, '')
            else:
                self.XMLWriter("type", typeTag, self.variableType, '')
        if self.parameterList:
            parameterTag = etree.SubElement(swumIdentifierTag, 'parameters')
            for key in self.parameterDict:
                self.XMLWriter("parameter", parameterTag, key, self.parameterDict[key])
        identifierTag = etree.SubElement(swumIdentifierTag, 'identifier')
        self.PartOfSpeechTag(name, identifierTag)
        # Resetting the function, constructor, and parameter attributes
        self.functionName = ""
        self.constructorName = ""
        self.parameterList = []
        self.function = ""
        self.parameterType = []
        self.type = ""
        self.functionType = ""
        self.variableType =""
        self.parameterDict.clear()
    # Call when an elements ends
    def endElement(self, tag):
        # The function and constructor information is complete and therefore sent to their XML writer
        if tag == "parameter_list":
            for tempNum in range(0,len(self.parameterList)):
                self.parameterDict[self.parameterList[tempNum]] = self.parameterType[tempNum]
            self.functionConstructorDeclXMLWriter()
        # Determining self.currentContent's location and attribute
        if tag == "name":
            if not (self.dictTag["expr"] or self.dictTag["expr_stmt"]):
                if not (self.dictTag["type"]) or self.dictTag["parameter_list"]:
                    if self.dictTag["class"] and not (self.dictTag["decl"] or self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"] or self.dictTag["constructor"]):
                        print("Class Name: ", self.currentContent)
                        self.className = self.currentContent
                        self.XMLWriter("class", self.xmlResult, self.currentContent, '')
                    elif self.dictTag["constructor"] and not(self.dictTag["parameter"]):
                        print("Constructor Name: ", self.currentContent)  
                        self.constructorName = self.currentContent            
                    elif self.dictTag["parameter_list"]:
                        if self.dictTag["parameter"]and self.dictTag["type"]:
                            print("Parameter Type: ", self.currentContent)
                            self.parameterType.append(self.currentContent)
                        else:
                            print("Parameter Name: ", self.currentContent)
                            self.parameterList.append(self.currentContent)
                    elif self.dictTag["decl_stmt"] or self.dictTag["decl"] and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                        print("Variable Name: ", self.currentContent)
                        self.variableName = self.currentContent
                        self.functionConstructorDeclXMLWriter()
                    elif self.dictTag["function"] or self.dictTag["function_decl"] and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                        print("Function Name: ", self.currentContent)
                        self.functionName = self.currentContent
                    elif self.dictTag["interface"] or self.dictTag["interface_decl"] and not(self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                        print("Interface Name: ", self.currentContent)
                        self.interfaceName = self.currentContent 
                        self.XMLWriter("interface", self.xmlResult, self.currentContent, '')
                elif(self.dictTag["type"]):
                    if (self.dictTag["function"] or self.dictTag["function_decl"]) and not(self.dictTag["decl_stmt"] or self.dictTag["decl"]):
                        print("Function Type: ", self.currentContent)
                        self.functionType = self.currentContent
                    else:
                        print("Variable Type: ", self.currentContent)
                        self.variableType = self.currentContent             
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
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces,0)  
    Handler = JavaHandler()  
    parser.setContentHandler(Handler)
    parser.parse("die.xml")
    finalXMLResult = prettify(Handler.xmlResult) 
    print(finalXMLResult)

