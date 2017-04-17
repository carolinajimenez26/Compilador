# goparser.py
# -*- coding: utf-8 -*-


# ----------------------------------------------------------------------
# Los parsers son definidos usando el módulo yacc de PLY
#
# Vea http://www.dabeaz.com/ply/ply.html#ply_nn23
# ----------------------------------------------------------------------
from ply import yacc

# ----------------------------------------------------------------------
# El siguiente import carga la funcion error(lineno, msg) que debe ser
# usada para reportar todos los mensajes de error generados por su parser.
# Las pruebas Unitarias y otras caracteristicas del compilador se basaran
# en esta función.  vea el archivo errors.py para una mayor documentación
# acerca del mecanismo de manejo de errores.
from errors import error

# ----------------------------------------------------------------------
# Obtener la lista de token definidos en el módulo lexer.  Esto es
# necesario con el fin de validar y construir la tabla de sintaxis.
from golex import tokens

# ----------------------------------------------------------------------
# Obtener los nodos del AST.
# Lea las instrucciones en hocast.py
from goast import *

# ----------------------------------------------------------------------
# Tabla de precedencia de operadores.  Los operadores deben de seguir
# las mismas reglas de precedencia que Python.  Instrucciones que se
# dan el el proyecto.
# Vea http://www.dabeaz.com/ply/ply.html#ply_nn27

precedence = (
    ('right', 'ASSIGN', 'POSITIVEINCREASE','NEGATIVEINCREASE', 'MULTIPLIINCREASE', 'DIVIDEINCREASE', 'EVADETYPEDECLAR'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'LNOT'),
    ('nonassoc', 'LT', 'LE', 'EQ', 'GT', 'GE', 'NE'),
    ('left', 'PLUS', 'MINUS', 'OR'),
    ('left', 'TIMES', 'DIVIDE', 'RESIDUE', 'AND', 'COMMA'),
    # Operador ficticio para mantener la mas alta prioridad
    ('left', 'UNARY', 'INCREASE', 'DECREMENT', 'LPAREN', 'LBRACE', 'RETURN'),
    ('right', 'RBRACE', 'RPAREN'    ),
)

def p_program(p):
    '''
    program : statements
            | empty
    '''
    p[0] = Program(p[1])

def p_statements(p):
    '''
    statements :  statements statement
    '''
    p[0] = p[1]
    p[0].append(p[2])
    # p[0] = [statements, statement]

def p_statements_1(p):
    '''
    statements :  statement
    '''
    p[0] = Statements([p[1]])

#https://golang.org/ref/spec#Statements
def p_statement(p):
    '''
    statement :  const_declaration
          |  var_declaration
          |  extern_declaration
          |  assign_statement
          |  short_declaration
          |  print_statement
          |  if_statement
          |  funcall
          |  while_statement
          |  for_statement
          |  return_statement
          |  opper_statement
          |  func_declaration
          |  read_statement
          |  write_statement
    '''

    p[0] = Statement(p[1])

def p_const_declaration(p):
    '''
    const_declaration : CONST ID ASSIGN expression semi_optional
    '''
    p[0] = ConstDeclaration(p[2],p[4])

def p_var_declaration(p):
    '''
    var_declaration : VAR ID typename semi_optional
    '''
    p[0] = VarDeclaration(p[2], p[3], None, lineno=p.lineno(2))

def p_var_declaration_1(p):
    '''
    var_declaration : VAR ID typename ASSIGN expression semi_optional
    '''
    p[0] = VarDeclaration(p[2], p[3], p[5], lineno=p.lineno(1))

def p_extern_declaration(p):
    '''
    extern_declaration : EXTERN func_prototype semi_optional
    '''
    p[0] = Extern(p[2])

def p_func_prototype(p):
    '''
    func_prototype : FUNC ID LPAREN parameters RPAREN typename
    '''
    p[0] = FuncPrototype(p[2], p[4], p[6])

def p_parameters(p):
    '''
    parameters : parameters COMMA parm_declaration
    '''
    p[0] = p[1]
    p[0].append(p[3])

def p_parameters_1(p):
    '''
    parameters : parm_declaration
           | empty
    '''
    p[0] = Parameters([p[1]])

def p_parm_declaration(p):
    '''
    parm_declaration : ID typename
    '''
    p[0] = ParamDecl(p[1], p[2])

def p_assign_statement(p):
    '''
    assign_statement : location ASSIGN expression semi_optional
            | location POSITIVEINCREASE expression semi_optional
            | location NEGATIVEINCREASE expression semi_optional
            | location MULTIPLIINCREASE expression semi_optional
            | location DIVIDEINCREASE expression semi_optional
    '''
    p[0] = AssignmentStatement(p[1], p[3], p[2],lineno=p.lineno(2))

def p_print_statement(p):
    '''
    print_statement : PRINT expression semi_optional
    '''
    #import pydb; pydb.debugger()
    p[0] = PrintStatement(p[2])

def p_expression_unary(p):
    '''
    expression :  PLUS expression %prec UNARY
           |  MINUS expression %prec UNARY
           |  LNOT expression %prec UNARY
    '''
    p[0] = UnaryOp(p[1], p[2], lineno=p.lineno(1))

def p_expression_binary(p):
    '''
    expression :  expression PLUS expression
           | expression MINUS expression
           | expression TIMES expression
           | expression DIVIDE expression
           | expression RESIDUE expression
    '''
    p[0] = BinaryOp(p[2], p[1], p[3],lineno=p.lineno(2))


def p_expression_relation(p):
    '''
    expression : expression LE expression
            | expression LT expression
            | expression EQ expression
            | expression NE expression
            | expression GE expression
            | expression GT expression
            | expression LAND expression
            | expression LOR expression
            | expression AND expression
            | expression OR expression
    '''
    p[0] = RelationalOp(p[2], p[1], p[3], lineno=p.lineno(2))

def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = Group(p[2])

def p_expression_funcall(p):
    '''
    funcall :  ID LPAREN exprlist RPAREN semi_optional
    '''
    p[0] = FunCall(p[1], p[3],lineno=p.lineno(1))

def p_expression_funcall1(p):
    '''
    expression : funcall
    '''
    p[0] = (p[1])

def p_if_statement(p):
    '''
    if_statement : IF expression LBRACE statements RBRACE
    '''
    p[0] = IfStatement(p[2], p[4], None,lineno=p.lineno(1))

def p_if_else_statement(p):

    '''
    if_statement : IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE
    '''
    p[0] = IfStatement(p[2], p[4], p[8],lineno=p.lineno(1))

def p_while_statement(p):
    '''
    while_statement : WHILE expression LBRACE statements RBRACE
    '''
    p[0] = WhileStatement(p[2], p[4],lineno=p.lineno(1))

def p_expression_location(p):
    '''
    expression :  location
    '''
    p[0] = LoadLocation(p[1], lineno=p.lineno(1),isLeaf=True)

def p_expression_literal(p):
    '''
    expression :  literal
    '''
    p[0] = Literal(p[1],isLeaf=True)

def p_exprlist(p):
    '''
    exprlist :  exprlist COMMA expression
    '''
    p[0] = p[1]
    p[0].append(p[3])

def p_exprlist_1(p):
    '''
    exprlist : expression
           | empty
    '''
    p[0] = ExprList([p[1]])

def p_literal(p):
    '''
    literal : INTEGER
            | FLOAT
            | STRING
            | BOOLEAN
    '''
    p[0] = Literal(p[1],lineno=p.lineno(1),isLeaf=True)

# Gramaticas agregadas

def p_semi_optional(p):
    '''
    semi_optional : SEMI
            | empty
    '''

def p_return_statement(p):
    '''
    return_statement : RETURN expression semi_optional
    '''
    p[0] = Return(p[2])

def p_for_statement(p):
    '''
    for_statement : FOR cond1 expression SEMI cond2 LBRACE statements RBRACE
    '''
    p[0] = ForStatement(p[2], p[3], p[5], p[7],lineno=p.lineno(1))

def p_cond1(p):
    '''
    cond1 : var_declaration
            | short_declaration
    '''
    p[0] = Statement(p[1])

def p_cond2(p):
    '''
    cond2 : expression
            | assign_statement
            | opper_statement
    '''
    p[0] = Statement(p[1])

def p_short_declaration(p):
    '''
    short_declaration : location EVADETYPEDECLAR expression semi_optional
    '''
    p[0] = AssignmentStatement(p[1], p[3], p[2])

def p_opper_statement(p):
    '''
    opper_statement : location INCREASE
            | location DECREMENT
    '''
    p[0] = Opper(p[1],p[2],lineno=p.lineno(2))

def p_location(p):
    '''
    location : ID
    '''
    p[0] = Location(p[1], isLeaf=True)

def p_func_declaration(p):
    '''
    func_declaration : FUNC ID LPAREN parameters RPAREN typename LBRACE statements RBRACE
    '''
    p[0] = FuncDeclaration(p[2], p[4], p[6], p[8])

def p_read_statement(p):
    '''
    read_statement : READ LPAREN expression RPAREN semi_optional
    '''
    p[0] = ReadStatement(p[3])

def p_write_statement(p):
    '''
    write_statement : WRITE LPAREN expression RPAREN semi_optional
    '''
    p[0] = WriteStatement(p[3])

def p_typename(p):
    '''
    typename : FLOAT
            | STRING
            | INT
            | BOOL
    '''
    p[0] = TypeName(p[1],lineno=p.lineno(1),isLeaf=True)

def p_empty(p):
    '''
    empty    :
    '''

# ----------------------------------------------------------------------
# capturar todos los errores.  La siguiente función es llamada si existe
# una entrada mala. Vea http://www.dabeaz.com/ply/ply.html#ply_nn31

def p_error(p):
    if p:
        error(p.lineno, "Error de sintaxis de entrada en token '%s'" % p.value)
    else:
        error("EOF","Error de sintaxis. No hay mas entrada.")

def p_literal_error(p):
    'statement : PRINT error SEMI'
    print("Error en los literales")

# ----------------------------------------------------------------------
#              NO MODIFIQUE NADA DE AQUI EN ADELANTE
# ----------------------------------------------------------------------

def make_parser():
    parser = yacc.yacc()
    return parser

if __name__ == '__main__':
    import golex
    import sys
    from errors import subscribe_errors
    lexer = golex.make_lexer()
    parser = make_parser()

    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())

    # Output the resulting parse tree structure
    """print ("....")
    for depth,node in flatten(program):
        print("%s    %s" % (" "*(4*depth),node))
    print ("....")"""

    #flatten(program)

    if program:
        dot = DotVisitor()
        dot.visit(program)
        dot.printGraph("salida.png")
    else:
        print ("Error al crear el parser")
