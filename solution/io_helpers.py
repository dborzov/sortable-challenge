import json, re
import collections

class JSONL:
    def __init__(self, filepath):
        self.f = open(filepath, 'rb').__iter__()

    def __iter__(self):
        return self

    def next(self):
        line = self.f.next()
        return json.loads(line)


listings = JSONL('data/listings.txt')
products = JSONL('data/products.txt')

"""
count_values is a wrapper around value counter
"""
def count_values(path, getter):
    counter = collections.defaultdict(int)
    for item in JSONL(path):
        counter[getter(item)] += 1
    chart = sorted([(key, count) for key, count in counter.iteritems()], key=lambda x: -x[1])
    for val, count in chart:
        print "{}, {}".format(val, count)



manufacturer_special_cases = json.loads(open("sets/company_classifier/special_cases.json","rb").read())
