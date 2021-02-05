from lxml import etree
import numpy as np


ignore_tokens = [
    "",
    "Scr.",
    "Scr.,",
]

names = [
    "Attici Ficuleano",
    "Pompeiano"
]

names_tokenized = [name.split(' ') for name in names]


class EpiDocXMLParser():
    def __init__(self, fname):
        self.tree = etree.parse(fname)
        # get edition div, which contains all relevant info
        edition_path = "./{*}text/{*}body/{*}div[@type='edition']"
        edition_divs = self.tree.findall(edition_path)
        if len(edition_divs) > 1:
            raise ValueError("Expected XML file with one edition div")
        self.edition_div = edition_divs[0]
        # define selectors used for different tags
        self.sels = {
            "books": "{*}div[@type='textpart'][@subtype='Book']",
            "letters": "{*}div[@type='textpart'][@subtype='letter']",
            "opener": "{*}label[@rend='opener']",
            "dateline": "{*}seg[@rend='dateline']",
            "date": "{*}date",
        }
        # get tags used by methods
        self.datelines = self.edition_div.findall(
            self.rel_path([
                self.sels["books"],
                self.sels["letters"],
                self.sels["opener"],
                self.sels["dateline"],
            ])
        )

    def dateline_text(self):
        return np.asarray(
            [etree.tostring(dateline, encoding=str, method="text").strip()
             for dateline in self.datelines]
        )

    def parse_dateline_locs(self):
        datelines = self.dateline_text()
        locations = []
        # get one location for every dateline
        for dateline in datelines:
            location = None
            # tokenize dateline for easier parsing logic
            tokens = dateline.split(" ")
            i = 0
            while i < len(tokens):
                token = tokens[i]
                # skip useless tokens
                if token in ignore_tokens:
                    pass
                # parse words with uppercase first letter as location
                elif token[0].isupper():
                    if token == "Patris":
                        # unsure about mapping
                        location = "Patra"
                    elif token[-2:] == "ae":
                        location = token[:-1]
                    elif token[-2:] == "is":
                        location = token[:-2] + "s"
                    elif token[-2:] == "ii":
                        location = token[:-1] + "um"
                    elif token[-1:] == "i":
                        location = token + "um"
                    else:
                        # raise ValueError("Unexpected dateline token for location: " + token)
                        pass
                # parse words after "in"
                elif token == "in":
                    # parse people's houses by checking for matching name
                    for j, name_tokens in enumerate(names_tokenized):
                        for k, name_token in enumerate(name_tokens):
                            if name_token != tokens[i + k + 1]:
                                break
                            elif k == len(name_tokens) - 1:
                                location = names[j] + " house"
                        if location is not None:
                            break
                    if location is None:
                        next_token = tokens[i + 1]
                        if next_token[0].isupper():
                            if next_token[-1] == "o":
                                location = next_token[:-1] + "um"
                            else:
                                location = next_token
                # parse words after "ad"
                elif token == "ad":
                    next_token = tokens[i + 1]
                    if next_token[0].isupper():
                        if next_token[-2:] == "um":
                            location = next_token[:-1] + "s"
                # parse "ibidem"
                elif token == "ibidem" or token == "ibid":
                    location = locations[-1]
                else:
                    # raise ValueError("Unexpected dateline token: " + token)
                    pass

                # stop if location is found
                if location is not None:
                    break
                i += 1
            locations.append(location)
        return np.asarray(locations)

    def rel_path(self, selectors):
        """Generates relative path from tag selectors

        Args:
            selectors (iterable): Iterable of selectors to apply
        """
        return "./" + "/".join(selectors)
