# swum_words
## Name
Analysis of word nodes within SWUM <sub>words</sub>
## Description
Using a word node in SWUM <sub>words</sub> in a specific code sample, we split each identifier using the NLTK python library and identifier splitting techniques. Then we annotate each word node with parts of speech tagging and its role in the code. The analysis of the word nodes are then sent to the SWUM <sub>phrases</sub> stage where word relationships are used to develop edges between word nodes.
## Usage 
Input: XML file representing a code sample. 
Output: Prints out the role the word node plays and its name("Role: Name") and XML file of the result.
        The
