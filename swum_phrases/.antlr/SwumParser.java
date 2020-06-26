// Generated from /home/brian/reu/swum_project/swum_phrases/SwumParser.g4 by ANTLR 4.8
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class SwumParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.8", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		POS_Tag=1, End_Tag=2, Bracket=3, Metadata=4, Whitespace=5, Noun_Modifier=6, 
		Noun=7, Verb_Modifier=8, Verb_Particle=9, Verb=10, Conjunction=11, Determiner=12, 
		Digit=13, Pronoun=14, Preposition=15, End_POS_Tag=16;
	public static final int
		RULE_start = 0, RULE_noun_phrase = 1, RULE_prepositional_phrase = 2, RULE_verb_group = 3, 
		RULE_verb_phrase = 4;
	private static String[] makeRuleNames() {
		return new String[] {
			"start", "noun_phrase", "prepositional_phrase", "verb_group", "verb_phrase"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'<POS>'", null, null, null, null, "'NM'", "'N'", "'VM'", "'VPR'", 
			"'V'", "'CJ'", "'DT'", "'D'", "'PR'", "'P'", "'</POS>'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "POS_Tag", "End_Tag", "Bracket", "Metadata", "Whitespace", "Noun_Modifier", 
			"Noun", "Verb_Modifier", "Verb_Particle", "Verb", "Conjunction", "Determiner", 
			"Digit", "Pronoun", "Preposition", "End_POS_Tag"
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

	@Override
	public String getGrammarFileName() { return "SwumParser.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public SwumParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class StartContext extends ParserRuleContext {
		public Noun_phraseContext noun_phrase() {
			return getRuleContext(Noun_phraseContext.class,0);
		}
		public Verb_phraseContext verb_phrase() {
			return getRuleContext(Verb_phraseContext.class,0);
		}
		public Prepositional_phraseContext prepositional_phrase() {
			return getRuleContext(Prepositional_phraseContext.class,0);
		}
		public Verb_groupContext verb_group() {
			return getRuleContext(Verb_groupContext.class,0);
		}
		public StartContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_start; }
	}

	public final StartContext start() throws RecognitionException {
		StartContext _localctx = new StartContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_start);
		try {
			setState(14);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(10);
				noun_phrase();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(11);
				verb_phrase();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(12);
				prepositional_phrase();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(13);
				verb_group();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Noun_phraseContext extends ParserRuleContext {
		public TerminalNode Noun() { return getToken(SwumParser.Noun, 0); }
		public List<TerminalNode> Noun_Modifier() { return getTokens(SwumParser.Noun_Modifier); }
		public TerminalNode Noun_Modifier(int i) {
			return getToken(SwumParser.Noun_Modifier, i);
		}
		public Noun_phraseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_noun_phrase; }
	}

	public final Noun_phraseContext noun_phrase() throws RecognitionException {
		Noun_phraseContext _localctx = new Noun_phraseContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_noun_phrase);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(19);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==Noun_Modifier) {
				{
				{
				setState(16);
				match(Noun_Modifier);
				}
				}
				setState(21);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(22);
			match(Noun);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Prepositional_phraseContext extends ParserRuleContext {
		public TerminalNode Preposition() { return getToken(SwumParser.Preposition, 0); }
		public Noun_phraseContext noun_phrase() {
			return getRuleContext(Noun_phraseContext.class,0);
		}
		public Prepositional_phraseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prepositional_phrase; }
	}

	public final Prepositional_phraseContext prepositional_phrase() throws RecognitionException {
		Prepositional_phraseContext _localctx = new Prepositional_phraseContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_prepositional_phrase);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(24);
			match(Preposition);
			setState(25);
			noun_phrase();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Verb_groupContext extends ParserRuleContext {
		public List<TerminalNode> Verb_Modifier() { return getTokens(SwumParser.Verb_Modifier); }
		public TerminalNode Verb_Modifier(int i) {
			return getToken(SwumParser.Verb_Modifier, i);
		}
		public List<TerminalNode> Verb() { return getTokens(SwumParser.Verb); }
		public TerminalNode Verb(int i) {
			return getToken(SwumParser.Verb, i);
		}
		public TerminalNode Verb_Particle() { return getToken(SwumParser.Verb_Particle, 0); }
		public Verb_groupContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_verb_group; }
	}

	public final Verb_groupContext verb_group() throws RecognitionException {
		Verb_groupContext _localctx = new Verb_groupContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_verb_group);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(30);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==Verb_Modifier) {
				{
				{
				setState(27);
				match(Verb_Modifier);
				}
				}
				setState(32);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(34); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(33);
				match(Verb);
				}
				}
				setState(36); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==Verb );
			setState(39);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==Verb_Particle) {
				{
				setState(38);
				match(Verb_Particle);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Verb_phraseContext extends ParserRuleContext {
		public Verb_groupContext verb_group() {
			return getRuleContext(Verb_groupContext.class,0);
		}
		public Noun_phraseContext noun_phrase() {
			return getRuleContext(Noun_phraseContext.class,0);
		}
		public Prepositional_phraseContext prepositional_phrase() {
			return getRuleContext(Prepositional_phraseContext.class,0);
		}
		public Verb_phraseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_verb_phrase; }
	}

	public final Verb_phraseContext verb_phrase() throws RecognitionException {
		Verb_phraseContext _localctx = new Verb_phraseContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_verb_phrase);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(41);
			verb_group();
			setState(42);
			noun_phrase();
			setState(44);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==Preposition) {
				{
				setState(43);
				prepositional_phrase();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\22\61\4\2\t\2\4\3"+
		"\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3\2\3\2\5\2\21\n\2\3\3\7\3\24\n\3"+
		"\f\3\16\3\27\13\3\3\3\3\3\3\4\3\4\3\4\3\5\7\5\37\n\5\f\5\16\5\"\13\5\3"+
		"\5\6\5%\n\5\r\5\16\5&\3\5\5\5*\n\5\3\6\3\6\3\6\5\6/\n\6\3\6\2\2\7\2\4"+
		"\6\b\n\2\2\2\63\2\20\3\2\2\2\4\25\3\2\2\2\6\32\3\2\2\2\b \3\2\2\2\n+\3"+
		"\2\2\2\f\21\5\4\3\2\r\21\5\n\6\2\16\21\5\6\4\2\17\21\5\b\5\2\20\f\3\2"+
		"\2\2\20\r\3\2\2\2\20\16\3\2\2\2\20\17\3\2\2\2\21\3\3\2\2\2\22\24\7\b\2"+
		"\2\23\22\3\2\2\2\24\27\3\2\2\2\25\23\3\2\2\2\25\26\3\2\2\2\26\30\3\2\2"+
		"\2\27\25\3\2\2\2\30\31\7\t\2\2\31\5\3\2\2\2\32\33\7\21\2\2\33\34\5\4\3"+
		"\2\34\7\3\2\2\2\35\37\7\n\2\2\36\35\3\2\2\2\37\"\3\2\2\2 \36\3\2\2\2 "+
		"!\3\2\2\2!$\3\2\2\2\" \3\2\2\2#%\7\f\2\2$#\3\2\2\2%&\3\2\2\2&$\3\2\2\2"+
		"&\'\3\2\2\2\')\3\2\2\2(*\7\13\2\2)(\3\2\2\2)*\3\2\2\2*\t\3\2\2\2+,\5\b"+
		"\5\2,.\5\4\3\2-/\5\6\4\2.-\3\2\2\2./\3\2\2\2/\13\3\2\2\2\b\20\25 &).";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}