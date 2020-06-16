parser grammar SwumParser;
options {tokenVocab=SwumLexer; }

phrase: noun_phrase | verb_phrase | prepositional_phrase | verb_group | equivalence;  // experimental starting rule
noun_phrase: Noun_Modifier* Noun;
prepositional_phrase: Preposition noun_phrase;
verb_group: Verb_Modifier* Verb Verb_Particle?; // what is VI? (as seen in paper)
verb_phrase: (verb_group | equivalence_vg) (noun_phrase | equivalence_np) prepositional_phrase?;
equivalence: equivalence_np | equivalence_vg;
equivalence_np: noun_phrase+;
equivalence_vg: verb_group+;
