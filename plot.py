import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


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


def rank_change_regularization(rank_lists, rank_stats):
    all_rank_list = []
    for rank_list in rank_lists:
        if len(all_rank_list) < len(rank_list):
            all_rank_list = rank_list

    for i, rank_list in enumerate(rank_lists):
        if len(all_rank_list) > len(rank_list):
            for j, rank in enumerate(all_rank_list):
                if rank not in rank_list:
                    rank_stats[i] = np.insert(rank_stats[i], j, 0, axis=0)
                    rank_stats[i] = np.insert(rank_stats[i], j, 0, axis=1)
    return rank_stats, all_rank_list


def rank_change(rank_lists, rank_stats):
    rank_arrays, rank_labels = rank_change_regularization(rank_lists, rank_stats)
    num_ranks = len(rank_labels)
    num_arrays = len(rank_arrays)
    # labels for bar plots
    plot_labels = ["Legge", "James II", "James II Before", "James II After"]
    tick_label = ["To %i" % (rank_label) for rank_label in rank_labels]
    # positions for bars
    total_width = .8
    width = total_width/num_arrays
    max_offset = total_width/2 - width/2
    positions = np.asarray([[x + offset for x in range(num_ranks)]
                            for offset in
                            np.linspace(-1 * max_offset, max_offset, num=num_arrays)])
    for i in range(num_ranks):
        ax = plt.subplot(num_ranks, 1, i + 1)
        for j in range(num_arrays):
            plt.bar(positions[j], rank_stats[j][i, :], width,
                    label=plot_labels[j],
                    tick_label=tick_label if j == num_arrays//2 else None)
        # axes settings
        ax.set_ylabel("Average From %i" % (rank_labels[i]))
        if i == 0:
            ax.legend()
    plt.show()
