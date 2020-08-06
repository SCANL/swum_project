parser grammar SwumParser;
options {tokenVocab=SwumLexer; }

start_rule: (noun_phrase | verb_phrase | prepositional_phrase | verb_group) stop_rule;
noun_phrase: Noun_Modifier* Noun;
prepositional_phrase: Preposition noun_phrase;
verb_group: Verb_Modifier* Verb+ Verb_Particle?;
verb_phrase: verb_group noun_phrase prepositional_phrase?;

// fail_rule: unknown_phrase;
// unknown_phrase: (Noun_Modifier | Noun | Verb_Modifier | Verb_Particle | Verb | Conjunction | Determiner | Digit | Pronoun | Preposition)+ Stop_Code; // match all possible lexer tokens

stop_rule: Stop_Code;
fail_rule1: (noun_phrase | verb_phrase | prepositional_phrase | verb_group);
fail_rule2: (Noun_Modifier | Noun | Verb_Modifier | Verb_Particle | Verb | Conjunction | Determiner | Digit | Pronoun | Preposition);
unknown_phrase: ;   // constructed manually after parsing

// Equivalences are constructed in a post-processing step after parsing

// verb_phrase: (verb_group | equivalence_vg) (noun_phrase | equivalence_np) prepositional_phrase?;
// equivalence: equivalence_np | equivalence_vg;
// equivalence_np: noun_phrase+;
// equivalence_vg: verb_group+;
