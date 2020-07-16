parser grammar SwumParser;
options {tokenVocab=SwumLexer; }

start_rule: noun_phrase | verb_phrase | prepositional_phrase | verb_group;  // experimental starting rule (allow multiple subrules for robustness)
noun_phrase: Noun_Modifier* Noun;
prepositional_phrase: Preposition noun_phrase;
verb_group: Verb_Modifier* Verb+ Verb_Particle?;
verb_phrase: verb_group noun_phrase prepositional_phrase?;

// Equivalences are constructed in a post-processing step after parsing

// verb_phrase: (verb_group | equivalence_vg) (noun_phrase | equivalence_np) prepositional_phrase?;
// equivalence: equivalence_np | equivalence_vg;
// equivalence_np: noun_phrase+;
// equivalence_vg: verb_group+;
