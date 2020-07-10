# swum_words
## Name
Analysis of word nodes within SWUM <sub>words</sub>
## Description of Project
Using a word node in SWUM <sub>words</sub> in a specific code sample, we split each identifier using the NLTK python library and identifier splitting techniques. Then we annotate each word node with parts of speech tagging and its role in the code. The analysis of the word nodes are then sent to the SWUM <sub>phrases</sub> stage where word relationships are used to develop edges between word nodes.
## Usage 
Input: XML file representing a code sample. 
Output: Prints out the role the word node plays and its name("Role: Name") and XML file of the result.
### Example: 
Lets take a XML file like Java.xml (uploaded in repository) and perform these commands:
    </br> parser = xml.sax.make_parser()
    </br> parser.setFeature(xml.sax.handler.feature_namespaces,0)  
    </br> Handler = JavaHandler()  
    </br> parser.setContentHandler(Handler)
    </br> parser.parse("Java.xml")
    </br> finalXMLResult = prettify(Handler.xmlResult) 
    </br> print(finalXMLResult)
## Description of Code
swum_words.py imports xml.sax (a XML (SAX) interface for Python) and methods part of xml.sax. A dictionary is used to keep track which tags are "open" and "closed" using the increment/decrement operator. swum_words.py utilizes lxml to write a XML file where <swum_identifiers> indicate the beginning of the file, <<location>> indicates the role of the word node, <<name>> indicates the name of the word node, <<type>> indicates the return type of a function or type of variable, <<pos>> indicates the part of speech tagging of each word node, and <<parameters>> indicates the parameters of a function and constructor.
