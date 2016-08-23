# golex.py
# -*- coding: utf-8 -*-
r'''
Projecto 1 - Escribir un Lexer
==============================
En este primer proyecto, usted debe escribir un lexer sencillo para un
lenguaje de expresiones (miniGO). El proyecto es basado en código que usted 
debe leer y completar (este archivo). Por favor, lea el contenido 
completo de este archivo y cuidadosamente complete los pasos indicados
como comentarios.
 
Revisión:
---------
El proceso del analizador léxico es la de tomar el texto de entrada y 
descomponerlo en un flujo de tokens (símbolos). Cada token es como una
palabra válida del diccionario. Escencialmente, el papel del lexer es
simplemente asegurarse de que el texto de entrada se compone de símbolos
válidos antes de cualquier procesamiento adicional relacionado con el
análisis sintático.
 
Cada token es definido por una expresion regular. Por lo tanto, su principal 
tarea en este primer proyecto es definir un conjunto de expresiones
regulares para el lenguaje. El trabajo actual del análisis léxico deberá
ser manejado por PLY (http://www.dabeaz.com/ply).
 
Especificación:
---------------
Su lexer debe reconocer los siguientes tokens (símbolos). El nombre a la
izquierda es el nombre del token, el valor en la derecha es el texto de
coincidencia.
 
Palabras Reservadas:
    CONST   : 'const'
    VAR     : 'var'  
    PRINT   : 'print'
    FUNC    : 'func'
    EXTERN  : 'extern'
 
Identificadores: (Las mismas reglas como para Python)
    ID      : El texto inicia con una letra o '_', seguido por cualquier
              número de letras, digitos o guión bajo.
 
Operadores y Delimitadores:
    PLUS    : '+'
    MINUS   : '-'
    TIMES   : '*'
    DIVIDE  : '/'
    ASSIGN  : '='
    SEMI    : ';'
    LPAREN  : '('
    RPAREN  : ')'
    COMMA   : ','
 
Literales:
    INTEGER : '123'   (decimal)
              '0123'  (octal)
              '0x123' (hex)
 
    FLOAT   : '1.234'
              '1.234e1'
              '1.234e+1'
              '1.234e-1'
              '1e2'
              '.1234'
              '1234.'
 
    STRING  : '"Hola Mundo\n"'
 
Comentarios:  Para ser ignorados por el lexer
     //             Ignora el resto de la línea
     /* ... */      Omite un bloque (sin anidamiento permitido)
 
Errores: Su lexer debe reportar los siguientes mensajes de error:
 
     lineno: Caracter ilegal 'c' 
     lineno: Cadena sin terminar
     lineno: Comentario sin terminar
     lineno: Cadena de código de escape malo '\..'
 
Pruebas
-------
Para el desarrollo inicial, trate de correr el lexer sobre un archivo de
entrada de ejemplo, como:
 
     bash % python golex.py sample.go
 
Estudie cuidadosamente la salida del lexer y asegúrese que tiene sentido.
Una vez que este rasonablemente contento con la salida, intente ejecutar
alguna de las pruebas mas difíciles:
 
     bash % python golex.py testlex1.go
     bash % python golex.py testlex2.go
 
Bono: ¿Cómo haría usted para convertir estas pruebas en pruebas unitarias
adecuadas?
'''
 
# ----------------------------------------------------------------------
# El siguiente import carga una función error(lineno,msg) que se debe
# utilizar para informar de todos los mensajes de error emitidos por su
# lexer. Las pruebas unitarias y otras caracteristicas del compilador
# confiarán en esta función. Ver el archivo errors.py para más documentación
# acerca del mecanismo de manejo de errores.
from errors import error
 
# ----------------------------------------------------------------------
# Los lexers son definidos usando la librería ply.lex
#
# Ver http://www.dabeaz.com/ply/ply.html#ply_nn3
from ply.lex import lex
 
# ----------------------------------------------------------------------
# Lista de tokens. Esta lista identifica la lista completa de nombres de
# token que deben ser reconocidos por su lexer.  No cambie ninguno de
# estos nombres. Si lo hace, se dañaran las pruebas unitarias.
 
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
 
# ----------------------------------------------------------------------
# Ignora caracteres (whitespace)
#
# Los siguientes caracteres son ignorados completamente por el lexer.
# No lo cambie.
 
t_ignore = ' \t\r'
 
# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : escriba las regexs indicadas mas adelante ***
# 
# Tokens para símbolos simples: + - * / = ( ) ; 
 
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_ASSIGN    = r'='
t_SEMI      = r';'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
 
# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : escriba las regexs y código adicional ***
#
# Tokens para literales, INTEGER, FLOAT, STRING. 
 
# Constante de punto flotante.   Se debe reconocer números de punto flotante
# en formatos como se muestra en los siguientes ejemplos:
#
#   1.23, 1.23e1, 1.23e+1, 1.23e-1, 123., .123, 1e1, 0.
#
# El valor debe ser convertido a un float de Python cuando lo analice
def t_FLOAT(t):
	r'(([0-9]+\.[0-9]*)|(\.[0-9]+))([eE][-+]?[0-9]+)?'
    t.value=float(t.value)
    return t

# Constante entera.  Debe reconocer enteros en todos los formatos
# siguientes:
#
#     1234             (decimal)
#     01234            (octal)
#     0x1234 or 0X1234 (hex)
#
# El valor debe ser convertido The value should be converted to a Python int when lexed.
def t_INTEGER(t):
	r'0x[0-9]+[A-F]+|0x[A-F]+[0-9]+|0x[0-9]+[A-F]*|0x[0-9]*[A-F]+|[0-9]+|0[0-7]+'
    t.value = int(str(t.value),0)
    return t

# Constante de Cadena. Debe reconocer texto encerrado entre comillas.
# Por ejemplo:
#
#     "Hola Mundo"
#
# Las cadenas se les permite tener codigos de escape que se definen por
# un backslash.  Los siguientes códigos de barra deben entenderse:
#      
#       \n    = newline (10)
#       \r    = carriage return (13) 
#       \t    = tab (9)
#       \\    = baskslash char (\)
#       \"    = comillas (")
#       \bhh  = código byte de caracter hh  (h es un digito hex)
#
# Todos los demás códigos de escape deben dar lugar a un error. Nota: literales
# de cadena hacen *NO* comprender el rango completo de códigos de caracter
# soportados por Python.
#
# El valor del token debe ser la cadena con todos los códigos de escape sustituidos
# por su correspondiente código de caracter primitivo.
 
escapes_not_b = r'nrt\"'
escapes = escapes_not_b + "b"
def _replace_escape_codes(t):
    t.value=t.value.replace('\\n','\u000A')
    t.value=t.value.replace('\\t','\u0009')
    t.value=t.value.replace('\\','\u005C')
    t.value=t.value.replace('\\"','\u0022')
    t.value=t.value.replace('\\r','\u000D')
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

# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : Escriba la regex y keywords ***
#
 
# Identificadores y keywords. 
# Coincida con un identificador primario. Los identificadores siguen las
# mismas reglas de Python.  Esto es, ellos inician con una letra o 
# subrayado (_) y puede contener un numero arbitario de letras, digitos
# o subrayado desde de ella.
def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in tokens:
        t.type = t.value.upper()
    return t
 
 def t_ELSE(t):
    r'else'
    return t_ELSE
    

# *** DEBE IMPLEMENTAR ***
# Adicione codigo que conincida con las palabras reservadas tales como:
# 'var','const','print','func','extern'
 
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
 
# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : escriba las regexs indicada ***
#
# Ignore texto.  Las siguientes reglas son usadas para ignorar texto en
# el archivo de entrada.  Esto incluye comentarios y lineas en blanco.
 
# Una o mas lineas en blanco
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
# *** DEBE COMPLETAR : escriba las regexs indicada ***
#
# Manejo de Errors.  Las siguientes condiciones de error deben ser
# manejadas en su lexer.
 
# Caracteres ilegales (Manejador generico de errores)
def t_error(t):
    error(t.lexer.lineno,"Illegal character %r" % t.value[0])
    t.lexer.skip(1)
 
# Comentarios no cerrados estilo-C
def t_COMMENT_UNTERM(t):
	pass 

# Constantes de cadena no terminadas
def t_STRING_UNTERM(t):
	pass

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