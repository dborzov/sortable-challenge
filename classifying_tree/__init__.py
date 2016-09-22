from build import tree, add_product, UnrecognizedListing
import json

class JSONL:
    def __init__(self, filepath):
        self.f = open(filepath, 'rb').__iter__()

    def __iter__(self):
        return self

    def next(self):
        line = self.f.next()
        return json.loads(line)
