# golex.py
# -*- coding: utf-8 -*-
"""
Compilador léxico
Profesor: Angel Augusto Zapata
Materia: Compiladores
Integrantes:
	Carolina Jimenez Gomez
	Juan Diego Suarez
	Carlos Enrique Angel
"""
from errors import error
from ply.lex import lex

tokens = [
    # keywords
    'ID', 'CONST', 'VAR', 'PRINT', 'FUNC', 'EXTERN',
 
    # Control de flujo
    'IF', 'ELSE', 'WHILE',
 
    # Operatores y delimitadores
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'SEMI', 'LPAREN', 'RPAREN', 'COMMA',
    'LBRACE', 'RBRACE',
 
    # Operadores lógicos
    'LT', 'LE', 'GT', 'GE', 'LAND', 'LOR', 'LNOT',
    'EQ', 'NE',
 
    # Literales
    'INTEGER', 'FLOAT', 'STRING', 'BOOLEAN',
]

#-----------Palabras reservadas----------

reserved = {
    'if'    : 'IF',
    'else'  : 'ELSE',
    'while' : 'WHILE',
    'var'   : 'VAR',
    'const' : 'CONST',
    'func'  : 'FUNC',
    'extern': 'EXTERN',
    'print' : 'PRINT',
}
 
#------------Operadores----------
operators = {

    r'+'  : "PLUS",
    r'-'  : "MINUS",    
    r'*'  : "TIMES",    
    r'/'  : "DIVIDE",   
    r'='  : "ASSIGN",   
    r';'  : "SEMI",     
    r'('  : "LPAREN",   
    r')'  : "RPAREN",   
    r','  : "COMMA", 
    r'{' : "LBRACE", 
    r'}' : "RBRACE",

    r'<'  : "LT",       
    r'<=' : "LE",       
    r'==' : "EQ",       
    r'>=' : "GE",       
    r'>'  : "GT",       
    r'!=' : "NE",       
    r'&&' : "LAND",     
    r'||' : "LOR",      
    r'!'  : "LNOT",     
}

t_ignore = ' \t\r'
 

#---------Operatores y delimitadores-----------

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_ASSIGN    = r'='
t_SEMI      = r';'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COMMA     = r','
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'

#----------Operadores lógicos-------


t_LT      = r'<'
t_LE      = r'<='
t_GT      = r'>'
t_GE      = r'>='
t_LAND    = r'&&'
t_LOR     = r'\|\|'
t_LNOT    = r'!'
t_EQ      = r'=='
t_NE      = r'!='
 

#-----------Simbolos de escape-------------

escapes_not_b = r'nrt\"'
escapes = escapes_not_b + "b"
def _replace_escape_codes(t):
    t.value = t.value.replace('\\n','\u000A')
    t.value = t.value.replace('\\t','\u0009')
    t.value = t.value.replace('\\','\u005C')
    t.value = t.value.replace('\\"','\u0022')
    t.value = t.value.replace('\\r','\u000D')
    t.value = t.value.replace('\\b','\u0062')
    return t


#---------Literales----------

def t_FLOAT(t):
    r'(([0-9]+\.[0-9]*)|(\.[0-9]+))([eE][-+]?[0-9]+)?'
    t.value=float(t.value)
    return t

def t_INTEGER(t):
    r'0x[0-9]+[A-F]+|0x[A-F]+[0-9]+|0x[0-9]+[A-F]*|0x[0-9]*[A-F]+|[0-9]+|0[0-7]+'
    t.value = int(str(t.value),0)
    return t
      
def t_STRING(t):
    r'".*"'
    # Convierte t.value dentro de una cadena con códigos de escape reemplazados por valores actuales.
    t.value = t.value[1:-1]
    _replace_escape_codes(t)    # Debe implementarse antes
    return t
 
def t_BOOLEAN(t):
    r'True|False' 
    if t.value.upper() in tokens:
        t.type=t.value.upper()
    return t

#----------keywords-----------
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in tokens:
        t.type = t.value.upper()
    return t
 

 #---------Control de flujo---------

def t_ELSE(t):
    r'else'
    return t_ELSE
    
def t_IF(t):
    r'if'
    return t_IF

def t_WHILE(t):
    r'while'
    return t_WHILE
 
# -----------Ignorar textos especiales-----------

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
# Comentarios estilo-C (/* ... */)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
     
# Comentarios estilo-C++ (//...)
def t_CPPCOMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1
 
# -------------Caracteres ilegales-----------------
def t_error(t):
    error(t.lexer.lineno,"Illegal character %r" % t.value[0])
    t.lexer.skip(1)
 
# Comentarios no cerrados estilo-C
def t_COMMENT_UNTERM(t):
    r'/\*(.|\n)*'
    print("Comentario sin terminar '%s'"  % t.value[0], t.lineno)
    t.lexer.skip(1)

# Constantes de cadena no terminadas
def t_STRING_UNTERM(t):
    r'\"(.|\n)*'
    print("Cadena sin terminar '%s'" % t.value[0], t.lineno)
    t.lexer.skip(1)

# ----------------------------------------------------------------------
#                   NO CAMBIE NADA A PARTIR DE AQUI
# ----------------------------------------------------------------------
def make_lexer():
    '''
    Función de utilidad para crear el objeto lexer
    '''
    return lex()
 
if __name__ == '__main__':
    import sys
    from errors import subscribe_errors
     
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s filename\n" % sys.argv[0])
        raise SystemExit(1)
 
     
    lexer = make_lexer()
    with subscribe_errors(lambda msg: sys.stderr.write(msg+"\n")):
        lexer.input(open(sys.argv[1]).read())
        for tok in iter(lexer.token,None):
            sys.stdout.write("%s\n" % tok)