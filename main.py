import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from data import load_letters


letters = load_letters("data/BeinekieRecordLetters.tsv")
to_from = letters[:, [1, 5]]
to_from_graph = nx.convert.from_edgelist(to_from, create_using=nx.MultiGraph)
to_from_pos = nx.planar_layout(to_from_graph)
nx.draw_networkx(to_from_graph, pos=to_from_pos, with_labels=True)
plt.show()
