import data
import graph
import plot


hierarchy = data.load_hierarchy("data/Hierarchy.tsv")
letter_sets = ["data/BeinekieRecordLetters.tsv",
               "data/BeinekieRecordLetters2.tsv"]
to_from_graphs = []
for letter_set in letter_sets:
    letter_array = data.load_letters(letter_set)
    to_from_graph = graph.to_from(letter_array)
    to_from_graphs += [to_from_graph]
    if letter_set == "data/BeinekieRecordLetters2.tsv":
        to_from_graphs += [*graph.to_from_dates(letter_array)]

for to_from_graph in to_from_graphs:
    for node in to_from_graph.nodes:
        if node not in hierarchy:
            print(node)
            to_from_graph.nodes[node]["rank"] = 10
        else:
            to_from_graph.nodes[node]["rank"] = hierarchy[node]
    print("\n")
    plot.draw_planar(to_from_graph)
