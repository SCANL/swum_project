# SWUM Words
Analysis of word nodes within SWUM <sub>words</sub>
In SWUM <sub>words</sub>, there exists a word node for every word ocurrence in a specific code sample. We analyze each word node by splitting each word using the NLTK python library and identifier splitting techniques. Then we annotate each word node with parts of speech tagging and its role in the code (function, class, variable name, etc.). The analysis of the word nodes are then sent to the SWUM <sub>phrases</sub> stage where word relationships are used to develop edges between word nodes.
## Installation
1. SWUM <sub>words</sub> requires [Python 3.7+](https://www.python.org) and has been tested on Python 3.8.
2. To convert your Java and C++ file, I would recommend downloading [SRCML](https://www.srcml.org) with directions downloading SRCML [here](https://www.srcml.org/#download)
Input: XML file representing a code sample. 
Output: Prints out the role the word node plays and its name("Role: Name") and XML file of the result.
### Example: 
Lets take a XML file like Java.xml (uploaded in repository) and perform these commands:
    </br> parser = xml.sax.make_parser() #Create an XML reader
    </br> parser.setFeature(xml.sax.handler.feature_namespaces,0) #Turn off namepsaces  
    </br> Handler = JavaHandler()   
    </br> parser.setContentHandler(Handler) # Override the default ContextHandler
    </br> parser.parse("Java.xml")  # Parses an xml file
    </br> finalXMLResult = prettify(Handler.xmlResult) # Prints the SAX Parser result as a "pretty" XML file
    </br> print(finalXMLResult)
    </br> The output is located in the JavaOutput.xml
## Description of Code
swum_words.py imports xml.sax a XML interface for Python and methods part of xml.sax. A dictionary is used to keep track which tags are "open" and "closed" using the increment/decrement operator. swum_words.py utilizes lxml to write a XML file where the swum_identifiers tag indicate the beginning of the file, location tag indicates the role of the word node, name tag indicates the name of the word node, type tag indicates the return type of a function or type of variable, pos tag indicates the part of speech tagging of each word node, and parameters tag indicates the parameters of a function and constructor.
