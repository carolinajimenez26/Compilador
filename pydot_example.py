import pydotplus

graph = pydotplus.Dot(graph_type = 'digraph')

n1 = pydotplus.Node("A", shape='box', style="filled", fillcolor="green")
n2 = pydotplus.Node("B", shape='box', style="filled", fillcolor="green")
graph.add_edge(pydotplus.Edge(n1,n2))

graph.add_node(n1)

graph.write_png("ans.png")
