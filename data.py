import numpy as np


def load_heirarchy(fname):
    names = np.loadtxt(fname, delimiter='\t', skiprows=1, dtype=str, usecols=0)
    names = remove_comments(names[np.newaxis])[0]
    ranks = np.loadtxt(fname, delimiter='\t', skiprows=1, dtype=int, usecols=1)
    return dict(zip(names, ranks))


def load_letters(fname):
    letters = np.loadtxt(fname, delimiter='\t', skiprows=1, dtype=str)
    letters = remove_comments(letters)
    # fix incorrect names
    name_dict = {"Lord J. Butler": "Lord John Butler",
                 "Sir John Warr": "John Warre",
                 "Willam Legge": "William Legge"}
    for bad_name, new_name in name_dict.items():
        letters[letters == bad_name] = new_name
    return letters


def remove_comments(str_array):
    # remove comments
    for i in range(str_array.shape[0]):
        for j in range(str_array.shape[1]):
            index = max(str_array[i, j].find('('), str_array[i, j].find('['))
            if index > -1:
                str_array[i, j] = str_array[i, j][:index]
    # remove whitespace
    str_array = np.char.strip(str_array)
    return str_array
