package pl.pwr.miasi;

import grammar.CircuitGrammarLexer;
import grammar.CircuitGrammarParser;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import java.io.IOException;

public class VisitorInitializer {
    public static void initialize(String program) throws IOException {
//        CharStream input = CharStreams.fromString(program);
        CharStream input = CharStreams.fromFileName("example.ls");    // for testing

        CircuitGrammarLexer lexer = new CircuitGrammarLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        CircuitGrammarParser parser = new CircuitGrammarParser(tokens);
        ParseTree tree = parser.program();

        CircuitVisitor visitor = new CircuitVisitor();
    }
}