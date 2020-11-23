from datetime import datetime

import networkx as nx
import numpy as np


def to_from(letter_array):
    to_from = letter_array[:, [1, 5]]
    to_from = remove_empty(to_from)
    to_from_graph = nx.convert.from_edgelist(to_from, create_using=nx.MultiDiGraph)
    return to_from_graph


def to_from_dates(letter_array):
    to_from_dates = letter_array[:, [1, 5, 3]]
    to_from_dates = remove_empty(to_from_dates)
    to_from = to_from_dates[:, :2]
    # do conversion to datetime
    dates = []
    for str_date in to_from_dates[:, 2]:
        dates += [datetime.strptime(str_date, "%m/%d/%Y")]
    dates = np.asarray(dates)
    is_before = dates < datetime.strptime("12/1/1688", "%m/%d/%Y")
    # create graphs
    before_graph = nx.convert.from_edgelist(to_from[is_before], create_using=nx.MultiDiGraph)
    after_graph = nx.convert.from_edgelist(to_from[np.logical_not(is_before)],
                                           create_using=nx.MultiDiGraph)
    return (before_graph, after_graph)


def remove_empty(str_array):
    str_array = np.delete(str_array, np.any(str_array == "", axis=1), axis=0)
    return str_array
