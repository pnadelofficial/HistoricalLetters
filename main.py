import networkx as nx
import numpy as np
import pandas as pd

import data
import graph
import plot


hierarchy = data.load_hierarchy("data/Hierarchy.tsv")
letter_sets = ["data/BeinekieRecordLetters.tsv",
               "data/BeinekieRecordLetters2.tsv"]
# construct graphs
to_from_graphs = []
for letter_set in letter_sets:
    letter_array = data.load_letters(letter_set)
    to_from_graph = graph.to_from(letter_array)
    to_from_graphs += [to_from_graph]
    if letter_set == "data/BeinekieRecordLetters2.tsv":
        to_from_graphs += [*graph.to_from_dates(letter_array)]

graph_names = ["BeinekieRecordLetters",
               "BeinekieRecordLetters2",
               "BeinekieRecordLetters2Before",
               "BeinekieRecordLetters2After"]
for i, to_from_graph in enumerate(to_from_graphs):
    # add rank node attributes and make rank dictionary
    rank_dict = {}
    for j, node in enumerate(to_from_graph.nodes):
        if node not in hierarchy:
            print(node)
            rank = 10
        else:
            rank = hierarchy[node]
        to_from_graph.nodes[node]["rank"] = rank
        if rank not in rank_dict:
            rank_dict[rank] = []
        rank_dict[rank] += [j]
    print("\n")
    # output adjacency matricies
    pd_adj = nx.to_pandas_adjacency(to_from_graph, dtype=int)
    pd_adj.to_csv("output/Adj%s.csv" % (graph_names[i]))
    # get statistics for each rank
    np_adj = pd_adj.to_numpy()
    ranks = np.sort(np.asarray(list(rank_dict.keys()), dtype=int))
    num_ranks = len(ranks)
    rank_stats = np.zeros((num_ranks + 1, num_ranks + 1))
    for j, from_rank in enumerate(ranks):
        from_idx = rank_dict[from_rank]
        for k, to_rank in enumerate(ranks):
            to_idx = rank_dict[to_rank]
            num_from_to = np.sum(np_adj[from_idx][:, to_idx])
            # number of letters sent from this rank
            rank_stats[j, -1] += num_from_to
            # number of letters sent to this rank
            rank_stats[-1, k] += num_from_to
            # average number of letters from rank to rank
            rank_stats[j, k] = num_from_to/len(from_idx)
    # total number of letters
    rank_stats[-1, -1] = np.sum(rank_stats[-1])
    pd_rank_stats = pd.DataFrame(rank_stats,
                                 index=["Average From " + rank for rank in ranks.astype(str)] +
                                       ["Total Letters Received"],
                                 columns=["To " + rank for rank in ranks.astype(str)] +
                                         ["Total Letters Sent"])
    pd_rank_stats.to_csv("output/Rank%s.csv" % (graph_names[i]))
    # plot the graph
    plot.draw_planar(to_from_graph)
