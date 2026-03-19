package pl.pwr.miasi;

import grammar.CircuitGrammarBaseVisitor;
import grammar.CircuitGrammarParser;

public class CircuitVisitor extends CircuitGrammarBaseVisitor<Boolean> {
    @Override
    public Boolean visitProgram(CircuitGrammarParser.ProgramContext ctx) {
        this.visit(ctx.main_component());

        return null;
    }

    @Override
    public Boolean visitMain_component(CircuitGrammarParser.Main_componentContext ctx) {
        return null;
    }
}
