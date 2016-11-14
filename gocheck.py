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

def help(object, spacing=10, collapse=1): 
    """Print methods and doc strings.
    
    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])

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
<<<<<<< HEAD
                if self.symtab.has_key(a):
=======
                #if self.symtab.has_key(a):
                if a in self.symtab:
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                        if self.symtab[a].type.get_string() != v.type.get_string():
                                raise SymbolTable.SymbolConflictError()
                        else:
                                raise SymbolTable.SymbolDefinedError()
                self.symtab[a] = v
                
               
                

        def lookup(self, a):
<<<<<<< HEAD
             
                i=str(a)
                i= i.strip("'")
               
                
                
                
                
                if self.symtab.has_key(i):
                       
=======
                i=str(a)
                i= i.strip("'")
                #if self.symtab.has_key(i):
                if i in self.symtab:
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                        return self.symtab[i]
                else:
                        if self.parent != None:
                                return self.parent.lookup(a)
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
                self.symtab = self.current # SymbolTable()

        def push_symtab(self, node):
                self.current = SymbolTable(self.current)
                node.symtab = self.current

        def pop_symbol(self):
                self.current = self.current.parent

        def visit_Program(self,node):
                print ("visit_Program")

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
<<<<<<< HEAD
                
=======
                print ("visit_IfStatement")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                self.visit(node.condition)
                if not node.condition.type == gotype.boolean_type:
                        error(node.lineno, "Tipo incorrecto para condición if")
                else:
                        self.visit(node.then_b)
                        if node.else_b:
                                self.visit(node.else_b)

        def visit_WhileStatement(self, node):
<<<<<<< HEAD
               

                self.visit(node.condition)
                
                if not node.condition.type == gotype.boolean_type:
=======
                print ("visit_WhileStatement")
                self.visit(node.condition)
                #print ("caro",node.condition) # ARREGLAAAAARRR
                if not node.condition.isBoolean():
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                        error(node.lineno, "Tipo incorrecto para condición while")
                else:
                        self.visit(node.body)

        def visit_UnaryOp(self, node):
<<<<<<< HEAD
                
=======
                print ("visit_UnaryOp")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                # 1. Asegúrese que la operación es compatible con el tipo
                # 2. Ajuste el tipo resultante al mismo del operando
                self.visit(node.left)
                if not golex.operators[node.op] in node.left.type.un_ops:
                        error(node.lineno, "Operación no soportada con este tipo")
                self.type = node.left.type

        def visit_BinaryOp(self, node):
<<<<<<< HEAD
                
=======
                print ("visit_BinaryOp")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                # 1. Asegúrese que los operandos left y right tienen el mismo tipo
                # 2. Asegúrese que la operación está soportada
                # 3. Asigne el tipo resultante
                self.visit(node.left)
                self.visit(node.right)
                if node.left.type != node.right.type:
                    error(node.lineno,"Operación no valida %s" %node.id)
                node.type = node.left.type

        def visit_AssignmentStatement(self,node):
<<<<<<< HEAD
                
                algo = str(node.location)
                sym = self.symtab.lookup(algo)
                
                if not sym:
                        error(node.lineno,"Variable %s no declarada" %node.location)
=======
                print ("visit_AssignmentStatement")
                # 1. Asegúrese que la localización de la asignación está definida
                algo = str(node.location)
                sym = self.symtab.lookup(algo)
                assert sym, "Asignado a un sym desconocido"
                # 2. Revise que la asignación es permitida, pe. sym no es una constante
                # 3. Revise que los tipos coincidan.
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                self.visit(node.value)
                if not (sym == node.value.type):
                        error(node.lineno,"Tipos no coinciden en asignación")
                node.value=node.value.type

        def visit_ConstDeclaration(self,node):
<<<<<<< HEAD
                
=======
                print ("visit_ConstDeclaration")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                # 1. Revise que el nombre de la constante no se ha definido
                if self.symtab.lookup(node.id):
                        error(node.lineno, "Símbol %s ya definido" %node.id)
                # 2. Agrege una entrada a la tabla de símbolos
<<<<<<< HEAD
                else:   
                        self.visit(node.value)
                        node.type = node.value.type
                        #self.symtab.add(node.id, node)
                        self.current.add(node.id, node.type)
                

        def visit_VarDeclaration(self,node):
                
                node.type = self.current.lookup(node.typename.typename)
                assert(node.type)
                #muestra la __repr__
=======
                else:
                        #self.symtab.add(node.id, node)
                        self.current.add(node.id, node)
                self.visit(node.value)
                node.type = node.value.type

        def visit_VarDeclaration(self,node):
                print ("visit_VarDeclaration")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                # 1. Revise que el nombre de la variable no se ha definido
                if self.current.lookup(node.id):
                        error(node.lineno, "Símbol %s ya definido" % node.id)
                # 2. Agrege la entrada a la tabla de símbolos
                else:
<<<<<<< HEAD
                        self.current.add(node.id, node.type)
                       
                # 2. Revise que el tipo de la expresión (si lo hay) es el mismo
                if node.value:
                        self.visit(node.value)
                        assert(node.typename.typename == node.value.type.name) 
=======
                        self.current.add(node.id, node)
                # 2. Revise que el tipo de la expresión (si lo hay) es el mismo
                if node.value:
                        self.visit(node.value)
                        #assert(node.typename.typename == node.value.type.name) ¿?
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                       # assert(node.typename == node.value.type.name)
                # 4. Si no hay expresión, establecer un valor inicial para el valor
                else:
                        node.value = None
<<<<<<< HEAD
                
                

        def visit_Typename(self,node):
                # 1. Revisar que el nombre de   tipo es válido que es actualmente un tipo
                
                if (node.type not in self.tipos):
                    error(node.lineno,"%s Tipo Invalido" %node.type)
=======
                node.type = self.current.lookup(node.typename.typename)
                print (node.type)
                assert(node.type)

        def visit_Typename(self,node):
                print ("visit_Typename")
                # 1. Revisar que el nombre de   tipo es válido que es actualmente un tipo
                if (node.type not in tipos):
                    error(node.lineno,"Tipo Invalido")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                else:
                    self.visit(node.type)

        def visit_Location(self,node):
                print ("visit_Location")
                # 1. Revisar que la localización es una variable válida o un valor constante
                # 2. Asigne el tipo de la localización al nodo
                if (self.current.lookup(node.location) not in  self.tipos):
                        error(node.lineno,"La localizacion no es una variable valida")
                else:
                    node.type = self.current.lookup(node.location)

        def visit_LoadLocation(self,node):
<<<<<<< HEAD
                
                # 1. Revisar que loa localización cargada es válida.
                # 2. Asignar el tipo apropiado
                

                sym = self.current.lookup(node)
                
                if (sym==None): 
                     error(node.lineno,"La variable no ah sido declarada")
                     node.type=None;
                else:
                    node.type = sym
                

        def visit_Literal(self,node):

                
                
                if(node.value.value=='false'):
                    node.value.value=False;
                if(node.value.value=='true'):
                    node.value.value=True;
                if isinstance(node.value.value, types.BooleanType):
                        
                        node.type = self.symtab.lookup("bool")
                elif isinstance(node.value.value, types.IntType):
                        
                        node.type = self.symtab.lookup("int")
                elif isinstance(node.value.value, types.FloatType):
                        
                        node.type = self.symtab.lookup("float")
                elif isinstance(node.value.value, types.StringTypes):
                       
=======
                print ("visit_LoadLocation")
                print ("node : ", node)
                # 1. Revisar que loa localización cargada es válida.
                # 2. Asignar el tipo apropiado
                print ("current:", self.current)
                print ("symtab:", self.symtab)
                sym = self.current.lookup(node.name)
                print ("node.name:",node.name)
                print ("sym:",type(sym))
                assert(sym)
                node.type = sym

        def visit_Literal(self,node):
                print ("visit_Literal")
                print ("node : ", node.value)
                # Adjunte un tipo apropiado a la constante
                print ("isString?",node.isString())
                #if isinstance(node.value, types.BooleanType):
                #if isinstance(node.value, bool):
                if (node.isBoolean()):
                        node.type = self.symtab.lookup("bool")
                #elif isinstance(node.value, types.IntType):
                #elif isinstance(node.value, int):
                #elif isinstance(node.value, int):
                elif(node.isInteger()):
                        node.type = self.symtab.lookup("int")
                #elif isinstance(node.value, types.FloatType):
                #elif isinstance(node.value, float):
                elif (node.isFloat()):
                        node.type = self.symtab.lookup("float")
                #elif isinstance(node.value, types.StringTypes):
                #elif isinstance(node.value, str):
                elif(node.isString()):
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                        node.type = self.symtab.lookup("string")
               #     print ("node type",node.type)

                print ("tipo : ", node.type)

        def visit_PrintStatement(self, node):
                print ("visit_PrintStatement")
                self.visit(node.expr)
                print ("node.expr",node.expr)
                node.type = self.current.lookup(node.expr.type)
                print ("tipo:",node.type)

        def visit_Extern(self, node):
                print ("visit_Extern")
                # obtener el tipo retornado
                # registe el nombre de la función
                self.visit(node.func_prototype)

<<<<<<< HEAD
        def visit_FuncPrototype(self, node): # ¿?
                self.push_symtab(node)
                self.visit(node.typename)
                node.type = self.symtab.lookup(node.typename)
                if self.symtab.lookup(node.id):
                        error(node.lineno, "Símbol %s ya definido" % node.id)
                else:
                    self.symtab.add(node.id, node.type) # ¿?
                self.visit(node.params)
                
                if not node.params.__class__.__name__ == "Empty" :
                    self.symtab.add(node.id , node.params.param_decls[0].type)
                self.pop_symbol()
                

        def visit_Parameters(self, node):
                
=======
        def visit_FuncPrototype(self, node):
                print ("visit_FuncPrototype")
                node.type = self.symtab.lookup(node.typename)
                print ("visit_FuncPrototype")
                if self.symtab.lookup(node.id):
                        error(node.lineno, "Símbol %s ya definido" % node.id)
                else:
                    self.symtab.add(node.id, node.type)
                self.visit(node.params)

        def visit_Parameters(self, node):
                print ("visit_Parameters")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                for p in node.param_decls:
                        self.visit(p)

        def visit_ParamDecl(self, node):
<<<<<<< HEAD
               
                node.type = self.current.lookup(node.typename)
                self.current.add(node.id,node.type)
                #node.type = self.symtab.lookup(node.typename.typename) ¿?

        def visit_Group(self, node):
                
                
=======
                print ("visit_ParamDecl")
                print ("node:",node)
                print ("typename",node.typename)
                self.current.add(node.id,self.current.lookup(node.typename))
                node.type = self.current.lookup(node.typename)
                #node.type = self.symtab.lookup(node.typename.typename) ¿?

        def visit_Group(self, node):
                print ("visit_Group")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                self.visit(node.expression)
                node.type = node.expression.type

        def visit_RelationalOp(self, node):
                print ("visit_RelationalOp")
                print ("node : ", node)
                print ("node_izq : ", node.left)
                print ("node_der : ", node.right)
                self.visit(node.left)
                self.visit(node.right)
                if not node.left.type == node.right.type:
                        error(node.lineno, "Operandos de relación no son del mismo tipo")
                elif not golex.operators[node.op] in node.left.type.bin_ops:
                        error(node.lineno, "Operación no soportada con este tipo")
                node.type = self.symtab.lookup('bool')

        def visit_FunCall(self, node):
<<<<<<< HEAD
                if not self.current.lookup(node.id):
                    error(node.lineno,"La funcion %s no esta definida " %node.id)
                else:
                    self.visit(node.params)
                    #self.visit(node.id)
                    node.type = node.id
                

        def visit_ExprList(self, node):
            
=======
                print ("visit_FunCall")
                print ("node : ", node.id)
                print ("buscando:",self.current.lookup(node.id))
                print ("tabla:",self.current)
                if not self.current.lookup(node.id):
                    error(node.lineno,"La funcion no esta definida ")
                else:
                    self.visit(node.params)
                    node.type = node.id

        def visit_ExprList(self, node):
            print ("visit_ExprList")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
            for p in node.expressions:
                self.visit(p)

        def visit_Empty(self, node):
                pass

        # Agregados

        def visit_Statements(self,node):
<<<<<<< HEAD
            
=======
            print ("visit_Statements")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
            for s in node.statements:
                    self.visit(s)

        def visit_Statement(self,node):
<<<<<<< HEAD
           

            self.visit(node.statement)

        def visit_StoreVar(self,node):#j
=======
            print ("visit_Statement")
            self.visit(node.statement)

        def visit_StoreVar(self,node):
            print ("visit_StoreVar")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
            sym = self.current.lookup(node.name)
            assert(sym)
            node.type = sym.type

        def visit_Return(self,node):
            print ("visit_Return")
            self.visit(node.expression)

        def visit_Opper(self,node):
<<<<<<< HEAD
            if(self.current.lookup(node.ID)==None):
                self.current.add(node.ID,gotype.int_type)
            else:
                error(node.lineno,"La variable %s ya ha sido agregada" %node.id)
            
            node.type = gotype.int_type
            node.value=node

        def visit_ForStatement(self,node):
           
=======
            print ("visit_Opper")
            sym = self.current.lookup(node.ID)
            assert(sym)
            node.type = sym.type

        def visit_ForStatement(self,node):
            print ("visit_ForStatement")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
            self.visit(node.condition)
            if not node.condition.type == gotype.boolean_type:
                error(node.lineno,"Tipo incorrecto para la condicion for")
            else:
                
                self.visit(node.statement)
<<<<<<< HEAD
                
                if not node.statement.statement.value == gotype.int_type:
=======
                if not node.statement.type == gotype.int_type:
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
                    error(node.lineno,"Tipo incorrecto para la asignacion for")
                else:
                    self.visit(node.expression)
                    
                    if (node.expression.statement.type not in self.tipos): 
                        error(node.lineno,"Tipo incorrecto para la expresion for")
                    else:
                        self.visit(node.body)

<<<<<<< HEAD
        def visit_FuncDeclaration(self,node):#?¡
            node.type = self.symtab.lookup(node.typename.typename)
            if self.symtab.lookup(node.id):
                    error(node.lineno, "Símbol %s ya definido" %node.id)
=======
        def visit_FuncDeclaration(self,node):
            print ("visit_FuncDeclaration")
            print ("node")
            node.type = self.symtab.lookup(node.typename.typename)
            print("tipo",node.type)
            if self.symtab.lookup(node.id):
                    error(node.lineno, "Símbol %s ya definido" % node.id)
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
            else:
                self.symtab.add(node.id, node.type)
            self.visit(node.params)
            self.visit(node.body)
<<<<<<< HEAD
            
=======
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d

        def visit_Number(self,node):
            print ("visit_Number")
            if not(node.type == gotype.int_type or node.type == gotype.float_type):
                error(node.lineno,"Error en el tipo de dato %s" %node.id)
            else:
                self.visit(node.expression)

<<<<<<< HEAD
        def visit_ReadStatement(self,node):#j
            
            self.visit(node.expression)

        def visit_WriteStatement(self,node):#j
=======
        def visit_ReadStatement(self,node):
            print ("visit_ReadStatement")
            self.visit(node.expression)

        def visit_WriteStatement(self,node):
            print ("visit_WriteStatement")
>>>>>>> ea47bd0d33f2dc974145a97374958d246c58957d
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