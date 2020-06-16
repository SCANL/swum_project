// Generated from /home/brian/reu/swum_project/swum_phrases/xml_input/SwumParser.g4 by ANTLR 4.8
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
		Noun_Modifier=1, Noun=2, Verb_Modifier=3, Verb_Particle=4, Verb=5, Conjunction=6, 
		Determiner=7, Digit=8, Pronoun=9, Preposition=10, Whitespace=11;
	public static final int
		RULE_phrase = 0, RULE_noun_phrase = 1, RULE_prepositional_phrase = 2, 
		RULE_verb_group = 3, RULE_verb_phrase = 4, RULE_equivalence = 5, RULE_equivalence_np = 6, 
		RULE_equivalence_vg = 7;
	private static String[] makeRuleNames() {
		return new String[] {
			"phrase", "noun_phrase", "prepositional_phrase", "verb_group", "verb_phrase", 
			"equivalence", "equivalence_np", "equivalence_vg"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'NM'", "'N'", "'VM'", "'VPR'", "'V'", "'CJ'", "'DT'", "'D'", "'PR'", 
			"'P'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "Noun_Modifier", "Noun", "Verb_Modifier", "Verb_Particle", "Verb", 
			"Conjunction", "Determiner", "Digit", "Pronoun", "Preposition", "Whitespace"
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

	public static class PhraseContext extends ParserRuleContext {
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
		public EquivalenceContext equivalence() {
			return getRuleContext(EquivalenceContext.class,0);
		}
		public PhraseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_phrase; }
	}

	public final PhraseContext phrase() throws RecognitionException {
		PhraseContext _localctx = new PhraseContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_phrase);
		try {
			setState(21);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(16);
				noun_phrase();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(17);
				verb_phrase();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(18);
				prepositional_phrase();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(19);
				verb_group();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(20);
				equivalence();
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
			setState(26);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==Noun_Modifier) {
				{
				{
				setState(23);
				match(Noun_Modifier);
				}
				}
				setState(28);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(29);
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
			setState(31);
			match(Preposition);
			setState(32);
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
		public TerminalNode Verb() { return getToken(SwumParser.Verb, 0); }
		public List<TerminalNode> Verb_Modifier() { return getTokens(SwumParser.Verb_Modifier); }
		public TerminalNode Verb_Modifier(int i) {
			return getToken(SwumParser.Verb_Modifier, i);
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
			setState(37);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==Verb_Modifier) {
				{
				{
				setState(34);
				match(Verb_Modifier);
				}
				}
				setState(39);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(40);
			match(Verb);
			setState(42);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==Verb_Particle) {
				{
				setState(41);
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
		public Equivalence_vgContext equivalence_vg() {
			return getRuleContext(Equivalence_vgContext.class,0);
		}
		public Noun_phraseContext noun_phrase() {
			return getRuleContext(Noun_phraseContext.class,0);
		}
		public Equivalence_npContext equivalence_np() {
			return getRuleContext(Equivalence_npContext.class,0);
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
			setState(46);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,4,_ctx) ) {
			case 1:
				{
				setState(44);
				verb_group();
				}
				break;
			case 2:
				{
				setState(45);
				equivalence_vg();
				}
				break;
			}
			setState(50);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				{
				setState(48);
				noun_phrase();
				}
				break;
			case 2:
				{
				setState(49);
				equivalence_np();
				}
				break;
			}
			setState(53);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==Preposition) {
				{
				setState(52);
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

	public static class EquivalenceContext extends ParserRuleContext {
		public Equivalence_npContext equivalence_np() {
			return getRuleContext(Equivalence_npContext.class,0);
		}
		public Equivalence_vgContext equivalence_vg() {
			return getRuleContext(Equivalence_vgContext.class,0);
		}
		public EquivalenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_equivalence; }
	}

	public final EquivalenceContext equivalence() throws RecognitionException {
		EquivalenceContext _localctx = new EquivalenceContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_equivalence);
		try {
			setState(57);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case Noun_Modifier:
			case Noun:
				enterOuterAlt(_localctx, 1);
				{
				setState(55);
				equivalence_np();
				}
				break;
			case Verb_Modifier:
			case Verb:
				enterOuterAlt(_localctx, 2);
				{
				setState(56);
				equivalence_vg();
				}
				break;
			default:
				throw new NoViableAltException(this);
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

	public static class Equivalence_npContext extends ParserRuleContext {
		public List<Noun_phraseContext> noun_phrase() {
			return getRuleContexts(Noun_phraseContext.class);
		}
		public Noun_phraseContext noun_phrase(int i) {
			return getRuleContext(Noun_phraseContext.class,i);
		}
		public Equivalence_npContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_equivalence_np; }
	}

	public final Equivalence_npContext equivalence_np() throws RecognitionException {
		Equivalence_npContext _localctx = new Equivalence_npContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_equivalence_np);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(60); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(59);
				noun_phrase();
				}
				}
				setState(62); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==Noun_Modifier || _la==Noun );
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

	public static class Equivalence_vgContext extends ParserRuleContext {
		public List<Verb_groupContext> verb_group() {
			return getRuleContexts(Verb_groupContext.class);
		}
		public Verb_groupContext verb_group(int i) {
			return getRuleContext(Verb_groupContext.class,i);
		}
		public Equivalence_vgContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_equivalence_vg; }
	}

	public final Equivalence_vgContext equivalence_vg() throws RecognitionException {
		Equivalence_vgContext _localctx = new Equivalence_vgContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_equivalence_vg);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(65); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(64);
				verb_group();
				}
				}
				setState(67); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==Verb_Modifier || _la==Verb );
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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\rH\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\3\2\3\2\3\2\3\2\3\2"+
		"\5\2\30\n\2\3\3\7\3\33\n\3\f\3\16\3\36\13\3\3\3\3\3\3\4\3\4\3\4\3\5\7"+
		"\5&\n\5\f\5\16\5)\13\5\3\5\3\5\5\5-\n\5\3\6\3\6\5\6\61\n\6\3\6\3\6\5\6"+
		"\65\n\6\3\6\5\68\n\6\3\7\3\7\5\7<\n\7\3\b\6\b?\n\b\r\b\16\b@\3\t\6\tD"+
		"\n\t\r\t\16\tE\3\t\2\2\n\2\4\6\b\n\f\16\20\2\2\2L\2\27\3\2\2\2\4\34\3"+
		"\2\2\2\6!\3\2\2\2\b\'\3\2\2\2\n\60\3\2\2\2\f;\3\2\2\2\16>\3\2\2\2\20C"+
		"\3\2\2\2\22\30\5\4\3\2\23\30\5\n\6\2\24\30\5\6\4\2\25\30\5\b\5\2\26\30"+
		"\5\f\7\2\27\22\3\2\2\2\27\23\3\2\2\2\27\24\3\2\2\2\27\25\3\2\2\2\27\26"+
		"\3\2\2\2\30\3\3\2\2\2\31\33\7\3\2\2\32\31\3\2\2\2\33\36\3\2\2\2\34\32"+
		"\3\2\2\2\34\35\3\2\2\2\35\37\3\2\2\2\36\34\3\2\2\2\37 \7\4\2\2 \5\3\2"+
		"\2\2!\"\7\f\2\2\"#\5\4\3\2#\7\3\2\2\2$&\7\5\2\2%$\3\2\2\2&)\3\2\2\2\'"+
		"%\3\2\2\2\'(\3\2\2\2(*\3\2\2\2)\'\3\2\2\2*,\7\7\2\2+-\7\6\2\2,+\3\2\2"+
		"\2,-\3\2\2\2-\t\3\2\2\2.\61\5\b\5\2/\61\5\20\t\2\60.\3\2\2\2\60/\3\2\2"+
		"\2\61\64\3\2\2\2\62\65\5\4\3\2\63\65\5\16\b\2\64\62\3\2\2\2\64\63\3\2"+
		"\2\2\65\67\3\2\2\2\668\5\6\4\2\67\66\3\2\2\2\678\3\2\2\28\13\3\2\2\29"+
		"<\5\16\b\2:<\5\20\t\2;9\3\2\2\2;:\3\2\2\2<\r\3\2\2\2=?\5\4\3\2>=\3\2\2"+
		"\2?@\3\2\2\2@>\3\2\2\2@A\3\2\2\2A\17\3\2\2\2BD\5\b\5\2CB\3\2\2\2DE\3\2"+
		"\2\2EC\3\2\2\2EF\3\2\2\2F\21\3\2\2\2\f\27\34\',\60\64\67;@E";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}