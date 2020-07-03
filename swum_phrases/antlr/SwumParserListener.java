// Generated from SwumParser.g4 by ANTLR 4.8
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link SwumParser}.
 */
public interface SwumParserListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link SwumParser#swum_phrase}.
	 * @param ctx the parse tree
	 */
	void enterSwum_phrase(SwumParser.Swum_phraseContext ctx);
	/**
	 * Exit a parse tree produced by {@link SwumParser#swum_phrase}.
	 * @param ctx the parse tree
	 */
	void exitSwum_phrase(SwumParser.Swum_phraseContext ctx);
	/**
	 * Enter a parse tree produced by {@link SwumParser#noun_phrase}.
	 * @param ctx the parse tree
	 */
	void enterNoun_phrase(SwumParser.Noun_phraseContext ctx);
	/**
	 * Exit a parse tree produced by {@link SwumParser#noun_phrase}.
	 * @param ctx the parse tree
	 */
	void exitNoun_phrase(SwumParser.Noun_phraseContext ctx);
	/**
	 * Enter a parse tree produced by {@link SwumParser#prepositional_phrase}.
	 * @param ctx the parse tree
	 */
	void enterPrepositional_phrase(SwumParser.Prepositional_phraseContext ctx);
	/**
	 * Exit a parse tree produced by {@link SwumParser#prepositional_phrase}.
	 * @param ctx the parse tree
	 */
	void exitPrepositional_phrase(SwumParser.Prepositional_phraseContext ctx);
	/**
	 * Enter a parse tree produced by {@link SwumParser#verb_group}.
	 * @param ctx the parse tree
	 */
	void enterVerb_group(SwumParser.Verb_groupContext ctx);
	/**
	 * Exit a parse tree produced by {@link SwumParser#verb_group}.
	 * @param ctx the parse tree
	 */
	void exitVerb_group(SwumParser.Verb_groupContext ctx);
	/**
	 * Enter a parse tree produced by {@link SwumParser#verb_phrase}.
	 * @param ctx the parse tree
	 */
	void enterVerb_phrase(SwumParser.Verb_phraseContext ctx);
	/**
	 * Exit a parse tree produced by {@link SwumParser#verb_phrase}.
	 * @param ctx the parse tree
	 */
	void exitVerb_phrase(SwumParser.Verb_phraseContext ctx);
}