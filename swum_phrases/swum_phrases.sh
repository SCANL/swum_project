#!/bin/bash

echo 'creating antlr files...'
cd antlr
java -Xmx500M -cp "/usr/local/lib/antlr-4.8-complete.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 SwumLexer.g4 SwumParser.g4 -visitor
cd ..
echo 'done'
python3 SwumPhrases.py $1
echo 'deleting antlr files...'
cd antlr
rm -r __pycache__ SwumLexer.interp SwumLexer.py SwumLexer.tokens SwumParser.interp SwumParser.py SwumParser.tokens SwumParserListener.py SwumParserVisitor.py
echo 'done'
