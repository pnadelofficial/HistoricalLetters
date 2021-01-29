import numpy as np

import data

fname = "canonical-latinLit/data/phi0474/phi056/phi0474.phi056.perseus-lat1.xml"
parser = data.EpiDocXMLParser(fname)
dateline_text = parser.dateline_text()[:, np.newaxis]
np.savetxt("output/phi056dateline.csv", dateline_text, fmt='"%s"', delimiter=',')
