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
    'IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'READ', 'WRITE',

    # Operatores y delimitadores
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'SEMI', 'RESIDUE',
    'LPAREN', 'RPAREN', 'COMMA', 'LBRACE', 'RBRACE', 'COLONS',
    'LBRACKET', 'RBRACKET', 'INCREASE', 'POSITIVEINCREASE',
    'NEGATIVEINCREASE', 'DECREMENT','MULTIPLIINCREASE', 'DIVIDEINCREASE',
    'EVADETYPEDECLAR',

    # Operadores lógicos
    'LT', 'LE', 'GT', 'GE', 'LAND', 'LOR', 'LNOT',
    'EQ', 'NE', 'OR', 'AND',

    # Literales
    'INTEGER', 'FLOAT', 'STRING', 'BOOLEAN', 'INT', 'BOOL',
]

# ----------------------------------------------------------------------
#                          PALABRAS RESERVADAS
# ----------------------------------------------------------------------
reserved = {
    'string'      : 'STRING',
    'if'          : 'IF',
    'else'        : 'ELSE',
    'while'       : 'WHILE',
    'var'         : 'VAR',
    'const'       : 'CONST',
    'func'        : 'FUNC',
    'extern'      : 'EXTERN',
    'print'       : 'PRINT',
    'return'      : 'RETURN',
    'for'         : 'FOR',
    'read'        : 'READ',
    'write'       : 'WRITE'
}

# ----------------------------------------------------------------------
#                               OPERADORES
# ----------------------------------------------------------------------
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
    r'{'  : "LBRACE",
    r'}'  : "RBRACE",
    r'%'  : "RESIDUE",

    r'<'  : "LT",
    r'<=' : "LE",
    r'==' : "EQ",
    r'>=' : "GE",
    r'>'  : "GT",
    r'!=' : "NE",
    r'&&' : "LAND",
    r'||' : "LOR",
    r'!'  : "LNOT",

    r'['  : "LBRACKET",
    r']'  : "RBRACKET",
    r':=' : "EVADETYPEDECLAR",
    r':'  : "COLONS",
    r'&'  : "AND",
    r'|'  : "OR",
    r'+=' : "POSITIVEINCREASE",
    r'++' : "INCREASE",
	r'--' : "DECREASE",
    r'-=' : "NEGATIVEINCREASE",
    r'*=' : "MULTIPLIINCREASE",
    r'/=' : "DIVIDEINCREASE",
}

t_ignore = ' \t\r'

# ----------------------------------------------------------------------
#                       OPERATORES Y DELIMITADORES
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
#                           OPERADORES LOGICOS
# ----------------------------------------------------------------------
t_LT      = r'<'
t_LE      = r'<='
t_GT      = r'>'
t_GE      = r'>='
t_LAND    = r'\&\&'
t_LOR     = r'\|\|'
t_LNOT    = r'!'
t_EQ      = r'=='
t_NE      = r'!='

# ----------------------------------------------------------------------
#                                 NUEVOS
# ----------------------------------------------------------------------
t_RESIDUE          = r'%'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_COLONS           = r':'
t_EVADETYPEDECLAR  = r':='
t_AND              = r'\&'
t_OR               = r'\|'
t_POSITIVEINCREASE = r'\+='
t_NEGATIVEINCREASE = r'-='
t_MULTIPLIINCREASE = r'\*='
t_DIVIDEINCREASE   = r'/='
t_INCREASE         = r'\+\+'
t_DECREMENT        = r'--'

# ----------------------------------------------------------------------
#                           SIMBOLOS DE ESCAPE
# ----------------------------------------------------------------------
escapes_not_b = r'nrt\"'
escapes = escapes_not_b + "b"

def _replace_escape_codes(t):
    t.value = t.value.replace('\\n','\u000A')
    t.value = t.value.replace('\\t','\u0009')
    t.value = t.value.replace('\\"','\u0022')
    t.value = t.value.replace('\\r','\u000D')
    t.value = t.value.replace('\\b','\u0062')
    t.value = t.value.replace('\\','\u005C')
    return t

def _replace_escape_codes2(t):
    s = ""
    size = len(t.value)
    cont = 0
    aux = 0
    flag = False # ignora el que sigue para que no lo agregue a s
    for i in range (0,size):
        if (aux >= 2):
            flag = False
        if (flag):
            aux += 1
        if (t.value[i] == "\\" and cont < size - 1):
            if (str(t.value[i+1]) == "n"):
                s += "\\u000A"
                flag = True
            elif (t.value[i+1] == "t"):
                s += "\\u0009"
                flag = True
            elif (t.value[i+1] == "\""):
                s = s + "\\u0022"
                flag = True
            elif (t.value[i+1] == "r"):
                s += "\\u000D"
                flag = True
            elif (t.value[i+1] == "b"):
                s += "\\u0062"
                flag = True
            elif(t.value[i+1] == "\\"):
                s += "\\u005C"
                flag = True
            aux += 1
        else:
            if (not flag):
                if (t.value[i] != "\""):
                    s = s + str(t.value[i])
                    flag = False
    return s


# ----------------------------------------------------------------------
#                               LITERALES
# ----------------------------------------------------------------------
def t_FLOAT(t):
    r'(\d*\.\d+|\d+\.\d*)([eE][-+]?\d+)?|\d+([eE][-+]?\d+)'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'0[xX][0-9a-fA-F]+|[\d]+|0[0-7]*'
    t.value = int(str(t.value),0)
    return t

def t_STRING(t):
    #r'"[^"]*"'
    #r'"([^"](\\")?)*"'
	r'".*"'
	t.value = t.value[1:-1]
	t.value = _replace_escape_codes2(t)
	return t

def t_BOOL(t):
    r'true|false'
    if t.value.upper() in tokens:
        t.type = t.value.upper()
    return t

# ----------------------------------------------------------------------
#                                KEYWORDS
# ----------------------------------------------------------------------
#Tener en cuenta que no sean palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in tokens:
        t.type = t.value.upper()
    return t

# ----------------------------------------------------------------------
#                           TEXTOS ESPECIALES
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
#                          CARACTERES ILEGALES
# ----------------------------------------------------------------------
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

    lexer = make_lexer()

    lexer = make_lexer()
    with subscribe_errors(lambda msg: sys.stderr.write(msg+"\n")):
        lexer.input(open(sys.argv[1]).read())
        for tok in iter(lexer.token,None):
            sys.stdout.write("%s\n" % tok)
