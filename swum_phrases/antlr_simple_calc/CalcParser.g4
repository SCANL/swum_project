// inspired by the basic grammar at https://stackoverflow.com/questions/1931307/antlr-is-there-a-simple-example
parser grammar CalcParser;
options { tokenVocab=CalcLexer; }   // allow literals contained in lexer
expression
    : addop
    ;
addop
    : mulop # ADD_ATOM
    | mulop '+' mulop   # ADD
    | mulop '-' mulop   # SUB
    ;
mulop
    : term  # MUL_ATOM
    | term '*' term # MUL
    | term '/' term # DIV
    ;
term
    : Number    # NUMBER
    | '(' expression ')'    # NESTED_EXPR
    ;
