import numpy as np


def load_hierarchy(fname):
    names = np.loadtxt(fname, delimiter='\t', skiprows=1, dtype=str, usecols=0)
    names = remove_comments(names[np.newaxis])[0]
    name_dict = {"Mr. Samuel Pepys Esq.": "Samuel Pepys",
                 "Dartmouth": "Lord Dartmouth",
                 "Philip Frowd": "Mr. Frowd",
                 "James II": "King James II",
                 "Preston": "Lord Preston",
                 "Berkeley": "Lord Berkeley",
                 "Dover": "Lord Dover",
                 "Feversham": "Earl of Feversham",
                 "Berwick": "Duke of Berwick"}
    names = map_values(names, name_dict)
    ranks = np.loadtxt(fname, delimiter='\t', skiprows=1, dtype=int, usecols=1)
    return dict(zip(names, ranks))


def load_letters(fname):
    letters = np.loadtxt(fname, delimiter='\t', skiprows=1, dtype=str)
    letters = remove_comments(letters)
    # fix incorrect names
    if fname == "data/BeinekieRecordLetters.tsv":
        name_dict = {"Lord J. Butler": "Lord John Butler",
                     "Sir John Warr": "John Warre",
                     "Willam Legge": "William Legge"}
    elif fname == "data/BeinekieRecordLetters2.tsv":
        name_dict = {"The Prince of Orange": "Prince of Orange",
                     "John Lord Berkeley, commander of the Montaigne and others": "Lord Berkeley",
                     "Mr. Frowd": "Phillip Frowd",
                     "Phil. Frowd Esq., then to Pepys": ["Phillip Frowd", "Samuel Pepys"],
                     "King James II, witnessed by Pepys": ["King James II", "Samuel Pepys"]}
    letters = map_values(letters, name_dict)
    return letters


def map_values(str_array, str_dict):
    for bad_str, new_str in str_dict.items():
        # replace row in place
        if type(new_str) is str:
            str_array[str_array == bad_str] = new_str
        # replace row in place and append additional rows
        elif type(new_str) is list:
            # iterate over rows with bad_str
            for row_index in np.argwhere(np.any(str_array == bad_str, axis=1)):
                row = str_array[row_index]
                row_replace = row == bad_str
                for i in range(len(new_str)):
                    row[row_replace] = new_str[i]
                    # in place replacement
                    if i == 0:
                        str_array[row_index] = row
                    # appending additional rows
                    else:
                        str_array = np.append(str_array, row[:np.newaxis], axis=0)
    return str_array


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
