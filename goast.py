# coding: utf-8

import pydotplus
import re

# ---------------------------------------------------------
# Nodos del Arbol de Sintaxis Abstracto
class AST:
    '''
    Clase base. No se usará directamente
    '''
    _fields = []
    def __init__(self, *args, **kwargs):
        flag = False
        assert len(args) == len(self._fields)
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
        # Asigna argumentos adicionales si son entregados
        for name, value in kwargs.items():
            setattr(self, name, value)
            if (name == "isLeaf"):
                flag = True

        setattr(self,"isLeaf",flag)

def validate_fields(**fields):
    def validator(cls):
        old_init = cls.__init__
        def __init__(self, *args, **kwargs):
            old_init(self, *args, **kwargs)
            for field,expected_type in fields.items():
                assert isinstance(getattr(self, field), expected_type)
        cls.__init__ = __init__
        return cls
    return validator


class PrintStatement(AST):
    '''
    print expression ;
    '''
    _fields = ['expr']

    def __repr__(self):
        return ''

class Literal(AST):
    '''
    Un valor constante como 2, 2.5, o "dos"
    '''
    _fields = ['value']

    def __repr__(self):
        return '%r' % self.value

    def isBoolean(self):
        print ("isBoolean")
        print (self.value)
        p = re.compile("true|false")
        if (p.match(str(self.value).strip("'")) != None):
            return True
        else:
            return False

    def isString(self):
        print ("isString")
        p = re.compile("'.*'")
        if (p.match(str(self.value)) != None):
            return True
        else:
            return False

    def isInteger(self):
        p = re.compile("0[xX][0-9a-fA-F]+|[\d]+|0[0-7]*")
        if (p.match(str(self.value).strip("'")) != None):
            return True
        else:
            return False

    def isFloat(self):
        p = re.compile("(\d*\.\d+|\d+\.\d*)([eE][-+]?\d+)?|\d+([eE][-+]?\d+)")
        if (p.match(str(self.value).strip("'")) != None):
            return True
        else:
            return False

class Program(AST):
    _fields = ['program']

    def __repr__(self):
        return ''

@validate_fields(statements=list)
class Statements(AST):
    _fields = ['statements']

    def append(self,e):
        self.statements.append(e)

    def __repr__(self):
        #return '(%r)' % self.statements
        return ""

class Statement(AST):
    _fields = ['statement']

    def __repr__(self):
        #return '%r' % self.statement
        return ""

class Extern(AST):
    _fields = ['func_prototype']

    def __repr__(self):
        return ''

class FuncPrototype(AST):
    _fields = ['id', 'params', 'typename']

    def __repr__(self):
        return '%r' % self.id

@validate_fields(param_decls=list)
class Parameters(AST):
    _fields = ['param_decls']

    def append(self,e):
        self.param_decls.append(e)

    def __repr__(self):
        return ''

class ParamDecl(AST):
    _fields = ['id', 'typename']

    def __repr__(self):
        return '%r' % self.id

class AssignmentStatement(AST):
    _fields = ['location', 'value', 'asig']

    def __repr__(self):
        return '%r' % self.asig

class ConstDeclaration(AST):
    _fields = ['id', 'value']

    def __repr__(self):
        return '%r' % self.id

class VarDeclaration(AST):
    _fields = ['id', 'typename', 'value']

    def __repr__(self):
        return '%r' % self.id

class IfStatement(AST):
    _fields = ['condition', 'then_b', 'else_b']

    def __repr__(self):
        return ''

class WhileStatement(AST):
    _fields = ['condition', 'body']

    def __repr__(self):
        return ''

class LoadLocation(AST):
    _fields = ['name']

    def __repr__(self):
        return '%r' % self.name

class StoreVar(AST):
    _fields = ['name']

    def __repr__(self):
        return '%r' % self.name

class UnaryOp(AST):
    _fields = ['op', 'left']

    def __repr__(self):
        return '%r' % self.op

class BinaryOp(AST):
    _fields = ['op', 'left', 'right']

    def __repr__(self):
        return '%r' % self.op

class RelationalOp(AST):
    _fields = ['op', 'left', 'right']

    def __repr__(self):
        return '%r' % self.op

class Group(AST):
    _fields = ['expression']

    def __repr__(self):
        return ''

class FunCall(AST):
    _fields = ['id', 'params']

    def __repr__(self):
        return '%r' % self.id

class ExprList(AST):
    _fields = ['expressions']

    def append(self, e):
        self.expressions.append(e)

    def __repr__(self):
        return ""

class Empty(AST):
    _fields = []

    def __repr__(self):
        return ''


# Agregados

class TypeName(AST):
    _fields = ['typename']

    def __repr__(self):
        return '%r' % self.typename

class Return(AST):
    _fields = ['expression']

    def __repr__(self):
        return ''

class Location(AST):
    _fields = ['location']

    def __repr__(self):
        return '%r' % self.location

class Opper(AST):
    '''operacion de el estillo var++ var-- '''
    _fields = ['ID', 'op']

    def __repr__(self):
        return '%r' % self.op

class ForStatement(AST):
    _fields = ['statement','condition', 'expression', 'body']

    def __repr__(self):
        return ''

class FuncDeclaration(AST):
    _fields = ['id', 'params', 'typename', 'body']

    def __repr__(self):
        return '%r' % self.id

class ReadStatement(AST):
    _fields = ['expression']

    def __repr__(self):
        return ""

class WriteStatement(AST):
    _fields = ['expression']

    def __repr__(self):
        return ""

# ---------------------------------------------------------
# NO MODIFIQUE
class NodeVisitor(object):
    '''
    Clase para visitar nodos del árbol de sintaxis.  Se modeló a partir
    de una clase similar en la librería estándar ast.NodeVisitor.  Para
    cada nodo, el método visit(node) llama un método visit_NodeName(node)
    el cual debe ser implementado en la subclase.  El método genérico
    generic_visit() es llamado para todos los nodos donde no hay coincidencia
    con el método visit_NodeName().
    Es es un ejemplo de un visitante que examina operadores binarios:
        class VisitOps(NodeVisitor):
            visit_Binop(self,node):
                print("Operador binario", node.op)
                self.visit(node.left)
                self.visit(node.right)
            visit_Unaryop(self,node):
                print("Operador unario", node.op)
                self.visit(node.expr)
        tree = parse(txt)
        VisitOps().visit(tree)
    '''
    def visit(self,node):
        '''
        Ejecuta un método de la forma visit_NodeName(node) donde
        NodeName es el nombre de la clase de un nodo particular.
        '''
        if node:
            method = 'visit_' + node.__class__.__name__
            # visitor es el metodo que visita el nodo, primero pregunta
            # si el nodo ya tiene este metodo, para asignarlo a visitor,
            # si no, entonces le asigna el metodo generic_visit
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
            # retorna el llamado a la funcion que visita el nodo
        else:
            return None

    def generic_visit(self,node):
        '''
        Método ejecutado si no se encuentra médodo aplicable visit_.
        Este examina el nodo para ver si tiene _fields, es una lista,
        o puede ser recorrido completamente.
        '''
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list): # si value es una lista
                for item in value: # recorremos los elementos de la lista
                    if isinstance(item,AST): # si el item es un AST
                        self.visit(item) # lo debemos visitar
            elif isinstance(value, AST): # si value es un AST
                self.visit(value) # debemos recorrerlo


class DotVisitor(): # para crear el grafo con graphviz

    excluidos = ["Statement","ExprList","Parameters"]

    def __init__(self):
        self.graph = pydotplus.Dot("AST", graph_type = 'digraph') # grafo dirigido
        self.id = 0

    def name_node(self):
        self.id += 1
        return 'n%02d' % self.id

    def printGraph(self,path):
        self.graph.write_png(path)

    def visit(self, node):
        if node:
            if (node.isLeaf):
                parent_node = self.visit_leaf(node)
                self.graph.add_node(parent_node)
            else:
                print ("class name : ",str(node.__class__.__name__))
                #method = 'visit_' + node.__class__.__name__
                if (str(node.__class__.__name__)  in self.excluidos):
                    #parent_node = self.visit_excluidos(node)
                #else:
                    print ("you are excluded!")
                    parent_node = self.visit_non_leaf(node)

                    #parent_node = self.visit_non_leaf(node)

                else:
                    print ("you are ok")
                    parent_node = self.visit_non_leaf(node)

                    self.graph.add_node(parent_node)
        return parent_node

    def visit_excluidos(self,node):
        print ("visit_excluidos")
        node_id = "%s %s"% (self.name_node(),node.__repr__())
        parent_node = pydotplus.Node(node_id,label="Exluido",shape='box3d', style="filled", fillcolor="red")

        for i in range (1,len(node._fields)):
            if (not isinstance(getattr(node,node._fields[i]) , list) ):
                child_node = self.visit(getattr(node,node._fields[i]))
                self.graph.add_edge(pydotplus.Edge(parent_node, child_node))
            else:
                for foo in getattr(node,node._fields[i]):
                    if isinstance(foo,AST):
                        child_node = self.visit(foo)
                        self.graph.add_edge(pydotplus.Edge(parent_node, child_node))
        return parent_node

    def visit_leaf(self, node):
        print ("---visit_leaf---")
        node_id = "%s %s"% (self.name_node(),node.__class__.__name__)
        print ("hoja : ", node_id)
        print ("id : ", node_id)
        child_node = pydotplus.Node(node_id, label = node.__repr__(),shape='box', style="filled", fillcolor="#7BC255")
        return child_node

    def visit_non_leaf(self,node):
        print ("---visit_non_leaf---")
        node_id = "%s %s"% (self.name_node(),node.__class__.__name__)
        parent_node = pydotplus.Node(node_id, label = node.__class__.__name__+" "+node.__repr__(), style="filled", fillcolor="#55B7C2")
        print ("agrega : ", node_id)

        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value,list):
                for item in value:
                    if isinstance(item,AST):
                        child_node = self.visit(item)

                        print ("nombresito : ", child_node.get_name())
                        #self.graph.del_node(child_node)
                        #if (child_node.get_name().split(" ")[1][:-1] not in self.excluidos):
                        self.graph.add_edge(pydotplus.Edge(parent_node, child_node))

            elif isinstance(value,AST):
                child_node = self.visit(value)
                print ("arco : ", child_node.__repr__())
                #if (child_node.get_name().split(" ")[1][:-1] not in self.excluidos):
                self.graph.add_edge(pydotplus.Edge(parent_node, child_node))

        print ("returning!!")
        return parent_node


def flatten(top):
    class Flattener(NodeVisitor):

        def __init__(self):
            self.depth = 0
            self.nodes = []

        def generic_visit(self, node):
            self.nodes.append((self.depth, node.__class__.__name__ + " " + node.__repr__()))
            self.depth += 1
            NodeVisitor.generic_visit(self, node)
            self.depth -= 1

    d = Flattener()
    d.visit(top)
    return d.nodes
