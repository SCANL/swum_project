// Generated from /home/brian/reu/antlr_simple_calc/CalcParser.g4 by ANTLR 4.7.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class CalcParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.7.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		Number=1, Whitespace=2, Comment=3, Add=4, Subtract=5, Multiply=6, Divide=7, 
		OpenParen=8, CloseParen=9;
	public static final int
		RULE_expression = 0, RULE_addop = 1, RULE_mulop = 2, RULE_term = 3;
	public static final String[] ruleNames = {
		"expression", "addop", "mulop", "term"
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

	@Override
	public String getGrammarFileName() { return "CalcParser.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public CalcParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class ExpressionContext extends ParserRuleContext {
		public AddopContext addop() {
			return getRuleContext(AddopContext.class,0);
		}
		public ExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expression; }
	}

	public final ExpressionContext expression() throws RecognitionException {
		ExpressionContext _localctx = new ExpressionContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_expression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(8);
			addop();
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

	public static class AddopContext extends ParserRuleContext {
		public AddopContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_addop; }
	 
		public AddopContext() { }
		public void copyFrom(AddopContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class ADDContext extends AddopContext {
		public List<MulopContext> mulop() {
			return getRuleContexts(MulopContext.class);
		}
		public MulopContext mulop(int i) {
			return getRuleContext(MulopContext.class,i);
		}
		public ADDContext(AddopContext ctx) { copyFrom(ctx); }
	}
	public static class SUBContext extends AddopContext {
		public List<MulopContext> mulop() {
			return getRuleContexts(MulopContext.class);
		}
		public MulopContext mulop(int i) {
			return getRuleContext(MulopContext.class,i);
		}
		public SUBContext(AddopContext ctx) { copyFrom(ctx); }
	}
	public static class ADD_ATOMContext extends AddopContext {
		public MulopContext mulop() {
			return getRuleContext(MulopContext.class,0);
		}
		public ADD_ATOMContext(AddopContext ctx) { copyFrom(ctx); }
	}

	public final AddopContext addop() throws RecognitionException {
		AddopContext _localctx = new AddopContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_addop);
		try {
			setState(19);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
			case 1:
				_localctx = new ADD_ATOMContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(10);
				mulop();
				}
				break;
			case 2:
				_localctx = new ADDContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(11);
				mulop();
				setState(12);
				match(Add);
				setState(13);
				mulop();
				}
				break;
			case 3:
				_localctx = new SUBContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(15);
				mulop();
				setState(16);
				match(Subtract);
				setState(17);
				mulop();
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

	public static class MulopContext extends ParserRuleContext {
		public MulopContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mulop; }
	 
		public MulopContext() { }
		public void copyFrom(MulopContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class DIVContext extends MulopContext {
		public List<TermContext> term() {
			return getRuleContexts(TermContext.class);
		}
		public TermContext term(int i) {
			return getRuleContext(TermContext.class,i);
		}
		public DIVContext(MulopContext ctx) { copyFrom(ctx); }
	}
	public static class MULContext extends MulopContext {
		public List<TermContext> term() {
			return getRuleContexts(TermContext.class);
		}
		public TermContext term(int i) {
			return getRuleContext(TermContext.class,i);
		}
		public MULContext(MulopContext ctx) { copyFrom(ctx); }
	}
	public static class MUL_ATOMContext extends MulopContext {
		public TermContext term() {
			return getRuleContext(TermContext.class,0);
		}
		public MUL_ATOMContext(MulopContext ctx) { copyFrom(ctx); }
	}

	public final MulopContext mulop() throws RecognitionException {
		MulopContext _localctx = new MulopContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_mulop);
		try {
			setState(30);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
			case 1:
				_localctx = new MUL_ATOMContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(21);
				term();
				}
				break;
			case 2:
				_localctx = new MULContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(22);
				term();
				setState(23);
				match(Multiply);
				setState(24);
				term();
				}
				break;
			case 3:
				_localctx = new DIVContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(26);
				term();
				setState(27);
				match(Divide);
				setState(28);
				term();
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

	public static class TermContext extends ParserRuleContext {
		public TermContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_term; }
	 
		public TermContext() { }
		public void copyFrom(TermContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class NUMBERContext extends TermContext {
		public TerminalNode Number() { return getToken(CalcParser.Number, 0); }
		public NUMBERContext(TermContext ctx) { copyFrom(ctx); }
	}
	public static class NESTED_EXPRContext extends TermContext {
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public NESTED_EXPRContext(TermContext ctx) { copyFrom(ctx); }
	}

	public final TermContext term() throws RecognitionException {
		TermContext _localctx = new TermContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_term);
		try {
			setState(37);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case Number:
				_localctx = new NUMBERContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(32);
				match(Number);
				}
				break;
			case OpenParen:
				_localctx = new NESTED_EXPRContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(33);
				match(OpenParen);
				setState(34);
				expression();
				setState(35);
				match(CloseParen);
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

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\13*\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\4\5\t\5\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3\26"+
		"\n\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4!\n\4\3\5\3\5\3\5\3\5\3\5"+
		"\5\5(\n\5\3\5\2\2\6\2\4\6\b\2\2\2*\2\n\3\2\2\2\4\25\3\2\2\2\6 \3\2\2\2"+
		"\b\'\3\2\2\2\n\13\5\4\3\2\13\3\3\2\2\2\f\26\5\6\4\2\r\16\5\6\4\2\16\17"+
		"\7\6\2\2\17\20\5\6\4\2\20\26\3\2\2\2\21\22\5\6\4\2\22\23\7\7\2\2\23\24"+
		"\5\6\4\2\24\26\3\2\2\2\25\f\3\2\2\2\25\r\3\2\2\2\25\21\3\2\2\2\26\5\3"+
		"\2\2\2\27!\5\b\5\2\30\31\5\b\5\2\31\32\7\b\2\2\32\33\5\b\5\2\33!\3\2\2"+
		"\2\34\35\5\b\5\2\35\36\7\t\2\2\36\37\5\b\5\2\37!\3\2\2\2 \27\3\2\2\2 "+
		"\30\3\2\2\2 \34\3\2\2\2!\7\3\2\2\2\"(\7\3\2\2#$\7\n\2\2$%\5\2\2\2%&\7"+
		"\13\2\2&(\3\2\2\2\'\"\3\2\2\2\'#\3\2\2\2(\t\3\2\2\2\5\25 \'";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}