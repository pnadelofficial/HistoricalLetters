import numpy as np


def load_letters(fname):
    letters = np.loadtxt(fname, delimiter='\t', skiprows=1, dtype=str)
    for i in range(letters.shape[0]):
        for j in range(letters.shape[1]):
            index = max(letters[i, j].find('('), letters[i, j].find('['))
            if index > -1:
                letters[i, j] = letters[i, j][:index]
    letters = np.char.strip(letters)
    return letters
