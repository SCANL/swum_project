// Generated from /home/brian/reu/swum_project/swum_phrases/SwumLexer.g4 by ANTLR 4.8
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class SwumLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.8", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		Whitespace=1, Noun_Modifier=2, Noun=3, Verb_Modifier=4, Verb_Particle=5, 
		Verb=6, Conjunction=7, Determiner=8, Digit=9, Pronoun=10, Preposition=11;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"Whitespace", "Noun_Modifier", "Noun", "Verb_Modifier", "Verb_Particle", 
			"Verb", "Conjunction", "Determiner", "Digit", "Pronoun", "Preposition"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, null, "'NM'", "'N'", "'VM'", "'VPR'", "'V'", "'CJ'", "'DT'", "'D'", 
			"'PR'", "'P'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "Whitespace", "Noun_Modifier", "Noun", "Verb_Modifier", "Verb_Particle", 
			"Verb", "Conjunction", "Determiner", "Digit", "Pronoun", "Preposition"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public SwumLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "SwumLexer.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\r;\b\1\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\3\2\6\2\33\n\2\r\2\16\2\34\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\5"+
		"\3\5\3\5\3\6\3\6\3\6\3\6\3\7\3\7\3\b\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\13"+
		"\3\13\3\13\3\f\3\f\2\2\r\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f"+
		"\27\r\3\2\3\5\2\13\f\17\17\"\"\2;\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2"+
		"\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3"+
		"\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\3\32\3\2\2\2\5 \3\2\2\2\7#\3\2\2\2\t"+
		"%\3\2\2\2\13(\3\2\2\2\r,\3\2\2\2\17.\3\2\2\2\21\61\3\2\2\2\23\64\3\2\2"+
		"\2\25\66\3\2\2\2\279\3\2\2\2\31\33\t\2\2\2\32\31\3\2\2\2\33\34\3\2\2\2"+
		"\34\32\3\2\2\2\34\35\3\2\2\2\35\36\3\2\2\2\36\37\b\2\2\2\37\4\3\2\2\2"+
		" !\7P\2\2!\"\7O\2\2\"\6\3\2\2\2#$\7P\2\2$\b\3\2\2\2%&\7X\2\2&\'\7O\2\2"+
		"\'\n\3\2\2\2()\7X\2\2)*\7R\2\2*+\7T\2\2+\f\3\2\2\2,-\7X\2\2-\16\3\2\2"+
		"\2./\7E\2\2/\60\7L\2\2\60\20\3\2\2\2\61\62\7F\2\2\62\63\7V\2\2\63\22\3"+
		"\2\2\2\64\65\7F\2\2\65\24\3\2\2\2\66\67\7R\2\2\678\7T\2\28\26\3\2\2\2"+
		"9:\7R\2\2:\30\3\2\2\2\4\2\34\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}