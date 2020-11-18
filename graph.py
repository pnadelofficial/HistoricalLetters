import networkx as nx
import numpy as np


def to_from(letter_array):
    to_from = letter_array[:, [1, 5]]
    to_from = remove_empty(to_from)
    to_from_graph = nx.convert.from_edgelist(to_from, create_using=nx.MultiGraph)
    return to_from_graph


def remove_empty(str_array):
    str_array = np.delete(str_array, np.any(str_array == "", axis=1), axis=0)
    return str_array
