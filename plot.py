import matplotlib.pyplot as plt
import networkx as nx


def draw_planar(graph):
    plt.figure(1, figsize=(8, 4.5))
    pos = nx.planar_layout(graph)
    nx.draw_networkx(graph, pos=pos, with_labels=False)
    plt.show()
