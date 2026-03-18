grammar CircuitGrammar;

LPARENTH : '(' ;
RPARENTH : ')' ;

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
ID : [a-z]+ ;
WS : [ \t\r\n] -> skip ;

program
    : (statement)+ EOF
    | EOF
    ;

block
    : LCPARENTH (statement)* RCPARENTH
    ;

statement
    : 'fun' ID LPARENTH (ID (',' ID)*)? RPARENTH block      #function_declaration
    | ID LPARENTH (expression (',' expression)*)? RPARENTH  #function_use
    | 'print' LPARENTH expression RPARENTH                  #print
    | 'if' LPARENTH expression RPARENTH block               #if_statement
    | 'while' LPARENTH expression RPARENTH block            #while_loop
    | 'do' block 'while' expression                         #do_while_loop
    | 'for' LPARENTH (ID EQ expression (',' ID EQ expression)*)? SEMI condition=expression SEMI (ID EQ expression (',' ID EQ expression)*)? RPARENTH block #for_loop
    | BREAK                                                 #break
    | CONTINUE                                              #continue
    | ID EQ expression                                      #assignment
    | VAR ID (EQ value=expression)?                         #declaration
    | block                                                 #block_statement
    ;

expression
    : LPARENTH expression RPARENTH
    | MINUS expression
    | l=expression (MULTIPLY|DIVIDE) r=expression
    | l=expression (PLUS|MINUS) r=expression
    | NOT expression
    | l=expression (AND|OR|IS_E|IS_M|IS_ME|IS_L|IS_LE) r=expression
    | NUMBER
    | ID
    ;
