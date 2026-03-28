package pl.pwr.miasi;

import grammar.CircuitGrammarLexer;
import grammar.CircuitGrammarParser;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import org.stringtemplate.v4.ST;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class VisitorInitializer {
    public String initialize(String program) {
        CharStream input = CharStreams.fromString(program);

        CircuitGrammarLexer lexer = new CircuitGrammarLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        CircuitGrammarParser parser = new CircuitGrammarParser(tokens);
        ParseTree tree = parser.program();

        CircuitVisitor visitor = new CircuitVisitor();
        ST res = visitor.visit(tree);

        return res.render();
    }

    // for testing
    public static void main(String[] args) throws IOException {
        VisitorInitializer testInitializer = new VisitorInitializer();
        String testProgram = Files.readString(Path.of("example.ls"));

        try {
            Files.writeString(Path.of("wy.json"), testInitializer.initialize(testProgram));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}