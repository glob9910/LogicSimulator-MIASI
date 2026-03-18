// Generated from /home/kamila/IdeaProjects/LogicSimulator/src/main/antlr/CircuitGrammar.g4 by ANTLR 4.13.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class CircuitGrammarParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, LPARENTH=7, RPARENTH=8, 
		LCPARENTH=9, RCPARENTH=10, NOT=11, AND=12, OR=13, XOR=14, NAND=15, NOR=16, 
		XNOR=17, EQ=18, SEMI=19, BOOL=20, ID=21, WS=22;
	public static final int
		RULE_program = 0, RULE_block = 1, RULE_main_component = 2, RULE_component_definition = 3, 
		RULE_statement = 4, RULE_input_declaration = 5, RULE_output_declaration = 6, 
		RULE_signal_definition = 7, RULE_component_instance = 8, RULE_expression = 9;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "block", "main_component", "component_definition", "statement", 
			"input_declaration", "output_declaration", "signal_definition", "component_instance", 
			"expression"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'main'", "'component'", "'input'", "'output'", "'signal'", "'.'", 
			"'('", "')'", "'{'", "'}'", "'not'", "'and'", "'or'", "'xor'", "'nand'", 
			"'nor'", "'xnor'", "'='", "';'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, "LPARENTH", "RPARENTH", "LCPARENTH", 
			"RCPARENTH", "NOT", "AND", "OR", "XOR", "NAND", "NOR", "XNOR", "EQ", 
			"SEMI", "BOOL", "ID", "WS"
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
	public String getGrammarFileName() { return "CircuitGrammar.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public CircuitGrammarParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public Main_componentContext main_component() {
			return getRuleContext(Main_componentContext.class,0);
		}
		public TerminalNode EOF() { return getToken(CircuitGrammarParser.EOF, 0); }
		public List<Component_definitionContext> component_definition() {
			return getRuleContexts(Component_definitionContext.class);
		}
		public Component_definitionContext component_definition(int i) {
			return getRuleContext(Component_definitionContext.class,i);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitProgram(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		int _la;
		try {
			setState(30);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__0:
			case T__1:
				enterOuterAlt(_localctx, 1);
				{
				setState(23);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__1) {
					{
					{
					setState(20);
					component_definition();
					}
					}
					setState(25);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(26);
				main_component();
				setState(27);
				match(EOF);
				}
				break;
			case EOF:
				enterOuterAlt(_localctx, 2);
				{
				setState(29);
				match(EOF);
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

	@SuppressWarnings("CheckReturnValue")
	public static class BlockContext extends ParserRuleContext {
		public TerminalNode LCPARENTH() { return getToken(CircuitGrammarParser.LCPARENTH, 0); }
		public TerminalNode RCPARENTH() { return getToken(CircuitGrammarParser.RCPARENTH, 0); }
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public BlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_block; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitBlock(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BlockContext block() throws RecognitionException {
		BlockContext _localctx = new BlockContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_block);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(32);
			match(LCPARENTH);
			setState(36);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 2097188L) != 0)) {
				{
				{
				setState(33);
				statement();
				}
				}
				setState(38);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(39);
			match(RCPARENTH);
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

	@SuppressWarnings("CheckReturnValue")
	public static class Main_componentContext extends ParserRuleContext {
		public Component_definitionContext component_definition() {
			return getRuleContext(Component_definitionContext.class,0);
		}
		public Main_componentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_main_component; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitMain_component(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Main_componentContext main_component() throws RecognitionException {
		Main_componentContext _localctx = new Main_componentContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_main_component);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(41);
			match(T__0);
			setState(42);
			component_definition();
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

	@SuppressWarnings("CheckReturnValue")
	public static class Component_definitionContext extends ParserRuleContext {
		public Token name;
		public TerminalNode LPARENTH() { return getToken(CircuitGrammarParser.LPARENTH, 0); }
		public TerminalNode RPARENTH() { return getToken(CircuitGrammarParser.RPARENTH, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public TerminalNode ID() { return getToken(CircuitGrammarParser.ID, 0); }
		public List<Input_declarationContext> input_declaration() {
			return getRuleContexts(Input_declarationContext.class);
		}
		public Input_declarationContext input_declaration(int i) {
			return getRuleContext(Input_declarationContext.class,i);
		}
		public List<Output_declarationContext> output_declaration() {
			return getRuleContexts(Output_declarationContext.class);
		}
		public Output_declarationContext output_declaration(int i) {
			return getRuleContext(Output_declarationContext.class,i);
		}
		public Component_definitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_component_definition; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitComponent_definition(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Component_definitionContext component_definition() throws RecognitionException {
		Component_definitionContext _localctx = new Component_definitionContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_component_definition);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(44);
			match(T__1);
			setState(45);
			((Component_definitionContext)_localctx).name = match(ID);
			setState(46);
			match(LPARENTH);
			setState(48); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(47);
				input_declaration();
				}
				}
				setState(50); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==T__2 );
			setState(53); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(52);
				output_declaration();
				}
				}
				setState(55); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==T__3 );
			setState(57);
			match(RPARENTH);
			setState(58);
			block();
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

	@SuppressWarnings("CheckReturnValue")
	public static class StatementContext extends ParserRuleContext {
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
	 
		public StatementContext() { }
		public void copyFrom(StatementContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DummyContext extends StatementContext {
		public Component_instanceContext component_instance() {
			return getRuleContext(Component_instanceContext.class,0);
		}
		public Signal_definitionContext signal_definition() {
			return getRuleContext(Signal_definitionContext.class,0);
		}
		public DummyContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitDummy(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AssignmentContext extends StatementContext {
		public Token input;
		public TerminalNode EQ() { return getToken(CircuitGrammarParser.EQ, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode ID() { return getToken(CircuitGrammarParser.ID, 0); }
		public AssignmentContext(StatementContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitAssignment(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_statement);
		try {
			setState(65);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__1:
				_localctx = new DummyContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(60);
				component_instance();
				}
				break;
			case ID:
				_localctx = new AssignmentContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(61);
				((AssignmentContext)_localctx).input = match(ID);
				setState(62);
				match(EQ);
				setState(63);
				expression(0);
				}
				break;
			case T__4:
				_localctx = new DummyContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(64);
				signal_definition();
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

	@SuppressWarnings("CheckReturnValue")
	public static class Input_declarationContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(CircuitGrammarParser.ID, 0); }
		public Input_declarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_input_declaration; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitInput_declaration(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Input_declarationContext input_declaration() throws RecognitionException {
		Input_declarationContext _localctx = new Input_declarationContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_input_declaration);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(67);
			match(T__2);
			setState(68);
			match(ID);
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

	@SuppressWarnings("CheckReturnValue")
	public static class Output_declarationContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(CircuitGrammarParser.ID, 0); }
		public Output_declarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_output_declaration; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitOutput_declaration(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Output_declarationContext output_declaration() throws RecognitionException {
		Output_declarationContext _localctx = new Output_declarationContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_output_declaration);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(70);
			match(T__3);
			setState(71);
			match(ID);
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

	@SuppressWarnings("CheckReturnValue")
	public static class Signal_definitionContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(CircuitGrammarParser.ID, 0); }
		public TerminalNode EQ() { return getToken(CircuitGrammarParser.EQ, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public Signal_definitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_signal_definition; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitSignal_definition(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Signal_definitionContext signal_definition() throws RecognitionException {
		Signal_definitionContext _localctx = new Signal_definitionContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_signal_definition);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(73);
			match(T__4);
			setState(74);
			match(ID);
			setState(75);
			match(EQ);
			setState(76);
			expression(0);
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

	@SuppressWarnings("CheckReturnValue")
	public static class Component_instanceContext extends ParserRuleContext {
		public Token instance_name;
		public Token comp_name;
		public Token input;
		public List<TerminalNode> EQ() { return getTokens(CircuitGrammarParser.EQ); }
		public TerminalNode EQ(int i) {
			return getToken(CircuitGrammarParser.EQ, i);
		}
		public TerminalNode LPARENTH() { return getToken(CircuitGrammarParser.LPARENTH, 0); }
		public TerminalNode RPARENTH() { return getToken(CircuitGrammarParser.RPARENTH, 0); }
		public List<TerminalNode> ID() { return getTokens(CircuitGrammarParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(CircuitGrammarParser.ID, i);
		}
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public Component_instanceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_component_instance; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitComponent_instance(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Component_instanceContext component_instance() throws RecognitionException {
		Component_instanceContext _localctx = new Component_instanceContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_component_instance);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(78);
			match(T__1);
			setState(79);
			((Component_instanceContext)_localctx).instance_name = match(ID);
			setState(80);
			match(EQ);
			setState(81);
			((Component_instanceContext)_localctx).comp_name = match(ID);
			setState(82);
			match(LPARENTH);
			setState(86); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(83);
				((Component_instanceContext)_localctx).input = match(ID);
				setState(84);
				match(EQ);
				setState(85);
				expression(0);
				}
				}
				setState(88); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==ID );
			setState(90);
			match(RPARENTH);
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

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressionContext extends ParserRuleContext {
		public ExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expression; }
	 
		public ExpressionContext() { }
		public void copyFrom(ExpressionContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Parenth_expContext extends ExpressionContext {
		public TerminalNode LPARENTH() { return getToken(CircuitGrammarParser.LPARENTH, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode RPARENTH() { return getToken(CircuitGrammarParser.RPARENTH, 0); }
		public Parenth_expContext(ExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitParenth_exp(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Not_expContext extends ExpressionContext {
		public TerminalNode NOT() { return getToken(CircuitGrammarParser.NOT, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public Not_expContext(ExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitNot_exp(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Bool_expContext extends ExpressionContext {
		public TerminalNode BOOL() { return getToken(CircuitGrammarParser.BOOL, 0); }
		public Bool_expContext(ExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitBool_exp(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Comp_out_expContext extends ExpressionContext {
		public Token c_name;
		public Token c_out;
		public List<TerminalNode> ID() { return getTokens(CircuitGrammarParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(CircuitGrammarParser.ID, i);
		}
		public Comp_out_expContext(ExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitComp_out_exp(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class And_or_expContext extends ExpressionContext {
		public ExpressionContext l;
		public ExpressionContext r;
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode AND() { return getToken(CircuitGrammarParser.AND, 0); }
		public TerminalNode OR() { return getToken(CircuitGrammarParser.OR, 0); }
		public And_or_expContext(ExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitAnd_or_exp(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Id_expd_expContext extends ExpressionContext {
		public TerminalNode ID() { return getToken(CircuitGrammarParser.ID, 0); }
		public Id_expd_expContext(ExpressionContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof CircuitGrammarVisitor ) return ((CircuitGrammarVisitor<? extends T>)visitor).visitId_expd_exp(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ExpressionContext expression() throws RecognitionException {
		return expression(0);
	}

	private ExpressionContext expression(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExpressionContext _localctx = new ExpressionContext(_ctx, _parentState);
		ExpressionContext _prevctx = _localctx;
		int _startState = 18;
		enterRecursionRule(_localctx, 18, RULE_expression, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(104);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,7,_ctx) ) {
			case 1:
				{
				_localctx = new Parenth_expContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(93);
				match(LPARENTH);
				setState(94);
				expression(0);
				setState(95);
				match(RPARENTH);
				}
				break;
			case 2:
				{
				_localctx = new Not_expContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(97);
				match(NOT);
				setState(98);
				expression(5);
				}
				break;
			case 3:
				{
				_localctx = new Bool_expContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(99);
				match(BOOL);
				}
				break;
			case 4:
				{
				_localctx = new Comp_out_expContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(100);
				((Comp_out_expContext)_localctx).c_name = match(ID);
				setState(101);
				match(T__5);
				setState(102);
				((Comp_out_expContext)_localctx).c_out = match(ID);
				}
				break;
			case 5:
				{
				_localctx = new Id_expd_expContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(103);
				match(ID);
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(111);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,8,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new And_or_expContext(new ExpressionContext(_parentctx, _parentState));
					((And_or_expContext)_localctx).l = _prevctx;
					pushNewRecursionContext(_localctx, _startState, RULE_expression);
					setState(106);
					if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
					setState(107);
					_la = _input.LA(1);
					if ( !(_la==AND || _la==OR) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(108);
					((And_or_expContext)_localctx).r = expression(5);
					}
					} 
				}
				setState(113);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,8,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 9:
			return expression_sempred((ExpressionContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean expression_sempred(ExpressionContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 4);
		}
		return true;
	}

	public static final String _serializedATN =
		"\u0004\u0001\u0016s\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0001\u0000\u0005\u0000\u0016\b\u0000\n\u0000"+
		"\f\u0000\u0019\t\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000"+
		"\u0003\u0000\u001f\b\u0000\u0001\u0001\u0001\u0001\u0005\u0001#\b\u0001"+
		"\n\u0001\f\u0001&\t\u0001\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0004\u0003"+
		"1\b\u0003\u000b\u0003\f\u00032\u0001\u0003\u0004\u00036\b\u0003\u000b"+
		"\u0003\f\u00037\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0003\u0004B\b\u0004\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0006\u0001\u0006\u0001\u0006\u0001"+
		"\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0001\b\u0001\b"+
		"\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0004\bW\b\b\u000b\b"+
		"\f\bX\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t"+
		"\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0003\ti\b\t\u0001\t"+
		"\u0001\t\u0001\t\u0005\tn\b\t\n\t\f\tq\t\t\u0001\t\u0000\u0001\u0012\n"+
		"\u0000\u0002\u0004\u0006\b\n\f\u000e\u0010\u0012\u0000\u0001\u0001\u0000"+
		"\f\ru\u0000\u001e\u0001\u0000\u0000\u0000\u0002 \u0001\u0000\u0000\u0000"+
		"\u0004)\u0001\u0000\u0000\u0000\u0006,\u0001\u0000\u0000\u0000\bA\u0001"+
		"\u0000\u0000\u0000\nC\u0001\u0000\u0000\u0000\fF\u0001\u0000\u0000\u0000"+
		"\u000eI\u0001\u0000\u0000\u0000\u0010N\u0001\u0000\u0000\u0000\u0012h"+
		"\u0001\u0000\u0000\u0000\u0014\u0016\u0003\u0006\u0003\u0000\u0015\u0014"+
		"\u0001\u0000\u0000\u0000\u0016\u0019\u0001\u0000\u0000\u0000\u0017\u0015"+
		"\u0001\u0000\u0000\u0000\u0017\u0018\u0001\u0000\u0000\u0000\u0018\u001a"+
		"\u0001\u0000\u0000\u0000\u0019\u0017\u0001\u0000\u0000\u0000\u001a\u001b"+
		"\u0003\u0004\u0002\u0000\u001b\u001c\u0005\u0000\u0000\u0001\u001c\u001f"+
		"\u0001\u0000\u0000\u0000\u001d\u001f\u0005\u0000\u0000\u0001\u001e\u0017"+
		"\u0001\u0000\u0000\u0000\u001e\u001d\u0001\u0000\u0000\u0000\u001f\u0001"+
		"\u0001\u0000\u0000\u0000 $\u0005\t\u0000\u0000!#\u0003\b\u0004\u0000\""+
		"!\u0001\u0000\u0000\u0000#&\u0001\u0000\u0000\u0000$\"\u0001\u0000\u0000"+
		"\u0000$%\u0001\u0000\u0000\u0000%\'\u0001\u0000\u0000\u0000&$\u0001\u0000"+
		"\u0000\u0000\'(\u0005\n\u0000\u0000(\u0003\u0001\u0000\u0000\u0000)*\u0005"+
		"\u0001\u0000\u0000*+\u0003\u0006\u0003\u0000+\u0005\u0001\u0000\u0000"+
		"\u0000,-\u0005\u0002\u0000\u0000-.\u0005\u0015\u0000\u0000.0\u0005\u0007"+
		"\u0000\u0000/1\u0003\n\u0005\u00000/\u0001\u0000\u0000\u000012\u0001\u0000"+
		"\u0000\u000020\u0001\u0000\u0000\u000023\u0001\u0000\u0000\u000035\u0001"+
		"\u0000\u0000\u000046\u0003\f\u0006\u000054\u0001\u0000\u0000\u000067\u0001"+
		"\u0000\u0000\u000075\u0001\u0000\u0000\u000078\u0001\u0000\u0000\u0000"+
		"89\u0001\u0000\u0000\u00009:\u0005\b\u0000\u0000:;\u0003\u0002\u0001\u0000"+
		";\u0007\u0001\u0000\u0000\u0000<B\u0003\u0010\b\u0000=>\u0005\u0015\u0000"+
		"\u0000>?\u0005\u0012\u0000\u0000?B\u0003\u0012\t\u0000@B\u0003\u000e\u0007"+
		"\u0000A<\u0001\u0000\u0000\u0000A=\u0001\u0000\u0000\u0000A@\u0001\u0000"+
		"\u0000\u0000B\t\u0001\u0000\u0000\u0000CD\u0005\u0003\u0000\u0000DE\u0005"+
		"\u0015\u0000\u0000E\u000b\u0001\u0000\u0000\u0000FG\u0005\u0004\u0000"+
		"\u0000GH\u0005\u0015\u0000\u0000H\r\u0001\u0000\u0000\u0000IJ\u0005\u0005"+
		"\u0000\u0000JK\u0005\u0015\u0000\u0000KL\u0005\u0012\u0000\u0000LM\u0003"+
		"\u0012\t\u0000M\u000f\u0001\u0000\u0000\u0000NO\u0005\u0002\u0000\u0000"+
		"OP\u0005\u0015\u0000\u0000PQ\u0005\u0012\u0000\u0000QR\u0005\u0015\u0000"+
		"\u0000RV\u0005\u0007\u0000\u0000ST\u0005\u0015\u0000\u0000TU\u0005\u0012"+
		"\u0000\u0000UW\u0003\u0012\t\u0000VS\u0001\u0000\u0000\u0000WX\u0001\u0000"+
		"\u0000\u0000XV\u0001\u0000\u0000\u0000XY\u0001\u0000\u0000\u0000YZ\u0001"+
		"\u0000\u0000\u0000Z[\u0005\b\u0000\u0000[\u0011\u0001\u0000\u0000\u0000"+
		"\\]\u0006\t\uffff\uffff\u0000]^\u0005\u0007\u0000\u0000^_\u0003\u0012"+
		"\t\u0000_`\u0005\b\u0000\u0000`i\u0001\u0000\u0000\u0000ab\u0005\u000b"+
		"\u0000\u0000bi\u0003\u0012\t\u0005ci\u0005\u0014\u0000\u0000de\u0005\u0015"+
		"\u0000\u0000ef\u0005\u0006\u0000\u0000fi\u0005\u0015\u0000\u0000gi\u0005"+
		"\u0015\u0000\u0000h\\\u0001\u0000\u0000\u0000ha\u0001\u0000\u0000\u0000"+
		"hc\u0001\u0000\u0000\u0000hd\u0001\u0000\u0000\u0000hg\u0001\u0000\u0000"+
		"\u0000io\u0001\u0000\u0000\u0000jk\n\u0004\u0000\u0000kl\u0007\u0000\u0000"+
		"\u0000ln\u0003\u0012\t\u0005mj\u0001\u0000\u0000\u0000nq\u0001\u0000\u0000"+
		"\u0000om\u0001\u0000\u0000\u0000op\u0001\u0000\u0000\u0000p\u0013\u0001"+
		"\u0000\u0000\u0000qo\u0001\u0000\u0000\u0000\t\u0017\u001e$27AXho";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}