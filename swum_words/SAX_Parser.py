# SAX_Parser.py
# Author: Aditya Bhargava (abhargava@g.hmc.edu)
# Date: Summer 2020
# Organization: RIT REU Cultivating New Generation Software
# Function: Takes an XML file and analyzes it based on identifier name and function using a SAX parser
# Input: SAX_Parser.py has the main method below and takes in an XML file (parser.parse(Java.xml))
# Output: [Specifier, Class Name, Parameter Name, Function Name, Variable Name,Type]: Literal
# Example
# Input: Java.xml
# <function><type><name>int</name></type> <name>getArea</name><parameter_list>()</parameter_list> <block>{<block_content>
#    <return>return <expr><name>width</name> <operator>*</operator> <name>height</name></expr>;</return>
# </block_content>}</block></function>
# Output:
# Type: int
# Function Name: getArea
import xml.sax, nltk
from dicttoxml import dicttoxml
from spiral import ronin
from nltk.tokenize import sent_tokenize, word_tokenize
class JavaHandler( xml.sax.ContentHandler ):  
    def __init__(self):
      self.currentTag = ""
      self.currentContent = ""
      self.dictTag = {"decl": 0, "decl_stmt": 0, "type": 0, "name": 0, "class": 0, "function": 0, "function_decl": 0, "expr": 0, "expr_stmt": 0, "parameter": 0, "parameter_list": 0, "operator": 0, "specifier": 0}
      self.listName = [] # Stores the names of identifiers
      self.dictName = {} # Stores the name and its meaning (class, function, method, parameter, etc.)
      self.dictPOS = {} # Stores the part of speech of every name 
      self.sentence = "" # Used for Part of Speech (POS) tagging
    def startElement(self, tag, attributes): # Call when an element starts
      for x in self.dictTag:
        if tag == x:
          self.dictTag[tag]+=1
    def endElement(self, tag): # Call when an elements ends
      self.sentence = ""
      if tag == "name":
        if not (self.dictTag["expr"] or self.dictTag["expr_stmt"]): # Eliminates the expression statments since variable names are already declared
          if not (self.dictTag["type"]): # Differentiates between type and name 
            if self.dictTag["class"] and not (self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]):
              print("Class Name: ",self.currentContent) # Stores the class name and assigns the key a "class" value
              self.dictName[self.currentContent] = "class" 
              self.listName.append(self.currentContent)
            elif self.dictTag["parameter"] or self.dictTag["parameter_list"] and not (self.dictTag["class"]):
              print("Parameter Name: ", self.currentContent)
              self.dictName[self.currentContent] = "parameter"
              self.listName.append(self.currentContent)
            elif self.dictTag["function"] or self.dictTag["function_decl"] and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):  
              print("Function Name: ", self.currentContent)
              self.dictName[self.currentContent] = "function"
              self.listName.append(self.currentContent)
            elif self.dictTag["decl_stmt"] or self.dictTag["decl"] and not (self.dictTag["parameter"] or self.dictTag["parameter_list"]):
              print("Variable Name: ", self.currentContent)
              self.dictName[self.currentContent] = "variable"
              self.listName.append(self.currentContent)
          else:
            print("Type: ",self.currentContent)
            self.dictName[self.currentContent] = "type"
        self.dictTag[tag]-=1
      elif tag == "specifier":
        print("Specifier: ", self.currentContent)
        self.dictTag[tag]-=1
      else:
        for x in self.dictTag:
          if tag == x:
            self.dictTag[tag]-=1
      if tag == "name":
        tempList = ronin.split(self.currentContent)
        for word in tempList:
          self.sentence = self.sentence + word + " "
          self.text = word_tokenize(self.sentence)
          self.dictPOS[self.currentContent] = nltk.pos_tag(self.text)
      self.currentTag = "" # Call when a character is read
    def characters(self, content):
        self.currentContent = ""
        self.currentContent += content
if ( __name__ == "__main__"): 
   parser = xml.sax.make_parser() # Create an XMLReader
   parser.setFeature(xml.sax.handler.feature_namespaces, 0) # Turn off namepsaces
   Handler = JavaHandler() # Override the default ContextHandler
   parser.setContentHandler(Handler)
   parser.parse("Java.xml") # Parses an xml file
