# Author: Aditya Bhargava (abhargava@g.hmc.edu)
# Date: Summer 2020
# Organization: RIT REU Cultivating New Generation Software
# Function: Takes an XML file and analyzes it based on identifier names and roles using a SAX parser. Saves the results as an XML file and outputs the respective input file with corresponding ID numbers.
import sys
# Part of Speech tagging tools
import spacy
from spiral import ronin
# XML Writer tools
from xml.sax import make_parser
from xml.sax.saxutils import XMLFilterBase, XMLGenerator
from xml.etree import ElementTree
from xml.dom import minidom
from lxml import etree

class JavaHandler(XMLFilterBase):
    def __init__(self, parent=None,errorMessage=False):
        super().__init__(parent)
        if len(sys.argv) == 3:
            self.checksInputAndOutput(sys.argv[1], sys.argv[2])
        else:
            sys.exit("Two arguments must be passed. The first must be a valid srcml input file and the other must be the output file")
        self.errorMessage = errorMessage
        self.dictTag = {"decl": 0, "decl_stmt": 0, "type": 0, "name": 0, "class": 0, "function": 0, "function_decl": 0, "index": 0, "extends": 0, "implements": 0, "throws": 0, "catch":0,
                        "expr": 0, "expr_stmt": 0, "parameter": 0, "parameter_list": 0, "operator": 0, "specifier": 0, "constructor": 0, "interface": 0, "interface_decl": 0, "argument": 0, "argument_list": 0}
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
        # Used for tracing SRCML and SWUM ID numbers
        self.idCount = 0

    # Checks to see if the input and output are valid
    def checksInputAndOutput(self, inputFile, outputFile):
        if ".xml" not in inputFile or ".xml" not in outputFile:
            sys.exit("Input/Output file is invalid. Make sure input file is in the certain directory and .xml is included")
    # Checks to see if identifier is valid
    def isValidIdentifier(self,identifier):
        if not identifier.isidentifier() and identifier != ">" and identifier != "[]" and self.errorMessage:
            print(identifier + " is not a valid identifier")
    # Call when an element starts
    def startElement(self, tag, attributes):
        for x in self.dictTag:
            if tag == x:
                self.dictTag[tag] += 1
        # Updates attributes with ID numbers and outputs to the ChangedInput XML file
        if not tag == "interface" and not tag == "constructor" and not tag == "function" and not tag == "class":
            super().startElement(tag, attributes)
        else:
            if tag == "interface" or tag=="constructor" or tag == "function" or tag == "class":
                attr = {"swum_ID": str(self.idCount)}
                super().startElement(tag, attr)
        if tag == "parameter_list":
            self.genericParameterAttribute = attributes.get("type")

    # Part Of Speech (POS) Tagging
    def PartOfSpeechTag(self, currentContent, tree):
        self.sentence = ""
        tempList = ronin.split(currentContent)
        nlp = spacy.load("en_core_web_sm")
        for word in tempList:
            self.sentence = self.sentence + word + " "
        self.sentence = nlp(self.sentence)
        for huh in self.sentence:
            wordTag = etree.SubElement(tree, 'word')
            wordTag.text = str(huh)
            partOfSpeechTag = etree.SubElement(wordTag, 'pos')
            partOfSpeechTag.text = str(huh.pos_)

    # XML writer for temporary class/interface names, parameters, types, formal parameters
    def XMLWriter(self,definedName,role,parameterType,tree,genericStatus):
        swumIdentifierTag = etree.SubElement(tree, 'swum_identifier')
        if role == "class" or role == "constructor" or role== "interface" or role== "function" or role == "variable":
            idTag = etree.SubElement(swumIdentifierTag, 'swum_ID')
            idTag.text = str(self.idCount)
            self.idCount = self.idCount+1
        locationTag = etree.SubElement(swumIdentifierTag, 'location')
        locationTag.text = role
        nameTag = etree.SubElement(swumIdentifierTag, 'name')
        nameTag.text = definedName
        # Recursive call to write parameter types
        if parameterType and self.parameterList and not genericStatus:
            typeTag = etree.SubElement(swumIdentifierTag, 'type')
            if "<" not in parameterType:
                self.XMLWriter(parameterType, "type", '', typeTag, False)
            else:
                self.XMLWriter(parameterType, "type", '', typeTag, True)
        # Recursive call to write generic parameter types
        if parameterType and self.parameterList and genericStatus:
            typeTagArgument = etree.SubElement(swumIdentifierTag, 'type')
            swumIdentifierTagArgument = etree.SubElement(
                typeTagArgument, 'swum_identifier')
            locationTagArgument = etree.SubElement(
                swumIdentifierTagArgument, 'location')
            locationTagArgument.text = "type"
            nameTagArgument = etree.SubElement(
                swumIdentifierTagArgument, 'name')
            nameTagArgument.text = parameterType
            argumentsTagArgument = etree.SubElement(
                swumIdentifierTagArgument, 'parameters')
            for argument in self.parameterArgument:
                argumentTag = etree.SubElement(
                    argumentsTagArgument, 'parameter')
                self.XMLWriter(argument, "parameter", '', argumentTag, False)
        if "<" in definedName:
            definedName = definedName.replace("<", '')
            definedName = definedName.replace(">", '')
        if "[" in definedName:
            definedName = definedName.replace("[", '')
            definedName= definedName.replace("]", '')
        identifierTag = etree.SubElement(swumIdentifierTag, 'identifier')
        if definedName:
            self.PartOfSpeechTag(definedName, identifierTag)
        else:
            print("Error associated at "+ role)  
        

    # XML writer for functions, constructor, class, variable declaration names
    def functionConstructorDeclXMLWriter(self, definedName, role, definedType, genericStatus):
        swumIdentifierTag = etree.SubElement(self.xmlResult, 'swum_identifier')
        #Updates self.idCount if tag is class, constructor, interface, function, or variable
        if role == "class" or role == "constructor" or role == "interface" or role == "function" or role == "variable":
            idTag = etree.SubElement(swumIdentifierTag, 'swum_ID')
            idTag.text = str(self.idCount)
            self.idCount = self.idCount+1
        locationTag = etree.SubElement(swumIdentifierTag, 'location')
        #Adds interface or class tags to constructor and function elements
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
        # Writes type elements if it is not a generic
        if definedType and not genericStatus:
            typeTag = etree.SubElement(swumIdentifierTag, 'type')
            self.XMLWriter(definedType, "type", '', typeTag, False)
        # Writes type elements if it is a generic
        elif definedType and genericStatus:
            typeTagArgument = etree.SubElement(swumIdentifierTag, 'type')
            swumIdentifierTagArgument = etree.SubElement(
                typeTagArgument, 'swum_identifier')
            locationTagArgument = etree.SubElement(
                swumIdentifierTagArgument, 'location')
            locationTagArgument.text = "type"
            nameTagArgument = etree.SubElement(
                swumIdentifierTagArgument, 'name')
            nameTagArgument.text = definedType
            argumentsTagArgument = etree.SubElement(
                swumIdentifierTagArgument, 'parameters')
            for argument in self.argument:
                argumentTag = etree.SubElement(
                    argumentsTagArgument, 'parameter')
                self.XMLWriter(argument,"parameter", '', argumentTag, False)
            locationOfBeginningTag = definedType.index("<")
            definedType = definedType[0:locationOfBeginningTag]
            identifierTag = etree.SubElement(
                swumIdentifierTagArgument, 'identifier')
            if definedType:
                self.PartOfSpeechTag(definedType, identifierTag)
            else:
                print("Error associated at "+ role + " with " +definedType)      
        # Assigns parameters to generics
        if self.parameterGenericList:
            parametersTag = etree.SubElement(swumIdentifierTag, 'parameters')
            parameterTag = etree.SubElement(parametersTag, 'parameter')
            for temp in self.parameterGenericList:
                self.XMLWriter(temp, "parameter", '', parameterTag, False)
        # Writes formal parameters to methods and constructors
        if self.parameterList:
            formalParametersTag = etree.SubElement(
                swumIdentifierTag, 'formal_parameters')
            formalParameterTag = etree.SubElement(
                formalParametersTag, 'formal_parameter')
            for key in self.parameterDict:
                if "<" in self.parameterDict[key]:
                    self.XMLWriter(
                        key, "formal_parameter", self.parameterDict[key], formalParameterTag, True)
                else:
                    self.XMLWriter(
                        key, "formal_parameter",self.parameterDict[key], formalParameterTag, False)
        identifierTag = etree.SubElement(swumIdentifierTag, 'identifier')
        if name:
            self.PartOfSpeechTag(name, identifierTag)
        else:
            print("Error associated at "+ role + " with " + definedType + " return type")
        # Resetting the function, constructor, and parameter attributes
        self.functionName = ""
        self.constructorName = ""
        self.functionType = ""
        self.variableType = ""
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
        if tag == "interface":
            self.interfaceName = ""
        if tag == "class":
            self.className = ""
        # The function,class,interface, and constructor information is complete and therefore sent to their XML writer
        if tag == "parameter_list":
            if len(self.parameterList) != len(self.parameterType):
                print("Parameters need a type")
                sys.exit(1)
            else:
                for tempNum in range(0, len(self.parameterList)):
                    self.parameterDict[self.parameterList[tempNum]] = self.parameterType[tempNum]
            if self.dictTag["catch"]:
                self.functionConstructorDeclXMLWriter("CatchExceptions", "CatchExceptions", '', False)
            elif self.functionName:
                if not self.functionType and self.errorMessage:
                    # Makes sure functions have return types
                    print(self.functionName + " must have a return type")
                if "<" in self.functionType:
                    self.functionConstructorDeclXMLWriter(
                        self.functionName, "function", self.functionType, True)
                else:
                    self.functionConstructorDeclXMLWriter(
                        self.functionName, "function", self.functionType, False)
            elif self.constructorName:
                self.functionConstructorDeclXMLWriter(
                    self.constructorName, "constructor", '', False)
            # Checks if the class or interface has generic parameters and writes the XML file accordingly
            elif (self.className or self.interfaceName) and self.genericParameterAttribute:
                for swumIdentifierTag in self.xmlResult.findall('swum_identifier'):
                    nameTagText = swumIdentifierTag.find('name').text
                    if nameTagText == self.interfaceName:
                        self.xmlResult.remove(swumIdentifierTag)
                        self.idCount = self.idCount-1
                        self.XMLWriter(
                             self.interfaceName, "interface",'', self.xmlResult, False)
                    elif nameTagText == self.className:
                        self.xmlResult.remove(swumIdentifierTag)
                        self.idCount = self.idCount-1
                        self.XMLWriter(self.className, "class", 
                                       '', self.xmlResult, False)
            elif (self.className or self.interfaceName) and not self.genericParameterAttribute:
                for swumIdentifierTag in self.xmlResult.findall('swum_identifier'):
                    nameTagText = swumIdentifierTag.find('name').text
                    if nameTagText == self.interfaceName and not swumIdentifierTag.find('parameter'):
                        self.xmlResult.remove(swumIdentifierTag)
                        self.idCount = self.idCount-1
                        self.functionConstructorDeclXMLWriter(
                            self.interfaceName, "interface", '', False)
                    elif nameTagText == self.className and not swumIdentifierTag.find('parameter'):
                        self.xmlResult.remove(swumIdentifierTag)
                        self.idCount = self.idCount-1
                        self.functionConstructorDeclXMLWriter(
                            self.className, "class", '', False)
        # Determining self.currentContent's location and attribute
        if tag == "name" or tag == "index":
            if not (self.dictTag["expr"] or self.dictTag["expr_stmt"] or self.dictTag["extends"] or self.dictTag["implements"] or self.dictTag["throws"] or (self.previousTag == "index" and tag == "name")):
                if not (self.dictTag["type"]) or self.dictTag["parameter_list"]:
                        if self.dictTag["class"] and not (self.dictTag["interface"] or self.dictTag["decl"] or self.dictTag["decl_stmt"] or self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"] or self.dictTag["constructor"]):
                            self.isValidIdentifier(self.currentContent)
                            if self.currentContent != ">" and self.currentContent != "[]":
                                self.className = self.currentContent
                                self.XMLWriter(
                                    self.className, "class", '', self.xmlResult, False)
                        elif self.dictTag["constructor"] and not (self.dictTag["decl"] or self.dictTag["decl_stmt"] or self.dictTag["parameter"]):
                            self.isValidIdentifier(self.currentContent)
                            if self.className != self.currentContent and self.errorMessage:
                                print(self.currentContent + " must have the same name as its parent class")
                            self.constructorName = self.currentContent
                        elif (self.dictTag["interface"] or self.dictTag["interface_decl"]) and not(self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                            self.isValidIdentifier(self.currentContent)
                            if self.currentContent != ">" and self.currentContent != "[]":
                                self.interfaceName = self.currentContent
                                self.XMLWriter(
                                    self.currentContent, "interface", '', self.xmlResult, False)
                        elif self.dictTag["parameter_list"]:
                            if self.dictTag["parameter"] and not (self.dictTag["type"] or self.dictTag["decl"] or self.dictTag["decl_stmt"] or self.dictTag["function_decl"] or self.dictTag["function"] or self.dictTag["constructor"]):
                                self.parameterGenericList.append(
                                    self.currentContent)
                            elif self.dictTag["parameter"] and self.genericParameterAttribute == "generic":
                                self.parameterGenericList.append(
                                    self.currentContent)
                            elif self.dictTag["parameter"]and self.dictTag["type"]:
                                if(tag == "index"):
                                    self.parameterTypeString = self.parameterTypeString+"[]"
                                    self.parameterType.remove(
                                        self.parameterType[-1])
                                    self.parameterType.append(
                                        self.parameterTypeString)
                                elif (self.dictTag["argument_list"]):
                                    if(self.dictTag["argument"]):
                                        if self.parameterTypeString[-1] == '>':
                                            self.parameterArgument.append(
                                                self.currentContent)
                                            self.parameterTypeString = self.parameterTypeString[:-1]
                                            self.parameterTypeString = self.parameterTypeString+","+self.currentContent+">"
                                            self.parameterType.remove(
                                                self.parameterType[-1])
                                            self.parameterType.append(
                                                self.parameterTypeString)
                                        else:
                                            self.parameterArgument.append(
                                                self.currentContent)
                                            self.parameterTypeString = self.parameterTypeString+"<"+self.currentContent+">"
                                            self.parameterType.remove(
                                                self.parameterType[-1])
                                            self.parameterType.append(
                                                self.parameterTypeString)
                                else:
                                    if self.currentContent != ">":
                                        self.parameterTypeString = self.currentContent
                                        self.parameterType.append(
                                            self.parameterTypeString)
                            else:
                                self.parameterList.append(self.currentContent)
                        elif (self.dictTag["decl_stmt"] or self.dictTag["decl"]) and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                            self.isValidIdentifier(self.currentContent)
                            self.variableName = self.currentContent
                            if not self.variableType and self.errorMessage:
                                # Makes sure variables have a type
                                print(
                                    self.variableName + " must have a variable type ")
                            if "<" in self.variableType:
                                self.functionConstructorDeclXMLWriter(
                                    self.variableName, "variable", self.variableType, True)
                            else:
                                self.functionConstructorDeclXMLWriter(
                                    self.variableName, "variable", self.variableType, False)
                        elif (self.dictTag["function"] or self.dictTag["function_decl"]) and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
                            self.isValidIdentifier(self.currentContent)
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
                            self.variableType = self.variableType+"[]"
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
            self.dictTag[tag] -= 1
            self.previousTag = tag
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
    # Used to parse an XML File and return an XML output file with the results
    parser = make_parser()
    Handler = JavaHandler('',False)
    parser.setContentHandler(Handler)
    parser.parse(str(sys.argv[1]))
    xmlstr = minidom.parseString(ElementTree.tostring(Handler.xmlResult)).toprettyxml(indent="   ")
    with open(str(sys.argv[2]), "w") as f:
        f.write(xmlstr)
    print(prettify(Handler.xmlResult))
    # Used to write a changed XML input file labeled with ID numbers
    reader = JavaHandler(make_parser(),True)
    index = sys.argv[1].index(".xml")
    root = sys.argv[1][0:index]
    ChangedInput = root+"ChangedInput.xml"
    with open(ChangedInput, 'w') as f:
        handler = XMLGenerator(f)
        reader.setContentHandler(handler)
        reader.parse(sys.argv[1])