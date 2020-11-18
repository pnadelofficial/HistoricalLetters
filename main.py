import data
import graph
import plot


hierarchy = data.load_hierarchy("data/Hierarchy.tsv")
letter_sets = ["data/BeinekieRecordLetters.tsv",
               "data/BeinekieRecordLetters2.tsv"]
for letter_set in letter_sets:
    letter_array = data.load_letters(letter_set)
    to_from_graph = graph.to_from(letter_array)
    print(letter_set)
    for node in to_from_graph.nodes:
        if node not in hierarchy:
            print(node)
    print("\n")
    plot.draw_planar(to_from_graph)
