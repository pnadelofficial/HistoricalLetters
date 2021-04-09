import numpy as np

import epidoc
import geodesy
import plot


# TODO test with 057-059
# dateline text from parsing EpiDocXML
epidoc_fname = "canonical-latinLit/data/phi0474/phi056/phi0474.phi056.perseus-lat1.xml"
parser = epidoc.EpiDocXMLParser(epidoc_fname)
# get a dictionary mapping known locations to lat/long
geodetic_fname = "input/loc_to_geodetic.csv"
loc_to_geodetic = geodesy.loc_to_geodetic(geodetic_fname)
plot.plot_geodetic(loc_to_geodetic, parser.sorted_unique_locs, parser.loc_to_count)
# plot year by year
unique_dates = np.unique(parser.dateline_dates[np.not_equal(parser.dateline_dates, None)])
for date in unique_dates:
    print(date)
    locations = parser.dateline_locs[parser.dateline_dates == date]
    sorted_unique_locs, unique_loc_counts = np.unique(
        locations[np.not_equal(locations, None)],
        return_counts=True
    )
    loc_to_count = dict(zip(sorted_unique_locs, unique_loc_counts))
    plot.plot_geodetic(loc_to_geodetic, sorted_unique_locs, loc_to_count)
