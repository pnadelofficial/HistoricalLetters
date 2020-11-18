import data
import graph
import plot


hierarchy = data.load_heirarchy("data/Hierarchy.tsv")
letter_sets = ["data/BeinekieRecordLetters.tsv",
               "data/BeinekieRecordLetters2.tsv"]
for letter_set in letter_sets:
    letter_array = data.load_letters(letter_set)
    to_from_graph = graph.to_from(letter_array)
    plot.draw_planar(to_from_graph)
