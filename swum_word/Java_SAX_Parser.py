# Takes a XML representation of Java and analyzes it based on identifiers
import xml.sax
class JavaHandler( xml.sax.ContentHandler ):   
    def __init__(self):
      self.currentTag = ""
      self.currentContent = ""
      self.dictTag = {"decl_stmt": 0, "type": 0, "name": 0, "class": 0, "function": 0, "expr": 0, "expr_stmt": 0, "parameter": 0, "parameter_list": 0, "argument_list": 0, "argument": 0, "operator": 0} 
# Call when an element starts
    def startElement(self, tag, attributes):
      for x in self.dictTag:
        if tag == x:
          self.dictTag[tag]+=1
# Call when an elements ends
    def endElement(self, tag):
      if tag == "name":
# Eliminates the expression statments so variable names are not as repeated as much
        if not (self.dictTag["expr"] or self.dictTag["expr_stmt"]):
# Differentiates between type and name 
          if not (self.dictTag["type"]):
            if self.dictTag["class"] and not (self.dictTag["argument_list"] or self.dictTag["function"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]):
              print("Class Name: ",self.currentContent)              
            elif self.dictTag["function"] and not (self.dictTag["expr_stmt"] or self.dictTag["argument"] or self.dictTag["argument_list"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]):  
              print("Function Name: ", self.currentContent)
            elif self.dictTag["parameter"] or self.dictTag["parameter_list"] and not (self.dictTag["argument"] or self.dictTag["argument_list"] or self.dictTag["class"]):
              print("Parameter Name: ", self.currentContent)
            elif self.dictTag["argument"] and not (self.dictTag["class"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]): 
              print("Arguments: ", self.currentContent)
            elif self.dictTag["decl_stmt"] or self.dictTag["expr"] and not (self.dictTag["argument"] or self.dictTag["parameter"] or self.dictTag["parameter_list"]):
              print("Variable Name: ", self.currentContent)
          else:
            print("Type: ",self.currentContent)
        self.dictTag[tag]-=1
      else:
        for x in self.dictTag:
          if tag == x:
            self.dictTag[tag]-=1
      self.currentTag = ""
# Call when a character is read
    def characters(self, content):
        self.currentContent = ""
        self.currentContent += content
if ( __name__ == "__main__"): 
# Create an XMLReader
   parser = xml.sax.make_parser()
# Turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
# Override the default ContextHandler
   Handler = JavaHandler()
   parser.setContentHandler( Handler )
   parser.parse("Java.xml")
