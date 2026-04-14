package pl.pwr.miasi;

import grammar.CircuitGrammarBaseVisitor;
import grammar.CircuitGrammarParser;
import org.stringtemplate.v4.ST;
import org.stringtemplate.v4.STGroup;
import org.stringtemplate.v4.STGroupFile;

import java.util.*;

public class CircuitVisitor extends CircuitGrammarBaseVisitor<ST> {
    private final STGroup stGroup;

    private List<ST> currentElements;
    private List<ST> currentConnections;
    private Map<String, Integer> gateCounters;
    private final List<ST> componentDefinitions = new ArrayList<>();
    private ST mainComponent = null;

    private Set<String> definedIds;
    public static class SemanticException extends RuntimeException {
        public SemanticException(String message) {
            super(message);
        }
    }

    public CircuitVisitor() {
        this.stGroup = new STGroupFile(Objects.requireNonNull(getClass().getClassLoader().getResource("circuit.stg")));
    }

    @Override
    public ST visitProgram(CircuitGrammarParser.ProgramContext ctx) {
        for (CircuitGrammarParser.Component_definitionContext compCtx : ctx.component_definition()) {
            visit(compCtx);
        }

        if (ctx.main_component() != null) {
            visit(ctx.main_component());
        }

        ST jsonST = stGroup.getInstanceOf("json");
        jsonST.add("componentsMap", componentDefinitions);
        jsonST.add("mainComp", mainComponent);

        return jsonST;
    }

    @Override
    public ST visitMain_component(CircuitGrammarParser.Main_componentContext ctx) {
        currentElements = new ArrayList<>();
        currentConnections = new ArrayList<>();
        gateCounters = new HashMap<>();
        definedIds = new HashSet<>();

        CircuitGrammarParser.Component_definitionContext compDef = ctx.component_definition();
        for (var in : compDef.input_declaration()) visit(in);
        for (var out : compDef.output_declaration()) visit(out);
        visit(compDef.block());

        ST compST = stGroup.getInstanceOf("component");
        compST.add("elements", currentElements);
        compST.add("connections", currentConnections);
        mainComponent = compST;

        return null;
    }

    @Override
    public ST visitComponent_definition(CircuitGrammarParser.Component_definitionContext ctx) {
        currentElements = new ArrayList<>();
        currentConnections = new ArrayList<>();
        gateCounters = new HashMap<>();
        definedIds = new HashSet<>();

        String compName = ctx.name.getText();

        for (var in : ctx.input_declaration()) visit(in);
        for (var out : ctx.output_declaration()) visit(out);
        visit(ctx.block());

        ST compST = stGroup.getInstanceOf("component");
        compST.add("elements", currentElements);
        compST.add("connections", currentConnections);

        ST dictEntry = stGroup.getInstanceOf("componentEntry");
        dictEntry.add("name", compName);
        dictEntry.add("comp", compST);

        componentDefinitions.add(dictEntry);

        return null;
    }

    @Override
    public ST visitInput_declaration(CircuitGrammarParser.Input_declarationContext ctx) {
        String name = ctx.ID().getText();
        definedIds.add(name);

        ST el = stGroup.getInstanceOf("element");
        el.add("type", "INPUT");
        el.add("name", name);
        currentElements.add(el);
        return null;
    }

    @Override
    public ST visitOutput_declaration(CircuitGrammarParser.Output_declarationContext ctx) {
        String name = ctx.ID().getText();
        definedIds.add(name);

        ST el = stGroup.getInstanceOf("element");
        el.add("type", "OUTPUT");
        el.add("name", name);
        currentElements.add(el);
        return null;
    }

    @Override
    public ST visitSignal_definition(CircuitGrammarParser.Signal_definitionContext ctx) {
        String name = ctx.ID().getText();

        ST el = stGroup.getInstanceOf("element");
        el.add("type", "SIGNAL");
        el.add("name", name);
        currentElements.add(el);

        ST exprNodeST = visit(ctx.expression());
        definedIds.add(name);

        addConnection(exprNodeST.render(), name);

        return null;
    }

    @Override
    public ST visitComponent_instance(CircuitGrammarParser.Component_instanceContext ctx) {
        String compType = ctx.comp_name.getText();
        String instanceName = ctx.instance_name.getText();
        definedIds.add(instanceName);

        ST el = stGroup.getInstanceOf("element");
        el.add("type", compType);
        el.add("name", instanceName);
        currentElements.add(el);

        for (int i = 2; i < ctx.ID().size(); i++) {
            String inputName = ctx.ID(i).getText();
            ST exprNodeST = visit(ctx.expression(i - 2));
            addConnection(exprNodeST.render(), instanceName + "." + inputName);
        }
        return null;
    }

    @Override
    public ST visitAssignment(CircuitGrammarParser.AssignmentContext ctx) {
        String target = ctx.input.getText();
        checkExists(target);

        ST exprNodeST = visit(ctx.expression());
        addConnection(exprNodeST.render(), target);
        return null;
    }

    @Override
    public ST visitParenth_exp(CircuitGrammarParser.Parenth_expContext ctx) {
        return visit(ctx.expression());
    }

    @Override
    public ST visitNot_exp(CircuitGrammarParser.Not_expContext ctx) {
        String gateName = addGate("NOT");
        ST innerNodeST = visit(ctx.expression());
        addConnection(innerNodeST.render(), gateName);
        return createSignalST(gateName);
    }

    @Override
    public ST visitBi_exp(CircuitGrammarParser.Bi_expContext ctx) {
        String op = "UNKNOWN";
        if (ctx.AND() != null) op = "AND";
        else if (ctx.OR() != null) op = "OR";
        else if (ctx.XOR() != null) op = "XOR";
        else if (ctx.NAND() != null) op = "NAND";
        else if (ctx.NOR() != null) op = "NOR";
        else if (ctx.XNOR() != null) op = "XNOR";

        String gateName = addGate(op);
        ST leftNodeST = visit(ctx.l);
        ST rightNodeST = visit(ctx.r);

        addConnection(leftNodeST.render(), gateName);
        addConnection(rightNodeST.render(), gateName);

        return createSignalST(gateName);
    }

    @Override
    public ST visitBool_exp(CircuitGrammarParser.Bool_expContext ctx) {
        return createSignalST(ctx.BOOL().getText());
    }

    @Override
    public ST visitComp_out_exp(CircuitGrammarParser.Comp_out_expContext ctx) {
        checkExists(ctx.c_name.getText());
        return createSignalST(ctx.c_name.getText() + "." + ctx.c_out.getText());    }

    @Override
    public ST visitId_exp(CircuitGrammarParser.Id_expContext ctx) {
        String id = ctx.ID().getText();
        checkExists(id);
        return createSignalST(id);
    }

    private String addGate(String type) {
        int count = gateCounters.getOrDefault(type, 1);
        gateCounters.put(type, count + 1);
        String name = type.toLowerCase() + count;

        ST el = stGroup.getInstanceOf("element");
        el.add("type", type.toUpperCase());
        el.add("name", name);
        currentElements.add(el);

        definedIds.add(name);
        return name;
    }

    private void addConnection(String from, String to) {
        ST conn = stGroup.getInstanceOf("connection");
        conn.add("from", from);
        conn.add("to", to);
        currentConnections.add(conn);
    }

    private ST createSignalST(String name) {
        ST st = stGroup.getInstanceOf("signal");
        st.add("name", name);
        return st;
    }

    private void checkExists(String id) {
        if (!definedIds.contains(id)) {
            throw new SemanticException("Użycie niezdefiniowanego identyfikatora: " + id);
        }
    }
}