// inspired by the basic grammar at https://stackoverflow.com/questions/1931307/antlr-is-there-a-simple-example
lexer grammar CalcLexer;
Number
    : ('0'..'9')+ ('.' ('0'..'9')+)?
    | '.' ('0'..'9')+   // support dropping leading zero
    ;
Whitespace
    : ('\t' | ' ' | '\r' | '\n')+   -> skip
    ;
Comment
    : ('//' ~[\r\n]* '\r'? '\n'  // single line (unix and windows line endings)
    | '/*' .*? '*/')    // multiline
    -> skip
    ;

// single character lexemes so that we can use these literals in the parser grammer via tokenVocab
Add
    : '+'
    ;
Subtract
    : '-'
    ;
Multiply
    : '*'
    ;
Divide
    : '/'
    ;
OpenParen
    : '('
    ;
CloseParen
    : ')'
    ;
