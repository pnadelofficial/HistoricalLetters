import numpy as np

import epidoc


# dateline text from parsing EpiDocXML
fname = "canonical-latinLit/data/phi0474/phi056/phi0474.phi056.perseus-lat1.xml"
parser = epidoc.EpiDocXMLParser(fname)
dateline_text = parser.dateline_text()
np.savetxt("output/phi056dateline.csv", dateline_text[:, np.newaxis], fmt='"%s"', delimiter=',')
# parse the datelines to get the locations
locations = parser.parse_dateline_locs()
np.savetxt("output/phi056locations.csv", np.vstack((locations, dateline_text)).T,
           fmt='"%s"', delimiter=',')
# save a sorted copy of the unique locations
unique_locations = set(locations)
unique_locations.remove(None)
sorted_unique_loc = np.sort(np.asarray(list(unique_locations)))
print(sorted_unique_loc)
np.savetxt("output/phi056sorted_locs.csv", sorted_unique_loc[:, np.newaxis],
           fmt='"%s"', delimiter=',')
