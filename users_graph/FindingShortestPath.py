import igraph
from FrequentFunctions import read

dct = read('graphFolder/dct.txt')
graph = igraph.Graph()

for i in dct:
    graph.add_vertices([i, *map(str, dct[i]['friends'])])

for i in dct:
    graph.add_edges([*map(lambda x: (i, str(x)), dct[i]['friends'])])

graph.simplify()
print(graph.shortest_paths('305617399', '5016211'))
