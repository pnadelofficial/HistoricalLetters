import networkx as nx

import data
import graph
import plot
import stats


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
# data needed for statistics comparisons
rank_lists = []
rank_stats = []
for i, to_from_graph in enumerate(to_from_graphs):
    # add rank node attributes and make rank dictionary
    rank_dict = {}
    names = list(to_from_graph.nodes)
    for j, name in enumerate(names):
        if name not in hierarchy:
            print(name)
            rank = 10
        else:
            rank = hierarchy[name]
        to_from_graph.nodes[name]["rank"] = rank
        if rank not in rank_dict:
            rank_dict[rank] = []
        rank_dict[rank] += [j]
    print("\n")
    # output adjacency matricies
    pd_adj = nx.to_pandas_adjacency(to_from_graph, dtype=int)
    pd_adj.to_csv("output/Adj%s.csv" % (graph_names[i]))
    # inputs for statistic functions
    np_adj = pd_adj.to_numpy()
    # get statistics for each rank
    rank_lists += [stats.rank_dict_to_array(rank_dict)[0]]
    rank_stats += [stats.output_rank(np_adj, rank_dict, graph_names[i])]
    # get statistics for each person
    stats.output_people(np_adj, rank_dict, names, graph_names[i])
    # plot the graph
    plot.draw_planar(to_from_graph)

plot.rank_change(rank_lists, rank_stats)
