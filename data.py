from lxml import etree
import numpy as np


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

    def rel_path(self, selectors):
        """Generates relative path from tag selectors

        Args:
            selectors (iterable): Iterable of selectors to apply
        """
        return "./" + "/".join(selectors)
