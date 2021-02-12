import numpy as np

import epidoc

fname = "canonical-latinLit/data/phi0474/phi056/phi0474.phi056.perseus-lat1.xml"
parser = epidoc.EpiDocXMLParser(fname)
dateline_text = parser.dateline_text()
np.savetxt("output/phi056dateline.csv", dateline_text[:, np.newaxis], fmt='"%s"', delimiter=',')

locations = parser.parse_dateline_locs()
np.savetxt("output/phi056locations.csv", np.vstack((locations, dateline_text)).T,
           fmt='"%s"', delimiter=',')
unique_locations = set(locations)
print(unique_locations)
print()
