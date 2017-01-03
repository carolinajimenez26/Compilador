# gocheck.py
# coding: utf-8
'''
Proyecto 3 : Chequeo del Programa
=================================
En este proyecto es necesario realizar comprobaciones semánticas en
su programa.   Hay algunos aspectos diferentes para hacer esto.

En primer lugar, tendrá que definir una tabla de símbolos que haga
un seguimiento de declaraciones de identificadores previamente
declarados.  Se consultará la tabla de símbolos siempre que el
compilador necesite buscar información sobre variables y declaración
de constantes.

A continuación, tendrá que definir los objetos que representen los
diferentes tipos de datos incorporados y registrar información
acerca de sus capacidades.  Revise el archivo gotype.py.

Por último, tendrá que escribir código que camine por el AST y
haga cumplir un conjunto de reglas semánticas.  Aquí está una lista
completa de todo los que deberá comprobar:

1.      Nombres y símbolos:

                Todos los identificadores deben ser definidos antes de ser usados.
                Esto incluye variables, constantes y nombres de tipo.  Por ejemplo,
                esta clase de código genera un error:

                                a = 3;              // Error. 'a' no está definido.
                                var a int;

                Nota: los nombres de tipo como "int", "float" y "string" son nombres
                incorporados que deben ser definidos al comienzo de un programa
                (función).

2.  Tipos de constantes

                A todos los símbolos constantes se le debe asignar un tipo como
                "int", "float" o "string". Por ejemplo:

                                const a = 42;         // Tipo "int"
                                const b = 4.2;        // Tipo "float"
                                const c = "forty";    // Tipo "string"

                Para hacer esta asignación, revise el tipo de Python del valor
                constante y adjunte el nombre de tipo apropiado.

3.  Chequeo de tipo operación binaria.

                Operaciones binarias solamente operan sobre operandos del mismo
                tipo y produce un resultado del mismo tipo.  De lo contrario, se
                tiene un error de tipo.  Por ejemplo:

                                var a int = 2;
                                var b float = 3.14;

                                var c int = a + 3;    // OK
                                var d int = a + b;    // Error.  int + float
                                var e int = b + 4.5;  // Error.  int = float

4.  Chequeo de tipo operador unario.

                Operadores unarios retornan un resultado que es del mismo tipo
                del operando.

5.  Operadores soportados

                Estos son los operadores soportados por cada tipo:

                                int:      binario { +, -, *, /}, unario { +, -}
                                float:    binario { +, -, *, /}, unario { +, -}
                                string:   binario { + }, unario { }

                Los intentos de usar operadores no soportados debería dar lugar a
                un error.  Por ejemplo:

                                var string a = "Hello" + "World";    // OK
                                var string b = "Hello" * "World";    // Error (op * no  soportado)

6.  Asignación.

                Los lados izquierdo y derecho de una operación de asignación deben
                ser declarados del mismo tipo.

                Los valores sólo se pueden asignar a las declaraciones de variables,
                no a constantes.

Para recorrer el AST, use la clase NodeVisitor definida en goast.py.
Un caparazón de código se proporciona a continuación.
'''

import sys, re, string, types
from errors import error
from goast import *
import gotype
import golex

class SymbolTable(object):
        '''
        Clase que representa una tabla de símbolos.  Debe proporcionar
        funcionabilidad para agregar y buscar nodos asociados con
        identificadores.
        '''

        class SymbolDefinedError(Exception):
                '''
                Exception disparada cuando el codigo trara de agragar un simbol
                a la tabla de simbolos, y este ya esta definido
                '''
                pass

        class SymbolConflictError(Exception):
                '''
                '''
                pass

        def __init__(self, parent=None):
                '''
                Crea una tabla de simbolos vacia con la tabla padre dada
                '''
                self.symtab = {}
                self.parent = parent
                if self.parent != None:
                        self.parent.children.append(self)
                self.children = []

        def add(self, a, v):
                '''
                Agrega un simbol con el valor dado a la tabla de simbolos

                func foo(x:int, y:int)
                x:float;
                '''

                #if self.symtab.has_key[a]:
                if a in self.symtab:
                        if self.symtab[a].name != v.name:

                                raise SymbolTable.SymbolConflictError()
                        else:
                                pass#raise SymbolTable.SymbolDefinedError()
                self.symtab[a] = v




        def lookup(self, a):

                i=str(a)
                i= i.strip("'")
                #if self.symtab.has_key(i):
                if i in self.symtab:

                        return self.symtab[i]
                else:
                        if self.parent != None:

                                return self.parent.lookup(a)
                        else:

                                return None
        def tipodato(self,a):
                i=str(a)
                i= i.strip("'")
                if i in self.symtab:
                        if(a!="int" and a!="float" and a!="bool" and a!="string"):
                                return(self.symtab[i]);

                else:
                        if self.parent != None:
                                return(self.parent.tipodato(i))
                        else:
                                return None



        def __repr__(self):
            return '%r' % self.symtab

class CheckProgramVisitor(NodeVisitor):
        '''
        Clase de Revisión de programa.  Esta clase usa el patrón cisitor
        como está descrito en mpasast.py.  Es necesario definir métodos de
        la forma visit_NodeName() para cada tipo de nodo del AST que se
        desee procesar.

        Nota: Usted tendrá que ajustar los nombres de los nodos del AST si
        ha elegido nombres diferentes.
        '''
        tipos = [gotype.boolean_type, gotype.int_type, gotype.float_type, gotype.string_type]
        def __init__(self):
                # Inicializa la tabla de simbolos
                self.current = SymbolTable()
                self.symtab = SymbolTable()

        def push_symtab(self, node):

                self.current = SymbolTable(self.current)
                node.symtab = self.current

        def pop_symbol(self):
                self.current = self.current.parent

        def visit_Program(self,node):

                """self.push_symtab(node)"""
                # Agrega nombre de tipos incorporados ((int, float, string) a la  tabla de simbolos
                """node.symtab.add("int",gotype.int_type)
                node.symtab.add("float",gotype.float_type)
                node.symtab.add("string",gotype.string_type)
                node.symtab.add("bool",gotype.boolean_type)"""
                """self.symtab.add("int",gotype.int_type)
                self.symtab.add("float",gotype.float_type)
                self.symtab.add("string",gotype.string_type)
                self.symtab.add("bool",gotype.boolean_type)"""
                self.current.add("int",gotype.int_type)
                self.current.add("float",gotype.float_type)
                self.current.add("string",gotype.string_type)
                self.current.add("bool",gotype.boolean_type)

                # 1. Visita todas las declaraciones (statements)
                # 2. Registra la tabla de simbolos asociada
                self.visit(node.program)

        def visit_IfStatement(self, node):

                self.visit(node.condition)


                if not node.condition.type == gotype.boolean_type:
                        a=self.current.tipodato(node.condition.type)

                        if not a == gotype.boolean_type:
                            error(node.lineno, "Tipo incorrecto para condición if")
                else:
                        self.visit(node.then_b)
                        if node.else_b:
                                self.visit(node.else_b)

        def visit_WhileStatement(self, node):


                self.visit(node.condition)

                if not node.condition.type == gotype.boolean_type:
                        error(node.lineno, "Tipo incorrecto para condición while")
                        self.visit(node.body)
                else:
                        self.visit(node.body)

        def visit_UnaryOp(self, node):

                # 1. Asegúrese que la operación es compatible con el tipo
                # 2. Ajuste el tipo resultante al mismo del operando
                self.visit(node.left)
                if not golex.operators[node.op] in node.left.type.un_ops:
                        error(node.lineno, "Operación no soportada con este tipo")
                self.type = node.left.type
                node.type=node.left.type

        def visit_BinaryOp(self, node):

                # 1. Asegúrese que los operandos left y right tienen el mismo tipo
                # 2. Asegúrese que la operación está soportada
                # 3. Asigne el tipo resultante
                self.visit(node.left)
                self.visit(node.right)
                if node.left.type != node.right.type:
                    error(node.lineno,"Operación no valida %s" %node)
                node.type = node.left.type


        def visit_AssignmentStatement(self,node):

                self.visit(node.value)


                if node.asig==":=":
                        node.type=node.value.type
                        self.current.add(node.location.location, node.type)

                sym = self.current.lookup(node.location)

                if not sym:
                        error(node.lineno,"Variable %s no ha sido declarada" %node.location)

                else:


                        if str(node.value).strip("'")=="+" or str(node.value).strip("'")== "-" or node.value=="*" or node.value == "/":

                                if (sym != node.value.type):
                                        error(node.lineno,"Tipos no coinciden en asignación")
                                node.value = node.value



                        else:

                                a=self.current.tipodato(node.value)

                                if a==None:

                                        if (sym != node.value.type):
                                                error(node.lineno,"Tipos no coinciden en asignación")
                                        node.value = node.value

                                else:
                                        if(sym != a):
                                                error(node.lineno,"Tipos no coinciden en asignación")
                                        node.value = node.value

        def visit_ConstDeclaration(self,node):

                # 1. Revise que el nombre de la constante no se ha definido
                if self.current.lookup(node.id):
                        error(node.lineno, "Símbol %s ya definido" %node.id)
                        self.visit(node.value)
                        node.type = node.value.type

                        #self.symtab.add(node.id, node.type)
                # 2. Agrege una entrada a la tabla de símbolos
                else:
                        self.visit(node.value)

                        node.type = node.value.type
                        #self.symtab.add(node.id, node.type)
                        self.current.add(node.id, node.type)


        def visit_VarDeclaration(self,node):

                node.type = self.current.lookup(node.typename.typename)
                assert(node.type)
                #print("node.value:",node.value.value.value)
                #print("node.value:",dir(node.value))
                #print("node.value.type:",node.value.type)
                #print("node.typename.typename:",node.typename.typename)
                #muestra la __repr__
                # 1. Revise que el nombre de la variable no se ha definido
                if self.current.lookup(node.id):
                        error(node.lineno, "Símbol %s ya definido" % node.id)
                # 2. Agrege la entrada a la tabla de símbolos
                else:
                        self.current.add(node.id, node.type)

                # 2. Revise que el tipo de la expresión (si lo hay) es el mismo

                if node.value:
                        self.visit(node.value)

                        if isinstance(node.value.type,str):
                            a=self.current.tipodato(node.value.type)

                            assert(node.typename.typename == a.name)
                       # assert(node.typename == node.value.type.name)
                # 4. Si no hay expresión, establecer un valor inicial para el valor
                else:
                        node.value = None



        def visit_Typename(self,node):
                # 1. Revisar que el nombre de   tipo es válido que es actualmente un tipo

                if (node.type not in self.tipos):
                    error(node.lineno,"%s Tipo Invalido" %node.type)
                else:
                    self.visit(node.type)

        def visit_Location(self,node):
                # 1. Revisar que la localización es una variable válida o un valor constante
                # 2. Asigne el tipo de la localización al nodo
                if (self.current.lookup(node.location) not in  self.tipos):
                        error(node.lineno,"La localizacion no es una variable valida")
                else:
                    node.type = self.current.lookup(node.location)

        def visit_LoadLocation(self,node):

                # 1. Revisar que loa localización cargada es válida.
                # 2. Asignar el tipo apropiado


                sym = self.current.lookup(node)

                if (sym==None):
                     error(node.lineno,"La variable %s no ha sido declarada" %node)
                     node.type=None;
                else:
                    node.type = sym


        def visit_Literal(self,node):

                if(node.value.value=='false'):
                    node.value.value=False;
                if(node.value.value=='true'):
                    node.value.value=True;
                if isinstance(node.value.value, types.BooleanType):

                        node.type = self.current.lookup("bool")
                elif isinstance(node.value.value, types.IntType):

                        node.type = self.current.lookup("int")
                elif isinstance(node.value.value, types.FloatType):

                        node.type = self.current.lookup("float")
                elif isinstance(node.value.value, types.StringTypes):

                        node.type = self.current.lookup("string")
               #     print ("node type",node.type)

        def visit_PrintStatement(self, node):
                self.visit(node.expr)

        def visit_Extern(self, node):
                # obtener el tipo retornado
                # registe el nombre de la función
                self.visit(node.func_prototype)

        def visit_FuncPrototype(self, node):



                self.visit(node.typename)
                node.type = self.current.lookup(node.typename)

                if self.current.lookup(node.id):
                        error(node.lineno, "Símbol %s ya definido" % node.id)
                else:
                    self.current.add(node.id, node.type)

                self.visit(node.params)
                self.push_symtab(node)

                if not node.params.__class__.__name__ == "Empty" :
                    self.current.add(node.id , node.params.param_decls[0].type)
                self.pop_symbol()


        def visit_Parameters(self, node):

                for p in node.param_decls:
                        self.visit(p)

        def visit_ParamDecl(self, node):

                node.type = self.current.lookup(node.typename)
                self.current.add(node.id,node.type)
                #node.type = self.symtab.lookup(node.typename.typename) ¿?

        def visit_Group(self, node):


                self.visit(node.expression)
                node.type = node.expression.type

        def visit_RelationalOp(self, node):
                self.visit(node.left)
                self.visit(node.right)
                if not node.left.type == node.right.type:
                        error(node.lineno, "Operandos de relación no son del mismo tipo")
                elif not golex.operators[node.op] in node.left.type.bin_ops:
                        error(node.lineno, "Operación no soportada con este tipo")
                node.type = self.current.lookup('bool')

        def visit_FunCall(self, node):

                if not self.current.lookup(node.id):
                    error(node.lineno,"La funcion %s no esta definida " %node.id)
                else:
                    self.visit(node.params)
                    #self.visit(node.id)


                    node.type = self.current.lookup(node)



        def visit_ExprList(self, node):

            for p in node.expressions:
                self.visit(p)

        def visit_Empty(self, node):
                pass

        # Agregados

        def visit_Statements(self,node):

            for s in node.statements:
                    self.visit(s)

        def visit_Statement(self,node):


            self.visit(node.statement)

        def visit_StoreVar(self,node):#j
            sym = self.current.lookup(node.name)
            assert(sym)
            node.type = sym.type

        def visit_Return(self,node):
            self.visit(node.expression)

        def visit_Opper(self,node):
            print("nodepér",node)
            if not self.current.lookup(node.ID.location):
                error(node.lineno,"La variable %s no ha sido declarada" %node.ID.location)
            node.type = gotype.int_type
            node.value=node

        def visit_ForStatement(self,node):

            self.visit(node.condition)

            if not node.condition.type == gotype.boolean_type:
                error(node.lineno,"Tipo incorrecto para la condicion for")
            else:

                self.visit(node.statement)
                
                if not node.statement.statement.value.type == gotype.int_type:
                    error(node.lineno,"Tipo incorrecto para la asignacion for")
                else:
                    self.visit(node.expression)

                    if (node.expression.statement.value.type not in self.tipos):
                        error(node.lineno,"Tipo incorrecto para la expresion for")
                    else:
                        self.visit(node.body)

        def visit_FuncDeclaration(self,node):#?¡



            node.type = self.current.lookup(node.typename.typename)

            if self.current.lookup(node.id):
                    error(node.lineno, "Símbol %s ya definido" %node.id)
            else:

                self.current.add(node.id, node.type)
                self.push_symtab(node)

            self.visit(node.params)
            self.visit(node.body)


            self.pop_symbol()



        def visit_Number(self,node):
            if not(node.type == gotype.int_type or node.type == gotype.float_type):
                error(node.lineno,"Error en el tipo de dato %s" %node.id)
            else:
                self.visit(node.expression)

        def visit_ReadStatement(self,node):#j

            self.visit(node.expression)

        def visit_WriteStatement(self,node):#j
            self.visit(node.expression)


# ----------------------------------------------------------------------
#                       NO MODIFICAR NADA DE LO DE ABAJO
# ----------------------------------------------------------------------

def check_program(node):
        '''
        Comprueba el programa suministrado (en forma de un AST)
        '''
        checker = CheckProgramVisitor()
        checker.visit(node)

def main():
        import goparser
        import sys
        from errors import subscribe_errors
        lexer = golex.make_lexer()
        parser = goparser.make_parser()
        with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
                program = parser.parse(open(sys.argv[1]).read())
                # Revisa el programa
                check_program(program)

if __name__ == '__main__':
        main()
