parser grammar SwumParser;
options {tokenVocab=SwumLexer; }

start_rule: (noun_phrase | verb_phrase | prepositional_phrase | verb_group) stop_rule;
noun_phrase: Noun_Modifier* Noun;
prepositional_phrase: Preposition noun_phrase;
verb_group: Verb_Modifier* Verb+ Verb_Particle?;
verb_phrase: verb_group noun_phrase prepositional_phrase?;

// enables mandating the entire input to be parsed
stop_rule: Stop_Code;

// when start_rule fails, try to parse nonterminal, then terminal
fail_rule1: (noun_phrase | verb_phrase | prepositional_phrase | verb_group);
fail_rule2: (Noun_Modifier | Noun | Verb_Modifier | Verb_Particle | Verb | Conjunction | Determiner | Digit | Pronoun | Preposition);

// constructed manually after parsing
unknown_phrase: ;

