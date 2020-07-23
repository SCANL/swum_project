lexer grammar SwumLexer;

// channels {
//     METADATA
// }

// POS_Tag: '<POS>' ->skip, mode(POS);
// End_Tag: '</' .+? '>' -> skip;
// Bracket: ('<' | '>') -> skip;
// Metadata: ~[<>]+ -> channel(METADATA);

Whitespace: ('\t' | ' ' | '\r' | '\n')+   -> skip;
Stop_Code: 'STOP';

// mode POS;
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

// End_POS_Tag: '</POS>' ->skip, mode(DEFAULT_MODE);

