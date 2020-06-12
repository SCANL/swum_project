// Generated from /home/brian/reu/antlr_simple_calc/CalcLexer.g4 by ANTLR 4.7.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class CalcLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.7.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		Number=1, Whitespace=2, Comment=3, Add=4, Subtract=5, Multiply=6, Divide=7, 
		OpenParen=8, CloseParen=9;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	public static final String[] ruleNames = {
		"Number", "Whitespace", "Comment", "Add", "Subtract", "Multiply", "Divide", 
		"OpenParen", "CloseParen"
	};

	private static final String[] _LITERAL_NAMES = {
		null, null, null, null, "'+'", "'-'", "'*'", "'/'", "'('", "')'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, "Number", "Whitespace", "Comment", "Add", "Subtract", "Multiply", 
		"Divide", "OpenParen", "CloseParen"
	};
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


	public CalcLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "CalcLexer.g4"; }

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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\13Y\b\1\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\3\2\6\2"+
		"\27\n\2\r\2\16\2\30\3\2\3\2\6\2\35\n\2\r\2\16\2\36\5\2!\n\2\3\2\3\2\6"+
		"\2%\n\2\r\2\16\2&\5\2)\n\2\3\3\6\3,\n\3\r\3\16\3-\3\3\3\3\3\4\3\4\3\4"+
		"\3\4\7\4\66\n\4\f\4\16\49\13\4\3\4\5\4<\n\4\3\4\3\4\3\4\3\4\3\4\7\4C\n"+
		"\4\f\4\16\4F\13\4\3\4\3\4\5\4J\n\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b"+
		"\3\b\3\t\3\t\3\n\3\n\3D\2\13\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13"+
		"\3\2\4\5\2\13\f\17\17\"\"\4\2\f\f\17\17\2b\2\3\3\2\2\2\2\5\3\2\2\2\2\7"+
		"\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2"+
		"\2\2\23\3\2\2\2\3(\3\2\2\2\5+\3\2\2\2\7I\3\2\2\2\tM\3\2\2\2\13O\3\2\2"+
		"\2\rQ\3\2\2\2\17S\3\2\2\2\21U\3\2\2\2\23W\3\2\2\2\25\27\4\62;\2\26\25"+
		"\3\2\2\2\27\30\3\2\2\2\30\26\3\2\2\2\30\31\3\2\2\2\31 \3\2\2\2\32\34\7"+
		"\60\2\2\33\35\4\62;\2\34\33\3\2\2\2\35\36\3\2\2\2\36\34\3\2\2\2\36\37"+
		"\3\2\2\2\37!\3\2\2\2 \32\3\2\2\2 !\3\2\2\2!)\3\2\2\2\"$\7\60\2\2#%\4\62"+
		";\2$#\3\2\2\2%&\3\2\2\2&$\3\2\2\2&\'\3\2\2\2\')\3\2\2\2(\26\3\2\2\2(\""+
		"\3\2\2\2)\4\3\2\2\2*,\t\2\2\2+*\3\2\2\2,-\3\2\2\2-+\3\2\2\2-.\3\2\2\2"+
		"./\3\2\2\2/\60\b\3\2\2\60\6\3\2\2\2\61\62\7\61\2\2\62\63\7\61\2\2\63\67"+
		"\3\2\2\2\64\66\n\3\2\2\65\64\3\2\2\2\669\3\2\2\2\67\65\3\2\2\2\678\3\2"+
		"\2\28;\3\2\2\29\67\3\2\2\2:<\7\17\2\2;:\3\2\2\2;<\3\2\2\2<=\3\2\2\2=J"+
		"\7\f\2\2>?\7\61\2\2?@\7,\2\2@D\3\2\2\2AC\13\2\2\2BA\3\2\2\2CF\3\2\2\2"+
		"DE\3\2\2\2DB\3\2\2\2EG\3\2\2\2FD\3\2\2\2GH\7,\2\2HJ\7\61\2\2I\61\3\2\2"+
		"\2I>\3\2\2\2JK\3\2\2\2KL\b\4\2\2L\b\3\2\2\2MN\7-\2\2N\n\3\2\2\2OP\7/\2"+
		"\2P\f\3\2\2\2QR\7,\2\2R\16\3\2\2\2ST\7\61\2\2T\20\3\2\2\2UV\7*\2\2V\22"+
		"\3\2\2\2WX\7+\2\2X\24\3\2\2\2\r\2\30\36 &(-\67;DI\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}