import numpy as np
import pandas as pd


def output_rank(np_adj, rank_dict, graph_name):
    # get statistics for each rank
    ranks, num_ranks = rank_dict_to_array(rank_dict)
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
    # add labels to rank statistics
    pd_rank_stats = pd.DataFrame(rank_stats,
                                 index=["Average From " + rank for rank in ranks.astype(str)] +
                                       ["Total Letters Received"],
                                 columns=["To " + rank for rank in ranks.astype(str)] +
                                         ["Total Letters Sent"])
    pd_rank_stats.to_csv("output/Rank%s.csv" % (graph_name))


def output_people(np_adj, rank_dict, person_names, graph_name):
    # get statistics for each person
    ranks, num_ranks = rank_dict_to_array(rank_dict)
    person_stats = np.zeros((len(person_names), 2 * num_ranks), dtype=int)
    for j, rank in enumerate(ranks):
        # letters to people from rank
        person_stats[:, j] = np.sum(np_adj[rank_dict[rank]], axis=0)
        # letters from rank to people
        person_stats[:, j + num_ranks] = np.sum(np_adj[:, rank_dict[rank]], axis=1)
    # add labels to person statistics
    pd_person_stats = pd.DataFrame(person_stats,
                                   index=person_names,
                                   columns=["To " + rank for rank in ranks.astype(str)] +
                                           ["From " + rank for rank in ranks.astype(str)])
    pd_person_stats.to_csv("output/People%s.csv" % (graph_name))


def rank_dict_to_array(rank_dict):
    ranks = np.sort(np.asarray(list(rank_dict.keys()), dtype=int))
    num_ranks = len(ranks)
    return (ranks, num_ranks)
