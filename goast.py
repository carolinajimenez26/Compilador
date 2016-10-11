# coding: utf-8

import pydotplus

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
        return '%r' % self.expr

class Literal(AST):
    '''
    Un valor constante como 2, 2.5, o "dos"
    '''
    _fields = ['value']

    def __repr__(self):
        return '%r' % self.value

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
    _fields = ['id', 'params', 'typename', 'body']

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
    _fields = ['location', 'value']

    def __repr__(self):
        return '%r' % self.location

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
        return '%r' % self.condition

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
        return '%r' % self.expression

class FunCall(AST):
    _fields = ['id', 'params']

    def __repr__(self):
        return '%r' % self.id,self.params

class ExprList(AST):
    _fields = ['expressions']

    def append(self, e):
        self.expressions.append(e)

    def __repr__(self):
        return '%r' % self.expressions

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
        return '%r' % self.expression

class Location(AST):
    _fields = ['location']

    def __repr__(self):
        return '%r' % self.location

class Opper(AST):
    '''operacion de el estillo var++ var-- '''
    _fields = ['ID', 'op']

    def __repr__(self):
        return '%r' % self.op

class SwitchStatement(AST):
    _fields = ['condition', 'body']

    def __repr__(self):
        return '%r' % self.condition

class CaseStatement(AST):
    _fields = ['value', 'body', 'else']

    def __repr__(self):
        return '%r' % self.value

class ForStatement(AST):
    _fields = ['condition', 'statement', 'expression', 'body']

    def __repr__(self):
        return '%r' % self.condition

# ---------------------------------------------------------
# Patron Visitor
class NodeVisitor:
    '''
    Clase para visitar nodos en el AST
    '''

    def createGraph(self):
        self.graph = pydotplus.Dot("AST", graph_type = 'digraph') # grafo dirigido
        self.id = 0

    def name_node(self):
        self.id += 1
        return 'n%02d' % self.id

    def visit(self, node):
        print ("---visit---")
        '''
        Ejecuta un metodo de la forma visit_NodeName(node) donde
        NodeName es el nombre de la clase de un nodo en particular
        '''
        if node:
            print ("node : ", node)
            #method = 'visit_' + node.__class__.__name__
            #visitor = getattr(self, method, self.generic_visit)
            #return visitor(node)
            parent_node = self.generic_visit(node)
            print ("parent_node : ", parent_node)
            if parent_node:
                self.graph.add_node(parent_node)

                return parent_node

        else:
            print ("there is not node")
            return None

    def generic_visit(self, node):
        print ("---generic_visit---")
        '''
        Metodo ejecutado si no es aplicable visit_method.
        '''

        node_id = "%s %s %s"% (self.name_node(),node.__class__.__name__,node.__repr__())
        parent_node = pydotplus.Node(node_id, style="filled", fillcolor="#55B7C2")
        print ("parent_node : ", parent_node)
        print ("parent_node id :", node_id)

        for field in getattr(node, '_fields'):

            value = getattr(node, field, None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        #self.visit(item)
                        child_node = self.visit(item)
                        if child_node:
                            self.graph.add_edge(pydotplus.Edge(parent_node, child_node))

            elif isinstance(value, AST):
                #self.visit(value)
                child_node = self.visit(value)
                if child_node:
                    self.graph.add_edge(pydotplus.Edge(parent_node, child_node))

        return parent_node

    def printGraph(self,path):
        self.graph.write_png(path)


class DotVisitor(): # para crear el grafo con graphviz

    #excluidos = ["FunCall","BinaryOp","FuncPrototype","RelationalOp"]
    excluidos = ["Statements","Statement","ExprList"]

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
                    parent_node = self.visit_excluidos(node)

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
        node_id = "%s %s %s"% (self.name_node(),node.__class__.__name__,node.__repr__())
        print ("hoja : ", node_id)
        return pydotplus.Node(node_id, label = node.__repr__(),shape='box', style="filled", fillcolor="#7BC255")

    def visit_non_leaf(self,node):
        print ("---visit_non_leaf---")
        node_id = "%s %s %s"% (self.name_node(),node.__class__.__name__,node.__repr__())
        parent_node = pydotplus.Node(node_id, label=node.__class__.__name__, style="filled", fillcolor="#55B7C2")
        print ("agrega : ", node_id)

        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value,list):
                for item in value:
                    if isinstance(item,AST):
                        child_node = self.visit(item)
                        print ("arco : ")
                        self.graph.add_edge(pydotplus.Edge(parent_node, child_node))

            elif isinstance(value,AST):
                child_node = self.visit(value)
                print ("arco : ", child_node.__repr__())
                self.graph.add_edge(pydotplus.Edge(parent_node, child_node))

        print ("returning!!")
        return parent_node

def flatten(top):
    class Flattener(NodeVisitor):

        def __init__(self):
            self.depth = 0
            self.nodes = []
            NodeVisitor.createGraph(self)

        def generic_visit(self, node):
            #self.nodes.append((self.depth, node))
            #self.depth += 1
            NodeVisitor.generic_visit(self, node)
            #self.depth -= 1

    d = Flattener()
    d.visit(top)
    d.printGraph("answer.png")
    #return d.nodes
