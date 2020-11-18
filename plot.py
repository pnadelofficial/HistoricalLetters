import matplotlib.pyplot as plt
import networkx as nx


def draw_planar(graph):
    pos = nx.planar_layout(graph)
    nx.draw_networkx(graph, pos=pos, with_labels=True)
    plt.show()
