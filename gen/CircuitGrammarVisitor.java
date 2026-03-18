// Generated from /home/kamila/IdeaProjects/LogicSimulator/src/main/antlr/CircuitGrammar.g4 by ANTLR 4.13.2
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link CircuitGrammarParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface CircuitGrammarVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link CircuitGrammarParser#program}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProgram(CircuitGrammarParser.ProgramContext ctx);
	/**
	 * Visit a parse tree produced by {@link CircuitGrammarParser#block}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock(CircuitGrammarParser.BlockContext ctx);
	/**
	 * Visit a parse tree produced by {@link CircuitGrammarParser#main_component}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMain_component(CircuitGrammarParser.Main_componentContext ctx);
	/**
	 * Visit a parse tree produced by {@link CircuitGrammarParser#component_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComponent_definition(CircuitGrammarParser.Component_definitionContext ctx);
	/**
	 * Visit a parse tree produced by the {@code dummy}
	 * labeled alternative in {@link CircuitGrammarParser#statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDummy(CircuitGrammarParser.DummyContext ctx);
	/**
	 * Visit a parse tree produced by the {@code assignment}
	 * labeled alternative in {@link CircuitGrammarParser#statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssignment(CircuitGrammarParser.AssignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link CircuitGrammarParser#input_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInput_declaration(CircuitGrammarParser.Input_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link CircuitGrammarParser#output_declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOutput_declaration(CircuitGrammarParser.Output_declarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link CircuitGrammarParser#signal_definition}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSignal_definition(CircuitGrammarParser.Signal_definitionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CircuitGrammarParser#component_instance}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComponent_instance(CircuitGrammarParser.Component_instanceContext ctx);
	/**
	 * Visit a parse tree produced by the {@code parenth_exp}
	 * labeled alternative in {@link CircuitGrammarParser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParenth_exp(CircuitGrammarParser.Parenth_expContext ctx);
	/**
	 * Visit a parse tree produced by the {@code not_exp}
	 * labeled alternative in {@link CircuitGrammarParser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNot_exp(CircuitGrammarParser.Not_expContext ctx);
	/**
	 * Visit a parse tree produced by the {@code bool_exp}
	 * labeled alternative in {@link CircuitGrammarParser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBool_exp(CircuitGrammarParser.Bool_expContext ctx);
	/**
	 * Visit a parse tree produced by the {@code comp_out_exp}
	 * labeled alternative in {@link CircuitGrammarParser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComp_out_exp(CircuitGrammarParser.Comp_out_expContext ctx);
	/**
	 * Visit a parse tree produced by the {@code and_or_exp}
	 * labeled alternative in {@link CircuitGrammarParser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAnd_or_exp(CircuitGrammarParser.And_or_expContext ctx);
	/**
	 * Visit a parse tree produced by the {@code id_expd_exp}
	 * labeled alternative in {@link CircuitGrammarParser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitId_expd_exp(CircuitGrammarParser.Id_expd_expContext ctx);
}