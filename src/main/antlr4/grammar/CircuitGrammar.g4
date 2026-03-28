grammar CircuitGrammar;

LPARENTH : '(' ;
RPARENTH : ')' ;
LCPARENTH : '{' ;
RCPARENTH : '}' ;

NOT : 'not' ;
AND : 'and' ;
OR : 'or' ;
XOR : 'xor' ;
NAND : 'nand' ;
NOR : 'nor' ;
XNOR : 'xnor' ;

EQ : '=' ;
SEMI : ';' ;

BOOL : [0-1] ;
ID : [a-zA-Z_][a-zA-Z_0-9]* ;
WS : [ \t\r\n] -> skip ;

program
    : (component_definition)* main_component EOF
    | EOF
    ;

block
    : LCPARENTH (statement)* RCPARENTH
    ;

main_component
    : 'main' component_definition
    ;

component_definition
    : 'component' name=ID LPARENTH (input_declaration)+ (output_declaration)+ RPARENTH block
    ;

statement
    : component_instance        #dummy
    | input=ID EQ expression    #assignment
    | signal_definition         #dummy
    ;

input_declaration
    : 'input' ID
    ;

output_declaration
    : 'output' ID
    ;

signal_definition
    : 'signal' ID EQ expression
    ;

component_instance
    : 'component' instance_name=ID EQ comp_name=ID LPARENTH (ID EQ expression)+ RPARENTH
    ;

expression
    : LPARENTH expression RPARENTH                           #parenth_exp
    | NOT expression                                         #not_exp
    | l=expression (AND|OR|XOR|XNOR|NAND|NOR) r=expression   #bi_exp
    | BOOL                                                   #bool_exp
    | c_name=ID '.' c_out=ID                                 #comp_out_exp
    | ID                                                     #id_exp
    ;
