# Author: Aditya Bhargava (abhargava@g.hmc.edu)
# Date: Summer 2020
# Organization: RIT REU Cultivating New Generation Software
# Function: Takes an XML file and analyzes it based on identifier names and roles using a SAX parser. Saves the results as an XML file and outputs the respective input file with corresponding ID numbers.
import sys
# Part of Speech tagging tools
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from spiral import ronin
# XML Writer
from xml.sax import make_parser
from xml.sax.saxutils import XMLFilterBase, XMLGenerator
from xml.etree import ElementTree
from xml.dom import minidom
from lxml import etree

class JavaHandler(XMLFilterBase):
    def __init__(self, parent = None,inputStatus = True):
        if inputStatus:
            self.input = input("XML Input File: ")
            self.output = input("XML Output File: ")
            self.checksInputAndOutput(self.input, self.output)
        super().__init__(parent)
        self.dictTag = {"decl": 0, "decl_stmt": 0, "type": 0, "name": 0, "class": 0, "function": 0, "function_decl": 0, "index":0, "extends":0, "implements":0,
                        "expr": 0, "expr_stmt": 0, "parameter": 0, "parameter_list": 0, "operator": 0, "specifier": 0, "constructor": 0, "interface": 0, "interface_decl": 0, "argument":0, "argument_list":0}
        self.previousTag = ""
        self.xmlResult = etree.Element('swum_identifiers')
        # Used to define attributes
        self.interfaceName = ""
        self.variableName = ""
        self.functionName = ""
        self.constructorName = ""
        self.className = ""
        self.currentContent = ""
        # Used for arguments in types
        self.variableType = ""
        self.functionType = ""
        self.argument = []
        self.parameterArgument = []
        self.genericParameterAttribute = ""
        # Used for parameters in functions and constructors
        self.parameterGenericList = []
        self.parameterList = []
        self.parameterType = []
        self.parameterDict = {}
        self.parameterTypeString = ""
        # Used for Part of Speech (POS) tagging
        self.dictPOS = {}  
        self.sentence = ""
        # Used for tracing SRCML and SWUM
        self.idCount = 0
    def checksInputAndOutput(self,inputFile,outputFile):
        if ".xml" not in inputFile or "xml" not in outputFile:
            raise NameError("Include the .xml file extension")
    # Call when an element starts
    def startElement(self, tag, attributes):
        for x in self.dictTag:
            if tag == x:
                self.dictTag[tag] += 1
        if not tag == "interface" and not tag == "constructor" and not tag == "function" and not tag == "class":     
            super().startElement(tag, attributes)
        else:
            if tag == "interface":
                attr = {"swum_id":str(self.idCount)}
                super().startElement(tag,attr)
            if tag == "constructor":
                attr = {"swum_id":str(self.idCount)}
                super().startElement(tag,attr)
            if tag == "function":
                attr = {"swum_id":str(self.idCount)}
                super().startElement(tag,attr)
            if tag == "class":
                attr = {"swum_id":str(self.idCount)}
                super().startElement(tag,attr)
        if tag == "parameter_list":
            self.genericParameterAttribute = attributes.get("type")
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
    # XML writer for temporary class/interface names, parameters, types, formal parameters
    def XMLWriter(self,locationTagText,currentContent,parameterType,tree, genericStatus):
        swumIdentifierTag = etree.SubElement(tree, 'swum_identifier')
        if locationTagText == "class" or locationTagText == "constructor" or locationTagText == "interface" or locationTagText == "function":
            idTag = etree.SubElement(swumIdentifierTag, 'swum_ID')
            idTag.text = str(self.idCount)
            self.idCount = self.idCount+1
        locationTag = etree.SubElement(swumIdentifierTag, 'location')
        locationTag.text = locationTagText
        nameTag = etree.SubElement(swumIdentifierTag, 'name')
        nameTag.text = currentContent
        # Recursive call to write parameter types
        if parameterType and self.parameterList and not genericStatus:
            typeTag = etree.SubElement(swumIdentifierTag, 'type')
            if "<" not in parameterType:
                self.XMLWriter("type",parameterType,'',typeTag, False )
            else:
                self.XMLWriter("type",parameterType,'', typeTag, True)
        if parameterType and self.parameterList and genericStatus:
            typeTagArgument = etree.SubElement(swumIdentifierTag, 'type')
            swumIdentifierTagArgument = etree.SubElement(typeTagArgument, 'swum_identifier')
            locationTagArgument = etree.SubElement(swumIdentifierTagArgument, 'location')
            locationTagArgument.text = "type"
            nameTagArgument = etree.SubElement(swumIdentifierTagArgument, 'name')
            nameTagArgument.text = parameterType
            argumentsTagArgument = etree.SubElement(swumIdentifierTagArgument, 'parameters')
            for argument in self.parameterArgument:
                argumentTag = etree.SubElement(argumentsTagArgument, 'parameter')
                self.XMLWriter("parameter",argument, '',argumentTag, False)
        if "<" in currentContent:
            currentContent = currentContent.replace("<", '')
            currentContent = currentContent.replace(">", '')
        if "[" in currentContent:
            currentContent = currentContent.replace("[", '')
            currentContent = currentContent.replace("]", '')
        identifierTag = etree.SubElement(swumIdentifierTag, 'identifier')
        self.PartOfSpeechTag(currentContent, identifierTag)
    # XML writer for functions, constructor, class, variable declaration names
    def functionConstructorDeclXMLWriter(self,definedName, role, definedType,genericStatus):
        swumIdentifierTag = etree.SubElement(self.xmlResult, 'swum_identifier')
        if role == "class" or role == "constructor" or role == "interface" or role == "function":
            idTag = etree.SubElement(swumIdentifierTag, 'swum_ID')
            idTag.text = str(self.idCount)
            self.idCount = self.idCount+1
        locationTag = etree.SubElement(swumIdentifierTag, 'location')
        if role == "constructor" or role == "function":
            if self.interfaceName:
                interfaceTag = etree.SubElement(swumIdentifierTag, 'interface')
                interfaceTag.text = self.interfaceName
            elif self.className:
                classTag = etree.SubElement(swumIdentifierTag, 'class')
                classTag.text = self.className
        name = definedName
        locationTag.text = role
        nameTag = etree.SubElement(swumIdentifierTag, 'name')
        nameTag.text = name
        if definedType and not genericStatus:
            typeTag = etree.SubElement(swumIdentifierTag, 'type')
            self.XMLWriter("type",definedType, '', typeTag, False)
        elif definedType and genericStatus:
            typeTagArgument = etree.SubElement(swumIdentifierTag, 'type')
            swumIdentifierTagArgument = etree.SubElement(typeTagArgument, 'swum_identifier')
            locationTagArgument = etree.SubElement(swumIdentifierTagArgument, 'location')
            locationTagArgument.text = "type"
            nameTagArgument = etree.SubElement(swumIdentifierTagArgument, 'name')
            nameTagArgument.text = definedType
            argumentsTagArgument = etree.SubElement(swumIdentifierTagArgument, 'parameters')
            for argument in self.argument:
                argumentTag = etree.SubElement(argumentsTagArgument, 'parameter')
                self.XMLWriter("parameter",argument, '',argumentTag, False)
            locationOfBeginningTag = definedType.index("<")
            definedType = definedType[0:locationOfBeginningTag]
            identifierTag = etree.SubElement(swumIdentifierTagArgument, 'identifier')
            self.PartOfSpeechTag(definedType, identifierTag)
        if self.parameterGenericList:
            parametersTag = etree.SubElement(swumIdentifierTag, 'parameters')
            parameterTag = etree.SubElement(parametersTag, 'parameter')
            for temp in self.parameterGenericList:
                self.XMLWriter("parameter",temp,'', parameterTag, False)
        if self.parameterList:
            formalParametersTag = etree.SubElement(swumIdentifierTag, 'formal_parameters')
            formalParameterTag = etree.SubElement(formalParametersTag, 'formal_parameter')
            for key in self.parameterDict:
                if "<" in self.parameterDict[key]:
                    self.XMLWriter("formal_parameter",key,self.parameterDict[key], formalParameterTag, True)
                else:
                    self.XMLWriter("formal_parameter",key,self.parameterDict[key], formalParameterTag, False)
        identifierTag = etree.SubElement(swumIdentifierTag, 'identifier')
        self.PartOfSpeechTag(name, identifierTag)
        # Resetting the function, constructor, and parameter attributes
        self.functionName = ""
        self.constructorName = ""
        self.functionType = ""
        self.variableType =""
        self.parameterType = []
        self.parameterList = []
        self.parameterArgument = []
        self.parameterDict.clear()
        self.argument = []
        self.parameterGenericList = []
        self.genericParameterAttribute = ""

    # Call when an elements ends
    def endElement(self, tag):
        super().endElement(tag)
        # The function and constructor information is complete and therefore sent to their XML writer
        if tag == "interface":
            self.interfaceName = ""
        if tag == "class":
            self.className = ""
        if tag == "parameter_list":
            for tempNum in range(0,len(self.parameterList)):
                self.parameterDict[self.parameterList[tempNum]] = self.parameterType[tempNum]
            if self.functionName:
                if not self.functionType:
                    #Makes sure functions have return types
                    raise AttributeError("Functions must have a return type")
                if "<" in self.functionType:
                    self.functionConstructorDeclXMLWriter(self.functionName, "function",self.functionType, True)
                else:
                    self.functionConstructorDeclXMLWriter(self.functionName, "function", self.functionType, False)
            elif self.constructorName:
                self.functionConstructorDeclXMLWriter(self.constructorName, "constructor", '',False)
            elif (self.className or self.interfaceName) and self.genericParameterAttribute:
                for swumIdentifierTag in self.xmlResult.findall('swum_identifier'):
                    nameTagText = swumIdentifierTag.find('name').text
                    if nameTagText == self.interfaceName:
                        self.xmlResult.remove(swumIdentifierTag)
                        self.idCount = self.idCount-1
                        self.XMLWriter("interface", self.interfaceName, '', self.xmlResult, False)
                    elif nameTagText == self.className:
                        self.xmlResult.remove(swumIdentifierTag)
                        self.idCount = self.idCount-1
                        self.XMLWriter("class", self.className, '', self.xmlResult, False)
            elif (self.className or self.interfaceName) and not  self.genericParameterAttribute:
                for swumIdentifierTag in self.xmlResult.findall('swum_identifier'):
                    nameTagText = swumIdentifierTag.find('name').text
                    if nameTagText == self.interfaceName and not swumIdentifierTag.find('parameter'): 
                        self.xmlResult.remove(swumIdentifierTag)
                        self.idCount = self.idCount-1
                        self.functionConstructorDeclXMLWriter(self.interfaceName, "interface", '',False)                       
                    elif nameTagText == self.className and not swumIdentifierTag.find('parameter'):
                        self.xmlResult.remove(swumIdentifierTag)
                        self.idCount = self.idCount-1
                        self.functionConstructorDeclXMLWriter(self.className, "class", '',False)
        # Determining self.currentContent's location and attribute
        if tag == "name" or tag == "index":
            if not (self.dictTag["expr"] or self.dictTag["expr_stmt"] or self.dictTag["extends"] or self.dictTag["implements"] or (self.previousTag == "index" and tag == "name")):
                if not (self.dictTag["type"]) or self.dictTag["parameter_list"]:
                    if self.currentContent.isidentifier() or "$" in self.currentContent or "[]" in self.currentContent or ">" in self.currentContent:
                        if self.dictTag["class"] and not (self.dictTag["interface"] or self.dictTag["decl"] or self.dictTag["decl_stmt"] or self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"] or self.dictTag["constructor"]):
                            if self.currentContent != ">" and self.currentContent != "[]":
                                self.className = self.currentContent
                                self.XMLWriter("class", self.className, '', self.xmlResult, False)
                        elif self.dictTag["constructor"] and not (self.dictTag["decl"] or self.dictTag["decl_stmt"] or self.dictTag["parameter"]):
                            self.constructorName = self.currentContent
                        elif (self.dictTag["interface"] or self.dictTag["interface_decl"]) and not(self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                            if self.currentContent != ">" and self.currentContent != "[]":
                                self.interfaceName = self.currentContent 
                                self.XMLWriter("interface", self.currentContent, '', self.xmlResult, False)
                        elif self.dictTag["parameter_list"]:
                            if self.dictTag["parameter"] and not (self.dictTag["type"] or self.dictTag["decl"] or self.dictTag["decl_stmt"] or self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["constructor"]):
                                self.parameterGenericList.append(self.currentContent)
                            elif self.dictTag["parameter"] and self.genericParameterAttribute == "generic":
                                self.parameterGenericList.append(self.currentContent)                            
                            elif self.dictTag["parameter"]and self.dictTag["type"]:
                                if(tag== "index"):
                                    self.parameterTypeString = self.parameterTypeString+"[]"
                                    self.parameterType.remove(self.parameterType[-1])
                                    self.parameterType.append(self.parameterTypeString)
                                elif (self.dictTag["argument_list"]):
                                    if(self.dictTag["argument"]):
                                        if self.parameterTypeString[-1] == '>':
                                            self.parameterArgument.append(self.currentContent)
                                            self.parameterTypeString= self.parameterTypeString[:-1]
                                            self.parameterTypeString= self.parameterTypeString+","+self.currentContent+">"
                                            self.parameterType.remove(self.parameterType[-1])
                                            self.parameterType.append(self.parameterTypeString)
                                        else:
                                            self.parameterArgument.append(self.currentContent)
                                            self.parameterTypeString = self.parameterTypeString+"<"+self.currentContent+">"
                                            self.parameterType.remove(self.parameterType[-1])
                                            self.parameterType.append(self.parameterTypeString)
                                else:
                                    if self.currentContent != ">":
                                        self.parameterTypeString = self.currentContent
                                        self.parameterType.append(self.parameterTypeString)
                            else:
                                self.parameterList.append(self.currentContent)
                        elif (self.dictTag["decl_stmt"] or self.dictTag["decl"]) and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                            if not self.variableType:
                                #Makes sure variables have a type 
                                raise AttributeError("Variables must have a type ")
                            self.variableName = self.currentContent
                            if "<" in self.variableType:
                                self.functionConstructorDeclXMLWriter(self.variableName, "variable", self.variableType,True) 
                            else:
                                self.functionConstructorDeclXMLWriter(self.variableName, "variable", self.variableType, False)
                        elif (self.dictTag["function"] or self.dictTag["function_decl"]) and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                            self.functionName = self.currentContent
                elif(self.dictTag["type"]):
                    if (self.dictTag["function"] or self.dictTag["function_decl"]) and not(self.dictTag["decl_stmt"] or self.dictTag["decl"]):
                        if(self.dictTag["index"]):
                            self.functionType = self.functionType+"[]"
                        elif (self.dictTag["argument_list"]):
                            if(self.dictTag["argument"]):
                                if self.functionType[-1] == '>':
                                    self.argument.append(self.currentContent)
                                    self.functionType = self.functionType[:-1]
                                    self.functionType = self.functionType+","+self.currentContent+">"
                                else:
                                    self.argument.append(self.currentContent)
                                    self.functionType = self.functionType+"<"+self.currentContent+">"
                        else:
                            if self.currentContent != ">":
                                self.functionType = self.currentContent
                    else:
                        if(self.dictTag["index"]):
                            self.variableType= self.variableType+"[]"
                        elif (self.dictTag["argument_list"]):
                            if(self.dictTag["argument"]):
                                if self.variableType[-1] == '>':
                                    self.argument.append(self.currentContent)
                                    self.variableType = self.variableType[:-1]
                                    self.variableType = self.variableType+","+self.currentContent+">"
                                else:
                                    self.argument.append(self.currentContent)
                                    self.variableType = self.variableType+"<"+self.currentContent+">"
                        else:
                            if self.currentContent != ">" and self.currentContent != "[]":
                                self.variableType = self.currentContent         
                else:
                    # Raises an NameError if self.currentContent is not a valid identifier (only includes alphanumeric characters, underscores, and "$")
                    raise NameError(self.currentContent + " is not a valid identifier")
            self.dictTag[tag] -= 1
            self.previousTag = tag
        elif tag == "specifier":
            self.dictTag[tag] -= 1
        else:
            for x in self.dictTag:
                if tag == x:
                    self.dictTag[tag] -= 1
    # Called when a character is called 
    def characters(self, content):
        self.currentContent = ""
        self.currentContent += content
        super().characters(content)

# Source: PyMOTW-3 "Building Documents with Element Nodes"
# Prints the XML file into an understandable and comprehensible format
def prettify(elem):  
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="   ")
if (__name__ == "__main__"):
    #Used to parse an XML File and return an XML output file with the results
    parser = make_parser()
    inputStatus = True
    Handler = JavaHandler((),inputStatus)  
    parser.setContentHandler(Handler)
    parser.parse(Handler.input)
    print(prettify(Handler.xmlResult))
    Handler.xmlResult = (Handler.xmlResult).getroottree()
    Handler.xmlResult.write(str(Handler.output))
    
    inputStatus = False
    reader = JavaHandler(make_parser(),inputStatus)
    with open("ChangedInput.xml", 'w') as f:
        handler = XMLGenerator(f)
        reader.setContentHandler(handler)
        handler.input = Handler.input
        reader.parse(handler.input) 
