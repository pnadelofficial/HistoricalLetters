import matplotlib.pyplot as plt
import networkx as nx


def draw_planar(graph):
    plt.figure(1, figsize=(8, 4.5))
    # color based on ranks
    ranks = list(nx.get_node_attributes(graph, "rank").values())
    num_ranks = max(ranks) - min(ranks) + 1
    # draw the graph
    node_size = 100
    pos = nx.planar_layout(graph)
    nx.draw_networkx_edges(graph, pos, alpha=.2, node_size=node_size)
    node_collection = nx.draw_networkx_nodes(
        graph, pos, cmap=plt.cm.get_cmap("plasma", num_ranks),
        node_size=node_size, node_color=ranks)
    plt.colorbar(node_collection)
    plt.show()
