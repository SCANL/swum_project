# SWUM Phrases
The phrases layer of SWUM infers semantic relationships among code identifiers using natural language information. The phrases layer parses identifiers into phrasal tree structures based on part of speech tags, and the layer annotates the phrasal trees with semantic relationships such as action, theme, and auxiliary arguments. Currently, annotation is only supported for method/function identifiers.

# Installation

1. Make sure a recent version of [Python 3](https://www.python.org/) is installed. SWUM phrases requires Python 3.7+ and is tested on 3.8.x.
2. The phrases layer uses the parser generator [ANTLR](https://www.antlr.org/) in order to parse the constituent words of a code identifier into a phrase structure. Download version 4 of the base ANTLR tool [here](https://www.antlr.org/download.html) and follow the installation instructions. After installation, make sure the tool can be launched using the `antlr4` alias.
```
> antlr4
ANTLR Parser Generator  Version 4.8
 -o ___              specify output directory where all output is generated
 ...
``` 
3. Install Python dependencies, including the [Python 3 runtime target](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) for ANTLR.
```
pip install antlr4-python3-runtime lxml
```


# Usage
```
. ./swum_phrases input_file output_file
```
Be sure to include the leading dot.

## Input
The program accepts a single XML input file containing program (type, location, parameters, etc.) and part of speech information per identifier. The input file may be automatically generated from source code using the [SWUM words](https://github.com/SCANL/swum_project/tree/master/swum_words) layer. See the `examples` directory for sample input.

## Output
An XML file containing phrasal structure and annotation information per code identifier in the input file. Program information per identifier is also preserved.
```
<swum_identifier>
  <id>0</id>
  <name>MainObject</name>
  <location>class</location>
  <swum_phrase>
    <noun_phrase>
      <noun_modifier>Main</noun_modifier>
      <noun swum_attr="head_noun">Object</noun>
    </noun_phrase>
  </swum_phrase>
</swum_identifier>
```