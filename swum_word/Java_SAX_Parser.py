# Takes a XML representation of Java and analyzes it based on identifiers
import xml.sax
class JavaHandler( xml.sax.ContentHandler ):
   nameList = []
   def __init__(self):
      self.CurrentData = ""
      self.PreviousData = ""
      self.name = ""
      self.parameterList = ""
      self.argumentList = ""
      self.type = ""
   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "constructor":
          print("***Constructor***")
      if tag == "class":
         print ("***Class***")
      if tag == "function":
         print ("***Function***")
      if tag == "expr_stmt":
         print ("***Expression Statement***")
      if tag == "decl_stmt":
         print ("***Declaration Statement***")
      if tag == "enum":
         print ("***Enum***")
      if tag == "package":
         print ("***Package***")
   # Call when an elements ends
   def endElement(self, tag):
      # global nameList
      if self.CurrentData == "name":
         # Removing the Java keywords from the output
         if (self.name != "void" and self.name != "System" and self.name != "out" and self.name != "println" and self.name != "super" and self.name != "boolean" and self.name != "String" and self.name != "char" and self.name != "int" and self.name != "Exception"):
            # Making sure no repeated names are printed out 
          #  if(self.name not in nameList):
               print ("Name:", self.name)
           #    nameList.append(self.name)
      if self.CurrentData == "parameter_list":
         print ("Parameter List:", self.parameterList)
      if self.CurrentData == "argument_list":
         print ("Argument List:", self.argumentList)
      self.CurrentData = ""
   # Call when a character is read
   def characters(self, content):
      if self.CurrentData == "name":
         self.name = content
      if self.CurrentData == "parameter_list":
         self.parameterList = content
      if self.CurrentData == "argument_list":
         self.argumentList = content
if ( __name__ == "__main__"): 
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
   # override the default ContextHandler
   Handler = JavaHandler()
   parser.setContentHandler( Handler )
   parser.parse("Java.xml")
