// Generated from SwumParser.g4 by ANTLR 4.8
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link SwumParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface SwumParserVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link SwumParser#swum_phrase}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSwum_phrase(SwumParser.Swum_phraseContext ctx);
	/**
	 * Visit a parse tree produced by {@link SwumParser#noun_phrase}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNoun_phrase(SwumParser.Noun_phraseContext ctx);
	/**
	 * Visit a parse tree produced by {@link SwumParser#prepositional_phrase}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrepositional_phrase(SwumParser.Prepositional_phraseContext ctx);
	/**
	 * Visit a parse tree produced by {@link SwumParser#verb_group}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVerb_group(SwumParser.Verb_groupContext ctx);
	/**
	 * Visit a parse tree produced by {@link SwumParser#verb_phrase}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVerb_phrase(SwumParser.Verb_phraseContext ctx);
}