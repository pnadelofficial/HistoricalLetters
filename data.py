import numpy as np


def load_letters(fname):
    letters = np.loadtxt(fname, delimiter='\t', skiprows=1, dtype=str)
    # remove comments
    for i in range(letters.shape[0]):
        for j in range(letters.shape[1]):
            index = max(letters[i, j].find('('), letters[i, j].find('['))
            if index > -1:
                letters[i, j] = letters[i, j][:index]
    # remove whitespace
    letters = np.char.strip(letters)
    # fix incorrect names
    name_dict = {"Lord J. Butler": "Lord John Butler",
                 "Sir John Warr": "John Warre",
                 "Willam Legge": "William Legge"}
    for bad_name, new_name in name_dict.items():
        letters[letters == bad_name] = new_name
    return letters
