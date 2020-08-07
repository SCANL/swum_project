# SWUM Words
Analysis of word nodes within SWUM <sub>words</sub>. In SWUM <sub>words</sub>, there exists a word node for every word ocurrence in a specific code sample. We analyze each word node by splitting each word using identifier splitting techniques. Then we annotate each word node with part of speech tagging and its role in the code (function, class, variable name, etc.). The analysis of the word nodes are then sent to the SWUM <sub>phrases</sub> stage where word relationships are used to develop edges between word nodes.
## Installation
1. SWUM <sub>words</sub> requires [Python 3.7+](https://www.python.org) and has been tested on Python 3.8.
2. To convert your Java and C++ file to a XML file, download [SRCML](https://www.srcml.org) with directions downloading SRCML [here](https://www.srcml.org/#download) 
3. To use SWUM <sub>words</sub>, you have to downdload the [Spiral](https://github.com/casics/spiral) module which includes Ronin (the most advanced identifier splitter in the module). 
4. Install [lxml](https://pypi.org/project/lxml/) which helps write the XML file
## Usage
Run this command in the terminal window or IDE 
```python
run swum_words.py [InputFileName].xml [OutputFileName].xml
```
## Input
The program takes a XML file that has been converted from Java/C++ using SRCML with tags representing the role, name, and specifier of identifiers. See the ```examples``` directory for a sample input, output, and changed input.
## Output
A XML file containing the role, name, part of speech, and type of an identifier. The program also outputs parameters for functions and arguments for types if applicable.
```<?xml version="1.0" ?><swum_identifiers><swum_identifier><location>class</location><name>MyClass</name><identifier><word>My<pos>PRP$</pos></word><word>Class<pos>NN</pos></word></identifier></swum_identifier><swum_identifier><location>constructor</location><class>MyClass</class><name>MyClass</name><identifier><word>My<pos>PRP$</pos></word><word>Class<pos>NN</pos></word></identifier></swum_identifier><swum_identifier><location>function</location><class>MyClass</class><name>getArea</name><type><swum_identifier><location>type</location><name>int</name><identifier><word>int<pos>NN</pos></word></identifier></swum_identifier></type><parameters><swum_identifier><location>parameter</location><name>x</name><type><swum_identifier><location>type</location><name>int</name>
<identifier><word>int<pos>NN</pos></word></identifier></swum_identifier></type><identifier><word>x<pos>NN</pos></word></identifier></swum_identifier><swum_identifier><location>parameter</location><name>y</name><type><swum_identifier><location>type</location><name>int</name><identifier><word>int<pos>NN</pos></word></identifier></swum_identifier></type><identifier><word>y<pos>NN</pos></word></identifier></swum_identifier></parameters><identifier><word>get<pos>VB</pos></word><word>Area<pos>NNP</pos></word></identifier></swum_identifier><swum_identifier><location>variable</location><name>z</name><type><swum_identifier><location>type</location><name>int</name><identifier><word>int<pos>NN</pos></word></identifier></swum_identifier></type><identifier><word>z<pos>NN</pos></word></identifier></swum_identifier></swum_identifiers>
```
## Changed Input
A second XML file is outputted with the input have ID numbers so one can easily locate the identifier in the output.
```xml<?xml version="1.0" encoding="iso-8859-1"?><main><class swum_ID="0"><specifier>public</specifier> class <name>MyClass</name> <block>{<constructor swum_ID="1"><specifier>public</specifier> <name>MyClass</name><parameter_list>()</parameter_list><block>{<block_content></block_content>}</block></constructor><function swum_ID="2"><type><specifier>public</specifier> <specifier>static</specifier> <name>int</name></type> <name>getArea</name><parameter_list>(<parameter><decl><type><specifier>final</specifier> <name>int</name></type> <name>x</name></decl></parameter>, <parameter><decl><type><specifier>final</specifier> <name>int</name></type> <name>y</name></decl></parameter>)</parameter_list> <block>{<block_content><decl_stmt><decl><type><name>int</name></type> <name>z</name> <init>= <expr><name>x</name> <operator>*</operator> <name>y</name></expr></init></decl>;</decl_stmt><return>return <expr><name>z</name></expr>;</return></block_content>}</block></function>}</block></class></main>```
