import networkx as nx


def to_from(letter_array):
    to_from = letter_array[:, [1, 5]]
    to_from_graph = nx.convert.from_edgelist(to_from, create_using=nx.MultiGraph)
    return to_from_graph
