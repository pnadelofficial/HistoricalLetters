import data
import graph
import plot


letter_array = data.load_letters("data/BeinekieRecordLetters.tsv")
to_from_graph = graph.to_from(letter_array)
plot.draw_planar(to_from_graph)
