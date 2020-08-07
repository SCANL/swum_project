lexer grammar SwumLexer;

Noun_Modifier: 'NM';
Noun: 'N';
Verb_Modifier: 'VM';
Verb_Particle: 'VPR';
Verb: 'V';
Conjunction: 'CJ';
Determiner: 'DT';
Digit: 'D';
Pronoun: 'PR';
Preposition: 'P';

Whitespace: ('\t' | ' ' | '\r' | '\n')+   -> skip;
Stop_Code: 'STOP';
