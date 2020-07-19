# SWUM Words
Analysis of word nodes within SWUM <sub>words</sub>
In SWUM <sub>words</sub>, there exists a word node for every word ocurrence in a specific code sample. We analyze each word node by splitting each word using the NLTK python library and identifier splitting techniques. Then we annotate each word node with parts of speech tagging and its role in the code (function, class, variable name, etc.). The analysis of the word nodes are then sent to the SWUM <sub>phrases</sub> stage where word relationships are used to develop edges between word nodes.
## Installation
1. SWUM <sub>words</sub> requires [Python 3.7+](https://www.python.org) and has been tested on Python 3.8.
2. To convert your Java and C++ file, I would recommend downloading [SRCML](https://www.srcml.org) with directions downloading SRCML [here](https://www.srcml.org/#download) 
3. To use SWUM <sub>words</sub>, you have to downdload the [Spiral](https://github.com/casics/spiral) module which includes Ronin( the most advanced identifier splitter in the module). 
4. Install [lxml](https://pypi.org/project/lxml/) which helps write the XML file
## Usage
Write this command in the terminal window or IDE 
```python
run swum_words.py
```
The program then asks 
```python
XML Input File: [InputFileName].xml
XML Output File: [OutputFileName].xml
```
## Description of Code
swum_words.py imports xml.sax a XML interface for Python and methods part of xml.sax. A dictionary is used to keep track which tags are "open" and "closed" using the increment/decrement operator. swum_words.py utilizes lxml to write a XML file where the swum_identifiers tag indicate the beginning of the file, location tag indicates the role of the word node, name tag indicates the name of the word node, type tag indicates the return type of a function or type of variable, pos tag indicates the part of speech tagging of each word node, and parameters tag indicates the parameters of a function and constructor.
