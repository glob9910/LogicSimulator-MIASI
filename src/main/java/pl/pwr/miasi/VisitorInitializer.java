package pl.pwr.miasi;

import grammar.CircuitGrammarLexer;
import grammar.CircuitGrammarParser;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class VisitorInitializer {
    public String initialize(String program) {
        CircuitGrammarLexer lexer = new CircuitGrammarLexer(CharStreams.fromString(program));
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        CircuitGrammarParser parser = new CircuitGrammarParser(tokens);

        DescriptiveErrorListener errorListener = new DescriptiveErrorListener();
        lexer.removeErrorListeners();
        parser.removeErrorListeners();
        lexer.addErrorListener(errorListener);
        parser.addErrorListener(errorListener);

        CircuitGrammarParser.ProgramContext tree = parser.program();

        if (errorListener.hasErrors()) {
            return formatErrorJson(errorListener.getFullErrorMessage());
        }

        try {
            CircuitVisitor visitor = new CircuitVisitor();
            return visitor.visit(tree).render();
        } catch (CircuitVisitor.SemanticException e) {
            return formatErrorJson("Błąd logiczny: " + e.getMessage());
        } catch (Exception e) {
            return formatErrorJson("Niezdefiniowany błąd: " + e.getMessage());
        }
    }

    private String formatErrorJson(String message) {
        String escaped = message.replace("\"", "\\\"").replace("\n", "\\n");
        return "{\"error\": \"" + escaped + "\"}";
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