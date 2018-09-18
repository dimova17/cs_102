import igraph
from igraph import Graph, plot
import numpy as np

# Создание вершин и ребер
vertices = [i for i in range(7)]
edges = [
    (0,2),(0,1),(0,3),
    (1,0),(1,2),(1,3),
    (2,0),(2,1),(2,3),(2,4),
    (3,0),(3,1),(3,2),
    (4,5),(4,6),
    (5,4),(5,6),
    (6,4),(6,5)
]

# Создание графа
g = Graph(vertex_attrs={"label":vertices},
    edges=edges, directed=False)

# Задаем стиль отображения графа
N = len(vertices)
visual_style = {
    "vertex_size": 20,
    "bbox": (2000, 2000),
    "margin": 100,
    "vertex_label_dist": 1.6,
    "edge_color": "black",
    "autocurve": True,
    "layout": g.layout_fruchterman_reingold(
    maxiter=1000,
    area=N ** 3,
    repulserad=N ** 3)}

communities = g.community_edge_betweenness(directed=False)
clusters = communities.as_clustering()
#clusters = g.community_multilevel()
pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
g.vs['color'] = pal.get_many(clusters.membership)
g.simplify(multiple=True, loops=True)
# Отрисовываем граф
plot(g, **visual_style)