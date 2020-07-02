# Author: Aditya Bhargava (abhargava@g.hmc.edu)
# Date: Summer 2020
# Organization: RIT REU Cultivating New Generation Software
# Function: Takes an XML file and analyzes it based on name, age, weight, and height. Serves as a practice tool for a real SAX Parser.
import xml.sax
class GroupHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.CurrentData = ""
      self.name = ""
      self.age = ""
      self.weight = ""
      self.height = ""
   # Method is called when the element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "person":
         print ("*****Person*****")
         id = attributes["id"]
         print ("ID:", id)
   # Method is called when the element ends
   def endElement(self, tag):
      if self.CurrentData == "name":
         print ("Name:", self.name)
      elif self.CurrentData == "age":
         print ("Age:", self.age)
      elif self.CurrentData == "weight":
         print ("Weight:", self.weight)
      elif self.CurrentData == "height":
         print ("Height:", self.height)
      self.CurrentData = ""
   # Call when a character is read where content is the parameter text
   def characters(self, content):
      if self.CurrentData == "name":
         self.name = content
      elif self.CurrentData == "age":
         self.age = content
      elif self.CurrentData == "weight":
         self.weight = content
      elif self.CurrentData == "height":
         self.height = content
# Main Method
if ( __name__ == "__main__"): 
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
   # override the default ContextHandler
   Handler = GroupHandler()
   parser.setContentHandler( Handler )
   parser.parse("Group.xml")
