import numpy as np

import epidoc
import geodesy
import plot


# TODO test with 057-059
# dateline text from parsing EpiDocXML
epidoc_fname = "canonical-latinLit/data/phi0474/phi056/phi0474.phi056.perseus-lat1.xml"
parser = epidoc.EpiDocXMLParser(epidoc_fname)
dateline_text = parser.dateline_text()
np.savetxt("output/phi056dateline.csv", dateline_text[:, np.newaxis], fmt='"%s"', delimiter=',')
# parse the datelines to get the dates
dateline_dates = parser.parse_dateline_dates()
# parse the datelines to get the locations
locations = parser.parse_dateline_locs()
np.savetxt("output/phi056locations.csv", np.vstack((locations, dateline_text)).T,
           fmt='"%s"', delimiter=',')
# save a sorted copy of the unique locations
unique_locations = set(locations)
unique_locations.remove(None)
sorted_unique_loc = np.sort(np.asarray(list(unique_locations)))
np.savetxt("output/phi056sorted_locs.csv", sorted_unique_loc[:, np.newaxis],
           fmt='"%s"', delimiter=',')
# get a dictionary mapping known locations to lat/long
geodetic_fname = "input/loc_to_geodetic.csv"
location_to_geodetic = geodesy.loc_to_geodetic(geodetic_fname)
plot.plot_geodetic(location_to_geodetic)
