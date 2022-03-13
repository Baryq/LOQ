import igraph

g = igraph.Graph()
g.add_vertices(5)
g.add_edges(((1, 2), (2, 3)))
print(g.shortest_paths(3, 2))
